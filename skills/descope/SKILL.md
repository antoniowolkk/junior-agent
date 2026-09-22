---
name: descope
description: Decide whether a change should be built at all before designing it. Use when a request arrives as a solution rather than a problem, when a ticket names a library or a component to add, when scope grows mid-task, or for "do we need this", "is this worth building", "can we skip this", "/descope". Skip for a bug with a reproduction — that work is already justified.
---

# Descope

The cheapest code is the code never written, and the second cheapest is code that already exists. This skill runs before `architect` and asks whether the requested thing should exist, then hands the human a recommendation. It does not decide. Silently building less than was asked is a worse failure than over-building, because nobody can review what was never mentioned.

`rigor` names the principle — Laziness Protocol, Subtract Before You Add. This is the procedure behind the name, and the only skill in the pack whose output can be "do not build this".

## 0. Precedence

`AGENTS.md` section 7 (Guardrails) outranks everything here.

**The human owns scope.** This skill produces a recommendation with evidence, never a unilateral cut. Where a verdict below says decline, defer, or shrink, the output is a proposal in your reply. Not a smaller diff you hand over quietly. Proceed as asked if the human repeats the request.

`delegate` sizes how much you take on. This runs first and asks whether there is anything to take.

## 1. When to run

| Signal | Run? |
| --- | --- |
| Request names a solution, not a problem ("add a date picker", "install X") | Yes |
| Request is a feature with no stated user or outcome | Yes |
| You are about to add a dependency, a file, an abstraction, or a config value | Yes |
| Scope grew mid-task and you are about to widen it | Yes — this is the most common miss |
| A defect with a reproduction | No. `reproduce` already proved the work is needed. |
| The human named the scope explicitly and gave the reason | No. Build it. |

Time-box this to minutes. A descope pass that costs more than the change it might prevent has failed.

## 2. Understand before you climb

The ladder in section 3 is not a substitute for reading the code. Run it after you can state, from evidence:

- Who the change is for and what is different for them afterwards.
- What already exists in this repo that touches the same problem. Search before concluding nothing does. Re-implementing a helper living three files over is the most common form of unnecessary code.
- What breaks if the change never ships. If nothing does, that is the finding.

Label each answer measured, inferred, or guess. A ladder climbed on guesses recommends the wrong rung.

## 3. The ladder

Stop at the first rung that holds. Adapted from ponytail's ladder (MIT); see `## Sources`.

| Rung | Ask | If yes |
| --- | --- | --- |
| 1 | Does this need to exist at all? | Recommend declining. Say what it was for and why nothing needs it. |
| 2 | Does deleting something solve it instead? | Propose the deletion. Subtraction is a smaller diff than any addition. |
| 3 | Does this repo already do it? | Reuse. Name the file and symbol. |
| 4 | Does the standard library do it? | Use it. |
| 5 | Does a native platform feature do it? | Use it. A DB constraint over app code, CSS over JS, a built-in input over a component. |
| 6 | Does an already-installed dependency do it? | Use it. Adding a new one is a section 7 stop and needs its own justification. |
| 7 | Can it be one line? | One line. |
| 8 | None of the above | Build the minimum that works. `architect` takes it from here. |

Two rungs both hold? Take the higher one and move on. The ladder is a reflex, not a research project.

## 4. The floor

These are never what gets cut, on any rung. Cutting one is not descoping, it is shipping a defect:

- Validation at a trust boundary.
- Handling for anything that loses or corrupts data.
- Security controls — authentication, authorization, secret handling.
- Accessibility of anything a person uses.
- The test that proves the change works.

If the only way to make a change small is to cross this line, the change is not too big. Say so and build it properly.

## 5. Write the verdict

One block in your reply, before any implementation detail. Five lines, not an essay:

```
Asked for:   <what the request said>
Recommend:   build as asked | build smaller | reuse <what> | defer | decline
Because:     <the rung that held, with the evidence>
Costs:       <what the human gives up if they take this>
Proceeding:  <what you will do unless told otherwise>
```

Rules:

- **State the cost honestly.** A recommendation with no downside listed has not been thought through.
- **Defer means a written line somewhere durable** — an issue, a backlog row, a TODO with a name. A deferral that exists only in a chat reply is a silent decline.
- **Decline or a material shrink that changes direction gets an ADR**, same as any other decision with no precedent. [`templates/docs/adr/0000-template.md`](../../templates/docs/adr/0000-template.md) is the form.
- Never bundle the verdict with a finished diff of the smaller thing. The human cannot evaluate the scope call and the implementation in one read.

## 6. Pitfalls

- Shrinking scope in the diff and mentioning it only in the PR body, or not at all.
- Running the ladder before reading the code, so rung 3 is answered "no" by ignorance.
- Treating the ladder as permission to skip the floor in section 4.
- Declining work because it is tedious rather than because it is unnecessary. The rung has to hold on evidence.
- Re-litigating a scope call the human already made. They said build it; build it.
- Spending longer on the descope pass than the change would have taken.
- Deferring everything. A backlog nobody reads is where scope goes to avoid review.

## Sources

- [ponytail](https://github.com/DietrichGebert/ponytail) — DietrichGebert, MIT. The rung ladder and the lazy-not-negligent floor are adapted from its skill. Its own agentic benchmark (twelve feature tickets against a real FastAPI + React repo, n=4, Haiku 4.5) reports a 54% mean reduction in lines of code against the same agent with no skill, with the largest cuts where the baseline over-built and near zero where the code was already minimal. That is evidence over-building is a real, measurable default rather than a stylistic complaint. It is an always-on coding-style mode; this skill is the narrower upstream gate that produces a reviewable verdict a human signs off on.
- [Building effective human–agent teams](https://claude.com/blog/building-effective-human-agent-teams) — Anthropic. Human attention is the bottleneck, which is why the verdict is five lines and why a scope cut is surfaced rather than absorbed.
