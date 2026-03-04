#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

DOMAIN_FILE="./benchmarks/blocksworld/domain.pddl"
LIFTED_DIR="./benchmarks/blocksworld/lifted"
GROUNDED_DIR="./benchmarks/blocksworld/grounded"
LANDMARKS_DIR="./benchmarks/blocksworld/landmarks"
MEMORY_LIMIT_KB=$((30 * 1024 * 1024))

mkdir -p "$GROUNDED_DIR" "$LANDMARKS_DIR"

shopt -s nullglob
instances=("$LIFTED_DIR"/medium-p*.pddl)

if ((${#instances[@]} == 0)); then
  echo "No medium instances found in $LIFTED_DIR" >&2
  exit 1
fi

failures=0

for instance_path in "${instances[@]}"; do
  instance_name="$(basename "$instance_path" .pddl)"

  grounded_out="$GROUNDED_DIR/$instance_name.txt"
  landmarks_out="$LANDMARKS_DIR/$instance_name.txt"

  echo "Running grounded for $instance_name..."
  if ! (ulimit -v "$MEMORY_LIMIT_KB"; uv run ./res/pyperplan/pyperplan -s grounded "$DOMAIN_FILE" "$instance_path" >"$grounded_out"); then
    echo "WARN: grounded failed for $instance_name" >&2
    rm -f "$grounded_out"
    ((failures += 1))
  fi

  echo "Running landmarks for $instance_name..."
  if ! (ulimit -v "$MEMORY_LIMIT_KB"; uv run ./res/pyperplan/pyperplan -s landmarks "$DOMAIN_FILE" "$instance_path" >"$landmarks_out"); then
    echo "WARN: landmarks failed for $instance_name" >&2
    rm -f "$landmarks_out"
    ((failures += 1))
  fi
done

if ((failures > 0)); then
  echo "Completed with $failures failure(s)." >&2
  exit 1
fi

echo "Completed successfully for ${#instances[@]} medium instance(s)."
