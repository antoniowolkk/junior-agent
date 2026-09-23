---
name: rigor
description: Route non-trivial engineering work through a matched playbook, named principles, and evidence-based verification. Use for any bug fix, feature, refactor, performance work, review, or autonomous run — anything where being wrong is expensive. Skip for casual questions and throwaway spikes.
---

# Rigor

Depth before speed. The goal is not more code, it is less code that is proven to work.

Adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by poteto (Lauren Tan), MIT. Condensed from 50 skills and 23 playbooks, rewritten for Claude Code, and reconciled with `AGENTS.md`. See `NOTICE`.

## Companion skills

This file is the spine. Reach for a companion when the route calls for it.

| Need | Skill |
| --- | --- |
| Decide whether the change should be built at all | **descope** |
| Size how much to take unsupervised, and what context to demand first | **delegate** |
| Turn a vague defect report into a failing test | **reproduce** |
| Understand code or its rationale before touching it | **investigate** |
| Design types and boundaries before writing code | **architect** |
| Know what a change breaks elsewhere | **blast-radius** |
| Change a live schema or backfill its data | **migrate** |
| Adversarial review of a diff or a design | **interrogate** |
| Parallel fan-out over slices or competing approaches | **swarm** |
| A reviewable trail for unattended work | **decision-log** |
| Keep the main thread lean across a long or fan-out-heavy task | **context-engineering** |
| Building or changing a prompt, agent, RAG pipeline, or other LLM-based feature | **ai-eval** |
| Any prose that ships | **unslop** |
| Install this pack into a repo | **setup-project** |
| Add a new skill to this pack | **grow-skill** |

## 0. Precedence

`AGENTS.md` section 7 (Guardrails) outranks everything in this file. Where this file says to proceed without asking and section 7 says to stop and ask, **stop and ask**. The human is the merge authority.

Everything else here is how to do the work between those stops.

## 1. Route the task

Before acting, name which of these the task is. Say it out loud in the first reply. Then write the matching steps into a todo list *before* any task-specific todos. A step you deliberately skip stays in the list as `skip: <reason>`.

| Task looks like | Route | Non-negotiable steps |
| --- | --- | --- |
| A read-only question ("how does X work", "are we sure") | **Investigate** | Answer from cited evidence. Change no code. |
| A defect | **Bug fix** | Reproduce first. Root-cause it. Fix. Re-run the reproduction. |
| Measured slowness | **Perf** | Measure a baseline. Profile. Fix the measured cause. Show before and after. |
| New or changed behavior | **Feature** | Name the data shape first. Then the caller's usage. Then implement. If the output is non-deterministic (a prompt, agent, RAG pipeline, or classifier), define the golden set first — see **ai-eval**. |
| Structure changes, behavior does not | **Refactor** | Record current output first. Move structure. Prove output unchanged. |
| A design decision with no precedent | **Prototype** | Build 2–3 cheap competing sketches. Let the result decide. Throw them away. |
| A diff you want broken | **Review** | Adversarial pass. Sort findings into act-on / consider / dismissed, with a reason per dismissal. |
| Work spanning phases or several PRs | **Multi-phase** | Write the phase plan before code. Each phase ends in a check. |
| Long work the human steps away from | **Autonomous run** | See section 6. |
| Nothing above fits, or the work is large and cross-cutting | **Design your own** | Write the bespoke playbook first, then follow it. |

**Do not enumerate tools in a prompt or a plan.** State the goal and the constraints. The route supplies the steps.

## 2. Before you write code

- **Understand it first.** Trace how the code works now. An agent that edits without a traced model fixes the symptom at the first plausible spot.
- **Ask why it is shaped this way** when history might explain the mess. Report a null result too — "nobody wrote down why" is an answer.
- **Name the data shape before the logic.** Core types and structures first, logic second.
- **Settle the caller's usage before the implementation** for anything crossing a function boundary. Write how it gets called, then the types, then the module map.
- **Classify every question before asking it.** If the answer is a fact you could observe by running something (behavior, timing, output, performance), it is not the human's to answer. Go observe it. Reserve questions for genuine product or preference calls, and for everything `AGENTS.md` section 7 requires.

## 3. The principles

These are names, not paragraphs. The human uses a name to redirect you mid-task; you cite a name in your reply **only alongside the specific decision it changed**. A citation with no decision behind it is name-dropping.

**How much to build**
- **Laziness Protocol.** Bias to deletion and the smallest change that solves the problem.
- **Subtract Before You Add.** Remove dead weight first, then build on the simpler base.
- **Foundational Thinking.** Core types and data structures before logic.
- **Redesign from First Principles.** Integrating a new requirement? Redesign as if it had been there day one.
- **Attack the Premise.** Two fixes that failed the same way share a premise. Question the premise instead of writing a third fix.
- **Minimize Reader Load.** Collapse layers, one-caller wrappers, and hidden state. Count what a reader must hold in their head.
- **Exhaust the Design Space.** No precedent? Build competing prototypes before committing.
- **Build the Lever.** Build the script that does or proves the work. The script is the artifact a reviewer re-runs.
- **Experience First.** Choose the user's result over implementation convenience.
- **Outcome-Oriented Execution.** Converge a migration on the target design. Do not preserve throwaway compatibility states.

**Where things live**
- **Model the Domain.** Encode a repeated rule in one structure (state machine, typed model, table, reducer) — not scattered conditionals.
- **Boundary Discipline.** Validate at the system boundary. Trust internal types. Keep business logic pure.
- **Type System Discipline.** Make illegal states unrepresentable. Parse external data at the boundary.
- **Make Operations Idempotent.** Retries and crashes converge on the same end state.
- **Migrate Callers Then Delete Legacy APIs.** Migrate and delete in one wave. No permanent second API.
- **Separate Before Serializing Shared State.** Eliminate the sharing before adding locks or coordination.

**What counts as proof**
- **Prove It Works.** Section 4.
- **Fix Root Causes.** Reproduce first. Ask why until you reach the cause.
- **Sequence Work into Verifiable Units.** Small units, each ending in a check, verified before the next starts.
- **Test Behavior, Not Implementation.** Call the code the way its users do. Assert a literal expected value. If the test would still pass when every imported function returns `undefined`, rewrite or delete it.

**Working with sub-agents**
- **Guard the Context Window.** Route bulk reading to sub-agents. Keep findings, not dumps, in the main thread. See **context-engineering**.

**Meta**
- **Encode Lessons in Structure.** Caught yourself writing the same instruction twice? Make it a lint, a test, a type, or a script — not more prose.

## 4. Prove it works

"It compiles" is not evidence. "The build is green" is not evidence. A confident report with no output attached is a red flag.

Match the check to the change:

| Change | Proof |
| --- | --- |
| CLI | Run the real command. Paste the output. |
| UI | Walk the changed flow in the running app. |
| Parser or migration | Replay a saved input. Diff the result. |
| Performance | Compare before and after measurements. |
| Storage | Read the written value back. |
| Delegated work | Read the actual diff. Never the delegate's summary. |
| AI/LLM feature (prompt, agent, RAG, classifier) | Run the golden set. Compare against the last-known baseline, not your own read of the output. See **ai-eval**. |

Rules:

- **Script the check when you can.** A deterministic script a reviewer re-runs beats a one-time eyeball.
- **When verification fails, suspect the observation method before the system.**
- **If a check could not run, say "inconclusive".** Do not round up.
- **Every claim carries its label in the same sentence:** measured, inferred, or guess. An unseen cause is a guess.
- **Never hand the human a check you could have run yourself.**

## 5. Clean the diff and write the reply

**Before commit** (still subject to `AGENTS.md` section 7 for the commit itself):
- Remove narrating comments, unsupported guards, dead compatibility paths, and unrelated edits.
- Keep a comment only for a non-obvious *why* the code cannot show. A test or script gets no phase-narrating comments — the assertion string documents the step.
- When a comment claims a constraint ("do not remove"), encode the claim as a type, test, or lint. Then delete the comment.
- Prefer several narrow PRs over one fat one.

**The reply:**
- Short declarative sentences. One thought each.
- Say who the work is for and what changes for them, before any implementation detail. Then what the next engineer inherits.
- Terse is not an excuse to drop content. Tradeoffs, choices, and open decisions stay.
- Never fabricate a link, a citation, or a file path. Link only what you produced or read this session.
- **No is an acceptable answer.** Asked whether to do something, give your real judgment. Decline or push back when true. Candour over agreement.

## 6. Autonomous runs

Only on an explicit hand-off from the human. The hand-off must contain:

1. **The goal.**
2. **A finish condition that can pass or fail.** A duration is not a finish condition — "work on this for 4 hours" buys four hours of motion. "Done means zero old callers and all fixtures pass" buys a result.
3. **An isolated worktree or branch**, so parallel work does not collide.
4. **Which section 7 permissions are pre-granted, named one by one.** Silence means not granted.
5. **An escape hatch.** Stop at a genuine dead end and write up why.

The loop, every iteration: check the finish condition → make the smallest justified change → verify against the real artifact → commit it if it helped, discard it if it did not → log one row → repeat.

**The decision log.** One row per decision: time, phase, decision, reason, evidence pointer, result. Plain TSV at `decisions.tsv`. This is what makes the night reviewable — the human audits decisions, not the whole transcript. End the morning report with an **Attention** section listing what deserves scrutiny first.

**The finish condition never quietly relaxes to declare victory.** A plateau means pivot, not redefine.

## 7. Pitfalls

- Reporting success off a green build.
- A vague finish condition on a long run.
- Parallel agents sharing one working tree.
- Accepting every review comment. Bots and humans file real catches and noise in the same list.
- Fixing the symptom at the first plausible spot because you skipped tracing.
- Editing a skill or a rule mid-task because it misbehaved. Fix it in its own change, keep the task moving.
- Enumerating tools instead of stating the goal.
- Letting a spike merge. Spike code is rewritten under TDD or it does not ship.
