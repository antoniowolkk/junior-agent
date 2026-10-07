---
name: spec
description: Turn one feature request into a short written spec whose Given/When/Then criteria each map to a named test, with non-goals and open questions for the human. Use for /spec, "write a spec", "acceptance criteria for this", "what does done mean here", or before building a feature whose finish line is fuzzy. Skip for a bug with a reproduction or a one-line change.
---

# Spec

A spec is the bridge between "what we want" and "which tests prove it". Each acceptance criterion becomes one test, and the spec changes whenever the code teaches you the criterion was wrong.

## 0. Precedence and position

`AGENTS.md` section 7 (Guardrails) outranks everything here. Where this says proceed and section 7 says ask, ask.

This skill overlaps `docs/prd.md`, which already holds user stories with Given/When/Then. The split:

| Artifact | Scope | Author | Changes when |
| --- | --- | --- | --- |
| `docs/prd.md` | Whole product or feature area | Human; the agent does not edit it | The human decides |
| Spec (this skill) | One change, one PR | Agent drafts, human signs off | Implementation contradicts a criterion |

Order: `descope` decides whether to build, `delegate` sizes how much to take, this pins what done means, `architect` designs the shape. If the PRD already has checkable criteria for this change, skip to section 4 and map them to tests.

## 1. Gather

1. Read the request, the PRD, and any linked issue or ADR.
2. Read the code the change touches. A criterion written without reading it is a guess.
3. Label every fact you will rely on: **measured** (read or ran it), **inferred** (follows from what you read), **guess** (neither). Guesses go to open questions, not criteria.

## 2. Write the spec

Put it in the PR description, or `docs/specs/<slug>.md` if the repo has that folder. Keep it under one screen.

```
Goal:        <who it is for, what is different for them afterwards>
Criteria:
  AC1  Given <state>, when <action>, then <observable result>.
  AC2  Given <invalid input>, when <action>, then <specific error>.
Non-goals:   <what a reader would assume is included but is not>
Open:        <question> — needed before AC<n> can be written
```

## 3. Check each criterion

| Check | Fails when |
| --- | --- |
| Observable | "Then" names internal state, not something a caller or user sees |
| Binary | Two reasonable people could disagree on pass or fail |
| One behavior | The line contains "and" joining two outcomes; split it |
| Unhappy path | No criterion covers invalid input, empty state, or a failure the PRD lists |
| No design | The criterion names a class, table, or library; that belongs to `architect` |
| Sourced | It rests on a guess instead of a measured or inferred fact |

Three to seven criteria is the normal range. More usually means two changes in one spec.

## 4. Trace criteria to tests

1. Before implementation, add a table to the spec: `AC | test file::name | status`.
2. Write each test so its name or a comment carries the AC id.
3. A criterion with no test is not done. A test with no criterion is either missing from the spec or is scope creep; say which.
4. At hand-off, every row reads `pass` with the command you ran (measured), never "should pass".

## 5. Open questions

- Ask before writing the criterion the question blocks. Do not fill the gap with a default and mention it later.
- Each question names what it blocks and offers a recommended answer so the human can reply "yes".
- Questions the human leaves unanswered stay in the spec as open, not silently resolved.

## 6. When reality changes

If implementation shows a criterion is wrong, impossible, or incomplete:

1. Stop coding on that criterion.
2. Edit the spec line, mark it `changed: <reason>`, and update its test row.
3. If the change alters what the user gets, tell the human before continuing. A spec edited quietly to match the code is a spec that proves nothing.
4. A change that reverses an earlier decision gets an ADR per `AGENTS.md` section 8.

## 7. Pitfalls

- Restating the PRD instead of narrowing it to this one change.
- Criteria phrased as tasks ("add endpoint") rather than behavior.
- Writing tests first, then reverse-engineering criteria to fit them.
- Non-goals left empty. If nothing is excluded, the scope was not thought through.
- Treating sign-off as permanent; the spec lives until the PR merges.

## Sources

- IBM Bob Modes catalog, modes sdd-engineer/requirements-management/end-to-end-sdlc/business-analyst — https://bob-modes.2azhe5jwptg4.au-syd.codeengine.appdomain.cloud (used as inspiration; no text reused)
