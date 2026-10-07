---
name: test-first
description: Drive new behavior with a failing test first, then write the least code that passes, then refactor. Use for "TDD", "write tests first", "red-green-refactor", "add tests for this", "what should I test", "are these tests any good", "raise coverage", or any feature where the expected behavior can be stated up front. For a bug report, use reproduce instead.
---

# Test First

`rigor` says verify with evidence. This is the procedure for making that evidence before the code
exists: one failing test, the smallest change that passes it, then cleanup with the test as a net.
The deliverable is behavior plus tests that would catch it breaking.

`AGENTS.md` section 7 outranks this file. Installing a test framework, adding a coverage tool, or
changing CI thresholds is a new dependency or config change — stop and ask.

Bug work belongs to `reproduce`, which owns the failing test for a defect. Whether the feature
should exist at all belongs to `descope`. Type and module shape belong to `architect`.

## 1. State the behavior

Before any test, write one line per behavior in the form:

> Given **&lt;state&gt;**, when **&lt;action&gt;**, then **&lt;observable result&gt;**.

Each line becomes one test. If the result is not observable from outside the unit (a return value,
an output, a stored record, an emitted event), the behavior is not yet specified. Any expected
result you invented rather than read from the request or the code is a **guess** — list it and ask
before building on it.

## 2. Choose what to test

Order the list so the simplest case comes first and each test forces one new piece of code.

| Case | Include when |
| --- | --- |
| Happy path, simplest input | Always, first |
| Boundaries (empty, zero, one, max, off-by-one) | The input has a range or size |
| Invalid input and error paths | The caller can pass it, or the spec names the error |
| State transitions | The unit holds state across calls |
| Interactions with a dependency | The behavior *is* the call (sent the email, wrote the row) |

Skip: trivial getters, framework code, and anything whose only assertion would restate the
implementation.

## 3. Pick the level

| Level | Use for | Watch out for |
| --- | --- | --- |
| Unit | Logic in one function or class, no I/O | Mocking so much the test checks the mocks |
| Integration | Two or more real components, a real DB or file system | Slow setup; shared state between tests |
| End-to-end | A user-visible flow that must not break | Slowness and flakiness; keep these few |

Default to the lowest level that can observe the behavior. Most tests should be unit tests; a few
integration tests cover the seams; end-to-end tests cover only the critical flows.

## 4. The loop

Run once per behavior line from step 1.

1. **Red.** Write one test. Run it. It must fail, and the failure message must say the behavior is
   missing — not a syntax error, import error, or missing fixture. If it passes already, either the
   behavior exists or the test asserts nothing; find out which.
2. **Green.** Write the least code that makes it pass. Hard-coding is allowed here; the next test
   will force the general version. Run the whole relevant suite, not only the new test.
3. **Refactor.** Remove duplication and fix names in both the code and the test. Change no
   behavior. Run the suite after each change; it stays green throughout.
4. Commit if the project's workflow wants small commits, then take the next line.

If a step stays red for more than a few minutes, the step was too big. Delete the change, write a
smaller test.

## 5. Check the tests themselves

A passing suite proves only that the code matches the tests. Check each new test against this list:

- [ ] It failed before the code existed, and you saw that failure (**measured**, not assumed).
- [ ] It fails when the behavior breaks. Mutate the code by hand — flip a comparison, return a
      constant, delete a line — run the test, confirm it goes red, revert. A test that survives
      the mutation is not testing that line.
- [ ] It asserts on the outcome, not on private calls or internal structure.
- [ ] One behavior per test; the name says which.
- [ ] Deterministic: no real clock, network, random seed, or order dependence. Inject them.
- [ ] Independent: passes alone, in reverse order, and in parallel.
- [ ] Fast enough that people will run it on every change.

## 6. Coverage is a signal

Coverage tells you which lines ran, not whether anything checked them. Use it to find untested
code, never as the target.

| Reading | What to do |
| --- | --- |
| A changed line is uncovered | Write a test for the behavior it implements, or ask why it exists |
| Coverage is high, mutations survive | Assertions are weak; fix them per step 5 |
| Pressure to hit a number | Report the uncovered branches and their risk instead of padding tests |

Report coverage numbers as **measured** only when you ran the tool in this session. Otherwise say
it is a guess or leave it out. Do not change a project's coverage threshold.

## 7. Hand off

1. The behavior list from step 1, guesses marked.
2. Tests added, by level, and the command that runs them.
3. Evidence that each new test was seen red then green.
4. Mutations tried and whether the tests caught them.
5. What is still untested, and why.

## Failure modes

| Smell | What it means |
| --- | --- |
| Code written before its test | The loop was skipped; the test may only describe what the code happens to do. |
| Test never seen failing | It may pass for any implementation. Mutate and check. |
| Every dependency mocked | The test checks wiring, not behavior. Move up a level. |
| Refactor step changed a test's assertion | That was a behavior change. Go back to red. |
| Tests added only to raise a percentage | Coverage became the goal. See step 6. |

## Sources

- IBM Bob Modes catalog, modes tdd/tester/code-quality — https://bob-modes.2azhe5jwptg4.au-syd.codeengine.appdomain.cloud (used as inspiration; no text reused)
- Kent Beck, *Test-Driven Development: By Example*, Addison-Wesley, 2002 — the red-green-refactor loop and "fake it" in step 4.
- Martin Fowler, ["TestCoverage"](https://martinfowler.com/bliki/TestCoverage.html), 2012 — coverage as a tool for finding untested code, not a quality target.
- Mike Cohn, *Succeeding with Agile*, 2009 — the test pyramid behind step 3.
