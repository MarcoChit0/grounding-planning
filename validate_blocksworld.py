#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional, Tuple

DOMAIN_NAME = "blocksworld"
LOG_PATTERN = re.compile(r"^(?P<instance>.+)_(?P<template>[^_]+)_seed(?P<seed>\d+)\.log$")


@dataclass
class LogSpec:
    instance_id: str
    template: str
    seed: int
    log_path: Path
    plan_path: Path
    problem_path: Optional[Path]


@dataclass
class ValidationResult:
    domain: str
    instance: str
    template: str
    log_file: str
    seed: int
    is_valid: int
    error_type: str


def load_validator() -> Optional[Callable[[str, str, str], Tuple[bool, Optional[str], Optional[str]]]]:
    try:
        from plan_validation import validate_plan

        return validate_plan
    except Exception:
        return None


def resolve_problem_path(lifted_dir: Path, instance_id: str) -> Optional[Path]:
    direct = lifted_dir / f"{instance_id}.pddl"
    if direct.exists():
        return direct

    if not instance_id.startswith("easy-"):
        prefixed = lifted_dir / f"easy-{instance_id}.pddl"
        if prefixed.exists():
            return prefixed

    if instance_id.startswith("easy-"):
        stripped = instance_id[len("easy-") :]
        alt = lifted_dir / f"{stripped}.pddl"
        if alt.exists():
            return alt

    return None


def collect_log_specs(outdir: Path, lifted_dir: Path) -> List[LogSpec]:
    specs: List[LogSpec] = []
    for log_path in sorted(outdir.glob("*.log")):
        match = LOG_PATTERN.match(log_path.name)
        if not match:
            continue
        instance_id = match.group("instance")
        template = match.group("template")
        seed = int(match.group("seed"))
        plan_path = log_path.with_suffix(".plan")
        problem_path = resolve_problem_path(lifted_dir, instance_id)
        specs.append(
            LogSpec(
                instance_id=instance_id,
                template=template,
                seed=seed,
                log_path=log_path,
                plan_path=plan_path,
                problem_path=problem_path,
            )
        )
    if not specs:
        raise FileNotFoundError(f"No log files found in {outdir}")
    return specs


def validate_specs(
    specs: List[LogSpec],
    domain_path: Path,
    validator: Optional[Callable[[str, str, str], Tuple[bool, Optional[str], Optional[str]]]],
) -> List[ValidationResult]:
    results: List[ValidationResult] = []
    for spec in specs:
        error_type = ""
        is_valid = 0
        validate_status = "invalid"
        val_output: Optional[str] = None

        if spec.problem_path is None or not spec.problem_path.exists():
            error_type = "problem_missing"
        elif not spec.plan_path.exists():
            error_type = "no_plan"
        elif validator is None:
            error_type = "validator_missing"
        else:
            normalize_plan_file(spec.plan_path)
            try:
                ok, message, val_output = validator(str(domain_path), str(spec.problem_path), str(spec.plan_path))
            except Exception as exc:
                ok = False
                message = f"validator_error: {exc}"
            if ok:
                is_valid = 1
                validate_status = "valid"
            else:
                error_type = message or "validation_failed"
                validate_status = "invalid"

        append_plan_validation_to_log(
            spec.log_path,
            validate_status=validate_status,
            val_output=val_output,
        )

        results.append(
            ValidationResult(
                domain=DOMAIN_NAME,
                instance=spec.instance_id,
                template=spec.template,
                log_file=str(spec.log_path),
                seed=spec.seed,
                is_valid=is_valid,
                error_type=error_type,
            )
        )

    return results


def normalize_plan_file(plan_path: Path) -> None:
    text = plan_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    updated: List[str] = []
    changed = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            updated.append("")
            continue
        if stripped.startswith(";"):
            updated.append(line)
            continue
        if stripped.startswith("(") and stripped.endswith(")"):
            updated.append(stripped)
            continue
        updated.append(f"({stripped})")
        changed = True
    if changed:
        plan_path.write_text("\n".join(updated) + "\n", encoding="utf-8")


def format_log_timestamp() -> str:
    timestamp = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    return f"[{timestamp}] INFO :: "


def append_plan_validation_to_log(log_path: Path, validate_status: str, val_output: Optional[str]) -> None:
    if not log_path.exists():
        return

    marker = "### Plan Validation ###"
    if val_output is None:
        val_output = "<val_output_unavailable>"
    val_output = val_output.rstrip("\n")

    prefix = format_log_timestamp()
    block = "\n".join(
        [
            f"{prefix}{marker}",
            "",
            val_output,
            "",
            f"{prefix}Validate status: {validate_status}",
            "",
        ]
    )

    text = log_path.read_text(encoding="utf-8", errors="replace")
    idx = text.find(marker)
    if idx != -1:
        return

    separator = "" if text.endswith("\n") else "\n"
    log_path.write_text(text + separator + block, encoding="utf-8")


def write_results_csv(results: List[ValidationResult], results_path: Path) -> None:
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with results_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["domain", "instance", "template", "log_file", "seed", "is_valid", "error_type"])
        for result in results:
            writer.writerow(
                [
                    result.domain,
                    result.instance,
                    result.template,
                    result.log_file,
                    result.seed,
                    result.is_valid,
                    result.error_type,
                ]
            )


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def natural_sort_key(value: str) -> List[object]:
    parts = re.split(r"(\\d+)", value)
    key: List[object] = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part)
    return key


def generate_latex_table(
    results: List[ValidationResult],
    table_path: Path,
    log_file_basename: bool,
) -> None:
    _ = log_file_basename
    seed_order = [1, 2, 3]
    template_set = {result.template for result in results}
    preferred_templates = [t for t in ["grounded", "lifted"] if t in template_set]
    extra_templates = sorted(template_set - set(preferred_templates))
    templates = preferred_templates + extra_templates
    if not templates:
        templates = ["grounded", "lifted"]

    instances = sorted({result.instance for result in results}, key=natural_sort_key)

    validity_map: dict[tuple[str, str, int], int] = {}
    for result in results:
        key = (result.instance, result.template, result.seed)
        validity_map[key] = max(validity_map.get(key, 0), result.is_valid)

    column_aligns = "l" + ("|cccc" * len(templates))
    lines: List[str] = []
    lines.append(f"\\begin{{tabular}}{{{column_aligns}}}")
    lines.append("\\hline")

    header_cells = ["Instance"]
    for template in templates:
        header_cells.append(f"\\multicolumn{{4}}{{c}}{{{latex_escape(template)}}}")
    lines.append(" & ".join(header_cells) + " \\\\")

    subheader_cells = [""]
    for _ in templates:
        subheader_cells.extend(["s1", "s2", "s3", "total"])
    lines.append(" & ".join(subheader_cells) + " \\\\")
    lines.append("\\hline")

    totals = [0 for _ in range(len(templates) * 4)]
    for instance in instances:
        row_cells = [latex_escape(instance)]
        col_index = 0
        for template in templates:
            seed_values = []
            for seed in seed_order:
                value = validity_map.get((instance, template, seed), 0)
                seed_values.append(value)
                row_cells.append(str(value))
                totals[col_index] += value
                col_index += 1
            total_value = 1 if any(seed_values) else 0
            row_cells.append(str(total_value))
            totals[col_index] += total_value
            col_index += 1
        lines.append(" & ".join(row_cells) + " \\\\")

    total_cells = ["Total"]
    total_cells.extend(str(value) for value in totals)
    lines.append("\\hline")
    lines.append(" & ".join(total_cells) + " \\\\")
    lines.append("\\hline")
    lines.append("\\end{tabular}")
    table_path.parent.mkdir(parents=True, exist_ok=True)
    table_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Blocksworld logs and generate results.csv and results.tex."
    )
    parser.add_argument(
        "--outdir",
        default="logs/blocksworld",
        help="Directory containing .log/.plan files and where outputs are written.",
    )
    parser.add_argument(
        "--base-dir",
        default="benchmarks/blocksworld",
        help="Blocksworld benchmark base directory (domain.pddl, grounded/, lifted/).",
    )
    parser.add_argument(
        "--results-path",
        default=None,
        help="Output path for results.csv (default: <outdir>/results.csv).",
    )
    parser.add_argument(
        "--table-path",
        default=None,
        help="Output path for results.tex (default: <outdir>/results.tex).",
    )
    parser.add_argument(
        "--log-file-basename",
        action="store_true",
        help="Use only the log filename (not full path) in the LaTeX table.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    outdir = Path(args.outdir)
    base_dir = Path(args.base_dir)
    domain_path = base_dir / "domain.pddl"
    lifted_dir = base_dir / "lifted"
    if not domain_path.exists():
        raise FileNotFoundError(f"Domain file not found: {domain_path}")
    if not lifted_dir.exists():
        raise FileNotFoundError(f"Lifted directory not found: {lifted_dir}")

    specs = collect_log_specs(outdir, lifted_dir)
    validator = load_validator()
    results = validate_specs(specs, domain_path, validator)

    results_path = Path(args.results_path) if args.results_path else (outdir / "results.csv")
    table_path = Path(args.table_path) if args.table_path else (outdir / "results.tex")

    write_results_csv(results, results_path)
    generate_latex_table(results, table_path, args.log_file_basename)


if __name__ == "__main__":
    main()
