---
name: setup-project
description: Install this pack's AGENTS.md, PRD, ADR, and guardrails into a project, whether new or existing, filling values from what is actually in the repo. Use for /setup-project, "set up AGENTS.md here", or onboarding this pack into a codebase.
---

# Set up a project

Install the templates into the target repo and fill them from what is actually there. Never ship a file with a `<...>` placeholder left in it.

The human is the merge authority throughout. Show, then ask, then write.

## 1. Detect what you are in

Run a quick pass before asking anything:

- Is this a git repo? Is it empty, or does it have code?
- What language, package manager, test runner, and framework? Read `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pubspec.yaml`, the lockfile, the CI config.
- What are the real commands? Read the scripts block and the CI workflow. Do not invent commands.
- Is there already an `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or `.github/copilot-instructions.md`?

Say what you found before you write anything.

## 2. Handle an existing agent file

If one exists, do not overwrite it. Show the human a diff-shaped summary: what this pack adds, what would change, what would be lost. Ask which to keep. Merging into their file is usually the right answer.

## 3. Copy the templates

```
templates/AGENTS.md          -> <repo>/AGENTS.md
templates/docs/prd.md        -> <repo>/docs/prd.md
templates/docs/adr/*.md      -> <repo>/docs/adr/
skills/                      -> <repo>/.claude/skills/   (or install this repo as a plugin)
```

Then link it so Claude Code picks it up:

```bash
ln -s AGENTS.md CLAUDE.md
```

## 4. Pick a variant

Choose from `templates/variants/` by what the repo actually is: `web-frontend`, `web-fullstack`, `backend-api`, `mobile-flutter`. Paste its sections over the matching sections of `AGENTS.md`. If none fits, say so and write the stack and conventions sections from the code instead.

## 5. Fill the blanks

Sections 3, 4, and 5 come from the repo — stack, layout, commands, conventions. Fill them from what you read, then show the human before writing.

**Verify every command in section 4 by running it.** A command in AGENTS.md that does not work is worse than no command, because the agent will trust it.

Sections 1 and 8 come from the human: what the product is, the business outcome, the definition of success. Ask. Do not guess a business outcome.

`docs/prd.md` is the human's job. They know the users and the outcome. Prompt for it, offer to interview them section by section, but do not fabricate one.

## 6. Keep section 7 strict

Guardrails ship strict by default. Do not relax them during setup. If the human wants something pre-approved, they name it explicitly, item by item, and it goes in the file as a named exception.

## 7. Hand back a checklist

- [ ] No `<...>` placeholders remain
- [ ] Every command in section 4 was run and works
- [ ] `CLAUDE.md` symlink exists
- [ ] Skills are installed and discoverable
- [ ] `docs/prd.md` written by a human
- [ ] ADR 0001 dated
- [ ] The human can answer: what business outcome does this project create?

Anything unchecked, say which and why.
