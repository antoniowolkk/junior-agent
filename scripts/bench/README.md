# Benchmark: does installing junior change the outcome?

A small, honest measurement, not a marketing number. Each task is a tiny repo
with one injected bug and a visible test suite that passes despite it. The
same one-line prompt ("read ISSUE.md and fix the bug it describes") is run
headlessly through the real `claude` CLI twice: once with nothing installed
("bare"), once with `AGENTS.md` and `.claude/skills/` installed ("junior").
A hidden test the agent never sees decides pass/fail. Everything else —
model, prompt, budget cap — is identical between conditions.

Run it yourself:

```bash
scripts/bench/run.sh billsplit 3
scripts/bench/run.sh rate_limiter 5
```

Raw results from every run are in [`results/`](results/), one TSV per
task per day.

## What was run (2026-09-23)

Two tasks, `claude-sonnet-5`, 8 runs per condition total:

- **`billsplit`** — `amount_cents // n_people` drops the remainder, so a
  bill that doesn't divide evenly shortchanges the total. Existing tests
  only cover evenly-divisible cases, so they pass with the bug in place.
- **`rate_limiter`** — the sliding-window prune keeps expired timestamps
  and drops recent ones (`>` where it should be `<`), so the limiter
  undercounts and lets more requests through than configured. Existing
  tests never send more requests than the limit, so they pass with the bug
  in place too.

| | bare | junior | delta |
| --- | --- | --- | --- |
| success rate (16 runs) | 8/8 | 8/8 | none detected |
| avg wall-clock | 24.0s | 34.2s | **+43%** |
| avg cost | $0.146 | $0.170 | **+17%** |
| avg output tokens | 1448 | 2571 | **+78%** |

## What this actually shows

No success-rate gap. Both tasks were solvable by the bare model without any
scaffolding — the model is simply strong enough to reproduce and fix a
subtly-wrong function on its own, TDD or not. What's real and consistent
across both tasks: junior costs more time and more tokens per task, on
tasks it doesn't need the help for. That is not a flaw this benchmark
uncovered — it's the trade-off the README already names: *"the cost is
speed."* Restating the task, writing a failing test first, and reporting
evidence before declaring done is real work, and it shows up here as real
cost, not as a hidden discount.

This benchmark does not (yet) measure the thing the pack actually claims:
that a bare agent will guess, declare success on a green build, or take an
irreversible action, and junior won't. Both injected bugs were within reach
of the base model either way, so neither run exercised that failure mode.
Testing it would need a task engineered around a tempting shortcut or an
irreversible action, graded on whether the agent takes it — a different
and harder benchmark to build honestly, not a bigger version of this one.

## Limitations, stated plainly

- n=8 per condition, two tasks, one model, one date. Not a statistically
  powered study — a pilot.
- Both tasks were chosen to be catchable by a hidden test, which biases
  toward tasks a strong model can also just solve. That is exactly why no
  success-rate gap shows up.
- `--permission-mode acceptEdits --allowedTools "Bash(python3 *)"` is
  narrower than a real interactive session; an earlier version of this
  harness left Bash unauthorized entirely, which silently denied every
  test run in both conditions and produced meaningless numbers. If you
  rerun this, verify `permission_denials` is empty in the output JSON
  before trusting the result.
- TDD's "stop and show the human" step has no human to show in a headless
  run; `AGENTS.md` here says so explicitly. A real interactive session
  would insert a real review pause there, which this benchmark cannot
  measure at all.

## Adding a task

A task is a directory under `tasks/<name>/`:

- `files/` — the buggy code plus a visible test suite that passes anyway.
- `ISSUE.md` — a vague, realistic bug report, not a spec.
- `AGENTS.md` — the junior-condition project file, filled in for this repo.
- `hidden_grade.py` — takes a repo path as `argv[1]`, prints PASS/FAIL and
  exits 0/1. Must fail against the unmodified `files/`, and pass against a
  hand-written correct fix — check both before trusting a result against it.
