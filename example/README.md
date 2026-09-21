# Filled example — "Warung Checkout"

A complete, realistic worked example of the starter pack. Fictional project: the cart and checkout flow for an Indonesian online grocery store, built as a full-stack web app.

Nothing here is a placeholder. Read it to see what "filled in" actually looks like, then write your own to the same standard.

## Files

- `AGENTS.md` — the base template plus the `web-fullstack` variant, fully filled
- `docs/prd.md` — what to build, written the way a product person would
- `docs/adr/0001` — record architecture decisions (the starting ADR)
- `docs/adr/0002` — allow guest checkout
- `docs/adr/0003` — use Midtrans as the payment provider

## What to notice

**The PRD names a number, not a feeling.** "61% abandonment, target under 45%" — not "checkout feels slow". Every acceptance criterion is a pass/fail sentence with a concrete value. `Given a postal code that is not 5 digits, then "Postal code must be 5 digits"` — an agent can turn that into a test without asking you anything.

**Out of scope is as long as in scope.** One-click checkout is excluded *with a reason*. Without that line, an agent reading "make checkout faster" would plausibly build it.

**Open questions are written down, not resolved by guessing.** Three of them, each with an owner and a date. That list is what the agent points at instead of inventing an answer.

**The ADRs record the rejected options.** ADR-0003 says Xendit was a close call and why Midtrans won. Six months on, when someone asks "why not Xendit?", the answer exists. An agent reading it will not quietly switch providers or bolt on a second one.

**The ADRs admit the costs.** "Vendor lock-in", "their outage is our outage", "fees higher than direct integrations". An ADR listing only benefits is marketing, not a decision record.

**AGENTS.md guardrails are specific to this project.** Not just "do not touch secrets" but "including the Midtrans keys", "never log a card number, CVV, or full address", "never call the Midtrans API, even in sandbox". Generic rules get ignored; named ones do not.

**Section 6 carries one project-specific rule.** "Every pricing change needs a test with a concrete rupiah figure." One line, born from a real risk. Yours should have its own equivalent — the thing that would hurt most if it broke.

## The test of a good PRD

Hand it to someone who has never seen the project. If they can list what to build, what not to build, and what is still undecided — it is good enough for an agent.
