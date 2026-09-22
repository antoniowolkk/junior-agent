---
name: update-pack
description: Bring an installed copy of this pack up to date without destroying local edits. Use for /update-pack (Codex CLI: $update-pack), "update junior-agent", "is my copy of the skills stale", "a new version came out", or after pulling a repo whose .claude/skills or .agents/skills were copied in by hand months ago.
---

# Update Pack

Refresh an installed copy of junior-agent in place. Skills are the pack's to replace. `AGENTS.md`, the PRD, and the ADRs are the human's, and this skill never writes them.

An update is a class of change where being wrong is expensive and quiet: a clobbered `AGENTS.md` looks like a successful update until the agent starts trusting a convention nobody in the project follows.

## 0. Precedence and the stop line

`AGENTS.md` section 7 outranks this file. Three of its clauses land here:

- "Delete or rename any file, directory, branch, or database table."
- Overwriting tracked files the human has edited.
- Installing anything.

Reading, fetching to a temp directory, and showing a diff need no permission. Every write into the target repo needs an explicit yes, after the plan in section 5 has been shown.

A repo may have skills installed at `.claude/skills/` (Claude Code), `.agents/skills/` (Codex CLI), both, or neither. Treat each directory that exists as its own install: same procedure, own stamp, own three-way compare. When both exist they were populated from the same commit and stay in lockstep — a skill that replaces in one replaces in the other, in the same step, from the same upstream copy.

Hard rules, no exceptions:

| Path | This skill may |
| --- | --- |
| `.claude/skills/**`, `.agents/skills/**` | replace, after showing the diff and asking |
| `.claude/skills/.junior-agent-version`, `.agents/skills/.junior-agent-version` | rewrite, as the last step |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `docs/prd.md`, `docs/adr/**` | read and report drift only — **never write** |
| everything else in the repo | nothing |

## 1. Find the install and read the stamp

```bash
ls .claude/skills/ .agents/skills/ 2>/dev/null
cat .claude/skills/.junior-agent-version .agents/skills/.junior-agent-version 2>/dev/null
claude plugin list 2>/dev/null | grep -i junior
```

Say which directories exist before doing anything else. If their stamps disagree (different commit or version), do not assume — report the mismatch and ask which one the human trusts, or run each as an independent update.

The stamp is written by `/setup-project` and by this skill. It records what was installed and from where:

```
# junior-agent install stamp - do not edit by hand
version: 0.1.0
commit: 4f1c2ab9d3e5f6708192a3b4c5d6e7f8091a2b3c
source: https://github.com/antoniowolkk/junior-agent
installed: 2026-09-22
method: copy
```

`commit` is the base of the three-way compare in section 4. Without it every local edit looks like a conflict.

## 2. Route by install method

Decide this once per directory found in section 1 — a repo can be a plugin install for Claude Code and a manual `.agents/skills/` copy for Codex CLI at the same time, and each follows its own row:

| What you found | Do this |
| --- | --- |
| Claude Code plugin, no `.claude/skills/` in the repo | **Stop on that directory.** Tell the human to update it through `/plugin` — the plugin system owns those files. Running this skill over it creates a second, divergent copy. |
| `.claude/skills/` or `.agents/skills/` with a stamp | Continue at section 3 for that directory. |
| `.claude/skills/` or `.agents/skills/` with no stamp | Continue in degraded mode, section 6, for that directory. |
| None of the above, for either directory | Not an install. Offer `/setup-project` instead. |

Say which case applies to each directory you found before doing anything else.

## 3. Fetch upstream read-only

Clone to a temp directory outside the target repo. Never add a remote to the human's repo, never fetch into it, never touch their working tree to read upstream.

```bash
tmp=$(mktemp -d)
git clone --quiet https://github.com/antoniowolkk/junior-agent "$tmp"
git -C "$tmp" log -1 --format='%H %cs'
```

Use the `source` line from the stamp when it points somewhere else — a fork is a legitimate upstream.

If the stamp's `commit` is not in the clone, say so and fall back to degraded mode. A rewritten history or a deleted fork is a fact to report, not a thing to work around silently.

## 4. Classify every skill three ways

For each skill directory found in section 1 (`.claude/skills/`, `.agents/skills/`, or both), and for each skill inside it, compare three versions: **base** (upstream at the stamped commit), **local** (what is installed now), **head** (upstream now).

```bash
git -C "$tmp" show <stamped-commit>:skills/<name>/SKILL.md | shasum
shasum <install-dir>/<name>/SKILL.md   # <install-dir> is .claude/skills or .agents/skills
shasum "$tmp/skills/<name>/SKILL.md"
```

If both install directories are present, run the classification once — the files are byte-identical when both are current with the same stamp — but confirm that with a hash before assuming it, and always apply the resulting write to both directories.

| base vs local | base vs head | Verdict | Action |
| --- | --- | --- | --- |
| same | same | current | nothing |
| same | differs | stale | safe to replace |
| differs | same | locally modified | keep local, say so |
| differs | differs | **conflict** | show both diffs, ask, default to keeping local |
| missing in local | exists in head | new skill | offer to install |
| exists in local | missing in head | removed upstream | report, never delete without a yes |

"Removed upstream" is the one that looks like cleanup and is not. A skill the human wrote themselves lives in the same directory and is indistinguishable from one this pack deleted.

Label each verdict **measured** — every row comes from a hash you actually computed. Do not infer a file is unchanged because its neighbour was.

## 5. Show the plan, then ask

One table, before any write:

```
skill              verdict             action
rigor              stale               replace  (upstream: 3 commits, +12/-4 lines)
reproduce          current             none
architect          locally modified    keep local
migrate            conflict            ask
swarm              new upstream        install?
our-house-style    unknown to pack     leave alone
```

Then the count: how many replace, how many need a decision. Ask for one yes covering the safe replacements, and a separate yes for each conflict.

## 6. Degraded mode, no stamp

Without a base you cannot tell a local edit from an upstream change. Do not guess.

1. Say plainly that the base is unknown and edits cannot be distinguished.
2. Diff local against head for every skill, and show the diffs.
3. Replace only the files where local is byte-identical to head — those are no-ops — plus any the human approves one at a time, having seen the diff.
4. Write a stamp at the end so the next update is a real three-way compare.

Never bulk-replace in degraded mode, however tidy the diffs look.

## 7. Templates: report, never write

`AGENTS.md`, `docs/prd.md`, and `docs/adr/**` are filled in by the human and diverge from the templates on purpose. That divergence is the project, not drift to be corrected.

Show what changed upstream in the corresponding template since the stamped commit:

```bash
git -C "$tmp" diff <stamped-commit>..HEAD -- templates/
```

Report it as a list of upstream changes worth considering, each with the section it touches and one line on what it does. Hand the human the diff. Stop there. If they want a change applied, that is a separate request they make explicitly, section by section.

Section 7 of their own `AGENTS.md` is the one file where a silent overwrite is most dangerous: a relaxed guardrail replaced by a strict template looks harmless, and a strict guardrail replaced by anything is a safety regression.

## 8. Restamp and verify

After writing, and only after, write the stamp into every install directory you touched:

```bash
for dir in .claude/skills .agents/skills; do
  [ -d "$dir" ] && printf '# junior-agent install stamp - do not edit by hand\nversion: %s\ncommit: %s\nsource: %s\ninstalled: %s\nmethod: copy\n' \
    "$version" "$(git -C "$tmp" rev-parse HEAD)" "$source" "$(date +%F)" \
    > "$dir/.junior-agent-version"
done
rm -rf "$tmp"
```

`version` comes from `.claude-plugin/plugin.json` in the clone.

Then hand back:

- [ ] Install method named per directory, and plugin installs routed to `/plugin`
- [ ] Every verdict backed by a hash that was computed, not assumed
- [ ] No file outside the install directories in use was written
- [ ] Every conflict decided by the human, not by a default
- [ ] Template drift reported, not applied
- [ ] Stamp rewritten with the new commit, in every directory in use
- [ ] Temp clone removed

Anything unchecked, say which and why.
