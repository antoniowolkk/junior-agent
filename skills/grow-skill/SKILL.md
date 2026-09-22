---
name: grow-skill
description: Pick one topic, research it as deep as it goes, and open a pull request for one new skill or one real improvement to an existing one. Use for /grow-skill, "go learn", "grow the pack", "add a skill", or any request to have this pack teach itself something new. Manual, on demand — never merges, the human is the merge authority.
---

# Grow Skill

Triggered by hand — "go learn", `/grow-skill`, or a direct ask — never by a timer. One call picks
one topic, researches it as deep as it goes, and produces exactly one pull request: one new skill,
or one real improvement to an existing one. The human reviews and merges. Nothing here authorizes
a merge, a force push, or a change to `main`.

Depth over speed, always. A call to this skill is a deliberate decision to spend real time and
real research on one thing done well — never a quick pass to have something to show.

`AGENTS.md` section 7 outranks this file. Where section 7 says stop and ask, stop and ask.

Read [`CONTRIBUTING-SKILLS.md`](../../CONTRIBUTING-SKILLS.md) before starting. It is the contract
this skill exists to satisfy.

## 0. Preflight

Abort the run, without a PR, if any holds:

- The working tree is dirty. Report and stop.
- Six or more agent-authored pull requests are already open. Count every open PR whose branch
  matches `skill/*`, `backlog/*`, or `maintain/*`:

  ```bash
  gh pr list --state open --json headRefName \
    -q '[.[] | select(.headRefName | test("^(skill|backlog|maintain)/"))] | length'
  ```

  At six or more, stop before any research — no reading, no searching, no writing. The queue is
  full until a human merges or closes one. This is the backpressure that keeps unreviewed work from
  piling up no matter how often this is called.
- The pack is at its cap. Twelve skills is the ceiling; past that, routing gets worse, not better,
  and **maintain** is the only remaining mode.

An abort is a success. Say which condition fired and stop.

## 1. Pick the mode

A run does exactly one of these, and picks the first that applies. Being called at all is a
deliberate decision by a human to spend a real research cycle — so past the structural stops in
section 0, prefer **grow** or **propose** over **abort**. Never fall through to **grow** because
there is nothing else to do; do fall through to it because the research earned it.

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

Three sources, gone into deep rather than skimmed. A run that produces a skill is expensive for
the reviewer to check, so it earns that cost by being thorough here, not by being fast.

| Source | How |
| --- | --- |
| **Repo gaps** | Use the `Glob` tool for `skills/*/SKILL.md`, then the `Read` tool on each match and on `templates/AGENTS.md` — never a shell loop (`for`, `cat`, `find`). Name the exact gap the new skill fills and the existing skill it most nearly overlaps. If the overlap is more than a third, extend that skill instead and close the backlog row as `rejected`. |
| **Web** | Search for prior art: other skill packs, agent-engineering write-ups, primary docs for any tool the skill drives. Open and read at least two independent primary sources before writing a step from them — a blog post summarizing a spec is not the spec. Prefer the tool's own documentation or the paper over a tutorial about it. Verify any command the skill will tell an agent to run by executing it, not by reading that it should work. Anything you cannot verify is dropped, not hedged. |
| **This pack's own sessions** | This pack exists to help an agent write and use `AGENTS.md`-driven skills well — not to document its user's unrelated work. Use the `Grep` tool (never raw `Bash` — `grep`, `cat`, `for`-loops, and `find` invoked through Bash each need a fresh, unpredictable permission grant and are the single most common cause of an unattended run hanging forever) in two passes: first `output_mode: "files_with_matches"` on the literal text `"cwd":"<this repo's absolute path>"` across `~/.claude/projects/**/*.jsonl` to find this pack's own session files, then `Grep` only those specific files for recurring friction with *this pack's own skills* — one that didn't trigger, routing that confused an agent, a step nobody could follow. Never grep transcripts from other repositories or other projects — a different codebase's bugs, migrations, or incidents are not this pack's research material. Never source a skill's content from another installed plugin's own behavior or output (a terse-mode formatter, an unrelated command pack) — that is a different tool, not evidence about skill authoring. Do not stop at a count: read enough surrounding context in a handful of matches to tell a real recurring pattern from a coincidence of wording, and say how many sessions it spans. Quote the pattern, never the content: no file contents, paths, credentials, or personal data enter the skill or the PR. |

### Cross-verify before writing

Before step 3, every non-obvious claim needs two independent legs, not one:

- A step drawn from the web needs a second source that agrees with it, or a local run that
  confirms it, before it becomes an instruction.
- A step drawn from a repo gap needs the web or a transcript pattern behind it too — "nothing
  covers this" is not by itself evidence that a skill should.
- A step drawn from transcripts needs either a primary source that explains *why* the friction
  happens, or a repo gap that names where the fix belongs.

A claim with only one leg stays a **guess** and stays out of the skill, even if it looks right.
This is slower than writing from a single search result, and that is the point: heavier research
now is cheaper than a wrong instruction a reviewer has to catch, or worse, misses.

Label every claim in your notes `measured`, `inferred`, or `guess`. A `guess` may not become an
instruction in the skill.

## 3. Write

In **propose** mode, write backlog rows only and skip to step 4. In **maintain** mode, make the one
cited change and skip to step 4.

In **grow** mode, create `skills/<name>/SKILL.md` with the `Write` tool directly — it creates the
new directory as it writes the file, so there is no need for `mkdir` or any other shell step first.
Use `Write`/`Edit` for every file touched in this step, never `Bash`. Shape:

1. Frontmatter: `name`, `description` with real trigger phrases.
2. `# Title`, then one paragraph on what the skill is for and what it refuses to do.
3. Numbered phases. Tables and checklists over paragraphs.
4. A precedence line pointing at `AGENTS.md` section 7.
5. `## Sources` at the bottom, linking anything external.

Then update, each with `Edit`:

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

Before committing, append one entry to [`LEARNINGS.md`](../../LEARNINGS.md) with `Edit`, newest
entry at the top (right after the `---`), in this shape:

```
## YYYY-MM-DD — <mode>: `<name>`

Plain-language summary: what the gap or friction was, what was researched, what it concluded,
in 3-6 sentences. Say plainly when a leg came up empty rather than omitting it.
```

Write this entry self-contained — no PR link, no PR number. Those don't exist yet at this point in
the run, and a plan to add them in a follow-up commit is exactly how work has gone missing before:
a second push to a branch whose PR already merged lands nowhere. The entry ships in the same commit
as everything else in this step, so it can never be orphaned that way.

```bash
git switch -c skill/<name>
git add skills/<name> README.md BACKLOG.md LEARNINGS.md
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
