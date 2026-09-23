---
name: context-engineering
description: Keep the main thread lean across a long or fan-out-heavy task — cap what a sub-agent or tool call returns, compact stale exploration into a short note, and prefer targeted reads over whole-file dumps. Use when a session is running long, before spawning sub-agents from investigate, swarm, or blast-radius, or on "keep this efficient", "watch the context budget", "compact this".
---

# Context engineering

`rigor` names the principle — Guard the Context Window — and stops there. This is the procedure.
The deliverable is a main thread that still has room to think on turn eighty, not a summary written
after the window is already gone.

Context is a finite resource, not a scratchpad. As token count rises, a model's ability to recall
and weigh everything in it degrades — this is context rot, and it is a property of attention, not a
bug that better prompting fixes. The defense is discipline about what enters the window, not a
bigger window.

`AGENTS.md` section 7 outranks this file.

## 1. Recognize when it applies

- A session has run long enough that early context is no longer load-bearing.
- A tool call or sub-agent is about to fan out over more than a handful of files.
- Multi-phase work where an earlier phase's detail will not be read again.
- Any point about to delegate to a sub-agent — set the contract in section 2 before spawning it,
  not after it reports back.

## 2. Set the return contract before spawning

State, before the sub-agent or tool call runs, what it owes the caller:

- A decision, a verdict, or a short `file:line` table — never a transcript.
- Findings, not the material the findings were found in. A sub-agent that read ten files reports
  what it concluded from them, not the ten files.
- An explicit cap when the task could plausibly return a lot ("under 200 words", "the three
  worst offenders, not every one you found").

What it must never return: full file contents, a full diff beyond the relevant hunk, or a raw
transcript "in case it's useful." If the caller needs the detail later, it can re-read the specific
file — that is cheaper than carrying it in every subsequent turn unread.

## 3. Read narrow before reading wide

- Grep or search for the symbol first; read the file only if the match needs surrounding context.
- Read a line range when you know roughly where the answer is, not the whole file.
- Reach for a sub-agent only once the read would not fit in a targeted pass — not by default for
  every unfamiliar file.

## 4. Compact at phase boundaries

When a phase finishes, its detailed exploration stops earning its place in the window:

- Replace it with a short note: the conclusion, the `file:line` it rests on, and nothing else.
- Write it somewhere durable if a later phase or a human review needs it back — a `decision-log`
  row, a scratch file, a PR description — rather than trusting it survives in context unmentioned.
- Let the raw exploration drop. Re-deriving it later from the same targeted read (section 3) is
  cheaper than protecting it in every subsequent turn.

## 5. Failure modes

| Smell | What it means |
| --- | --- |
| A sub-agent's full output gets pasted back into the reply | The return contract from section 2 was never set. |
| The same file gets read in full three times in one session | Reads are not narrow; grep or a line range would have done it once. |
| A todo list still references a file read forty turns ago, verbatim | That context should have been compacted into a one-line conclusion at the last phase boundary. |
| A long session gets slower and less accurate with no code change | Context rot, not a harder problem. Compact before continuing, do not push through. |

## Sources

- Anthropic, ["Effective context engineering for AI agents"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — context rot, and compaction, structured note-taking, and sub-agent architectures as the three countermeasures this skill is built from.
- Claude Cookbook, ["Context engineering: memory, compaction, and tool clearing"](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools) — a runnable walkthrough of the same primitives against a long-running agent.
