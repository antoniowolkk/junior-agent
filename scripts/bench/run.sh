#!/bin/bash
# Runs one benchmark task N times with junior installed and N times without,
# using the real `claude` CLI headlessly, and grades each run with the
# task's hidden test. See scripts/bench/README.md for what this measures
# and why.
#
# Usage: scripts/bench/run.sh <task-name> [trials]
#   task-name: a directory under scripts/bench/tasks/ (e.g. billsplit)
#   trials:    runs per condition (default 5)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TASK="${1:?usage: run.sh <task-name> [trials]}"
TRIALS="${2:-5}"
TASK_DIR="$SCRIPT_DIR/tasks/$TASK"
WORK_DIR="$(mktemp -d)"
RESULTS="$SCRIPT_DIR/results/$(date +%Y-%m-%d)-$TASK.tsv"

if [ ! -d "$TASK_DIR" ]; then
  echo "no such task: $TASK_DIR" >&2
  exit 1
fi

mkdir -p "$SCRIPT_DIR/results"
echo -e "condition\ttrial\tpass\tturns\tduration_ms\tcost_usd\tinput_tokens\toutput_tokens\tcache_read_tokens\tcache_creation_tokens" > "$RESULTS"

build_workdir () {
  local cond="$1" dir="$2"
  rm -rf "$dir"
  mkdir -p "$dir"
  cp "$TASK_DIR"/files/* "$dir"/
  cp "$TASK_DIR"/ISSUE.md "$dir"/
  if [ "$cond" = "junior" ]; then
    cp "$TASK_DIR"/AGENTS.md "$dir"/AGENTS.md
    ln -sf AGENTS.md "$dir"/CLAUDE.md
    mkdir -p "$dir"/.claude/skills
    cp -r "$REPO_ROOT"/skills/* "$dir"/.claude/skills/
  fi
}

for cond in bare junior; do
  for trial in $(seq 1 "$TRIALS"); do
    D="$WORK_DIR/${cond}_${trial}"
    build_workdir "$cond" "$D"

    echo "=== $TASK / $cond trial $trial ===" >&2
    ( cd "$D" && claude -p "Read ISSUE.md and fix the bug it describes." \
        --output-format json \
        --permission-mode acceptEdits \
        --allowedTools "Bash(python3 *)" \
        --max-budget-usd 0.75 \
        --model sonnet \
        > "$D.out.json" 2> "$D.err" )

    ok="FAIL"
    if python3 "$TASK_DIR/hidden_grade.py" "$D" > "$D.grade.txt" 2>&1; then ok="PASS"; fi

    row=$(python3 - "$D.out.json" "$cond" "$trial" "$ok" <<'PYEOF'
import json, sys
path, cond, trial, ok = sys.argv[1:5]
d = json.load(open(path))
u = d.get("usage", {})
print(f"{cond}\t{trial}\t{ok}\t{d.get('num_turns')}\t{d.get('duration_ms')}\t{d.get('total_cost_usd')}\t{u.get('input_tokens')}\t{u.get('output_tokens')}\t{u.get('cache_read_input_tokens')}\t{u.get('cache_creation_input_tokens')}")
PYEOF
)
    echo -e "$row" >> "$RESULTS"
    echo "$row" >&2
  done
done

echo "results: $RESULTS" >&2
echo "workdir kept at: $WORK_DIR" >&2
