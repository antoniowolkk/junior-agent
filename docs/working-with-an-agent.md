# How to actually run a project with an agent

The templates tell the agent how to behave. This tells *you* how to work. Written for someone who does not code.

Read this once before you start a project. Come back to the checklists.

---

## The one idea that matters

You are not writing code. You are not reviewing code either — you cannot, yet, and pretending otherwise is how non-developers get burned.

**You are reviewing three things you *can* judge:**

1. **The PRD** — is this the right thing to build? You know this better than the agent does.
2. **The tests** — do these sentences describe what should happen? A test reads like a claim in English. You can check a claim.
3. **The evidence** — did it actually run, and did it pass? You can read output. [How to read it](#how-to-read-the-evidence).

Everything else, delegate. Those three are yours. Do not delegate them, because those are the three places where a wrong answer is expensive and an agent's confidence tells you nothing.

---

## Order of work

Do it in this order. Skipping ahead is the most common failure.

### 1. Write the PRD first — by hand, before any agent

Open `docs/prd.md` and fill it in yourself. Not with the agent. You.

It will feel slow. It is the highest-leverage hour of the project. The agent can write code faster than you can read it; the only real control you have is being right about *what* it builds.

Do not move on until you can answer, without hedging:
- Who is this for?
- What changes for them if it works?
- What am I deliberately *not* building?

If you cannot answer the third one, you do not have a scope yet, you have a wish.

### 2. Let the agent interview you

Now bring the agent in, and ask it to attack the PRD — not implement it:

> Read docs/prd.md. Do not write any code. Ask me the 10 questions you would need answered before building this. Rank them by how badly a wrong guess would hurt.

Answer them. Put the answers back into the PRD. Repeat until the questions get boring.

This step catches more problems than any code review you are capable of doing.

### 3. Set up AGENTS.md

Copy in the base template plus a variant. Then:

> Read this repository. Fill in sections 3 and 4 of AGENTS.md from what is actually here — the real folder layout and the real commands from package.json / pyproject.toml. Show me the proposed text. Do not write the file yet.

Then verify yourself: run each command in section 4 and see it work. **A command in AGENTS.md that does not run is worse than no AGENTS.md**, because the agent will trust it and waste a session on a phantom.

### 4. Record the big decisions before building

Ask:

> Based on docs/prd.md, list the decisions that would be expensive to reverse later. For each, tell me the realistic options and what each one costs. Do not decide for me.

Pick. Then have it draft ADRs from your choices, and read them. If an ADR lists only benefits and no costs, it is not finished — send it back.

Three to five ADRs at the start is normal. You are not documenting everything, only the doors that only open one way.

### 5. Build one feature end to end

Not five. One — and preferably the riskiest one, the part you are least sure will work. Finding out in week one that the hard part is impossible is a good week. Finding out in week six is a dead project.

Per feature:

> Take user story 1 from docs/prd.md. Write the failing tests only. Do not implement anything. Show me the tests and explain each one in plain language.

Read them. Ask: *does this sentence describe what I want?* When the tests are right:

> Implement until those tests pass. Show me the test output when you are done.

### 6. Repeat, and keep AGENTS.md true

Every time a command changes or a convention shifts, update AGENTS.md in the same session. A stale AGENTS.md decays into active misinformation.

---

## Prompts worth keeping

**Before building anything**
> Restate what I just asked in one sentence. List what you are assuming. List what you would need to decide on your own. Do not start yet.

Catches misunderstandings while they cost nothing.

**When you get a wall of code you cannot read**
> Explain what this change does in plain language, as if to someone who does not code. What could break? What did you not handle?

**When something works and you do not know why**
> What is the weakest part of what you just built? Where would it fail first under real use?

Agents answer this honestly. It is one of the most useful questions available to you.

**Before you accept "done"**
> Show me the actual command you ran and its actual output. Do not summarize it.

**When you are about to trust a test**
> Is there a way this test passes while the feature is still broken?

This is the hole in TDD — a wrong test that passes. Asking directly closes most of it.

**When stuck in a loop of failed fixes**
> Stop. Do not try another fix. List the three most likely root causes and how you would tell them apart.

After two failed attempts, a third is usually worse than the first. Break the loop yourself.

---

## How to read the evidence

The rigor skill (`skills/rigor/SKILL.md`) makes the agent paste evidence instead of claiming success. That moves the work to you: evidence you do not read is worse than no evidence, because it feels like a check happened.

You cannot read code. You can read this.

### The three questions

Ask them in order, of every "done".

**1. Did it run the real thing, or a stand-in?**

A green build means the code compiles. It does not mean the feature works. Match the proof to the change:

| What changed | What you should see pasted |
| --- | --- |
| A command-line tool | The actual command, and its actual output |
| A screen or a button | A walkthrough of the flow in the running app, or a screenshot |
| Something that reads a file or an import | The input it used, and the result it produced |
| Something that saves data | The value read back out after saving |
| Speed | A number before and a number after, from the same measurement |
| Anything a sub-agent did | The diff. Not the sub-agent's summary of the diff. |

If the pasted evidence is a build log, a test-count line, or the agent's own prose, it did not check. Say: **"Run the real thing. Paste what it printed."**

**2. Does the output actually show what was claimed?**

This is the one people skip. Read the pasted output and ask whether it demonstrates the claim.

- Claim: "duplicate records are fixed." Output shows one record. Good — but does it show the retry that used to cause the duplicate? If not, it proved nothing about the bug.
- Claim: "both formats work." Output shows one format. Half a check.
- Claim: "text output is unchanged." A real proof is a comparison against the old output. A screenshot of the new output alone is not.

The pattern: **the evidence must include the condition that used to break.** A passing run under easy conditions is not a fix.

**3. What is labelled as a guess?**

The skill requires every claim to carry a label in the same sentence — *measured*, *inferred*, or *guess*. Read for those words.

- "Measured" — should have output behind it. Check that it does.
- "Inferred" — the agent reasoned to it. Reasonable, unverified. Fine for background, not fine for "it works".
- "Guess" — treat as unknown.
- **"Inconclusive"** — the agent tried and could not check. This is a good answer, not a failure. Do not pressure it into upgrading one.

A report with no labels anywhere is a report written before the rigor skill was read. Send it back.

### Red flags in an evidence block

- **Output that is summarized rather than pasted.** "All tests passed" is a summary. The test runner's actual lines are evidence.
- **A file path or a link you have never seen.** The skill forbids fabricating these. Click it. If it does not exist, the whole report is suspect.
- **Evidence for a different thing than you asked about.** Common when a task drifted. Check the output is about your feature.
- **Timestamps that predate the change**, if any are visible. It pasted an old run.
- **No mention of what it did not check.** Every honest report has a gap somewhere.

### The one prompt for all of this

> For each thing you just claimed: is it measured, inferred, or a guess? For the measured ones, paste the command and its raw output. For anything you could not check, say inconclusive and tell me what would check it.

Run it whenever a report feels smooth.

### After an unattended run

If you left the agent working, it kept a decision log (`decisions.tsv`) — one row per decision, with a reason and an evidence pointer.

Do not read the whole log first. Read the **Attention** section at the end of its report — that is where it flags what deserves your scrutiny. Then read only the log rows that section points at.

Then spot-check two rows it did *not* flag. If those two hold up, the rest probably does. If either one is thin, read the whole log.

---

## Rules for you, not the agent

**One task per session.** Long sessions drift. Agent forgets early instructions, mixes concerns, gets confident. Finish a feature, start fresh.

**Commit often, in small pieces.** Your undo button. Ask for a commit after each passing test. If a session goes bad you lose an hour, not a week.

**Never accept "it should work".** Should is not evidence. Ask it to run the thing.

**Suspect speed.** If a big feature arrives suspiciously fast and complete, something was skipped — usually the hard case, the error path, or the tests. Ask what was skipped. It will tell you.

**"I fixed it" without a test is not a fix.** A bug that had no test can come back. Ask for the failing test first, then the fix.

**Read the diff summary even if you cannot read the diff.** How many files changed? Does that number make sense for what you asked? Twelve files for a label change means something else happened.

**When a guardrail stops the agent, do not wave it through to save time.** That prompt is the entire safety system. Read what it wants to do. If you do not understand it, that is the answer — ask it to explain before you say yes.

---

## Warning signs

| You see | It usually means | Do this |
| --- | --- | --- |
| Tests were changed in a "bug fix" | It made the test agree with the bug | Revert. Ask for the fix without touching tests. |
| "Simplified" / "cleaned up" you did not ask for | Scope creep, unreviewed | Ask what changed and why. Revert the extra. |
| A new dependency appeared | Guardrail was skipped | Ask what it is for and whether existing code could do it. |
| Confident claim, no output pasted | It did not run it | "Run it. Paste the real output." |
| Three fixes for the same bug | It is guessing | Stop. Ask for root causes, not fixes. |
| A file you never heard of got deleted | Serious — guardrail breach | Revert everything. Restart the session. |
| Evidence pasted, but it is a build log | It proved compilation, not behavior | "Run the real thing. Paste what it printed." |
| No measured / inferred / guess labels anywhere | It did not follow the rigor skill | Ask it to re-label every claim before you read further. |
| A claim that is proved under easy conditions only | The failing case was never re-run | Ask for the evidence under the condition that used to break. |
| A link or file path you cannot find | Possibly fabricated | Check it. If it does not exist, distrust the whole report. |

---

## Where this actually goes wrong

Not in the code. In these three places:

1. **A PRD that sounded clear but was not.** Everything downstream inherits the vagueness. The agent will not tell you your PRD is vague — it will confidently build one of the readings.
2. **A test that encodes the wrong expectation.** Then green means nothing. Only you can catch this, and only if you actually read the tests instead of skimming them.
3. **Guardrail fatigue.** Week one you read every prompt. Week three you click yes. That is when the destructive one lands.

The workshop's line for this: *vibe to explore, TDD to ship.* Explore freely when it costs nothing. The moment it goes near something real — tests first, human decides.

---

## Two-week checklist

**Day 1**
- [ ] `docs/prd.md` written by hand
- [ ] Agent has interviewed you; answers folded back in
- [ ] Out-of-scope list is real and has reasons

**Day 2**
- [ ] `AGENTS.md` in place, no placeholders left
- [ ] Symlink created for your agent tool, if it needs one (`CLAUDE.md` for Claude Code, `GEMINI.md` for Gemini CLI — Codex CLI and Cursor read `AGENTS.md` directly)
- [ ] Every command in section 4 personally run and working
- [ ] Guardrails read start to finish, kept strict

**Day 3**
- [ ] ADRs written for the hard-to-reverse decisions
- [ ] Each ADR lists costs, not just benefits

**Week 1**
- [ ] Riskiest feature built end to end, TDD
- [ ] You have read and understood every test
- [ ] You have seen the tests fail before they passed
- [ ] You have rejected at least one "done" for weak evidence

**Week 2**
- [ ] AGENTS.md updated at least once — proof it is alive
- [ ] One decision recorded that came up mid-build
- [ ] You can explain to someone else what the system does and why
