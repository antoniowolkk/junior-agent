---
name: swarm
description: Fan out N parallel subagents over slices of one job, drain them, and return a single consolidated report. Use for /swarm, "swarm this", parallel coverage sweeps, races between approaches, and wide exploration.
---

# Swarm

Fan out N parallel workers. They cover separate slices, race the same brief, or both. The parent waits, aggregates, and returns one report.

This is the **guard the context window** principle made concrete: bulk reading and bulk editing happen in the workers, findings come back to the main thread.

## Phases

Write one todo per phase before launching anything.

### A. Frame

1. **State the done predicate** and the artifact or report the swarm must return.
2. **Choose the shape.** Partition into slices, race N workers on the same brief, or mix. For a race, declare the selection rule up front: `first pass`, `rank all`, or `best-of`.
3. **Set N.** From the user, or from the shape. Keep it proportional — a 4-file sweep does not need 8 workers.
4. **Give each worker its own writable output** when it writes anything. Two workers writing one file is a corruption bug waiting to happen.

Workers that edit the same files must be serialized or given separate worktrees. Eliminate the sharing before adding coordination.

### B. Fan out

Spawn all N in a single message so they run concurrently.

Every brief stands alone. The worker cannot see this conversation. Include:

- The goal and why it matters.
- Its exact slice or race arm, with explicit boundaries.
- How to verify its own result.
- What to report, and in what shape.

Require every worker to end with `PASS`, `ISSUES`, or `BLOCKED` plus evidence. If a worker drops out, proceed with N-1 and say so.

### C. Aggregate

Read the terminal results. For coverage, every required slice needs a result — a missing slice is a gap, not a pass. For a race, apply the rule you declared in phase A. Do not relax it after seeing the results.

Never paste raw worker dumps into the main thread. That defeats the point.

### D. Report

One consolidated report: a compact result table, one evidenced line per issue, explicit gaps and dropouts, and the selection rule if you raced.

## Rules

- A worker's summary is not evidence. For code changes, read the actual diff.
- Spawn read-only workers for investigation. Reserve write access for workers that must edit.
- `AGENTS.md` section 7 applies to every worker. A delegate cannot grant itself a permission the parent does not have.
