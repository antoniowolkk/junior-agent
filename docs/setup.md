# Setup tutorial

> Instructions **for the agent**. Point it at this file to install the pack into a project.
> `/setup-project` is the short version of this procedure.

**Read this file completely before creating or editing any AGENTS.md, CLAUDE.md, PRD, or ADR. Do not skim it. Do not start until you reach the end.**

You are being asked to install the agent onboarding pack — `AGENTS.md`, `docs/prd.md`, `docs/adr/` — into a project. This file tells you how. It is a procedure, not a suggestion.

The person asking you is very likely **not a developer**. They cannot check your work by reading code. That changes what "done well" means:

- Never invent a value. A wrong command in AGENTS.md is worse than a blank one, because you will trust it later and waste whole sessions on a phantom.
- Never fill a placeholder by guessing. Ask, or verify from the repo.
- Explain what you are doing in plain language, without jargon, at every halt.
- The finished file must be true today, not aspirational.

---

## Rules that apply the whole way through

1. **Do not write any file until you reach the STOP point that authorizes it.** There are explicit halts below. They are mandatory.
2. **Never leave a `<...>` placeholder** in a delivered file. Either fill it from verified fact, or ask the human, or delete the line and say you deleted it.
3. **Verify every command before writing it down.** Run it. If it fails, do not write it — report it.
4. **Only the human writes the PRD's substance.** You may format, structure, and interview. You may not invent users, metrics, or business outcomes. If you do not know the abandonment rate, you do not know it.
5. **Never invent an ADR decision.** ADRs record decisions that were actually made. For an existing repo you infer from code and label it as inferred. For a new project the human decides and you write it up.
6. **Do not modify existing project files** beyond the pack itself. Installing onboarding docs is not a license to refactor.
7. **Guardrails stay strict unless the human explicitly lowers them.** If they ask you to loosen a guardrail, tell them plainly what that permits, then do as they say.
8. **If the repo already has an AGENTS.md or CLAUDE.md, do not overwrite it.** Go to Step 0b.

---

## Step 0 — Work out which situation you are in

Run these checks before anything else:

```bash
ls -a                      # is this a repo at all?
git log --oneline | head   # is there history?
ls package.json pyproject.toml go.mod Cargo.toml pubspec.yaml Makefile 2>/dev/null
ls AGENTS.md CLAUDE.md docs/ 2>/dev/null
```

Classify:

- **NEW** — empty or near-empty folder, no source code, no dependency manifest.
- **EXISTING** — real source code, a dependency manifest, commit history.
- **AMBIGUOUS** — scaffolding only (a bare `create-next-app`, an empty repo with a README). Treat as NEW, but say so and let the human correct you.

State your classification out loud and why, in one sentence, before continuing.

### Step 0b — If AGENTS.md or CLAUDE.md already exists

Do not overwrite. Read it, then report:
- what it already covers well,
- what is missing compared to this pack,
- what in it is now false (commands that do not run, paths that do not exist).

Propose a merge. Wait for approval. Preserve their existing content and wording wherever it is still true — it may encode decisions you cannot see.

---

## PATH A — NEW project

Order: **PRD → decisions → AGENTS.md → code.** Never reorder this. Code written before the PRD is code built on a guess.

### A1. Copy the pack in

Copy `AGENTS.md` and `docs/` to the project root. Create the symlink:

```bash
ln -s AGENTS.md CLAUDE.md
```

If the platform does not support symlinks, copy the file and say clearly that both must be edited together.

### A2. Interview for the PRD

Do not write `docs/prd.md` from your own imagination. Ask the human, one small batch at a time — never all at once:

1. In one sentence, what does this thing do, and for whom?
2. What is bad today that this fixes? How do they know it is bad?
3. If this works, what changes — for the user, and for the business?
4. How would you measure whether it worked?
5. What will people assume is included that you are deliberately *not* building?
6. Any hard constraints — deadline, device, budget, regulation?
7. What do you not know yet?

**STOP.** Draft `docs/prd.md` from their answers only. Show it. Do not write the file until they confirm it.

Then challenge it once, before moving on:

> Here are the places this PRD is still ambiguous. For each, here are the two ways I could read it, and they lead to different software.

Fold the answers back in. Anything still undecided goes in **Open questions** with an owner — it does not get silently resolved by you.

### A3. Surface the one-way doors

From the PRD, list decisions that would be expensive to reverse: data storage, framework, auth model, API shape, hosting, payment provider, anything the rest of the system will be built on top of.

For each, give realistic options with honest costs. **Do not decide.** Present, then stop.

**STOP.** Wait for their choices.

Write one ADR per decision using `docs/adr/0000-template.md`. Number sequentially from 0002 (0001 is already written — just set its date and deciders).

Every ADR must contain rejected alternatives and real costs. An ADR listing only benefits is not finished — rewrite it before showing it.

### A4. Fill AGENTS.md

- Sections 1 and 2: derive from the PRD. These you can do now.
- Section 3 and 4 (layout and commands): **leave marked `TBD — fill once scaffolding exists`.** You cannot know the real commands before the project exists. Do not invent them. Do not copy them from the variant file as if they were verified — the variant is a suggestion, not a fact.
- Section 5: paste from the chosen variant in `variants/`, minus anything that does not apply.
- Section 6: keep TDD as written. Add one project-specific rule reflecting this project's biggest risk (money, personal data, safety, uptime — pick the real one).
- Section 7: keep strict. Then add project-specific dangers by name: the actual database, the actual deploy target, the actual secret files.
- Section 6b: keep the rigor reference as written. Do not delete it.
- Section 8: list the ADRs you just created.

Then install the skills so section 6b resolves to a real file:

```bash
mkdir -p .claude/skills && cp -r skills/* .claude/skills/
```

Run it and confirm `.claude/skills/rigor/SKILL.md` exists. Section 6b points at that path; if the file is missing, the reference is a dead end and the agent silently loses the method. The other skills (`architect`, `investigate`, `blast-radius`, `interrogate`, `swarm`, `decision-log`, `unslop`) install alongside it and are referenced from rigor.

**STOP.** Show the complete file. Get approval. Then write it.

### A5. Return after scaffolding

Once real code exists, come back and fill sections 3 and 4 using the **PATH B** verification procedure. Tell the human this is pending — it is the most-forgotten step in the whole process.

---

## PATH B — EXISTING project

Order: **AGENTS.md from reality → backfill ADRs → PRD per feature.** The code is the source of truth. Your job is to describe it accurately, not to improve it.

### B1. Read before writing

Explore properly. Do not guess from filenames:

- Dependency manifest: real dependencies, real scripts, real versions.
- Folder layout, two levels deep. What actually lives where.
- Test setup: framework, where tests live, how they are named, how they run.
- Lint / format / typecheck config.
- CI config — it usually contains the true build and test commands.
- Existing `README`, `docs/`, `CONTRIBUTING`.
- 3–5 representative source files, to learn the real conventions.

Report what you found before writing anything.

### B2. Verify every command — this step is not optional

For each command going into section 4, **run it and observe the result.**

- Works → record it.
- Fails → do not record it. Report the failure and ask.
- Cannot run safely (deploy, migration, anything that touches a real system) → record it, and mark `— not verified, do not run without approval`.

Never copy a command from a README without running it. READMEs rot.

### B3. Extract conventions from the code, not from best practice

Read the code and report the patterns it *actually* follows, each with a `file:line` example: naming, error handling, folder structure, test style, config handling.

**STOP.** Show the list. Ask which conventions to keep. Some existing patterns are mistakes the team wants to leave behind — you cannot tell which from the code alone.

Only approved conventions go into section 5.

### B4. Write AGENTS.md

- Sections 1 and 2: ask the human for the business outcome. It is not in the code. Do not infer it from the product name.
- Section 3: the real layout, from B1.
- Section 4: only verified commands, from B2.
- Section 5: only approved conventions, from B3.
- Section 6: TDD, plus one project-specific rule tied to this codebase's real risk.
- Section 7: strict, plus named dangers — the real database name, the real deploy command, the real secret file paths, the real external APIs that cost money.

**STOP.** Show it. Approval. Then write.

### B5. Backfill ADRs

Identify the architectural decisions visible in the codebase. For each, report what it is, the evidence in the code, and what would break if someone undid it without knowing.

**STOP.** Ask which are worth recording. Three to five is right. Do not write twenty.

Write them with:
- `Status: Accepted (backfilled <today's date>)`
- Context stating plainly that this was reconstructed from code, and that the original reasoning was not recorded at the time.

Do not fabricate the original debate. If you do not know why they chose Postgres, write that the reason was not recorded — that is the truthful and more useful answer.

### B6. PRD going forward

Do not write a PRD for the whole existing application. It would be a large fiction.

Instead, put `docs/prd.md` in place as a template for the *next* feature, and tell the human: from now on, one PRD per feature, written before work starts.

---

## Both paths — finish properly

Before you report done, verify every line:

- [ ] No `<...>` placeholder remains anywhere in a delivered file
- [ ] Every section-4 command was actually run, or is explicitly marked unverified
- [ ] Every path in section 3 exists — check them
- [ ] `CLAUDE.md` symlink exists and resolves
- [ ] `.claude/skills/rigor/SKILL.md` exists — section 6b of AGENTS.md points at it
- [ ] The companion skills are installed alongside it in `.claude/skills/`
- [ ] Section 6b survived editing and was not deleted as boilerplate
- [ ] Guardrails name this project's real dangers, not only generic ones
- [ ] ADRs list rejected alternatives and real costs
- [ ] Sections 1 and 2 came from the human, not from your inference
- [ ] Nothing outside the pack was modified

Then report, in plain language:

1. What you created, file by file.
2. What you verified yourself, and how.
3. **What you could not verify, and what you guessed.** Be specific. This is the most important line in your report — it is the only way a non-developer knows where to look.
4. What is still open and who needs to decide it.
5. The single next action.

---

## Things that go wrong — do not do these

- **Inventing commands** from framework convention instead of this repo. `npm test` when the repo uses `pnpm test` costs a whole session.
- **Copying the variant file verbatim.** It is a starting point with placeholders, not verified truth.
- **Writing a PRD for the human.** Producing a plausible PRD full of invented metrics is worse than producing none — it looks finished, so nobody fixes it.
- **Fabricating ADR history.** "We chose Postgres for its reliability" when nobody said that is fiction in the permanent record.
- **Loosening guardrails to be helpful.** Not your call.
- **Doing all of it in one pass without stopping.** The halts exist because a non-developer cannot catch your mistakes afterward. Skipping them removes their only control.
- **Refactoring while you are in there.** You were asked for documentation.
- **Reporting done with placeholders left.** Not done.

---

## The point

`AGENTS.md` is only worth having if it is true. A false one is worse than none, because future agents — including you — will trust it and act on it.

Accuracy over completeness. A short honest file beats a long confident one.
