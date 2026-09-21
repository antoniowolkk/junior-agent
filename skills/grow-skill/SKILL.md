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
- A branch matching `skill/*` already has an open PR. One in flight at a time.
- `BACKLOG.md` has no `proposed` row and step 1 produces no candidate worth a slot.

An abort is a success. Say which condition fired and stop.

## 1. Pick the target

Take the topmost `proposed` row in [`BACKLOG.md`](../../BACKLOG.md). If none, run the three
sources in step 2 to propose new rows, append them, open a PR that changes only `BACKLOG.md`, and
stop. Proposing and writing are separate runs, so a human sees the idea before it becomes prose.

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

Create `skills/<name>/SKILL.md` to the contract. Shape:

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

Stop there. Do not merge, do not enable auto-merge, do not comment further on the PR.

## Failure modes

| Smell | What it means |
| --- | --- |
| The skill reads like an essay | You researched a topic instead of writing a procedure. Cut to steps. |
| Description has no trigger phrase | It will never fire. Rewrite around what a user types. |
| Overlaps an existing skill | Extend that one. A ninth near-duplicate makes routing worse. |
| Cites nothing | Either it came from a gap analysis (say so) or it is a guess (drop it). |
| More than one skill in the diff | Split the PR. |
