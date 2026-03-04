#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import importlib.metadata
import importlib.util
import logging
import os
import random
import re
import sys
import threading
import time
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from string import Template
from typing import Any, Callable, Optional

try:
    import dotenv
except ImportError:  # pragma: no cover - optional dependency
    dotenv = None

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None

BASE_DIR = Path("benchmarks/blocksworld")
OUT_DIR = Path("logs/blocksworld_nvidia_gpt_oss_20b")

# Run configuration
INSTANCES = None  # e.g. 'medium-p01,medium-p02' or 'medium-p*'

MODEL_NAME = "openai/gpt-oss-20b"
DOMAIN_NAME = "blocksworld"
NVIDIA_NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"

MAX_OUTPUT_TOKENS = 130000
TEMPERATURE = 1.0
TOP_P = 0.95
REASONING_EFFORT = "high"
MAX_REQUESTS_PER_MINUTE_PER_KEY = 12
POST_RESPONSE_DELAY_SECONDS = 5
REQUEST_RETRY_DELAYS_SECONDS = (0, 30, 60)

SEEDS = [1]
TEMPLATES = ("grounded", "lifted", "landmarks")

LOG_FORMAT = "[%(asctime)s] INFO :: %(message)s"

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

LANDMARKS_PROMPT_TEMPLATE = """<role>
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
- An action is an **action landmark** if it must appear on every valid plan.
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
- The plan must transform the initial state into a goal state.
- All actions in the plan must be applicable.
- All action landmarks must be included in the plan.
- Your plan may include non-landmark actions.
</requirements>"""

LIFTED_PROMPT_TEMPLATE = """<role>
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
    preconditions: list[str]
    add_effects: list[str]
    del_effects: list[str]
    is_landmark: Optional[bool] = None


@dataclass
class RunSpec:
    instance_id: str
    template: str
    seed: int
    domain_path: Path
    problem_path: Path
    grounded_path: Path
    landmarks_path: Path
    log_path: Path
    plan_path: Path


class ParseError(Exception):
    pass


class KeyPool:
    def __init__(self, keys: list[str]) -> None:
        self._keys = list(keys)
        self._lock = threading.Lock()
        self._cursor = 0

    def next_key(self) -> tuple[int, str]:
        with self._lock:
            idx = self._cursor
            self._cursor = (self._cursor + 1) % len(self._keys)
            return idx, self._keys[idx]


class KeyedRequestGate:
    def __init__(self, delay_seconds: float) -> None:
        self._delay_seconds = delay_seconds
        self._guard = threading.Lock()
        self._locks: dict[str, threading.Lock] = {}

    def _get_key_lock(self, key: str) -> threading.Lock:
        with self._guard:
            lock = self._locks.get(key)
            if lock is None:
                lock = threading.Lock()
                self._locks[key] = lock
            return lock

    def run(self, key: str, fn: Callable[[], Any]) -> Any:
        key_lock = self._get_key_lock(key)
        with key_lock:
            try:
                return fn()
            finally:
                time.sleep(self._delay_seconds)


def setup_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger(f"run_{log_path.stem}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    formatter = logging.Formatter(LOG_FORMAT)
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


def load_validator() -> Optional[Callable[[str, str, str], tuple]]:
    path = Path("plan_validation.py").resolve()
    if not path.exists():
        return None

    spec = importlib.util.spec_from_file_location("plan_validation", str(path))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "validate_plan"):
            return getattr(module, "validate_plan")
        if hasattr(module, "val"):
            return getattr(module, "val")
    return None


def parse_fact_block(lines: list[str]) -> list[str]:
    facts: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if set(stripped) == {"-"}:
            continue
        for fact in re.findall(r"\([^()]*\)", stripped):
            facts.append(fact.strip())
    return facts


def parse_fact_list(text: str) -> list[str]:
    if not text:
        return []
    return [f.strip() for f in re.findall(r"\([^()]*\)", text)]


def parse_grounded_actions(lines: list[str]) -> list[GroundedAction]:
    actions: list[GroundedAction] = []
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
        landmark_match = re.search(r"is action landmark:\s*(true|false)", stripped, re.IGNORECASE)
        landmark_flag = None if landmark_match is None else landmark_match.group(1).lower() == "true"
        actions.append(
            GroundedAction(
                name=name,
                preconditions=pre,
                add_effects=add,
                del_effects=delete,
                is_landmark=landmark_flag,
            )
        )
    return actions


def find_index(lines: list[str], candidates: list[str], start: int = 0) -> Optional[int]:
    lowered = [c.lower() for c in candidates]
    for i in range(start, len(lines)):
        line = lines[i].strip().lower()
        for cand in lowered:
            if line.startswith(cand):
                return i
    return None


def parse_grounded_file(path: Path) -> tuple[list[str], list[str], list[GroundedAction]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.lstrip().startswith("version https://git-lfs.github.com/spec/v1"):
        raise ParseError(
            f"Grounded file appears to be a Git LFS pointer (missing content). Run 'git lfs pull' to fetch: {path}"
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


def format_fact_list(facts: list[str]) -> str:
    return "\n".join(facts)


def format_actions(actions: list[GroundedAction], include_landmarks: bool = False) -> str:
    parts: list[str] = []
    for action in actions:
        pre = ", ".join(action.preconditions)
        delete = ", ".join(action.del_effects)
        add = ", ".join(action.add_effects)
        line = f"name:  {action.name} ; preconditions:  {pre} ; delete effects:  {delete} ; add effects:  {add}"
        if include_landmarks:
            is_landmark = action.is_landmark is True
            line += f" ; is action landmark:  {is_landmark}"
        parts.append(line)
    return "\n".join(parts)


def build_grounded_prompt(grounded_path: Path) -> str:
    initial_facts, goal_facts, actions = parse_grounded_file(grounded_path)
    return Template(GROUND_PROMPT_TEMPLATE).safe_substitute(
        initial_state=format_fact_list(initial_facts),
        goal_facts=format_fact_list(goal_facts),
        actions=format_actions(actions),
    )


def build_landmarks_prompt(landmarks_path: Path) -> str:
    initial_facts, goal_facts, actions = parse_grounded_file(landmarks_path)
    return Template(LANDMARKS_PROMPT_TEMPLATE).safe_substitute(
        initial_state=format_fact_list(initial_facts),
        goal_facts=format_fact_list(goal_facts),
        actions=format_actions(actions, include_landmarks=True),
    )


def build_lifted_prompt(domain_text: str, problem_text: str) -> str:
    return Template(LIFTED_PROMPT_TEMPLATE).safe_substitute(
        pddl_domain=domain_text,
        pddl_instance=problem_text,
    )


def extract_plan(response_text: str) -> Optional[str]:
    match = re.search(r"<plan>(.*?)</plan>", response_text, re.DOTALL)
    if not match:
        return None
    return match.group(1).strip()


def extract_reasoning(response_text: str) -> Optional[str]:
    for tag in ["think", "reasoning"]:
        match = re.search(rf"<{tag}>(.*?)</{tag}>", response_text, re.DOTALL | re.IGNORECASE)
        if match:
            reasoning = match.group(1).strip()
            return reasoning if reasoning else None
    return None


def _count_tokens(text: str) -> int:
    if not text:
        return 0
    return len(re.findall(r"\S+", text))


def _collect_text_chunks(value: object, chunks: list[str]) -> None:
    if value is None:
        return
    if isinstance(value, str):
        stripped = value.strip()
        if stripped:
            chunks.append(stripped)
        return
    if isinstance(value, list):
        for item in value:
            _collect_text_chunks(item, chunks)
        return
    if isinstance(value, dict):
        for key in ("text", "content", "reasoning_content", "reasoning", "value"):
            if key in value:
                _collect_text_chunks(value[key], chunks)
        return

    text = getattr(value, "text", None)
    if isinstance(text, str):
        _collect_text_chunks(text, chunks)
        return

    content = getattr(value, "content", None)
    if content is not None:
        _collect_text_chunks(content, chunks)
        return

    reasoning_content = getattr(value, "reasoning_content", None)
    if reasoning_content is not None:
        _collect_text_chunks(reasoning_content, chunks)


def _message_content_to_text(content: object) -> str:
    if isinstance(content, str):
        return content
    chunks: list[str] = []
    _collect_text_chunks(content, chunks)
    return "\n".join(chunks).strip()


def _extract_reasoning_and_answer(message: object) -> tuple[Optional[str], str, str]:
    response_text = _message_content_to_text(getattr(message, "content", ""))

    reasoning_chunks: list[str] = []
    _collect_text_chunks(getattr(message, "reasoning_content", None), reasoning_chunks)
    reasoning_text = "\n".join(reasoning_chunks).strip() or None
    reasoning_source = "reasoning_content" if reasoning_text else "none"

    think_match = re.search(r"<think>(.*?)</think>", response_text, flags=re.DOTALL | re.IGNORECASE)
    if think_match:
        if not reasoning_text:
            reasoning_text = think_match.group(1).strip() or None
            reasoning_source = "think_tag" if reasoning_text else "none"
        response_text = re.sub(
            r"<think>.*?</think>",
            "",
            response_text,
            flags=re.DOTALL | re.IGNORECASE,
        ).strip()

    if not reasoning_text:
        extracted = extract_reasoning(response_text)
        if extracted:
            reasoning_text = extracted
            reasoning_source = "reasoning_tag"

    return reasoning_text, response_text, reasoning_source


def _extract_thinking_tokens(usage: object, reasoning_text: Optional[str]) -> int:
    if usage is not None:
        details = getattr(usage, "completion_tokens_details", None)
        if details is not None:
            reasoning_tokens = getattr(details, "reasoning_tokens", None)
            if isinstance(reasoning_tokens, int):
                return reasoning_tokens
            if isinstance(details, dict):
                dict_tokens = details.get("reasoning_tokens")
                if isinstance(dict_tokens, int):
                    return dict_tokens

        if hasattr(usage, "model_dump"):
            usage_dump = usage.model_dump()
            if isinstance(usage_dump, dict):
                details_dump = usage_dump.get("completion_tokens_details")
                if isinstance(details_dump, dict):
                    dict_tokens = details_dump.get("reasoning_tokens")
                    if isinstance(dict_tokens, int):
                        return dict_tokens

    return _count_tokens(reasoning_text or "")


def _run_nvidia_nim_chat(
    prompt: str,
    seed: int,
    api_key: str,
    temperature: float,
    top_p: float,
    max_output_tokens: int,
    reasoning_effort: str,
) -> tuple[str, Optional[str], str, Optional[int], Optional[int], int]:
    if OpenAI is None:
        raise RuntimeError("Missing dependency 'openai'. Install with: pip install openai")

    client = OpenAI(base_url=NVIDIA_NIM_BASE_URL, api_key=api_key)

    request_kwargs: dict[str, Any] = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_output_tokens,
        "reasoning_effort": reasoning_effort,
        "seed": seed,
        "stream": False,
    }
    try:
        completion = client.chat.completions.create(**request_kwargs)
    except TypeError:
        request_kwargs.pop("reasoning_effort", None)
        request_kwargs["extra_body"] = {"reasoning_effort": reasoning_effort}
        completion = client.chat.completions.create(**request_kwargs)

    usage = completion.usage
    prompt_tokens = usage.prompt_tokens if usage else None
    completion_tokens = usage.completion_tokens if usage else None

    message = completion.choices[0].message
    reasoning_text, response_text, reasoning_source = _extract_reasoning_and_answer(message)
    thinking_tokens = _extract_thinking_tokens(usage, reasoning_text)

    return (
        response_text,
        reasoning_text,
        reasoning_source,
        prompt_tokens,
        completion_tokens,
        thinking_tokens,
    )


def format_generation_config(
    max_output_tokens: int,
    temperature: float,
    top_p: float,
    reasoning_effort: str,
) -> dict[str, Any]:
    return {
        "max_tokens": max_output_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "reasoning_effort": reasoning_effort,
        "seeded": True,
    }


def gather_library_versions() -> dict[str, str]:
    versions = {"python": sys.version.split()[0]}
    for package_name in ("openai", "python-dotenv", "numpy"):
        try:
            versions[package_name] = importlib.metadata.version(package_name)
        except Exception:
            versions[package_name] = "unavailable"
    return versions


def _load_api_keys() -> list[str]:
    if dotenv is not None:
        dotenv.load_dotenv(dotenv.find_dotenv())

    env_keys = os.environ.get("NVIDIA_API_KEYS")
    if env_keys:
        keys = [key.strip() for key in env_keys.split(",") if key.strip()]
        if keys:
            return keys

    fallback = os.environ.get("NVIDIA_API_KEY")
    if fallback:
        return [fallback]

    raise ValueError("No API keys found. Set NVIDIA_API_KEYS=key1[,key2,...] or NVIDIA_API_KEY.")


def log_metadata(
    logger: logging.Logger,
    spec: RunSpec,
    timestamp: str,
    model_name: str,
    device: str,
    dtype: str,
    gen_config: dict[str, Any],
    library_versions: dict[str, str],
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


def run_generation(
    spec: RunSpec,
    request_gate: KeyedRequestGate,
    api_key: str,
    generation_config: dict[str, Any],
    domain_text: str,
) -> tuple[Optional[str], Optional[str]]:
    if spec.log_path.exists():
        return None, None

    spec.log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = setup_logger(spec.log_path)
    timestamp = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    error_type: Optional[str] = None
    response_text = ""
    prompt_logged = False
    response_logged = False
    prompt_tokens_logged = False
    response_tokens_logged = False
    reasoning_logged = False
    reasoning_metadata_logged = False
    plan_logged = False

    try:
        log_metadata(
            logger,
            spec,
            timestamp,
            MODEL_NAME,
            device="nvidia-nim-api",
            dtype="n/a",
            gen_config=generation_config,
            library_versions=gather_library_versions(),
        )

        if spec.template == "grounded":
            prompt = build_grounded_prompt(spec.grounded_path)
        elif spec.template == "landmarks":
            prompt = build_landmarks_prompt(spec.landmarks_path)
        else:
            problem_text = spec.problem_path.read_text(encoding="utf-8", errors="replace")
            prompt = build_lifted_prompt(domain_text, problem_text)

        logger.info("Prompt:\n\n%s", prompt)
        prompt_logged = True

        prompt_tokens = _count_tokens(prompt)
        response_tokens = 0
        reasoning_text: Optional[str] = None
        reasoning_tokens = 0
        reasoning_source = "none"
        last_error: Optional[str] = None

        set_seed(spec.seed)
        for attempt, delay in enumerate(REQUEST_RETRY_DELAYS_SECONDS, start=1):
            if delay:
                time.sleep(delay)
            try:
                (
                    response_text,
                    reasoning_text,
                    reasoning_source,
                    usage_prompt_tokens,
                    usage_completion_tokens,
                    usage_thinking_tokens,
                ) = request_gate.run(
                    api_key,
                    lambda: _run_nvidia_nim_chat(
                        prompt=prompt,
                        seed=spec.seed,
                        api_key=api_key,
                        temperature=float(generation_config["temperature"]),
                        top_p=float(generation_config["top_p"]),
                        max_output_tokens=int(generation_config["max_tokens"]),
                        reasoning_effort=str(generation_config["reasoning_effort"]),
                    ),
                )
                if usage_prompt_tokens is not None:
                    prompt_tokens = usage_prompt_tokens
                if usage_completion_tokens is not None:
                    response_tokens = usage_completion_tokens
                else:
                    response_tokens = _count_tokens(response_text)
                reasoning_tokens = usage_thinking_tokens
                last_error = None
                break
            except Exception as exc:
                last_error = str(exc)
                logger.warning("Attempt %s failed: %s", attempt, last_error)

        if last_error:
            raise RuntimeError(last_error)

        logger.info("Prompt tokens: %d", prompt_tokens)
        prompt_tokens_logged = True

        logger.info("Reasoning trace:\n%s", reasoning_text if reasoning_text is not None else "<none>")
        reasoning_logged = True
        logger.info(
            "Reasoning metadata: reasoning_tokens=%d, reasoning_source=%s",
            reasoning_tokens,
            reasoning_source,
        )
        reasoning_metadata_logged = True

        plan_text = extract_plan(response_text)
        if plan_text is not None:
            response_for_log = f"<plan>\n{plan_text}\n</plan>"
        else:
            response_for_log = response_text or "<empty_response>"

        logger.info("Response:\n%s", response_for_log)
        response_logged = True
        logger.info("Response tokens: %d", response_tokens)
        response_tokens_logged = True

        if plan_text is not None:
            logger.info("Plan:\n%s", plan_text)
            plan_logged = True
            plan_tokens = _count_tokens(plan_text)
            logger.info("Extracted plan tokens: %d", plan_tokens)
            logger.info(
                "Response metadata: response_tokens=%d, extracted_plan_tokens=%d",
                response_tokens,
                plan_tokens,
            )
            if plan_text:
                spec.plan_path.write_text(plan_text + "\n", encoding="utf-8")
            else:
                spec.plan_path.write_text("", encoding="utf-8")
            logger.info("Plan file: %s", spec.plan_path)
        else:
            logger.info("Plan:\n<no_plan>")
            plan_logged = True
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
        if not reasoning_metadata_logged:
            logger.info("Reasoning metadata: reasoning_tokens=0, reasoning_source=none")
        if not plan_logged:
            logger.info("Plan:\n<no_plan>")
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
        if not reasoning_metadata_logged:
            logger.info("Reasoning metadata: reasoning_tokens=0, reasoning_source=none")
        if not plan_logged:
            logger.info("Plan:\n<no_plan>")
        logger.info("Extracted plan tokens: 0")
        logger.info("Response metadata: response_tokens=0, extracted_plan_tokens=0")
        logger.info("Error: generation_error: %s", exc)

    finally:
        cleanup_logger(logger)

    return error_type, response_text


def resolve_instances(base_dir: Path, instance_arg: Optional[str]) -> list[str]:
    lifted_dir = base_dir / "lifted"
    grounded_dir = base_dir / "grounded"
    landmarks_dir = base_dir / "landmarks"

    for dirname, path in (
        ("lifted", lifted_dir),
        ("grounded", grounded_dir),
        ("landmarks", landmarks_dir),
    ):
        if not path.exists():
            raise FileNotFoundError(f"{dirname.capitalize()} directory not found: {path}")

    lifted_instances = {p.stem for p in lifted_dir.glob("*.pddl")}
    grounded_instances = {p.stem for p in grounded_dir.glob("*.txt")}
    landmarks_instances = {p.stem for p in landmarks_dir.glob("*.txt")}
    available = sorted(lifted_instances & grounded_instances & landmarks_instances)

    if not available:
        raise FileNotFoundError(
            "No shared instances found across lifted (*.pddl), grounded (*.txt), and landmarks (*.txt)."
        )

    if not instance_arg:
        return available

    selected: list[str] = []
    tokens = [t.strip() for t in instance_arg.split(",") if t.strip()]
    for token in tokens:
        token = token.strip()
        if token.endswith(".pddl") or token.endswith(".txt"):
            token = Path(token).stem

        if any(ch in token for ch in ("*", "?")):
            selected.extend(name for name in available if fnmatch(name, token))
            continue

        candidates = {token}
        if token.startswith("medium-"):
            candidates.add(token[len("medium-") :])
        elif token.startswith("p"):
            candidates.add(f"medium-{token}")

        for candidate in candidates:
            if candidate in available:
                selected.append(candidate)

    selected = sorted(set(selected))
    if not selected:
        raise ValueError("No shared instances match the provided filter.")
    return selected


def build_run_specs(instances: list[str], base_dir: Path, outdir: Path) -> list[RunSpec]:
    specs: list[RunSpec] = []
    domain_path = base_dir / "domain.pddl"
    lifted_dir = base_dir / "lifted"
    grounded_dir = base_dir / "grounded"
    landmarks_dir = base_dir / "landmarks"

    for instance_id in instances:
        problem_path = lifted_dir / f"{instance_id}.pddl"
        grounded_path = grounded_dir / f"{instance_id}.txt"
        landmarks_path = landmarks_dir / f"{instance_id}.txt"
        for template in TEMPLATES:
            for seed in SEEDS:
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
                        landmarks_path=landmarks_path,
                        log_path=log_path,
                        plan_path=plan_path,
                    )
                )
    return specs


def _unpack_validator_result(result: Any) -> tuple[bool, Optional[str]]:
    if isinstance(result, tuple):
        if len(result) >= 2:
            return bool(result[0]), result[1]
        if len(result) == 1:
            return bool(result[0]), None
    if isinstance(result, bool):
        return result, None
    return False, "validation_failed"


def validate_plans(
    specs: list[RunSpec],
    run_errors: dict[tuple[str, str, int], str],
    validator: Optional[Callable[[str, str, str], tuple]],
    results_path: Path,
) -> None:
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with results_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["domain", "instance", "template", "log_file", "seed", "is_valid", "error_type"])

        for spec in specs:
            error_type = run_errors.get((spec.instance_id, spec.template, spec.seed))
            if error_type:
                writer.writerow(
                    [
                        DOMAIN_NAME,
                        spec.instance_id,
                        spec.template,
                        str(spec.log_path),
                        spec.seed,
                        0,
                        error_type,
                    ]
                )
                continue

            if not spec.plan_path.exists():
                writer.writerow(
                    [
                        DOMAIN_NAME,
                        spec.instance_id,
                        spec.template,
                        str(spec.log_path),
                        spec.seed,
                        0,
                        "no_plan",
                    ]
                )
                continue

            if validator is None:
                writer.writerow(
                    [
                        DOMAIN_NAME,
                        spec.instance_id,
                        spec.template,
                        str(spec.log_path),
                        spec.seed,
                        0,
                        "validator_missing",
                    ]
                )
                continue

            raw_result = validator(str(spec.domain_path), str(spec.problem_path), str(spec.plan_path))
            is_valid, message = _unpack_validator_result(raw_result)
            writer.writerow(
                [
                    DOMAIN_NAME,
                    spec.instance_id,
                    spec.template,
                    str(spec.log_path),
                    spec.seed,
                    1 if is_valid else 0,
                    "" if is_valid else (message or "validation_failed"),
                ]
            )


def run_blocksworld(
    base_dir: Path,
    outdir: Path,
    instances: Optional[str],
    temperature: float,
    top_p: float,
    max_output_tokens: int,
    reasoning_effort: str,
    max_requests_per_minute_per_key: int,
    post_response_delay_seconds: int,
) -> None:
    domain_path = base_dir / "domain.pddl"
    if not domain_path.exists():
        raise FileNotFoundError(f"Domain file not found: {domain_path}")

    instances_list = resolve_instances(base_dir, instances)
    specs = build_run_specs(instances_list, base_dir, outdir)
    generation_config = format_generation_config(max_output_tokens, temperature, top_p, reasoning_effort)

    domain_text = domain_path.read_text(encoding="utf-8", errors="replace")

    runs_to_generate = [spec for spec in specs if not spec.log_path.exists()]

    api_keys = _load_api_keys()
    key_pool = KeyPool(api_keys)

    request_gate = KeyedRequestGate(
        max(60.0 / max(1, max_requests_per_minute_per_key), float(post_response_delay_seconds))
    )

    logging.info("Loaded %s API key(s).", len(api_keys))
    logging.info("Total specs: %s | pending: %s", len(specs), len(runs_to_generate))

    run_errors: dict[tuple[str, str, int], str] = {}
    for spec in runs_to_generate:
        _, api_key = key_pool.next_key()
        error_type, _ = run_generation(
            spec=spec,
            request_gate=request_gate,
            api_key=api_key,
            generation_config=generation_config,
            domain_text=domain_text,
        )
        if error_type:
            run_errors[(spec.instance_id, spec.template, spec.seed)] = error_type

    validator = load_validator()
    results_path = outdir / "results.csv"
    validate_plans(specs, run_errors, validator, results_path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", type=Path, default=BASE_DIR)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--instances", type=str, default=INSTANCES)
    parser.add_argument("--temperature", type=float, default=TEMPERATURE)
    parser.add_argument("--top-p", type=float, default=TOP_P)
    parser.add_argument("--max-output-tokens", type=int, default=MAX_OUTPUT_TOKENS)
    parser.add_argument("--reasoning-effort", type=str, default=REASONING_EFFORT)
    parser.add_argument(
        "--max-requests-per-minute-per-key",
        type=int,
        default=MAX_REQUESTS_PER_MINUTE_PER_KEY,
    )
    parser.add_argument(
        "--post-response-delay-seconds",
        type=int,
        default=POST_RESPONSE_DELAY_SECONDS,
    )
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

    run_blocksworld(
        base_dir=args.base_dir,
        outdir=args.out_dir,
        instances=args.instances,
        temperature=args.temperature,
        top_p=args.top_p,
        max_output_tokens=args.max_output_tokens,
        reasoning_effort=args.reasoning_effort,
        max_requests_per_minute_per_key=args.max_requests_per_minute_per_key,
        post_response_delay_seconds=args.post_response_delay_seconds,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
