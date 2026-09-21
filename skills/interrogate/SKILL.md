---
name: interrogate
description: Adversarial multi-angle review of a diff or design by parallel subagents, synthesized into one verdict. Use for "interrogate this", "stress test this", "find blind spots", "tear this apart", or before shipping a contested design.
---

# Interrogate

Spawn parallel reviewers to attack the same change from independent angles, then act as lead reviewer over what comes back.

The deliverable is a verdict. Do not auto-apply the findings.

## 1. Scope

- The user pointed at files or a diff: use that.
- On a feature branch: `git diff main...HEAD` (or the real base branch).
- Otherwise: gather the files the recent work touched.

Package the diff plus whatever surrounding context a reviewer needs to understand it without the conversation.

## 2. State the intent

Write one paragraph on what this change is supposed to do, from the user's message, the commit messages, the PR description, and the code. A reviewer with no stated intent reviews against its own guess.

If you cannot state the intent, ask before spawning anything.

## 3. Spawn reviewers

Launch 3 to 4 reviewers in a single message so they run concurrently. Use read-only agents (`Explore`, or `general-purpose` instructed not to edit). Vary them: give each a different lens rather than the same prompt four times.

Lenses worth splitting across reviewers:

- **Correctness.** Wrong results, unhandled cases, race conditions, error paths that swallow failures.
- **Interface and design.** Shallow modules, information leakage, abstractions that leak internal rules to callers.
- **Blast radius.** What breaks elsewhere. Callers, wire formats, stored data, other languages reading the same bytes.
- **Security and data.** Boundary validation, secrets, authz checks, injection, anything user-controlled reaching a sink.

Each reviewer gets: the intent, the diff, its lens, and the instruction to cite `file:line` for every finding and to report "nothing found" rather than manufacture something.

If different models are available, use them. Model diversity catches more than persona diversity.

## 4. Synthesize

- **Consensus first.** A finding two reviewers reached independently is the highest signal in the pile.
- **Deduplicate.** Same issue, different words. Merge, note who raised it.
- **Keep lone findings**, weighted lower.
- **Note contradictions.** One reviewer flagging what another explicitly cleared is useful information about the verdict's confidence.

## 5. Lead judgment

You are a pragmatic senior engineer, not a neutral aggregator. Sort every finding:

- **Act on.** Real correctness, security, or maintainability issues given the actual goals. Would block a real PR.
- **Consider.** Legitimate, but the cost of addressing it now may exceed the benefit. Worth the human's attention.
- **Noted.** Valid but not actionable. Context-dependent or premature.
- **Dismissed.** Wrong, nitpicky, or missing context. Give the reason.

Every finding carries who raised it, its bucket, and a one-line rationale. Accepting every comment is as bad as dismissing every comment — reviewers file real catches and noise in the same list.

## Output

```
### Intent
### Reviewers        (one line each: lens, findings count)
### Act on           (description, who raised it, why it matters)
### Consider         (description, the tradeoff)
### Noted
### Dismissed        (with reason)
### Agreement map    (where they converged, where they split, what that tells you)
```
