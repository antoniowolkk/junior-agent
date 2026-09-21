---
name: grow-skill
description: Research, write, and open a pull request for one new skill in this pack. Use for /grow-skill, the scheduled growth run, "add a skill", "grow the pack", or when the backlog has an item ready to research. Never merges — the human is the merge authority.
---

# Grow Skill

One run produces at most one new skill, on its own branch, as one pull request. The human reviews
and merges. Nothing here authorizes a merge, a force push, or a change to `main`.

`AGENTS.md` section 7 outranks this file. Where section 7 says stop and ask, stop and ask.

Read [`CONTRIBUTING-SKILLS.md`](../../CONTRIBUTING-SKILLS.md) before starting. It is the contract
this skill exists to satisfy.

## 0. Preflight

Abort the run, without a PR, if any holds:

- The working tree is dirty. Report and stop.
- Three or more agent-authored pull requests are already open. Count every open PR whose branch
  matches `skill/*`, `backlog/*`, or `maintain/*`:

  ```bash
  gh pr list --state open --json headRefName \
    -q '[.[] | select(.headRefName | test("^(skill|backlog|maintain)/"))] | length'
  ```

  At three or more, stop before any research — no reading, no searching, no writing. The queue is
  full until a human merges or closes one. This is the backpressure that keeps the cadence honest:
  the agent may run ahead of review by three, never more.
- The pack is at its cap. Twelve skills is the ceiling; past that, routing gets worse, not better,
  and **maintain** is the only remaining mode.

An abort is a success. Say which condition fired and stop.

## 1. Pick the mode

A run does exactly one of these, and picks the first that applies. On a daily cadence most runs
are **maintain** or **abort**, and that is the system working. Never fall through to **grow**
because there is nothing else to do.

| Mode | When | Output |
| --- | --- | --- |
| **grow** | `BACKLOG.md` has a `proposed` row that still earns a slot after step 2's overlap check | One new skill, one PR |
| **propose** | No `proposed` row remains | Appends candidate rows, PR touching only `BACKLOG.md` |
| **maintain** | Backlog is empty *and* research surfaced no candidate, or the pack is at cap | One improvement to one existing skill, one PR |
| **abort** | None of the above produced anything worth a human's five minutes | Nothing. Say why. |

**grow** and **propose** are deliberately split across runs, so an idea is seen by a human before
anyone spends effort turning it into prose.

### What maintain means

Not rewriting for taste. One of:

- A step that research shows is wrong, outdated, or unverifiable as written.
- A trigger phrase missing from a `description`, found by grepping session logs for the thing a
  user actually typed when they wanted that skill and it did not fire.
- A concrete failure mode learned since the skill was written, added to its table.
- Dead weight: a section that could be deleted without changing what the agent does. Delete it.

Cite what prompted the change, same as a new skill. "Reads better" is not a reason and does not
earn a PR.

### The bar for a new skill

**grow** requires a yes to all of these. A no sends the run to **propose** or **maintain**, and
the backlog row gets marked `rejected` with the reason:

1. No existing skill covers it, and the nearest one overlaps by less than a third.
2. A user would plausibly reach for it more than once a month.
3. It can be written as a procedure, not an essay.
4. It came from evidence — a repo gap, a cited source, or an observed friction pattern — not from
   a run that needed something to do.

## 2. Research

Three sources. Use all that apply, and record where each claim came from.

| Source | How |
| --- | --- |
| **Repo gaps** | Read every existing `skills/*/SKILL.md` and `templates/AGENTS.md`. Name the exact gap the new skill fills and the existing skill it most nearly overlaps. If the overlap is more than a third, extend that skill instead and close the backlog row as `rejected`. |
| **Web** | Search for prior art: other skill packs, agent-engineering write-ups, primary docs for any tool the skill drives. Prefer primary sources. Verify any command the skill will tell an agent to run. Anything you cannot verify is dropped, not hedged. |
| **Session transcripts** | Grep `~/.claude/projects/**/*.jsonl` for recurring friction on this topic — repeated corrections, retried commands, the same question asked across sessions. Quote the pattern, never the content: no file contents, paths outside this repo, credentials, or personal data enter the skill or the PR. |

Label every claim in your notes `measured`, `inferred`, or `guess`. A `guess` may not become an
instruction in the skill.

## 3. Write

In **propose** mode, write backlog rows only and skip to step 4. In **maintain** mode, make the one
cited change and skip to step 4.

In **grow** mode, create `skills/<name>/SKILL.md` to the contract. Shape:

1. Frontmatter: `name`, `description` with real trigger phrases.
2. `# Title`, then one paragraph on what the skill is for and what it refuses to do.
3. Numbered phases. Tables and checklists over paragraphs.
4. A precedence line pointing at `AGENTS.md` section 7.
5. `## Sources` at the bottom, linking anything external.

Then update:

- The skills table in `README.md`.
- The companion table in `skills/rigor/SKILL.md`, if the skill is one `rigor` should route to.
- `keywords` in `.claude-plugin/plugin.json`, only if the skill introduces a new theme.
- The backlog row: `proposed` → `researching`.

Run the skill's own prose through the `unslop` skill before continuing.

## 4. Verify

Both must pass before a PR exists:

```bash
./scripts/validate-skills.sh
```

- Validator exits 0.
- `git diff --stat` touches only the paths CONTRIBUTING-SKILLS.md allows for an agent PR.

If the validator fails, fix and re-run. Do not open a failing PR and do not edit the validator to
pass.

## 5. Ship

Branch name carries the mode: `skill/<name>` for **grow**, `backlog/<date>` for **propose**,
`maintain/<skill>` for **maintain**.

```bash
git switch -c skill/<name>
git add skills/<name> README.md BACKLOG.md
git commit
git push -u origin skill/<name>
gh pr create --label agent-authored --draft
```

Commit and PR prose are written normally, not in any compressed mode.

The PR body states, in this order:

1. What the skill does, in two sentences.
2. The gap it fills and the nearest existing skill.
3. Sources, with links.
4. **What to check** — the two or three judgment calls the reviewer should push on.
5. Anything researched and deliberately left out.

For **maintain**, replace 1 and 2 with what changed and what prompted it. For **propose**, list
each new row with its evidence, and say which existing skill it nearly overlapped.

Stop there. Do not merge, do not enable auto-merge, do not comment further on the PR.

## Failure modes

| Smell | What it means |
| --- | --- |
| The skill reads like an essay | You researched a topic instead of writing a procedure. Cut to steps. |
| Description has no trigger phrase | It will never fire. Rewrite around what a user types. |
| Overlaps an existing skill | Extend that one. A ninth near-duplicate makes routing worse. |
| Cites nothing | Either it came from a gap analysis (say so) or it is a guess (drop it). |
| More than one skill in the diff | Split the PR. |
