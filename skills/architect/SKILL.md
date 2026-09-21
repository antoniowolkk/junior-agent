---
name: architect
description: Design the types, signatures, and module boundaries before writing code, then implement against that sketch. Use for /architect, "design this", or any change crossing a function or module boundary where jumping straight to code would lock in the wrong shape.
---

# Architect

Design before implementing. Sketch types, signatures, and module boundaries with `not implemented` bodies, agree on the shape, then fill it in. If implementation proves the sketch wrong, throw the sketch out rather than bolting fixes onto it.

Subordinate to `AGENTS.md` section 7. Where this says proceed and the guardrails say ask, ask.

## Phases

Write one todo per phase before starting.

### A. Ground

Trace how every system the new code touches works today. Run the **investigate** skill over the relevant subsystems.

Naming a file is not grounding. Produce the traced model: entry points, data flow, who owns what. If the design changes ownership or layering, also find out why the current shape exists — a constraint you cannot see is still a constraint.

Skip this phase only for genuinely greenfield work with no surrounding system.

### B. Sketch

Write the caller's usage first. How does this get called, with what, and what comes back? Derive the types from that, then the module map.

Design it twice. Produce at least two structurally distinct candidates before choosing, even when the first looks sufficient. Whole-shape alternatives, not point fixes inside one shape. For a contested or expensive decision, run the candidates as parallel subagents (see **swarm**) and synthesize.

Screen every candidate for:

- **Shallow modules.** A large interface hiding little complexity.
- **Information leakage.** Two modules that must both change when one fact changes.
- **Temporal decomposition.** Modules split by execution order instead of by what they know.
- **Pass-through methods.** A function that only forwards to another with the same signature.

Compare survivors on interface depth. Prefer the design that hides more complexity behind a smaller public surface.

### C. Agree

Default: proceed with the chosen sketch, no checkpoint.

Stop for sign-off when the human asked for one, or when `AGENTS.md` section 7 requires it (more than 3 files touched, an irreversible decision, a new dependency). A decision that is hard to reverse gets an ADR before implementation, per `AGENTS.md` section 8.

For adversarial pressure on the sketch before writing code, run **interrogate** on it.

### D. Implement against the sketch

Replace `not implemented` bodies with code. The sketch is the contract.

A deviation is signal, not friction to absorb silently. If a function needs a parameter the sketch did not anticipate, say which it is: the sketch was wrong, the requirement was missed, or the implementation is overreaching.

### E. Scrap when the architecture is wrong

Throw the sketch out when the friction is a pattern, not a single instance. Tells:

- The same shape of workaround appearing across unrelated code.
- Several unrelated edge cases that each need a special-case branch.
- Types needing escape hatches (`any`, casts, optionals that are always set) to compile.
- A "we need a lock" reflex when the sketch said the state was not shared.
- Callers needing to know the abstraction's internal rules to use it.

Use judgment. Complexity in the data is not complexity in the design.

When you scrap: re-trace what was built, redesign as if the new constraints had been day-one assumptions, subtract before you add, and return to phase B.

## Output

The caller's usage, the type sketch derived from it, and the module map for anything larger than one file. Alongside it: the alternative you rejected and the one sentence that decided it.
