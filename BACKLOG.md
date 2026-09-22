# Skill backlog

The queue `/grow-skill` works from. Top unclaimed `proposed` item wins; the agent may add new
proposals but may not promote its own without a human moving it up.

Status values: `proposed` (idea, unresearched) · `researching` (agent claimed it, PR open) ·
`shipped` (merged) · `rejected` (with a reason, kept as a record so it is not re-proposed).

| Status | Skill | Why it would earn a slot | Source |
| --- | --- | --- | --- |
| shipped | `reproduce` | `rigor` says "reproduce first" but gives no procedure for building a minimal deterministic repro from a vague report. | repo gap |
| proposed | `migrate` | Schema and data migrations are the highest blast-radius change a junior agent makes, and no skill covers reversibility or backfill. | repo gap |
| proposed | `bisect` | Regression hunting across history is mechanical and currently improvised every time. | repo gap |
| proposed | `handoff` | Ending a session so the next one (or the next agent) resumes without re-deriving context. Complements `decision-log`. | repo gap |
| proposed | `dependency-audit` | Adding a package is a guardrail stop in section 7, but nothing tells the agent how to evaluate one. | repo gap |
| proposed | `perf` | `rigor`'s own routing table names a "Perf" route ("measured slowness → measure a baseline, profile, fix the measured cause") but, unlike Investigate, Architect, or Blast-radius, no companion skill expands it into a procedure. Verified against Brendan Gregg's USE method (utilization/saturation/errors per resource) as real prior art for a systematic, non-guessing approach. Checked this pack's own sessions for a corroborating friction pattern: found none — all matches were the substring "perf" inside "perform," not real signal, so this candidate rests on the repo gap and the web source, not a third leg. | repo gap + web |

## Rejected

| Skill | Reason |
| --- | --- |
