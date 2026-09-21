# junior-agent

Depth before speed. A Claude Code plugin that makes an agent work like a careful engineer instead of a fast one: name the task before acting, reproduce before fixing, prove against the real thing, and stop at anything hard to undo.

The goal is not more code. It is less code that is proven to work.

Two halves that need each other:

- **The project files.** `AGENTS.md` is the agent's memory, the PRD says what, ADRs say why, tests say done.
- **The skills.** How the agent actually works on anything non-trivial: routing, principles, evidence.

Written so it works for someone who does not code. Section 7 of `AGENTS.md` is strict by default, and the human is the merge authority.

## Install

Add this repo as a plugin marketplace in Claude Code, then install `junior-agent`. The nine skills become available as `/rigor`, `/architect`, and so on.

Or copy the skills by hand into any project:

```bash
mkdir -p .claude/skills && cp -r skills/* .claude/skills/
```

The skills work on their own, but they refer to `AGENTS.md` section 7 for permissions. Install the templates too.

## Set up a project

Fastest path: paste the prompt in [`templates/KICKOFF-PROMPT.md`](templates/KICKOFF-PROMPT.md), or run `/setup-project`. The agent detects whether the repo is new or existing, fills the stack and command sections from what is actually there, verifies every command by running it, and stops to ask you at each decision.

By hand, six steps:

1. Copy `templates/AGENTS.md` and `templates/docs/` into your project root.
2. `ln -s AGENTS.md CLAUDE.md` so Claude Code picks it up.
3. Install the skills (above).
4. Pick a variant from `templates/variants/` and paste its sections over the matching ones in `AGENTS.md`.
5. Fill every `<...>`. If you do not know a value, ask the agent to read the repo and fill it, then review.
6. **Write `docs/prd.md` yourself.** You know the users and the outcome. The agent does not. This is the highest-value thing a non-developer contributes.

New to working this way? Read [`docs/working-with-an-agent.md`](docs/working-with-an-agent.md) first: order of work, prompts worth keeping, warning signs, a two-week checklist.

## What is in here

| Path | What it is |
| --- | --- |
| `skills/rigor/` | The spine. Route the task, apply the principles, prove the result. |
| `skills/investigate/` | How does this work, and why is it like this. Read-only, cited. |
| `skills/architect/` | Types, signatures, and boundaries before code. |
| `skills/blast-radius/` | What a change breaks elsewhere, proven by running code. |
| `skills/interrogate/` | Parallel adversarial review, synthesized into one verdict. |
| `skills/swarm/` | Parallel fan-out over slices or competing approaches. |
| `skills/decision-log/` | A reviewable TSV trail for unattended work. |
| `skills/unslop/` | Cut AI tells from anything that ships. |
| `skills/setup-project/` | Install this pack into a repo and fill it from the code. |
| `templates/AGENTS.md` | The main file. Rules, commands, conventions, guardrails. |
| `templates/variants/` | Platform sections to paste in: frontend, fullstack, backend API, Flutter. |
| `templates/docs/prd.md` | What to build and for whom. **Yours to write.** |
| `templates/docs/adr/` | Decision records. Copy `0000-template.md` per decision. |
| `templates/KICKOFF-PROMPT.md` | The prompt you paste to start. |
| `docs/setup.md` | Detailed setup instructions, written for the agent to read. |
| `docs/working-with-an-agent.md` | How to run a project with an agent when you do not code. |
| `example/` | A complete filled-in project to copy the standard from. |

## The three rules that make it work

**Safe.** Section 7 of `AGENTS.md` is strict: the agent stops and asks before anything hard to undo. Deleting, pushing, deploying, touching a database, installing packages, handling secrets. Keep it that way while you are learning. Every skill here is subordinate to it, so where a skill says proceed and section 7 says ask, the agent asks. Nothing irreversible happens without you.

**Rigorous.** `skills/rigor/` is the working method. Name which kind of task this is before acting. Reproduce a bug before fixing it. Name the data shape before writing logic. Prove the result against the real artifact, not a green build. Label every claim as measured, inferred, or guess, so you can tell which parts of an answer were actually checked.

**Powerful.** Section 6, TDD. The agent writes a failing test first, **you review the test**, then it writes code until the test passes. Reviewing a test is far easier than reviewing code: the test states in plain terms what the thing should do. If it says the wrong thing, you catch it before any code exists — while it is still one paragraph instead of four hundred lines. This is the main defense against an agent confidently building the wrong thing.

Two things follow from those rules. **The context survives the session**: `AGENTS.md` holds rules, commands, and conventions, `docs/prd.md` holds the outcome, ADRs hold why a past decision was made, so the agent stops re-deriving the project from scratch and stops re-litigating decisions you already made. And **hard tasks get a named tool instead of a longer prompt**: tracing unfamiliar code, designing a boundary, finding what a change breaks, reviewing adversarially, running work unattended — each is a skill with its own method and output format, so the work is legible afterwards.

**The cost is speed.** This produces less code per hour on purpose. Worth it when the code has to be right and you are the one merging it. Overhead on a throwaway script.

## Why this instead of a bare agent

A stock coding agent optimises for finishing the turn. It will guess a file path, assume a data shape, declare success on a green build, and take an irreversible action because the task implied it. None of that is a bug in the model; it is what "be helpful, quickly" produces. This pack changes the objective.

Against **a bare agent with no project files**, the difference is memory and authority. Conventions and commands live in `AGENTS.md` instead of in a prompt you retype, decisions live in ADRs instead of in a chat you closed, and the permission boundary is written down where every skill can see it rather than negotiated per request.

Against **a big CLAUDE.md of rules**, the difference is routing. Rules in one flat file all compete for attention and quietly stop being applied on long sessions. Here the method is split into skills that load when the task calls for them, so the agent gets the tracing method when it is tracing and the review method when it is reviewing, each at full strength.

Against **agent packs built for speed** (scaffold generators, autonomous PR bots, "ship it" loops), the difference is who holds the merge. Those are built to reduce your involvement. This is built to make your involvement cheap: review a test instead of a diff, read a cited investigation instead of a summary, approve a decision instead of discovering it. You stay the merge authority by design, not by remembering to check.

Against **just being careful in your prompts**, the difference is that care is not a habit here, it is structure. Reproduce-before-fix and prove-against-the-real-thing hold on turn eighty of a long session, when your own attention has gone.

The name is the point. A junior engineer who asks before doing anything permanent, writes the test first, and shows their evidence is more useful on a codebase you care about than a fast one who does not.

## Keep it alive

`AGENTS.md` is only useful while it is true. When a command changes or a convention shifts, update it in the same change. A stale `AGENTS.md` is worse than none, because the agent will trust it.

## Before you start a project

- [ ] No `<...>` placeholders left
- [ ] Every command in section 4 actually runs
- [ ] `docs/prd.md` filled in by a human
- [ ] `CLAUDE.md` symlink exists
- [ ] Skills installed and discoverable
- [ ] You can answer: what business outcome does this project create?

## Credit

The method is adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by poteto (Lauren Tan), MIT licensed, condensed and rewritten for Claude Code. The `AGENTS.md` / PRD / ADR structure comes from the "Agentic AI in the SDLC" workshop. See [`NOTICE`](NOTICE).

MIT licensed. Fork it, improve it, make it yours.
