# Skill backlog

The queue `/grow-skill` works from. Top unclaimed `proposed` item wins; the agent may add new
proposals but may not promote its own without a human moving it up.

Status values: `proposed` (idea, unresearched) · `researching` (agent claimed it, PR open) ·
`shipped` (merged) · `rejected` (with a reason, kept as a record so it is not re-proposed).

| Status | Skill | Why it would earn a slot | Source |
| --- | --- | --- | --- |
| shipped | `reproduce` | `rigor` says "reproduce first" but gives no procedure for building a minimal deterministic repro from a vague report. | repo gap |
| researching | `migrate` | Schema and data migrations are the highest blast-radius change a junior agent makes, and no skill covers reversibility or backfill. `AGENTS.md` section 7 stops on "write to, migrate, seed, or drop any database that is not a local throwaway" but nothing tells the agent how to plan the change it is asking permission for. Nearest existing skill is `blast-radius`, which analyses one diff rather than sequencing deploys. Checked this pack's own sessions for a corroborating friction pattern: none, every match was the backlog row itself or this run's own transcript, so the skill rests on the repo gap and the primary docs cited in it. | repo gap + web |
| shipped | `delegate` | `rigor` routes the work but never sizes it: nothing says how much scope to take unsupervised, what context to refuse to start without, or what has to be true before widening scope mid-task. Nearest neighbours are `swarm` (fanning work out) and `decision-log` (recording it after the fact). Sourced from Anthropic's agent-design and human-agent-teams guidance, with the METR RCT as a scope-limited caution on self-reported speed. | web |
| researching | `descope` | The pack optimises for code that is proven, but nothing argues for writing none. No skill asks whether the change is needed at all, whether existing code already covers it, or whether deleting beats adding. Nearest neighbours are `architect` (which assumes the thing gets built) and `delegate` (which sizes scope but does not question it). Sourced from `ponytail` (#9 in the AI Agents top-100 ranking, 143k stars), whose whole premise is that the best code is the code never written. | web |
| proposed | `handoff` | Ending a session so the next one (or the next agent) resumes without re-deriving context. Complements `decision-log`. Reviewing ranks 21-100 of the same ranking surfaced five separate agent-memory repos (`mem0` #28, `OpenViking` #63, `graphiti` #81, `cognee` #83, `agentmemory` #95), all solving persistence across sessions — a repeated signal that this is a real recurring need, not a one-off guess. | repo gap + web |
| proposed | `threat-model` | `rigor`'s routing table has no security route at all: a task that is really "is this safe to expose" gets routed to Investigate or Architect and treated as an ordinary design question. Section 7 stops on secrets but says nothing about reasoning over an attack surface. Sourced from `strix` (#29, 63k stars), an open-source pentest agent, as evidence that security review is a distinct procedure rather than a flavour of code review. Would be gated by section 7 and read-only by default. | repo gap + web |
| proposed | `context-budget` | `investigate`, `blast-radius`, and `swarm` all fan out and dump findings back into the main thread with no cap on volume, so a long session degrades from context exhaustion rather than from bad reasoning. Nothing in the pack says what a sub-task owes the caller versus what it should summarise. Sourced from `headroom` (#24, 73k stars), which compresses tool output before it reaches the model; the skill version is a discipline, not a proxy. | repo gap + web |
| proposed | `bisect` | Regression hunting across history is mechanical and currently improvised every time. | repo gap |
| proposed | `dependency-audit` | Adding a package is a guardrail stop in section 7, but nothing tells the agent how to evaluate one. | repo gap |
| proposed | `perf` | `rigor`'s own routing table names a "Perf" route ("measured slowness → measure a baseline, profile, fix the measured cause") but, unlike Investigate, Architect, or Blast-radius, no companion skill expands it into a procedure. Verified against Brendan Gregg's USE method (utilization/saturation/errors per resource) as real prior art for a systematic, non-guessing approach. Checked this pack's own sessions for a corroborating friction pattern: found none — all matches were the substring "perf" inside "perform," not real signal, so this candidate rests on the repo gap and the web source, not a third leg. | repo gap + web |

## Rejected

| Skill | Reason |
| --- | --- |
