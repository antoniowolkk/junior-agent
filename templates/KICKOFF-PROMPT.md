# The kickoff prompt

Copy the block below and paste it as your first message. Works for both new and existing projects — the agent detects which and picks the right path.

Replace `<PACK PATH>` once with where this pack lives, then save it somewhere you can copy from again.

---

```
Read <PACK PATH>/docs/setup.md completely before doing anything else.

Then follow it to install the agent onboarding pack into this project:
AGENTS.md, a symlink for whichever agent tool I use (CLAUDE.md for Claude Code,
GEMINI.md for Gemini CLI — skip this for Codex CLI or Cursor, they read
AGENTS.md directly), docs/prd.md, docs/adr/, and the skills — in .claude/skills/
for Claude Code, in .agents/skills/ for Codex CLI, same files either way
(rigor is the one AGENTS.md section 6b points at).

The pack is at <PACK PATH>/ — templates/AGENTS.md as the base, templates/variants/
for platform-specific sections, templates/docs/ for the PRD and ADR templates,
skills/ for the working method, and example/ showing a fully filled-in project
for the standard to aim at.

Important context about me: I am not a developer. I cannot verify your work by
reading code, so:
- Never invent a command, path, or value. Verify it or ask me.
- Explain everything in plain language, no jargon.
- Stop at every halt point in the tutorial and wait for my answer.
- Tell me explicitly what you could not verify.

Start with Step 0: work out whether this is a new or existing project, tell me
which and why, then wait for me to confirm before continuing.
```

---

## Set the path once

```bash
sed -i '' "s|<PACK PATH>|$HOME/projects/agent|g" templates/KICKOFF-PROMPT.md
```

## If you want it always available

Save it as a slash command so you can type `/setup-agents` in any project:

```bash
mkdir -p ~/.claude/commands && cp templates/KICKOFF-PROMPT.md ~/.claude/commands/setup-agents.md
```

Then trim that copy down to just the prompt block, with no surrounding explanation.

## Later, when the project has changed

```
Read AGENTS.md. Compare it against this repo as it is today. What is now false —
commands that no longer run, paths that no longer exist, conventions the code
stopped following? Show me the drift. Do not fix anything yet.
```

Run this every few weeks. A stale AGENTS.md is worse than none, because the agent trusts it.
