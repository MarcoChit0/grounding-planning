#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

DOMAIN_FILE="./benchmarks/blocksworld/domain.pddl"
LIFTED_DIR="./benchmarks/blocksworld/lifted"
GROUNDED_DIR="./benchmarks/blocksworld/grounded"
LANDMARKS_DIR="./benchmarks/blocksworld/landmarks"

mkdir -p "$GROUNDED_DIR" "$LANDMARKS_DIR"

shopt -s nullglob
instances=("$LIFTED_DIR"/*.pddl)

if ((${#instances[@]} == 0)); then
  echo "No .pddl instances found in $LIFTED_DIR" >&2
  exit 1
fi

for instance_path in "${instances[@]}"; do
  instance_name="$(basename "$instance_path" .pddl)"

  uv run ./res/pyperplan/pyperplan -s grounded "$DOMAIN_FILE" "$instance_path" \
    > "$GROUNDED_DIR/$instance_name.txt"

  uv run ./res/pyperplan/pyperplan -s landmarks "$DOMAIN_FILE" "$instance_path" \
    > "$LANDMARKS_DIR/$instance_name.txt"
done
