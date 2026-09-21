# Skill backlog

The queue `/grow-skill` works from. Top unclaimed `proposed` item wins; the agent may add new
proposals but may not promote its own without a human moving it up.

Status values: `proposed` (idea, unresearched) · `researching` (agent claimed it, PR open) ·
`shipped` (merged) · `rejected` (with a reason, kept as a record so it is not re-proposed).

| Status | Skill | Why it would earn a slot | Source |
| --- | --- | --- | --- |
| researching | `reproduce` | `rigor` says "reproduce first" but gives no procedure for building a minimal deterministic repro from a vague report. | repo gap |
| proposed | `migrate` | Schema and data migrations are the highest blast-radius change a junior agent makes, and no skill covers reversibility or backfill. | repo gap |
| proposed | `bisect` | Regression hunting across history is mechanical and currently improvised every time. | repo gap |
| proposed | `handoff` | Ending a session so the next one (or the next agent) resumes without re-deriving context. Complements `decision-log`. | repo gap |
| proposed | `dependency-audit` | Adding a package is a guardrail stop in section 7, but nothing tells the agent how to evaluate one. | repo gap |

## Rejected

| Skill | Reason |
| --- | --- |
