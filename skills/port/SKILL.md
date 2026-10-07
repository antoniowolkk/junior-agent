---
name: port
description: Convert code between languages, frameworks, or major versions and prove the new code behaves like the old. Use for "convert this to", "port to", "rewrite in", "upgrade framework", "move off Java 8", ".NET Framework to .NET 8", "Python 2 to 3", or any change where the same behavior must survive a new runtime. Not for schema changes; use migrate.
---

# Port

A port is done when the new code returns the same outputs as the old code on the same inputs, including the inputs nobody wrote a test for. Producing code that compiles in the target language is the easy part. Proving it means the same thing is the work.

Schema and data changes belong to `migrate`. When a port also changes storage, split it: `port` owns the code, `migrate` owns the tables, and they ship as separate steps.

## 0. Precedence

`AGENTS.md` section 7 (Guardrails) outranks this file wherever the two disagree. Adding a dependency, deleting the old implementation, or switching production traffic each needs an explicit yes from the human.

Run `descope` first when the request is "rewrite it in X" with no stated problem. A rewrite justified only by taste is the most expensive way to change nothing.

## 1. Inventory before translating

Write this table before touching target code. Label every cell measured, inferred, or guess.

| Item | What to record |
| --- | --- |
| Entry points | Public functions, endpoints, CLI commands, jobs, message handlers |
| Callers | Who depends on each entry point; `blast-radius` finds the ones outside the repo |
| Dependencies | Each library, and its target equivalent or "none" |
| Side effects | Files, network, env vars, clocks, randomness, global state |
| Existing tests | Count, and whether they run against the old code today (measured) |
| Hidden contracts | Output formatting, ordering, error messages that callers parse |

A dependency with no target equivalent is the largest risk in the port. Surface it now, not halfway through.

## 2. Map the semantic gaps

Code that reads the same can behave differently. Check each row for the specific pair you are porting and write down the decision.

| Gap | Typical trap |
| --- | --- |
| Integer width and overflow | Java `int` wraps silently; Python ints never overflow; Go wraps too, and panics on integer division by zero; JS numbers lose precision above 2^53 |
| Division and rounding | `-7 / 2` is `-3` in C/Java/Go, `-4` in Python's `//`; banker's rounding in .NET `Math.Round` and Python `round` |
| Nulls and absence | `null` vs `None` vs zero values vs `Option`; missing map key returns null, raises, or returns zero |
| Strings | UTF-16 code units (Java, C#, JS) vs bytes (Go) vs code points (Python 3); length, slicing, case folding, and sort order all differ |
| Floating point | Formatting of `0.1 + 0.2`, NaN equality, `-0.0`, decimal vs binary money types |
| Error model | Checked exceptions vs unchecked vs returned errors vs Result types; what gets swallowed in each |
| Concurrency | Threads vs async vs goroutines; memory visibility; whether a shared map is safe |
| Date and time | Default time zone, epoch units (ms vs s vs ns), month indexing, DST handling, leap seconds |
| Collections | Iteration order of hash maps, stable vs unstable sort, mutability of returned lists |
| Resource lifetime | Finalizers vs `using`/`with`/`defer`; connections left open |

A gap you did not check is a guess, and the report must say so.

## 3. Choose idiomatic or literal, per unit

| Choose | When |
| --- | --- |
| Literal | Numeric, parsing, crypto, financial, or protocol code where every edge case matters. Translate line by line first, prove equivalence, refactor later. |
| Idiomatic | Glue, wiring, I/O plumbing, and framework code where the target has a native pattern (DI container, async I/O, records) |

Never do both in one step. A literal translation that is proven equal is a safe base for an idiomatic refactor; an idiomatic rewrite with no literal baseline has nothing to diff against.

## 4. Prove equivalence by differential testing

1. Keep the old code runnable. A port whose original can no longer execute cannot be verified.
2. Build an input corpus: existing test inputs, captured production payloads (scrubbed of personal data), and generated edge cases from section 2 (max int, empty string, non-ASCII, NaN, DST boundary, null in every slot).
3. Run old and new on the same corpus. Compare outputs, errors, and side effects, not just return values.
4. Every difference is either a bug in the port or a documented, human-approved behavior change. There is no third category.
5. Add property-based or fuzz generation when the input space is large. Record the seed so a failure reproduces.
6. Report the corpus size and match rate as measured numbers.

## 5. Cut over incrementally

Prefer the strangler pattern over a big-bang switch:

1. Put a routing seam in front of the old code (facade, proxy, feature flag).
2. Move one entry point at a time. Optional: shadow mode, where the new code runs on live traffic and its output is logged and compared but not returned.
3. Keep the old path one flag flip away until the new one has run clean for an agreed period.
4. Delete the old code only after that period, as its own reviewed change.

## 6. What not to port

- Dead code. Check call sites and logs first; porting unused code doubles the cost of deleting it.
- Workarounds for bugs in the old runtime or library that the target does not have. Confirm the bug is gone, then drop the workaround with a test.
- Hand-rolled helpers the target's standard library already provides.
- Bug-compatible behavior callers do not rely on. Ask before fixing it; a fix during a port breaks the differential test, so ship it as a separate, labelled change.

## 7. Report

```
Ported:        <units, from -> to>
Corpus:        <n inputs, sources>; match <x/n> (measured)
Differences:   <each, with approved | bug | open>
Gaps unchecked:<rows from section 2 not verified>
Not ported:    <what, and why>
Cutover:       <seam, current traffic share, rollback step>
```

## Pitfalls

- Translating tests along with code, so both sides inherit the same mistake. Keep at least one oracle in the original language.
- Fixing bugs mid-port and losing the ability to tell a regression from an improvement.
- Trusting that it compiles. Type checkers do not see overflow, encoding, or time zone drift.
- Upgrading framework and language in one step. Do one, prove it, then the other.

## Sources

- IBM Bob Modes catalog, modes code-converter/migration/java-modernization/dotnet — https://bob-modes.2azhe5jwptg4.au-syd.codeengine.appdomain.cloud (used as inspiration; no text reused)
- [StranglerFigApplication](https://martinfowler.com/bliki/StranglerFigApplication.html) — Martin Fowler. The incremental cutover in section 5.
- [Differential testing for software](https://www.cs.swarthmore.edu/~bylvisa1/cs97/f13/Papers/DifferentialTestingForSoftware.pdf) — William McKeeman, Digital Technical Journal, 1998. Running two implementations on the same inputs as an oracle.
- [Scientist](https://github.com/github/scientist) — GitHub. Shadow-mode comparison of old and new code paths in production.
