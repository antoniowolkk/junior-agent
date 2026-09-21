# ADR-0001: Record architecture decisions

- **Status:** Accepted
- **Date:** 2026-10-14
- **Deciders:** Sari (Product), Rio (Tech lead)

## Context

Significant technical decisions on this project were being made in chat threads, meetings, and one person's head. When that person is unavailable, nobody can explain why the system is the way it is.

The problem is worse with AI coding agents. An agent has no memory of a meeting it was not in. Given no written record, it invents its own architecture — plausible, internally consistent, and inconsistent with ours.

## Decision

We record every significant, hard-to-reverse decision as a short markdown file in `docs/adr/`, numbered in sequence, using `docs/adr/0000-template.md`.

- **Hard to reverse** (database, framework, auth model, API shape, hosting, data schema, third-party dependency we would build on): write an ADR, review it as its own change, then implement.
- **Easy to reverse:** decide, note the reasoning in the commit message, move on.

ADRs are immutable once accepted. To change a decision, write a new ADR that supersedes the old one and update the old one's Status line.

`AGENTS.md` instructs agents to read `docs/adr/` before coding.

## Alternatives considered

- **A wiki or Confluence space** — drifts out of sync with the code, and agents working in the repo cannot see it.
- **Comments in the code** — captures what, not why, and cannot describe rejected alternatives.
- **No records** — the status quo that created this problem.

## Consequences

**Good**
- New people and agents can answer "why is it like this?" without interrupting anyone.
- The ADR review replaces the long architecture meeting.
- Agents follow our conventions instead of inventing their own.

**Bad / accepted cost**
- Small ongoing writing overhead.
- Requires discipline: an ADR written after the fact is worth much less.

**Follow-ups**
- Add `AGENTS.md` (and a `CLAUDE.md` symlink to it) at the repo root.
- Backfill ADRs for the two or three biggest existing decisions.
