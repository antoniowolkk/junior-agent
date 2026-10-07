---
name: refactor
description: Change the structure of code without changing what it does, in small steps each proven green. Use for "refactor this", "clean this up", "extract this", "remove duplication", "split this file", "untangle this", "should this be a pattern", or before a feature that the current shape fights. Skip when the behavior itself is wrong — that is a fix, not a refactor.
---

# Refactor

A refactor changes structure and keeps behavior. If any observable output changes, it was not a refactor, and it does not get reviewed as one. This skill is the procedure for keeping those two apart.

`descope` asks whether the cleanup is worth doing. `architect` sketches the target shape when it crosses a module boundary. `blast-radius` finds what the moved code touches elsewhere. This skill covers the walk from the current shape to the target without breaking anything on the way.

## 0. Precedence

`AGENTS.md` section 7 (Guardrails) outranks everything here. A refactor that needs a new dependency, a public API change, or a schema change has crossed into section 7 territory. Stop and ask.

## 1. When to run

| Signal | Run? |
| --- | --- |
| A feature is hard to add because of the current shape | Yes. Refactor first, in its own commit, then add the feature. |
| The same logic exists in three places and they are drifting | Yes |
| A function or file does several unrelated jobs | Yes |
| Code is merely unfamiliar or not to your taste | No. Run `investigate` and leave it. |
| The behavior is wrong | No. `reproduce`, then fix. Refactor after, if at all. |
| No tests cover the code and you cannot add any | Stop. Report the gap; do not refactor blind. |

## 2. Pin the behavior first

Before moving a line, the current behavior must be captured by tests that run in seconds.

1. List the entry points you will touch and what each one returns, writes, raises, or logs.
2. Run the existing tests on that code. Record which pass. Label coverage of each entry point measured (a test exercises it) or guess (you think one does).
3. For every guess, write a characterization test: call the code, assert whatever it does today, including the odd parts. You are recording, not judging. A bug you find goes in your report, not in the refactor.
4. Break the code on purpose once (flip a condition) and confirm a test goes red. A suite that cannot fail proves nothing.

## 3. Move in small steps

Each step is one named move: rename, extract function, inline, move, introduce parameter, replace conditional with lookup, split module.

1. Make one move.
2. Run the pinned tests. Green: continue. Red: revert the step, do not debug forward.
3. Commit, or at least checkpoint, every few green steps so any point is one revert away.
4. Never edit a test's expected value during a refactor. If an assertion has to change, behavior changed. Stop and reclassify.

**One commit, one kind of change.** Refactor commits and behavior commits never mix. A reviewer must be able to read a refactor commit as "nothing observable changed" and check that claim against the tests.

## 4. Principles, with judgement

| Principle | Apply when | Do not apply when |
| --- | --- | --- |
| KISS | Nesting, flags, or indirection hide what the code does | Simplifying would drop a case the tests pin |
| DRY | The third copy appears and all copies change for the same reason | Two blocks look alike but change for different reasons. That is coincidence, not duplication. |
| Separation of concerns | One unit mixes I/O, rules, and formatting so none can be tested alone | The split adds a layer nobody else calls |
| Rule of three | Wait for the third use before extracting a shared abstraction | The first two uses already disagree on details |

A wrong abstraction costs more than duplication. When unsure, inline and wait.

## 5. When a design pattern earns its place

Name a pattern only after the code already wants it. All three must hold:

- The variation it handles exists today, not in a forecast. Two real implementations, minimum.
- It removes a conditional or duplication you can point at with `file:line`.
- A reader new to the code finds the result easier, not just more familiar to you.

If any fails, a plain function or a lookup table is the answer. Patterns that cross a module boundary go through `architect` first.

## 6. When to stop

Stop when any of these is true, and say which one:

- The change you were clearing the way for now fits cleanly.
- The next step needs a behavior change, a public API change, or a section 7 item.
- The diff has grown past what one reviewer can verify in one sitting. Split it.
- You are moving code around with no named reason for the next step.

## 7. Report

```
Goal:        <what shape problem this fixed, and for what>
Pinned by:   <tests, with how many were added; measured>
Steps:       <named moves, in order>
Behavior:    unchanged — <evidence: same tests green before and after; measured>
Found:       <bugs or oddities recorded but not fixed>
Stopped:     <which stop condition from section 6>
```

Anything in that block you did not run is labelled inferred or guess.

## 8. Pitfalls

- "Small fix while I'm here" inside a refactor commit.
- Extracting a helper after the second copy, then bending it to fit the third.
- Characterization tests that assert on mocks instead of outputs, so they stay green when behavior moves.
- Renames that miss a string-keyed lookup, reflection, or a serialized field name. `blast-radius` covers where grep stops.
- Deleting "dead" code without proving nothing reaches it.

## Sources

- IBM Bob Modes catalog, modes refactor/lean/design-pattern — https://bob-modes.2azhe5jwptg4.au-syd.codeengine.appdomain.cloud (used as inspiration; no text reused)
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 2nd ed., Addison-Wesley, 2018. Named small moves, each followed by a test run; refactoring and feature work as separate hats.
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall, 2004. Characterization tests: pin what code does before changing it.
- Sandi Metz, [The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction), 2016. Duplication is cheaper than the wrong abstraction.
