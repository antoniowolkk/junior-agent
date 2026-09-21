---
name: reproduce
description: Turn a vague defect report into one deterministic failing test before any fix is attempted. Use for "it's broken", "can't reproduce", bug reports with no steps, flaky or intermittent failures, and anything that only fails in CI or in production.
---

# Reproduce

`rigor` routes a defect to "reproduce first" and stops there. This is the procedure. The
deliverable is one committed test that fails for the reported reason and passes once the defect is
fixed — not a fix, and not a theory.

A defect you cannot reproduce is a defect you cannot prove you fixed. The most expensive outcome
in bug work is not a slow fix; it is a merged fix for a defect that was never happening, while the
real one stays.

`AGENTS.md` section 7 outranks this file. Reproduction often wants production data, a database
reset, or a new dependency — every one of those is a stop-and-ask.

## 1. Extract the claim

Reports arrive as impressions. Convert to a falsifiable sentence before touching anything:

> Given **&lt;starting state&gt;**, when **&lt;action&gt;**, the system does **&lt;observed&gt;**, but should do **&lt;expected&gt;**.

Any blank you fill by assumption is a **guess** — label it and list it. If `expected` is a guess,
stop and ask. Fixing code to match an assumed expectation is how a working feature gets broken.

Cheap facts worth having first: exact version or commit, environment, exact error text and stack,
timestamp, whether it ever worked.

## 2. Reproduce at the coarsest level that works

Get any failure at all before making it small. Work down only as far as you need:

| Level | Use when | Cost |
| --- | --- | --- |
| Manual, in the running app | Nothing else reproduces it yet | Slowest, most faithful |
| End-to-end / integration test | The path crosses modules or the network | Medium |
| Unit test on the failing function | You already know the failing call | Fastest, least faithful |

Do not start at the unit level. A unit test written from a theory reproduces the theory, not the
defect.

## 3. Shrink it

Once anything fails, cut until nothing can be removed without the failure disappearing. Halve the
input, delete a step, drop a config flag — if it still fails, keep the cut; if not, put it back.
This is delta debugging; the systematic version is Zeller's `ddmin`, and doing it by hand with
bisection on the input gets most of the value.

Shrink these in order: input data, then steps, then configuration, then dependencies. Stop when
every remaining piece is load-bearing. Zeller's original case cut 896 lines of HTML to the one
line that crashed the browser — that is the target ratio, not a tidied-up version of the report.

## 4. When it is intermittent

The most common blocker, and the point where most agents start guessing. Do not accept "flaky" as
a diagnosis — it is a description of the symptom.

| Symptom | First suspects | How to force it |
| --- | --- | --- |
| Fails ~1 run in N | Race between concurrent work, shared mutable state | Loop the test; insert a delay on one side of the suspected race |
| Passes alone, fails in a suite | Order dependence, leaked global or DB state | Run the suite in reverse and in random order; run the pair alone |
| Only fails in CI | Timezone, locale, CPU count, cold cache, clock, missing env | Match the CI values locally, one at a time |
| Fails only the first or last run | Cache warmth, migration state, fixture teardown | Run twice from a clean state |

Make it fail **reliably** before fixing it. A fix validated against a test that fails one time in
twenty is not validated. If you cannot make it deterministic, say so in those words and stop —
that is a real, reportable result.

## 5. Commit the test, failing

Before any fix:

- The test fails for the reported reason, not an unrelated error. Read the failure text and
  confirm it matches the claim from step 1.
- Assert on the behavior, not the current implementation.
- It fails when the defect is present and passes when it is gone. Verify both directions — the
  second one comes after the fix, and the test is not done until you have seen it.
- Name it after the defect, and link the report or issue in a comment.

Hand the failing test to the human before writing the fix. `AGENTS.md` section 6 makes this the
review point: a test is far easier to review than a patch, and if it asserts the wrong thing that
is caught before any code exists.

## 6. Hand off

Report, in this order:

1. The claim from step 1, with guesses marked.
2. Where it reproduces and at which level.
3. The minimal case, and what was removed to get there.
4. For intermittents: the failure rate, measured, and what forces it.
5. What you could **not** reproduce, stated plainly. A null result is a result.

Only now route to the fix. Root-cause it before changing a line; a reproduction narrows *where*,
it does not tell you *why*.

## Failure modes

| Smell | What it means |
| --- | --- |
| A fix appears before a failing test | The route was skipped. The fix cannot be proven. |
| The test was written from the stack trace | You reproduced your theory. Go back to the reported action. |
| "Works on my machine" | An environment difference is the defect, or contains it. Diff the environments. |
| The repro is the whole app | Step 3 was skipped. Shrink it. |
| Retry added to make a test pass | The intermittency was hidden, not diagnosed. |
| Reproduced only in production | Say so, and treat every observation as **measured** there and **guess** everywhere else. |

## Sources

- Andreas Zeller and Ralf Hildebrandt, ["Simplifying and Isolating Failure-Inducing Input"](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf), IEEE TSE 28(2), 2002 — the `ddmin` algorithm and the Mozilla case behind step 3.
- ["Reducing Failure-Inducing Inputs"](https://www.debuggingbook.org/html/DeltaDebugger.html), The Debugging Book — a runnable treatment of the same technique.
- Step 4's table is a gap analysis of this repo plus the friction pattern in local session logs, where nondeterminism ("race condition", "flaky", "intermittent", "only fails in CI") dominates reproduction talk. Inferred, not measured.
