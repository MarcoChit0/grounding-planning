#!/usr/bin/env python3
"""
obfuscate_pddl.py — PDDL obfuscator with two modes:
  1) random (default): random 16-char ids (seedable; 16-char is from original paper)
  2) simple: a1/a2... for actions, p1/p2... for predicates, o1/o2... for objects,
             t1/t2... for types, ?v1/?v2... for variables,
             d1/d2... for domains, pr1/pr2... for problems

Notes:
- Comments (`; ...`) are ignored during collection and **removed** from output.
- Simple mode uses lightweight parsing with parentheses balancing (no full parser).
"""

from __future__ import annotations

import json
import pathlib
import random
import re
import string
import sys
from typing import Dict, Iterable, List, Set, Tuple

import click

###############################################################################
# Configuration
###############################################################################

# Minimal PDDL reserved words (extend as needed)
_RESERVED: Set[str] = {
    "define", "domain", "problem", "requirements", "strips", "typing", "types",
    "predicates", "action", "parameters", "precondition", "effect", "init",
    "goal", "objects", "constants", "functions", "and", "not", "or", "when",
    "forall", "exists", "either", "increase", "decrease", "assign", "total-time",
    "durative-actions", "constraints", "object",  # built-in type
}

# Token regex (excludes leading '?' so variables aren't matched as tokens)
# Token regex (excludes leading '?' so variables aren't matched as tokens)
_TOKEN_RE = re.compile(r"[A-Za-z0-9_\-]+")

# Characters to use for random identifiers
_ALPHANUM = string.ascii_lowercase + string.digits


###############################################################################
# Comment handling
###############################################################################

def _strip_comments(text: str) -> str:
    """Remove PDDL comments (semicolon to end-of-line)."""
    return re.sub(r";[^\n]*", "", text)


###############################################################################
# FS helpers
###############################################################################

def _pddl_files(directory: pathlib.Path) -> List[pathlib.Path]:
    """Return every `*.pddl` file directly contained in *directory*."""
    return sorted(directory.glob("*.pddl"))


###############################################################################
# Random-mode mapping (original behaviour)
###############################################################################

def _rand_name(existing: Set[str], length: int = 16) -> str:
    """Generate a *unique* random identifier of given *length*."""
    while True:
        name = "".join(random.choice(_ALPHANUM) for _ in range(length))
        if name not in existing and name[0].isalpha():  # must start with letter
            return name

def _collect_symbols_random(files: Iterable[pathlib.Path]) -> Dict[str, str]:
    """Scan *files* and return a mapping of original → random obfuscated symbols."""
    mapping: Dict[str, str] = {}
    seen_generated: Set[str] = set()

    for path in files:
        text = _strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
        for tok in _TOKEN_RE.findall(text):
            lower = tok.lower()
            if lower in _RESERVED or lower.isnumeric() or lower == "-":
                continue
            if tok not in mapping:
                obf = _rand_name(seen_generated)
                mapping[tok] = obf
                seen_generated.add(obf)
    return mapping


###############################################################################
# Simple-mode mapping (category-wise sequential names)
###############################################################################

# Regex “hooks” to find block heads; we’ll then balance parentheses.
_HEAD_PATTERNS = {
    "predicates": re.compile(r"\(\s*:\s*predicates\b", re.IGNORECASE),
    "types":      re.compile(r"\(\s*:\s*types\b", re.IGNORECASE),
    "objects":    re.compile(r"\(\s*:\s*objects\b", re.IGNORECASE),
    "constants":  re.compile(r"\(\s*:\s*constants\b", re.IGNORECASE),
}
_ACTION_RE = re.compile(r"\(\s*:\s*action\s+([A-Za-z0-9_\-+]+)", re.IGNORECASE)
_VAR_RE = re.compile(r"\?([A-Za-z0-9_\-+]+)")
_SPLIT_TOK_RE = re.compile(r"[A-Za-z0-9_\-+]+")
_DOMAIN_NAME_RE = re.compile(r"\(\s*define\s*\(\s*domain\s+([A-Za-z0-9_\-+]+)\s*\)", re.IGNORECASE)
_PROBLEM_NAME_RE = re.compile(r"\(\s*define\s*\(\s*problem\s+([A-Za-z0-9_\-+]+)\s*\)", re.IGNORECASE)

def _find_block_spans(text: str, head: str) -> List[Tuple[int, int]]:
    """Return [ (start,end) ] spans for each full s-expr starting at '(:head ...)'."""
    spans: List[Tuple[int, int]] = []
    pat = _HEAD_PATTERNS[head]
    for m in pat.finditer(text):
        start = m.start()
        depth = 0
        end = None
        for i in range(start, len(text)):
            c = text[i]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is not None:
            spans.append((start, end))
    return spans

def _extract_actions(text: str) -> Set[str]:
    return set(_ACTION_RE.findall(text))

def _extract_predicates(text: str) -> Set[str]:
    preds: Set[str] = set()
    for s, e in _find_block_spans(text, "predicates"):
        block = text[s:e]
        # In a :predicates block, each predicate is "( name ... )"
        for head in re.findall(r"\(\s*([A-Za-z0-9_\-+]+)", block):
            if head.lower() not in _RESERVED:
                preds.add(head)
    return preds

def _extract_types(text: str) -> Set[str]:
    types: Set[str] = set()
    for s, e in _find_block_spans(text, "types"):
        body = text[s:e]
        for tok in _SPLIT_TOK_RE.findall(body):
            low = tok.lower()
            if low == "-" or low in _RESERVED:
                continue
            types.add(tok)
    return types

def _extract_objects_and_constants(text: str) -> Set[str]:
    objs: Set[str] = set()
    for head in ("objects", "constants"):
        for s, e in _find_block_spans(text, head):
            body = text[s:e]
            tokens = _SPLIT_TOK_RE.findall(body)
            i = 0
            while i < len(tokens):
                if tokens[i] == "-":
                    i += 2  # skip '-' and the type name
                else:
                    tok = tokens[i]
                    if not tok.startswith("?") and tok.lower() not in _RESERVED:
                        objs.add(tok)
                    i += 1
    return objs

def _extract_variables(text: str) -> Set[str]:
    # Return variables with leading '?', e.g., '?x'
    return set("?" + name for name in _VAR_RE.findall(text))

def _extract_domain_names(text: str) -> Set[str]:
    return set(_DOMAIN_NAME_RE.findall(text))

def _extract_problem_names(text: str) -> Set[str]:
    return set(_PROBLEM_NAME_RE.findall(text))

def _collect_symbols_simple(files: Iterable[pathlib.Path]) -> Dict[str, str]:
    """
    Deterministically map categories:
      actions->a1, predicates->p1, objects/constants->o1, types->t1, vars->?v1,
      domain names->d1, problem names->pr1
    """
    actions: Set[str] = set()
    predicates: Set[str] = set()
    types: Set[str] = set()
    objects: Set[str] = set()
    variables: Set[str] = set()
    domains: Set[str] = set()
    problems: Set[str] = set()

    for path in files:
        text = _strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
        actions |= _extract_actions(text)
        predicates |= _extract_predicates(text)
        types |= _extract_types(text)
        objects |= _extract_objects_and_constants(text)
        variables |= _extract_variables(text)
        domains |= _extract_domain_names(text)
        problems |= _extract_problem_names(text)

    mapping: Dict[str, str] = {}

    # Sort to make numbering stable across runs
    for i, sym in enumerate(sorted(actions), start=1):
        mapping[sym] = f"a{i}"
    for i, sym in enumerate(sorted(predicates), start=1):
        mapping[sym] = f"p{i}"
    for i, sym in enumerate(sorted(objects), start=1):
        mapping[sym] = f"o{i}"
    for i, sym in enumerate(sorted(types), start=1):
        mapping[sym] = f"t{i}"
    for i, sym in enumerate(sorted(variables), start=1):
        mapping[sym] = f"?v{i}"
    for i, sym in enumerate(sorted(domains), start=1):
        mapping[sym] = f"d{i}"
    for i, sym in enumerate(sorted(problems), start=1):
        mapping[sym] = f"pr{i}"

    return mapping


###############################################################################
# Rewriter
###############################################################################

def _rewrite(text: str, mapping: Dict[str, str], *, strip_comments: bool = True) -> str:
    """
    Replace every *mapping* key that appears as an isolated token in *text*.
    Optionally strip comments from the output.
    """
    if strip_comments:
        text = _strip_comments(text)

    if not mapping:
        return text  # Nothing to do.

    # One giant alternation, longest-first for safety (though we have token guards).
    keys = sorted(mapping.keys(), key=len, reverse=True)
    pattern = re.compile(
        r"(?<![A-Za-z0-9_\-?])(" + "|".join(map(re.escape, keys)) + r")(?![A-Za-z0-9_\-])"
    )
    return pattern.sub(lambda m: mapping[m.group(0)], text)


###############################################################################
# CLI
###############################################################################

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("input_dir", type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.argument("output_dir", required=False, type=click.Path(file_okay=False, path_type=pathlib.Path))
@click.option(
    "-s", "--seed", type=int,
    help="Seed for RNG (random mode only). Use the same seed to reproduce the same obfuscation."
)
@click.option(
    "-m", "--mode", type=click.Choice(["random", "simple"], case_sensitive=False),
    default="random", show_default=True,
    help="Obfuscation mode: 'random' (8-char ids) or 'simple' (a1/p1/o1/t1/?v1, d1/pr1)."
)
def main(input_dir: pathlib.Path, output_dir: pathlib.Path | None, seed: int | None, mode: str) -> None:
    """
    Obfuscate a PDDL domain + problems.

    INPUT_DIR should contain domain.pddl and problem files.
    OUTPUT_DIR (optional) defaults to INPUT_DIR/obfuscated.
    Comments are removed in the output.
    """

    in_dir = input_dir.expanduser().resolve()
    out_dir = (output_dir.expanduser().resolve() if output_dir else in_dir / "obfuscated")
    out_dir.mkdir(parents=True, exist_ok=True)

    files = _pddl_files(in_dir)
    if not files:
        click.echo("No .pddl files found in input directory.", err=True)
        sys.exit(1)

    if mode.lower() == "random":
        if seed is not None:
            click.echo(f"[INFO] Using deterministic RNG seed {seed}")
            random.seed(seed)
        mapping = _collect_symbols_random(files)
    else:
        if seed is not None:
            click.echo("[WARN] --seed is ignored in simple mode.", err=True)
        mapping = _collect_symbols_simple(files)

    # Rewrite every file (comments are removed; replacements only hit code)
    for path in files:
        original = path.read_text(encoding="utf-8", errors="ignore")
        rewritten = _rewrite(original, mapping, strip_comments=True)
        (out_dir / path.name).write_text(rewritten, encoding="utf-8")
        click.echo(f"[OK] {path.name} → {(out_dir / path.name).relative_to(out_dir)}")

    # Dump the mapping so the process is reversible.
    with (out_dir / "mapping.json").open("w", encoding="utf-8") as fp:
        json.dump(mapping, fp, indent=2, ensure_ascii=False)
        click.echo(f"Mapping file written to {(out_dir / 'mapping.json').relative_to(out_dir)}")

if __name__ == "__main__":
    main()
