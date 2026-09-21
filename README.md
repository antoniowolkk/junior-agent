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
| `skills/reproduce/` | Turn a vague defect report into one deterministic failing test. |
| `skills/investigate/` | How does this work, and why is it like this. Read-only, cited. |
| `skills/architect/` | Types, signatures, and boundaries before code. |
| `skills/blast-radius/` | What a change breaks elsewhere, proven by running code. |
| `skills/interrogate/` | Parallel adversarial review, synthesized into one verdict. |
| `skills/swarm/` | Parallel fan-out over slices or competing approaches. |
| `skills/decision-log/` | A reviewable TSV trail for unattended work. |
| `skills/unslop/` | Cut AI tells from anything that ships. |
| `skills/setup-project/` | Install this pack into a repo and fill it from the code. |
| `skills/grow-skill/` | Research, write, and PR one new skill. The pack grows itself; you review. |
| `templates/AGENTS.md` | The main file. Rules, commands, conventions, guardrails. |
| `templates/variants/` | Platform sections to paste in: frontend, fullstack, backend API, Flutter. |
| `templates/docs/prd.md` | What to build and for whom. **Yours to write.** |
| `templates/docs/adr/` | Decision records. Copy `0000-template.md` per decision. |
| `templates/KICKOFF-PROMPT.md` | The prompt you paste to start. |
| `docs/setup.md` | Detailed setup instructions, written for the agent to read. |
| `docs/working-with-an-agent.md` | How to run a project with an agent when you do not code. |
| `CONTRIBUTING-SKILLS.md` | The contract every skill must satisfy, human- or agent-written. |
| `BACKLOG.md` | The queue `/grow-skill` works from. |
| `scripts/validate-skills.sh` | Mechanical checks on every `SKILL.md`. Run before any skill PR. |
| `example/` | A complete filled-in project to copy the standard from. |

## The three rules that make it work

**Safe.** Section 7 of `AGENTS.md` is strict: the agent stops and asks before anything hard to undo. Deleting, pushing, deploying, touching a database, installing packages, handling secrets. Keep it that way while you are learning. Every skill here is subordinate to it, so where a skill says proceed and section 7 says ask, the agent asks.

**Rigorous.** `skills/rigor/` is the working method. Name which kind of task this is before acting. Reproduce a bug before fixing it. Name the data shape before writing logic. Prove the result against the real artifact, not a green build. Label every claim as measured, inferred, or guess.

**Powerful.** Section 6, TDD. The agent writes a failing test first, **you review the test**, then it writes code until the test passes. Reviewing a test is far easier than reviewing code: the test states in plain terms what the thing should do. If it says the wrong thing, you catch it before any code exists. This is the main defense against an agent confidently building the wrong thing.

## Keep it alive

`AGENTS.md` is only useful while it is true. When a command changes or a convention shifts, update it in the same change. A stale `AGENTS.md` is worse than none, because the agent will trust it.

## Before you start a project

- [ ] No `<...>` placeholders left
- [ ] Every command in section 4 actually runs
- [ ] `docs/prd.md` filled in by a human
- [ ] `CLAUDE.md` symlink exists
- [ ] Skills installed and discoverable
- [ ] You can answer: what business outcome does this project create?

## The pack grows itself

`/grow-skill` researches one backlog item, writes the skill, and opens a draft pull request. It
reads three sources — the gaps between the skills already here, outside prior art, and recurring
friction in local session logs — and it never merges. You are the merge authority, same as
everywhere else in this pack.

The guardrails are structural, not promises:

- [`BACKLOG.md`](BACKLOG.md) is the queue. The agent proposes rows; only a human promotes one to
  the top.
- [`CONTRIBUTING-SKILLS.md`](CONTRIBUTING-SKILLS.md) is the contract, including the exact paths an
  agent-authored PR may touch.
- `./scripts/validate-skills.sh` fails the run before a PR exists if the frontmatter, naming,
  links, or README row are wrong.
- One skill per PR, opened as a draft, labelled `agent-authored`.

Run it on demand:

```bash
/grow-skill
```

Or put it on a timer. Frequency is safe to raise because the run is gated, not the schedule: it
stops before doing any research once three agent-authored pull requests are open, and when the
backlog is empty it either proposes new candidates or sharpens an existing skill rather than
inventing a twelfth one. Twelve skills is the hard cap.

So the review queue sets the real pace. The agent may run up to three pull requests ahead of you
and then waits. Your side of the deal is roughly five minutes per pull request.

## Credit

The method is adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by poteto (Lauren Tan), MIT licensed, condensed and rewritten for Claude Code. The `AGENTS.md` / PRD / ADR structure comes from the "Agentic AI in the SDLC" workshop. See [`NOTICE`](NOTICE).

MIT licensed. Fork it, improve it, make it yours.
