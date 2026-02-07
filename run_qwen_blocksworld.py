#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import importlib.util
import inspect
import logging
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Callable, List, Optional, Tuple

MODEL_NAME = "Qwen/Qwen3-0.6B"
DOMAIN_NAME = "blocksworld"

GROUND_PROMPT_TEMPLATE = """<role>
You are an AI planning expert.
</role>

<task>
Given the initial state, the set of goal facts, and a list of available actions, return **a plan** (a sequence of actions) that transforms the initial state into a goal state.
</task>

<definitions>
- A state is a set of facts.
- A goal state is a state that has all goal facts.
- An action is applicable if, and only if, **all** its preconditions are in the current state.
- When an action is applied: remove its delete effects from the state, then add its add effects.
</definitions>

<inputs>
This is the initial state:
<initial-state>
$initial_state
</initial-state>

These are the goal facts:
<goal-facts>
$goal_facts
</goal-facts>

These are the actions:
<actions>
$actions
</actions>
</inputs>

<output-format>
Return **only** a plan wrapped in "<plan>...</plan>", where each plan's action should be identified by its name on the table, each on a line. Do not include analysis, examples, or commentary outside the plan tags.
</output-format>

<requirements>
The plan must be valid: each action must be applicable in the state it is applied in, and the plan must end in a goal state.
</requirements>"""

UNGROUNDED_PROMPT_TEMPLATE = """<role>
You are an AI planning expert.
</role>

<task>
Given the PDDL domain and the PDDL instance, return a plan (a sequence of actions) that transforms the initial state into a goal state.
</task>

<definitions>
- A state is a set of facts.
- A goal state is a state that has all goal facts.
- An action is applicable if, and only if, **all** its preconditions are in the current state.
- When an action is applied: remove its delete effects from the state, then add its add effects.
</definitions>

<inputs>
This is the PDDL domain:
<pddl-domain>
$pddl_domain
</pddl-domain>

This is the PDDL instance:
<pddl-instance>
$pddl_instance
</pddl-instance>
</inputs>

<output-format>
Return **only** a plan wrapped in "<plan>...</plan>", where each plan's action must use the same name and same number of parameters as one of the action schemas, each on a line. Do not include analysis, examples, or commentary outside the plan tags.
</output-format>

<requirements>
The plan must be valid: each action must be applicable in the state it is applied in, and the plan must end in a goal state.
</requirements>"""


@dataclass
class GroundedAction:
    name: str
    preconditions: List[str]
    add_effects: List[str]
    del_effects: List[str]


@dataclass
class RunSpec:
    instance_id: str
    template: str
    seed: int
    domain_path: Path
    problem_path: Path
    grounded_path: Path
    log_path: Path
    plan_path: Path


class ParseError(Exception):
    pass


def setup_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger(f"run_{log_path.stem}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    formatter = logging.Formatter("[%(asctime)s] INFO :: %(message)s")
    handler.setFormatter(formatter)

    logger.handlers = [handler]
    return logger


def cleanup_logger(logger: logging.Logger) -> None:
    handlers = list(logger.handlers)
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)


def set_seed(seed: int) -> None:
    random.seed(seed)
    try:
        import numpy as np

        np.random.seed(seed)
    except Exception:
        pass

    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except Exception:
        pass


def load_validator() -> Optional[Callable[[str, str, str], Tuple[bool, Optional[str]]]]:
    path = Path(__file__).resolve().parent / "plan_validation.py"
    if not path.exists():
        return None

    spec = importlib.util.spec_from_file_location("plan_validation", str(path))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
        if hasattr(module, "validate_plan"):
            return getattr(module, "validate_plan")
        if hasattr(module, "val"):
            return getattr(module, "val")
    return None


def parse_fact_block(lines: List[str]) -> List[str]:
    facts: List[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if set(stripped) == {"-"}:
            continue
        for fact in re.findall(r"\([^()]*\)", stripped):
            facts.append(fact.strip())
    return facts


def parse_fact_list(text: str) -> List[str]:
    if not text:
        return []
    return [f.strip() for f in re.findall(r"\([^()]*\)", text)]


def parse_grounded_actions(lines: List[str]) -> List[GroundedAction]:
    actions: List[GroundedAction] = []
    pattern = re.compile(
        r"^name:\s*(?P<name>\([^;]+?\))\s*;\s*preconditions:\s*(?P<pre>[^;]*?)\s*;\s*delete effects:\s*(?P<del>[^;]*?)\s*;\s*add effects:\s*(?P<add>.*)$",
        re.IGNORECASE,
    )

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if set(stripped) == {"-"}:
            continue
        match = pattern.match(stripped)
        if not match:
            raise ParseError(f"Unrecognized operator line: {stripped}")
        name = match.group("name").strip()
        pre = parse_fact_list(match.group("pre"))
        delete = parse_fact_list(match.group("del"))
        add = parse_fact_list(match.group("add"))
        actions.append(GroundedAction(name=name, preconditions=pre, add_effects=add, del_effects=delete))
    return actions


def find_index(lines: List[str], candidates: List[str], start: int = 0) -> Optional[int]:
    lowered = [c.lower() for c in candidates]
    for i in range(start, len(lines)):
        line = lines[i].strip().lower()
        for cand in lowered:
            if line.startswith(cand):
                return i
    return None


def parse_grounded_file(path: Path) -> Tuple[List[str], List[str], List[GroundedAction]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.lstrip().startswith("version https://git-lfs.github.com/spec/v1"):
        raise ParseError(
            f"Grounded file appears to be a Git LFS pointer (missing content). "
            f"Run 'git lfs pull' to fetch: {path}"
        )
    lines = text.splitlines()

    idx_initial = find_index(lines, ["initial state facts:"])
    if idx_initial is None:
        idx_initial = find_index(lines, ["facts:"])
    if idx_initial is None:
        raise ParseError("Missing Facts or Initial State Facts section.")

    idx_goal = find_index(lines, ["goal facts:", "goals:"], start=idx_initial + 1)
    if idx_goal is None:
        raise ParseError("Missing Goal Facts section.")

    idx_ops = find_index(lines, ["operators:", "actions:", "grounded actions:"], start=idx_goal + 1)
    if idx_ops is None:
        raise ParseError("Missing Operators section.")

    init_lines = lines[idx_initial + 1 : idx_goal]
    goal_lines = lines[idx_goal + 1 : idx_ops]
    ops_lines = lines[idx_ops + 1 :]

    initial_facts = parse_fact_block(init_lines)
    goal_facts = parse_fact_block(goal_lines)
    actions = parse_grounded_actions(ops_lines)

    if not initial_facts:
        raise ParseError("No initial facts parsed.")
    if not goal_facts:
        raise ParseError("No goal facts parsed.")
    if not actions:
        raise ParseError("No grounded actions parsed.")

    return initial_facts, goal_facts, actions


def format_fact_list(facts: List[str]) -> str:
    return "\n".join(facts)


def format_actions(actions: List[GroundedAction]) -> str:
    parts: List[str] = []
    for action in actions:
        pre = ", ".join(action.preconditions)
        delete = ", ".join(action.del_effects)
        add = ", ".join(action.add_effects)
        parts.append(
            f"name:  {action.name} ; preconditions:  {pre} ; delete effects:  {delete} ; add effects:  {add}"
        )
    return "\n".join(parts)


def build_grounded_prompt(grounded_path: Path) -> str:
    initial_facts, goal_facts, actions = parse_grounded_file(grounded_path)
    return Template(GROUND_PROMPT_TEMPLATE).safe_substitute(
        initial_state=format_fact_list(initial_facts),
        goal_facts=format_fact_list(goal_facts),
        actions=format_actions(actions),
    )


def build_ungrounded_prompt(domain_text: str, problem_text: str) -> str:
    return Template(UNGROUNDED_PROMPT_TEMPLATE).safe_substitute(
        pddl_domain=domain_text,
        pddl_instance=problem_text,
    )


def extract_plan(response_text: str) -> Optional[str]:
    match = re.search(r"<plan>(.*?)</plan>", response_text, re.DOTALL)
    if not match:
        return None
    plan = match.group(1).strip()
    return plan if plan else None


def extract_reasoning(response_text: str) -> Optional[str]:
    for tag in ["think", "reasoning"]:
        match = re.search(rf"<{tag}>(.*?)</{tag}>", response_text, re.DOTALL | re.IGNORECASE)
        if match:
            reasoning = match.group(1).strip()
            return reasoning if reasoning else None
    return None


def build_chat_prompt(tokenizer, prompt: str) -> str:
    if not hasattr(tokenizer, "apply_chat_template"):
        return prompt

    messages = [
        {"role": "system", "content": "You are an AI planning expert."},
        {"role": "user", "content": prompt},
    ]
    kwargs = {
        "tokenize": False,
        "add_generation_prompt": True,
    }
    try:
        signature = inspect.signature(tokenizer.apply_chat_template)
        if "enable_thinking" in signature.parameters:
            kwargs["enable_thinking"] = True
    except Exception:
        pass

    return tokenizer.apply_chat_template(messages, **kwargs)


def filter_model_inputs(model, model_inputs: dict) -> dict:
    # Qwen chat tokenizers may include token_type_ids that many CausalLM models do not accept.
    model_inputs = dict(model_inputs)
    model_inputs.pop("token_type_ids", None)

    try:
        signature = inspect.signature(model.forward)
    except Exception:
        return model_inputs

    params = signature.parameters.values()
    if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params):
        return model_inputs

    allowed = set(signature.parameters.keys())
    return {k: v for k, v in model_inputs.items() if k in allowed}


def split_qwen_thinking(output_ids: List[int], tokenizer) -> Tuple[Optional[str], str]:
    end_think_id = tokenizer.convert_tokens_to_ids("</think>")
    split_idx = 0
    if isinstance(end_think_id, int) and end_think_id >= 0:
        for idx in range(len(output_ids) - 1, -1, -1):
            if output_ids[idx] == end_think_id:
                split_idx = idx + 1
                break

    if split_idx > 0:
        thinking = tokenizer.decode(output_ids[:split_idx], skip_special_tokens=True).strip()
        content = tokenizer.decode(output_ids[split_idx:], skip_special_tokens=True).strip()
        return (thinking if thinking else None), content

    full = tokenizer.decode(output_ids, skip_special_tokens=True).strip()
    return extract_reasoning(full), full


def count_tokens(tokenizer, text: str) -> int:
    return len(tokenizer.encode(text))


def load_model_and_tokenizer(device: str, dtype: str):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    if dtype == "auto":
        torch_dtype = torch.float16 if device == "cuda" else torch.float32
    else:
        torch_dtype = getattr(torch, dtype)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch_dtype,
        trust_remote_code=True,
    )
    model.to(device)
    model.eval()

    return model, tokenizer, torch_dtype


def generate_response(
    model, tokenizer, prompt: str, gen_config, device: str, seed: int
) -> Tuple[str, str, int, Optional[str], str]:
    import torch

    serialized_prompt = build_chat_prompt(tokenizer, prompt)
    inputs = tokenizer([serialized_prompt], return_tensors="pt")
    inputs = filter_model_inputs(model, inputs)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    input_len = int(inputs["input_ids"].shape[1])

    generate_kwargs = {
        **inputs,
        "generation_config": gen_config,
    }
    try:
        generate_sig = inspect.signature(model.generate)
        if "generator" in generate_sig.parameters:
            generator = torch.Generator(device=device)
            generator.manual_seed(seed)
            generate_kwargs["generator"] = generator
    except Exception:
        pass

    with torch.no_grad():
        outputs = model.generate(**generate_kwargs)

    generated_ids = outputs[0][input_len:].tolist()
    thinking_text, response_content = split_qwen_thinking(generated_ids, tokenizer)
    response_text_raw = tokenizer.decode(generated_ids, skip_special_tokens=False)
    response_text_clean = tokenizer.decode(generated_ids, skip_special_tokens=True)
    return response_text_raw, response_text_clean, len(generated_ids), thinking_text, response_content


def format_generation_config(args) -> dict:
    return {
        "max_new_tokens": args.max_new_tokens,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "top_k": args.top_k,
        "do_sample": args.temperature > 0,
    }


def log_metadata(
    logger: logging.Logger,
    spec: RunSpec,
    timestamp: str,
    model_name: str,
    device: str,
    dtype: str,
    gen_config: dict,
    library_versions: dict,
) -> None:
    logger.info("Stage: plan generation")
    logger.info(
        "Prompt metadata: domain=%s, instance=%s, template=%s, seed=%s, timestamp=%s",
        spec.domain_path,
        spec.problem_path,
        spec.template,
        spec.seed,
        timestamp,
    )
    logger.info(
        "Model metadata: model=%s, device=%s, dtype=%s, generation_config=%s, library_versions=%s",
        model_name,
        device,
        dtype,
        gen_config,
        library_versions,
    )


def gather_library_versions() -> dict:
    versions = {"python": sys.version.split()[0]}
    try:
        import torch

        versions["torch"] = torch.__version__
    except Exception:
        versions["torch"] = "unavailable"
    try:
        import transformers

        versions["transformers"] = transformers.__version__
    except Exception:
        versions["transformers"] = "unavailable"
    try:
        import numpy as np

        versions["numpy"] = np.__version__
    except Exception:
        versions["numpy"] = "unavailable"
    return versions


def run_generation(
    spec: RunSpec,
    model,
    tokenizer,
    gen_config,
    device: str,
    dtype: str,
    domain_text: str,
    model_load_error: Optional[str],
) -> Tuple[Optional[str], Optional[str]]:
    if spec.log_path.exists():
        return None, None

    spec.log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = setup_logger(spec.log_path)
    timestamp = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    error_type: Optional[str] = None
    prompt = ""
    response_text = ""
    response_text_clean = ""
    prompt_logged = False
    response_logged = False
    prompt_tokens_logged = False
    response_tokens_logged = False
    reasoning_logged = False

    try:
        log_metadata(
            logger,
            spec,
            timestamp,
            MODEL_NAME,
            device,
            dtype,
            gen_config,
            gather_library_versions(),
        )

        if spec.template == "grounded":
            prompt = build_grounded_prompt(spec.grounded_path)
        else:
            problem_text = spec.problem_path.read_text(encoding="utf-8", errors="replace")
            prompt = build_ungrounded_prompt(domain_text, problem_text)

        logger.info("Prompt:\n\n%s", prompt)
        prompt_logged = True

        if tokenizer is None or model is None:
            raise RuntimeError(model_load_error or "Model or tokenizer unavailable.")

        serialized_prompt = build_chat_prompt(tokenizer, prompt)
        prompt_tokens = count_tokens(tokenizer, serialized_prompt)
        logger.info("Prompt tokens: %d", prompt_tokens)
        prompt_tokens_logged = True

        set_seed(spec.seed)
        response_text, response_text_clean, response_tokens, reasoning_from_tokens, response_content = generate_response(
            model,
            tokenizer,
            prompt,
            gen_config,
            device,
            spec.seed,
        )

        reasoning = reasoning_from_tokens or extract_reasoning(response_text_clean)
        logger.info("Reasoning trace:\n%s", reasoning if reasoning is not None else "<none>")
        reasoning_logged = True

        plan_text = extract_plan(response_content) or extract_plan(response_text_clean)
        if plan_text:
            response_for_log = f"<plan>\n{plan_text}\n</plan>"
        else:
            response_for_log = response_content or response_text_clean or response_text or "<empty_response>"

        logger.info("Response:\n%s", response_for_log)
        response_logged = True
        logger.info("Response tokens: %d", response_tokens)
        response_tokens_logged = True

        if plan_text:
            plan_tokens = count_tokens(tokenizer, plan_text)
            logger.info("Extracted plan tokens: %d", plan_tokens)
            logger.info(
                "Response metadata: response_tokens=%d, extracted_plan_tokens=%d",
                response_tokens,
                plan_tokens,
            )
            spec.plan_path.write_text(plan_text + "\n", encoding="utf-8")
            logger.info("Plan file: %s", spec.plan_path)
        else:
            logger.info("Extracted plan tokens: 0")
            logger.info("Response metadata: response_tokens=%d, extracted_plan_tokens=0", response_tokens)

    except ParseError as exc:
        error_type = "parse_error"
        if not prompt_logged:
            logger.info("Prompt:\n\n<parse_error: %s>", exc)
        if not prompt_tokens_logged:
            logger.info("Prompt tokens: 0")
        if not response_logged:
            logger.info("Response:\n<no_response>")
        if not response_tokens_logged:
            logger.info("Response tokens: 0")
        if not reasoning_logged:
            logger.info("Reasoning trace:\n<none>")
        logger.info("Extracted plan tokens: 0")
        logger.info("Response metadata: response_tokens=0, extracted_plan_tokens=0")
        logger.info("Error: parse_error: %s", exc)
    except Exception as exc:
        error_type = f"generation_error: {exc}"
        if not prompt_logged:
            logger.info("Prompt:\n\n<unavailable>")
        if not prompt_tokens_logged:
            logger.info("Prompt tokens: 0")
        if not response_logged:
            logger.info("Response:\n<no_response>")
        if not response_tokens_logged:
            logger.info("Response tokens: 0")
        if not reasoning_logged:
            logger.info("Reasoning trace:\n<none>")
        logger.info("Extracted plan tokens: 0")
        logger.info("Response metadata: response_tokens=0, extracted_plan_tokens=0")
        logger.info("Error: generation_error: %s", exc)
    finally:
        cleanup_logger(logger)

    return error_type, response_text


def resolve_instances(base_dir: Path, instance_arg: Optional[str]) -> List[str]:
    available = sorted(p.stem for p in base_dir.glob("easy-*.pddl"))
    if not available:
        raise FileNotFoundError(f"No instances found in {base_dir}")

    if not instance_arg:
        return available

    selected: List[str] = []
    tokens = [t.strip() for t in instance_arg.split(",") if t.strip()]
    for token in tokens:
        token = token.strip()
        if token.endswith(".pddl"):
            token = Path(token).stem
        if token.startswith("p"):
            token = f"easy-{token}"
        if any(ch in token for ch in ["*", "?"]):
            matched = [name for name in available if fnmatch(name, token)]
            selected.extend(matched)
        else:
            if token in available:
                selected.append(token)
    selected = sorted(set(selected))
    if not selected:
        raise ValueError("No instances match the provided filter.")
    return selected


def fnmatch(name: str, pattern: str) -> bool:
    return re.fullmatch(fnmatch_to_regex(pattern), name) is not None


def fnmatch_to_regex(pattern: str) -> str:
    pattern = re.escape(pattern)
    pattern = pattern.replace(r"\*", ".*")
    pattern = pattern.replace(r"\?", ".")
    return pattern


def build_run_specs(instances: List[str], base_dir: Path, outdir: Path) -> List[RunSpec]:
    specs: List[RunSpec] = []
    domain_path = base_dir / "domain.pddl"
    for instance_id in instances:
        problem_path = base_dir / f"{instance_id}.pddl"
        grounded_path = base_dir / f"{instance_id}.txt"
        for template in ["grounded", "ungrounded"]:
            for seed in [1, 2, 3]:
                log_name = f"{instance_id}_{template}_seed{seed}.log"
                plan_name = f"{instance_id}_{template}_seed{seed}.plan"
                log_path = outdir / log_name
                plan_path = outdir / plan_name
                specs.append(
                    RunSpec(
                        instance_id=instance_id,
                        template=template,
                        seed=seed,
                        domain_path=domain_path,
                        problem_path=problem_path,
                        grounded_path=grounded_path,
                        log_path=log_path,
                        plan_path=plan_path,
                    )
                )
    return specs


def validate_plans(
    specs: List[RunSpec],
    run_errors: dict,
    validator: Optional[Callable[[str, str, str], Tuple[bool, Optional[str]]]],
    results_path: Path,
) -> None:
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with results_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["domain", "instance", "template", "log_file", "seed", "is_valid", "error_type"])

        for spec in specs:
            error_type = run_errors.get((spec.instance_id, spec.template, spec.seed))
            if error_type:
                writer.writerow([
                    DOMAIN_NAME,
                    spec.instance_id,
                    spec.template,
                    str(spec.log_path),
                    spec.seed,
                    0,
                    error_type,
                ])
                continue

            if not spec.plan_path.exists():
                writer.writerow([
                    DOMAIN_NAME,
                    spec.instance_id,
                    spec.template,
                    str(spec.log_path),
                    spec.seed,
                    0,
                    "no_plan",
                ])
                continue

            if validator is None:
                writer.writerow([
                    DOMAIN_NAME,
                    spec.instance_id,
                    spec.template,
                    str(spec.log_path),
                    spec.seed,
                    0,
                    "validator_missing",
                ])
                continue

            is_valid, message = validator(str(spec.domain_path), str(spec.problem_path), str(spec.plan_path))
            writer.writerow([
                DOMAIN_NAME,
                spec.instance_id,
                spec.template,
                str(spec.log_path),
                spec.seed,
                1 if is_valid else 0,
                "" if is_valid else (message or "validation_failed"),
            ])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Qwen/Qwen3-0.6B on Blocksworld IPC2023 grounded instances.")
    parser.add_argument(
        "--instances",
        default=None,
        help="Comma-separated list or glob pattern for instance IDs (e.g., p01,p02 or easy-p*).",
    )
    parser.add_argument(
        "--outdir",
        default="logs/blocksworld",
        help="Output directory for logs, plans, and results.csv.",
    )
    parser.add_argument("--max-new-tokens", type=int, default=38912)
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--top-p", type=float, default=0.95)
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument(
        "--device",
        choices=["auto", "cuda", "cpu"],
        default="auto",
        help="Device to run on: auto, cuda, or cpu.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    base_dir = Path("benchmarks/ipc2023-learning/grounded/blocksworld")
    outdir = Path(args.outdir)
    domain_path = base_dir / "domain.pddl"
    if not domain_path.exists():
        raise FileNotFoundError(f"Domain file not found: {domain_path}")

    instances = resolve_instances(base_dir, args.instances)
    specs = build_run_specs(instances, base_dir, outdir)

    device = args.device
    if device == "auto":
        try:
            import torch

            device = "cuda" if torch.cuda.is_available() else "cpu"
        except Exception:
            device = "cpu"

    gen_config = format_generation_config(args)

    domain_text = domain_path.read_text(encoding="utf-8", errors="replace")

    runs_to_generate = [spec for spec in specs if not spec.log_path.exists()]

    model = None
    tokenizer = None
    dtype_label = "unknown"
    model_load_error = None
    if runs_to_generate:
        try:
            model, tokenizer, torch_dtype = load_model_and_tokenizer(device, "auto")
            dtype_label = str(torch_dtype)
            from transformers import GenerationConfig

            gen_config = GenerationConfig(
                **gen_config,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        except Exception as exc:
            model = None
            tokenizer = None
            dtype_label = "unavailable"
            model_load_error = f"model_load_failed: {exc}"
    else:
        gen_config = None

    run_errors = {}
    for spec in runs_to_generate:
        error_type, _ = run_generation(
            spec,
            model,
            tokenizer,
            gen_config,
            device,
            dtype_label,
            domain_text,
            model_load_error,
        )
        if error_type:
            run_errors[(spec.instance_id, spec.template, spec.seed)] = error_type

    validator = load_validator()
    results_path = outdir / "results.csv"
    validate_plans(specs, run_errors, validator, results_path)


if __name__ == "__main__":
    main()
