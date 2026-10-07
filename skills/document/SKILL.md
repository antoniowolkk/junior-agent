---
name: document
description: Write or update technical docs from code so every claim stays true. Use for "document this", "write a README", "write docs for X", "add a how-to", "API reference", "draw an architecture diagram", "these docs are stale", or "explain this module in the docs". Picks the doc type by reader, cites file:line, runs every example.
---

# Document

`AGENTS.md` section 7 (Guardrails) outranks this skill wherever the two disagree.

The deliverable is a doc a reader can trust. Each sentence that describes behavior traces to code, and each example has been run. A short true doc beats a long plausible one.

Neighbors, so you pick the right route:

| Need | Route |
|---|---|
| Answer one question about the code, no file written | [investigate](skills/investigate/SKILL.md) |
| Clean up prose that is already correct | [unslop](skills/unslop/SKILL.md) |
| Record a decision and its tradeoffs | ADR from `templates/docs/adr/` |
| A doc that will live in the repo and be read again | this skill |

## 1. Pick the type by reader

Ask who opens this doc and what they are doing at that moment. One doc, one type. Mixing them is the usual reason docs feel long and still unhelpful.

| Reader is | Type | Shape |
|---|---|---|
| New, learning by doing | Tutorial | One guided path that ends in a working result. No options, no branches. |
| Competent, has a specific goal | How-to | Numbered steps toward that goal. Assumes context. |
| Working, needs a fact | Reference | Complete, dry, structured like the code. Every parameter, default, error. |
| Stepping back, wants to understand | Explanation | Why it is shaped this way, the alternatives, the constraints. |

If the request spans two types, write two docs and link them.

## 2. Gather evidence before prose

1. Find the entry points and trace one real path, as in `investigate`.
2. List every claim the doc will make. Next to each, write the `file:line` that supports it.
3. Label each claim **measured** (you ran it), **inferred** (it follows from cited code), or **guess**. A guess does not ship. Verify it or cut it.
4. Read existing tests. They show the behavior the authors committed to, including edge cases a reader will hit.

## 3. Write

1. Put the doc next to the code it describes: a package README, a `docs/` file beside the module, or a docstring. A central wiki drifts first.
2. Lead with what the reader can do after reading, then the steps or facts.
3. Use the names the code uses. If the code says `retry_budget`, the doc does not say "retry limit".
4. Comments in code explain why, not what. Delete a comment that restates the line below it. Keep or add one where the reason is not visible: a workaround, a constraint, a link to the bug.
5. State limits and failure modes. What the code does not do is often what the reader came for.

## 4. Examples run

1. Every code block a reader might paste gets executed in this session, exactly as written.
2. Paste the real output, trimmed. Never type an output you did not see.
3. If an example cannot run here (needs credentials, a paid service), say so above the block and mark it **unverified**.
4. Prefer examples the project can test automatically: doctests, example files under CI, snippets pulled from test code.

## 5. Diagrams earn their place

Draw a Mermaid diagram only when it shows a mechanism prose handles badly: a sequence across services, a state machine, a data flow with branches. Skip boxes-and-arrows that restate the directory tree.

- Every node maps to a real symbol or service. Cite it in the text below the diagram.
- Every arrow is a call, message, or data movement you traced. No arrow you inferred from naming.
- Keep it under about 12 nodes. Split larger ones by concern.

## 6. Keep it true

| Check | How |
|---|---|
| Cited lines still exist | Re-open each `file:line`; symbols move. Prefer citing a symbol plus file over a bare line number in long-lived docs. |
| Examples still run | Re-run them, or wire them into CI. |
| Doc changed with code | When a diff touches documented behavior, update the doc in the same change. |
| Stale doc found | Fix it or delete it. A wrong doc costs more than a missing one. |

## Checklist before handing back

- [ ] One doc type, matched to one reader.
- [ ] Every behavioral claim cites code and carries a measured or inferred label in your notes.
- [ ] Every runnable example was run; outputs are real.
- [ ] Each diagram shows a traced mechanism.
- [ ] Prose passed through `unslop`.
- [ ] Doc lives next to the code it describes.

## Sources

- IBM Bob Modes catalog, modes documentation/uml-architect — https://bob-modes.2azhe5jwptg4.au-syd.codeengine.appdomain.cloud (used as inspiration; no text reused)
- Diátaxis documentation framework — https://diataxis.fr
- Mermaid diagram syntax — https://mermaid.js.org
