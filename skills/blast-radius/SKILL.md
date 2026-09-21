---
name: blast-radius
description: Find what a change breaks somewhere else before it ships, and prove the one fact it is safe because of by running real code. Use for "what could this break", "blast radius of X", or reviewing a small diff you do not trust.
---

# Blast radius

Find what a change breaks beyond the diff. Companion to **investigate**: that one tells you what the code does and why, this one tells you what it breaks elsewhere.

Listing the callers is not the job. Grep does that in a second. The job is the breakage grep will not show you.

## Do not trust your own writeup

A blast-radius writeup reads as convincing whether or not it is true. So do not hand back the writeup. Find the one or two facts the whole thing depends on and prove them by running code.

### How sure are you

For each fact the change's safety depends on, get as far down this list as is cheap, and say where it stopped.

1. **You said so.** Worthless alone.
2. **You pointed at the line.** A real `file:line`, or the library's own source.
3. **You showed the bad case cannot happen.** You walked the failure path step by step and it does not reach.
4. **You ran it.** A script or test that calls the real code and fails loud if you are wrong.
5. **You reproduced it in the running app.**

Any safety fact you cannot get to step 4, say so. Do not write it up as settled. Step 4 is usually one small script that imports the same library the app ships and calls the exact function you are worried about.

## Steps

1. **Read the change.** The diff, the symbols it adds, changes, and deletes, and what now behaves differently — including the part the diff does not spell out.
2. **Find the one fact it is safe because of.** Most risky-looking changes are safe because of a single fact ("this only drops already-dead cache entries"). Find that fact. If it holds, most of the maybes clear at once. Spend your time here, not on a long list.
3. **Look where grep stops.** The pinned version and any local patch of a library you call. Timing: microtasks, teardown, unmount ordering. Things a symbol search misses: JSON an API returns, a DB column, a wire format, another language reading the same bytes, a feature flag, code three hops downstream.
4. **Be honest about each risk.** Real likelihood, real cost. Keep the confirmed ones. List what you checked and cleared separately.
5. **Prove the one fact.** Write the script, run it, paste what happened. If you cannot prove it cheaply, mark it **unproven**.

## Output

- **What it does.** Including the non-obvious part.
- **The one fact it is safe because of.** Which step you got it to, and the proof — or `unproven`.
- **Risks.** Only the real ones. Each names how it breaks, the `file:line`, likelihood, cost, and how to check.
- **Cleared.** What you checked and why it is fine.
- **Before you merge.** The cheapest test or repro that catches the real bug, including the script you wrote.
