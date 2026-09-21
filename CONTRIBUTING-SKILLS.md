# Contributing a skill

This applies to humans and to the growth agent (`/grow-skill`). Every skill in this pack must
pass all of it. `scripts/validate-skills.sh` enforces the mechanical half; the rest is judgment
the reviewer checks.

## Mechanical rules

1. One directory per skill: `skills/<name>/SKILL.md`. `<name>` is kebab-case, matches the
   directory, and is unique across the pack.
2. `SKILL.md` opens with YAML frontmatter containing exactly `name` and `description`:

   ```
   ---
   name: blast-radius
   description: What a change breaks elsewhere, proven by running code. Use for ...
   ---
   ```

3. `description` is one paragraph, 40–500 characters, and states **when to reach for the skill**,
   not only what it does. Include the trigger phrases a user would actually type. A description
   that omits triggers will not fire.
4. First heading after the frontmatter is `# <Title Case Name>`.
5. Relative links must resolve from the repo root.
6. Adding a skill also updates the table in `README.md` and, when it introduces a new theme, the
   `keywords` array in `.claude-plugin/plugin.json`.

## Judgment rules

- **Earn the slot.** A new skill must do something no existing skill does. If it overlaps
  `rigor`, extend `rigor` instead of adding a ninth near-duplicate.
- **Procedure, not essay.** Numbered phases, tables, checklists. If a section could be deleted
  without changing what the agent does, delete it.
- **Subordinate to the guardrails.** State that `AGENTS.md` section 7 outranks the skill wherever
  the two disagree.
- **Evidence over assertion.** Any claim the skill tells the agent to make must be labelled
  measured, inferred, or guess.
- **No AI tells.** Run the skill's own prose through `/unslop` before opening the PR.
- **Cite sources.** If the skill came from outside research, link the source in a `## Sources`
  section at the bottom.

## Scope of an agent-authored PR

The growth agent may touch only:

- `skills/**`
- `README.md` (the skills table only)
- `.claude-plugin/plugin.json` (the `keywords` array only)
- `BACKLOG.md`

It may not merge, force-push, edit `AGENTS.md` templates, rewrite existing skills beyond adding a
cross-reference row, or change anything under `scripts/` or `.github/`.

One skill per pull request.
