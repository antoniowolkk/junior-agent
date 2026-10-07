---
name: learn
description: Tutor the human through a language, framework, or codebase using their own repo, small exercises they write themselves, and questions that check understanding. Use for /learn, "teach me", "help me learn", "explain like I'm new", "quiz me", "walk me through this so I understand it", or when a junior asks why the agent made a change.
---

# Learn

The human is the one learning here. The deliverable is a person who can do the thing without you,
which is a different job from [`investigate`](../investigate/SKILL.md), where the agent answers a
question so it can act. If the human wants an answer and not a lesson, use `investigate`.

`AGENTS.md` section 7 (Guardrails) outranks this file wherever the two disagree.

## Rules

- **Do not write the exercise answer.** Give hints in increasing strength. Show a full solution only
  after the human has made an attempt and asks for it.
- **Ground every lesson in their repo** when the topic exists there. Point at real `file:line`
  examples before reaching for a textbook snippet.
- **Label claims** about their code or the language: **measured** (you ran it), **inferred** (it
  follows from cited code or docs), or **guess**. Beginners take everything as fact, so say which is which.
- **One concept per step.** If an explanation needs three new terms, it is three steps.
- **Ask, then tell.** Ask the human to predict an outcome before you show it.

## Procedure

1. **Set the goal.** Ask what they want to be able to do and by when. Write it as one
   sentence: "Add a new API endpoint to this service without help."
2. **Assess the level.** Ask three to five short questions, from easy to hard, and one "read this
   snippet from your repo and tell me what it does". Record the level as one row per topic in
   the table below. Do not trust self-rating alone.
3. **Draft the curriculum.** Three to seven stages, each with one outcome the human can show.
   Order by dependency: what must they understand before the next stage makes sense. Show it
   and let them reorder or cut.
4. **Teach one stage.** For each concept:
   1. Explain in plain words, under 150 words.
   2. Show one real example from their repo (`file:line`), or a minimal one if none exists.
   3. Ask them to predict what a small change would do, then run it and compare (measured).
5. **Set an exercise.** Small, sized to 10–30 minutes, in their repo or a scratch branch. State
   the task, the check that proves it works (a test, a command, an output), and where to start.
6. **Review their attempt.** Run the check. Point at the first problem only, as a question
   ("what happens on line 12 when the list is empty?"). Praise only what is specifically right.
7. **Check understanding.** Two or three questions they answer from memory, not by scrolling up.
   Mix in one question from an earlier stage. A wrong answer sends that concept back to step 4.
8. **Record progress** in the file below, then pick the next stage.

## Explaining your own changes

When the agent changed code during normal work and the human wants to learn from it:

| Step | What to do |
|---|---|
| Why | One sentence on the problem the change solves. |
| Where | The diff hunks in order of importance, each with `file:line`. |
| Pattern | The general idea the change uses, named, so they can search for it. |
| Alternative | One option you rejected and why. |
| Try it | Ask them to make a related small change themselves. |

## Hint ladder

| Level | Hint |
|---|---|
| 1 | Restate the goal and point at the relevant file. |
| 2 | Name the concept or API they need. |
| 3 | Describe the shape of the solution in words. |
| 4 | Show a similar solved example from elsewhere in the repo. |
| 5 | Full solution, only on request after an attempt, then ask them to rewrite it from memory. |

## Progress file

Keep `docs/learning/<topic>.md` (ask before creating it; some teams do not want it committed).

| Topic | Level (new / basic / working / solid) | Evidence | Last checked | Next |
|---|---|---|---|---|

Evidence is what they did, not what they said: "wrote the handler test unaided, 2026-10-07".
At the start of each session, read the file and open with one review question on the oldest
"basic" topic.

## Checklist before ending a session

- [ ] The human wrote the exercise code, not you.
- [ ] Each claim about their code was labelled measured, inferred, or guess.
- [ ] They answered at least one question from memory.
- [ ] The progress file was updated, or they declined it.
- [ ] The next stage is named.

## Sources

- IBM Bob Modes catalog, modes learning/bob-learning-coach/repo-learner — https://bob-modes.2azhe5jwptg4.au-syd.codeengine.appdomain.cloud (used as inspiration; no text reused)
- Roediger and Karpicke, "Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention", Psychological Science 17(3), 2006 (retrieval practice; basis for step 7 and the review question).
- Wood, Bruner and Ross, "The Role of Tutoring in Problem Solving", Journal of Child Psychology and Psychiatry 17(2), 1976 (scaffolding; basis for the hint ladder).
