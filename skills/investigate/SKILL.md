---
name: investigate
description: Answer "how does X work" and "why is it like this" from cited evidence, changing no code. Use before changing unfamiliar code, for walkthroughs, placement and ownership questions, design rationale, and regressions.
---

# Investigate

A read-only route. The deliverable is a cited answer, not a patch. Change no code.

Two questions, usually asked together:

- **How** does it work now? Runtime behavior, data flow, ownership, layering.
- **Why** is it shaped this way? Rationale, tradeoffs, the constraint that is no longer visible.

## How it works

1. **Find the entry points.** Where does control enter this subsystem: route, command, event, lifecycle hook, cron.
2. **Trace one real path end to end.** Follow one concrete request or action all the way through. A traced path beats a directory listing.
3. **Name the data shape at each hop.** What goes in, what comes out, what is mutated on the way.
4. **Mark the boundaries.** Where does trusted internal data become untrusted external data, and where is it validated.
5. **Note what surprised you.** The thing that did not match your first guess is usually the thing the reader needs.

Cite `file:line` for every claim. A search that finds nothing is still an answer — say so.

## Why it is that way

Evidence in rough order of reliability:

1. **ADRs** in `docs/adr/`. An accepted ADR is the answer, not a clue.
2. **Git history.** `git log -S<symbol>`, `git log --follow <file>`, then read the commit messages and the PR they came from.
3. **`git blame` on the exact line**, then the commit that introduced it.
4. **Issues, PR discussion, and code comments** that explain a constraint.
5. **Tests.** A test asserting an odd behavior often encodes the reason for it.

**Report a null result.** "Nobody wrote down why" is an answer, and it is better than a plausible story. Do not invent a rationale.

## Rules

- Never fabricate a file path, function name, symbol, or commit.
- Label every claim in the same sentence: **measured** (you ran it and saw it), **inferred** (it follows from cited code), or **guess**.
- Distinguish what the code does from what its name or comment says it does.
- Route bulk reading to subagents when the surface is large. Keep findings in the main thread, not raw file dumps.

## Output

- **Answer** in two or three sentences, up front.
- **The traced path**, with `file:line` at each hop.
- **Why it is this way**, with evidence, or an explicit "no recorded rationale".
- **What this means for the change you are about to make**, if one is planned.
