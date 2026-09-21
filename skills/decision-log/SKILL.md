---
name: decision-log
description: Keep a reviewable trail for long-running or unattended work as a TSV log, one row per decision, with evidence pointers. Use for autonomous runs, multi-phase work, or anything a human reviews after stepping away.
---

# Decision log

One canonical log, so a human audits decisions instead of the whole transcript.

## Format

A single TSV file, one row per decision. Cells stay single-line. Evidence is a pointer, never prose.

| Column | What goes in it |
| --- | --- |
| `ts` | ISO8601 timestamp |
| `phase` | The phase or workstream |
| `decision` | What was chosen or done, one line |
| `why` | The reason in plain words |
| `evidence` | Commit SHA, PR number, `file:line`, artifact or screenshot path |
| `result` | `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, `open` |

```
ts	phase	decision	why	evidence	result
2026-09-21T09:02:00Z	frame	counted the work first, ~100 components	wanted the size before a long run	commit 3a9f1c2	found 5 blockers
2026-09-21T09:40:00Z	harness	screenshotted the old version first	so we can catch any visual change	scripts/snapshot.sh	120 baselines saved
2026-09-21T11:15:00Z	widget	moved styles without changing appearance	keep the change small, result identical	commit 7c21e0a	pixel-diff 0, tests pass
2026-09-21T12:30:00Z	widget	threw out a subagent's work, screenshots blank	checked real files, not its summary	worktree reset	reverted, brief tightened
```

Illustration only. Do not copy these rows.

## What to log

Decision points and checkpoints, not every action. A fork chosen. A unit completed with its verification result. A pivot or revert with its trigger. A blocker surfaced. One row per iteration on a loop run. Skip the trivial.

Write each row the way you would tell a teammate what you did. Plain words, concrete actions, no jargon.

## Rules

- One row is one decision.
- **Append-only.** A wrong call gets a new row that supersedes it. Never edit or delete history.
- Prefer evidence produced by a committed script over a hand-made one-off — a reviewer can re-run the script.
- Guard the bytes if cells come from generated text: strip tabs and newlines, and prefix any cell starting with `=`, `+`, `-`, or `@` with a single quote so a spreadsheet does not evaluate it.

## Where it lives

`decisions.tsv` in the working directory, or `.audit/<task-slug>.tsv` when several efforts run at once. Not committed by default. Commit it when the work is ambitious enough that a reviewer needs the trail to trust the result.

## Audit it before handing back

Walk the log against what actually happened:

- Every row maps to a real action. Cut aspirational entries.
- Each evidence pointer resolves and shows what the row claims.
- A fork or abandoned approach that shaped the work but is not logged is a gap. Add it.

Fix the log, not the story. If the work diverged from what a row claims, the row is wrong.

## Attention section

Any reply for a run that produced a trail ends with an **Attention** section: what deserves scrutiny first. Decisions logged with weak evidence, verification claimed without proof, choices that look risky in hindsight, gaps a casual skim would miss. "No flags" is a valid value.

For high-stakes runs, have a subagent read the trail and flag these instead of self-reviewing.

## Reading it

`column -s$'\t' -t decisions.tsv` renders it in a terminal. GitHub renders a committed TSV as a table.
