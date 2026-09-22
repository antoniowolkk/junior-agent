# What junior has learned

A running record of every `/grow-skill` ("go learn") call that produced something, newest first.
Not a changelog of file diffs — that's `git log`. This is the plain-language summary: what junior
looked into, what it concluded, and why. Read this to catch up on the pack without reading a PR.

Every entry lands in the same pull request as the change it describes, written before the PR
number exists, so it never depends on a follow-up commit to a branch that may already be merged.

---

## 2026-09-22 — grow: `descope`

The pack had a lot to say about building something well and nothing about not building it. `rigor`
names Laziness Protocol and Subtract Before You Add as principles, but a name is not a procedure —
the same gap `reproduce` filled for "reproduce first." Researched ponytail, a skill pack built
entirely around this idea, whose agentic benchmark on a real FastAPI + React repo measures a 54%
mean cut in lines of code against the same agent with no skill, largest where the baseline
over-built and near zero where the code was already minimal. That is the second leg: over-building
is measurable, not a matter of taste. Took its rung ladder and its lazy-not-negligent floor, but
deliberately did not copy its always-on posture — ponytail writes less code by default, whereas a
junior agent that quietly narrows scope is harder to catch than one that over-builds, so `descope`
ends in a five-line verdict the human signs off on and never in a smaller diff handed over without
comment. Did not check this pack's own sessions for a friction pattern: the skill was written to a
direct request rather than through a `/grow-skill` run, so it stands on the repo gap and the cited
sources, not a third leg.

## 2026-09-22 — grow: `migrate`

Schema and data migrations are the highest blast-radius change this pack lets an agent make, and
nothing told it how to plan one safely. Researched the expand-contract pattern and backfill
separation as the standard way to ship a schema change without a matching deploy window, and wrote
`migrate` around reversibility and never coupling a migration to the code deploy that needs it.
Checked this pack's own sessions for a corroborating friction pattern and found none real — every
match was the backlog row's own text, not a genuine incident. Stands on the repo gap and primary
sources, not a third leg.

## 2026-09-22 — propose: `perf`

Not a new skill — a candidate added to the backlog. `rigor`'s own routing table names a "Perf"
route with real steps, but unlike Investigate, Architect, and Blast-radius, no companion skill
expands it. Verified against Brendan Gregg's USE method (utilization/saturation/errors per
resource) as real prior art for a systematic approach instead of guessing at a bottleneck. Checked
this pack's own sessions too: found nothing — every hit on "perf" was the substring inside
"perform," reported honestly as a null result rather than stretched into a pattern.

## 2026-09-21 — grow: `reproduce`

`rigor` said "reproduce first" but gave no procedure for turning a vague defect report into
something provably broken. Researched delta debugging — Zeller and Hildebrandt's `ddmin` algorithm
for shrinking a failing input to its smallest form, the case that inspired it cut 896 lines of HTML
down to the 1 line that crashed the browser — and built `reproduce` around extracting a falsifiable
claim, reproducing at the coarsest level that works, then shrinking it. The biggest section ended up
on intermittent failures, because this pack's own early sessions were dominated by nondeterminism
talk (race conditions, flaky tests, "works on my machine") more than any other kind of friction.
