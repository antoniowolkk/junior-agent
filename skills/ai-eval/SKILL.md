---
name: ai-eval
description: Define and run an accuracy check for AI-built features — prompts, agents, RAG pipelines, LLM-based classifiers — whose output cannot be asserted with a literal expected value the way an ordinary test can. Use when building or changing a prompt, adding an LLM-based feature, or on "did this prompt regress", "how do we know this is accurate", "eval", "hallucination", "golden set".
---

# AI eval

`rigor`'s TDD rule says assert a literal expected value. That rule assumes deterministic output. A
prompt, an agent, a RAG pipeline, and an LLM-based classifier do not have one — the same input can
produce two acceptable answers worded differently. This skill is the accuracy procedure for that
case: a small versioned set of cases with a real evaluator, run before the feature ships and again
on every change that could shift its output.

The deliverable is a golden set and a comparison against a recorded baseline — not a handful of
prompts that looked right when you tried them.

`AGENTS.md` section 7 outranks this file.

## 1. Define the accuracy criterion before building

Before writing the prompt or wiring the pipeline, decide what correct looks like:

- **Exact-match.** The output (or an extractable field of it) has one right answer. Use this
  wherever the task allows it — it needs no judge and no ambiguity.
- **Rubric-scored.** The output must satisfy named, checkable properties (cites a source that
  exists, stays under a length, refuses a listed case). Score each property independently.
- **LLM-as-judge.** Open-ended output with no fixed right answer. The weakest evaluator of the
  three — use it only when the first two do not apply, and validate it per section 3 before
  trusting it.

Naming the criterion first is this skill's version of writing the failing test first. Building the
feature before deciding how it will be checked means the check gets fitted to whatever the feature
already does, which proves nothing.

## 2. Build a small golden set first

- 50–200 cases, stratified across the common cases and the known edge cases — not one giant pile of
  similar inputs.
- Source it from real usage where any exists (logged inputs, prior support tickets, actual queries)
  before inventing cases. Invented cases skew toward what you already expected to handle.
- Version it. A golden set that changes silently between runs makes every comparison meaningless.
- Hold out a slice you do not look at while iterating on the prompt (see section 5).

## 3. Choose the evaluator honestly

- Use exact-match for any part of the output that is deterministic, even inside an otherwise
  open-ended feature. Do not judge what you can just compare.
- Use rubric scoring for named, checkable properties. Each property gets its own pass/fail, not one
  blended score that hides which property failed.
- If you use LLM-as-judge, validate the judge itself first: hand-label a handful of cases yourself,
  run the judge against them, and confirm it agrees with your labels before trusting it on the rest
  of the set.
- Label the result the same way `rigor` labels any claim: a judge score is **measured** only after
  that validation step; before it, or without it, the score is **inferred** at best.

## 4. Run the regression gate

- Every change to the prompt, the model, or the retrieval configuration reruns the full golden set
  before it ships.
- Compare against the last recorded baseline score, not against reading the new output and deciding
  it looks fine. "Looks fine" is exactly the failure mode a golden set exists to catch.
- A drop past an agreed threshold blocks the change, the same way a failing test blocks a merge
  under `rigor`'s TDD rule. Record the before and after numbers, not just "passed" or "failed."

## 5. Do not overfit to visible cases

Iterating on a prompt against the same cases you can see makes it better at those cases and can
silently make it worse at everything else. Keep the held-out slice from section 2 unseen during
iteration, and check it before calling a change done. A "better" prompt that was never checked
against unseen cases is a guess about the cases you were not looking at.

## Failure modes

| Smell | What it means |
| --- | --- |
| "It looked right in the three examples I tried" | No golden set exists. Section 2 was skipped. |
| A prompt change ships with no before/after score | Section 4's regression gate was skipped. |
| The judge is trusted without ever being checked against a human label | Section 3's validation step was skipped; the score is a guess wearing a number. |
| The eval set keeps growing to include whatever the current prompt already handles | Overfitting from section 5. The set should reflect real usage, not the feature's current blind spots. |

## Sources

- Langfuse, ["Golden dataset evaluation: build and maintain LLM test sets"](https://langfuse.com/resources/engineering/golden-dataset-evaluation) — sourcing, versioning, and sizing a golden set from real usage.
- DeepEval, ["Datasets"](https://deepeval.com/docs/evaluation-datasets) — the tiered fast-gate / comprehensive-suite structure a regression gate is built from.
- ["When 'Better' Prompts Hurt: Evaluation-Driven Iteration for LLM Applications"](https://arxiv.org/html/2601.22025v1) — the held-out-slice argument behind section 5.
