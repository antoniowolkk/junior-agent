---
name: unslop
description: Cut AI tells from any writing — replies, docs, PR descriptions, commit messages, comments, ADRs. Apply to any prose surface before it ships.
---

# Unslop

Edit text to remove the patterns that mark it as machine-written. Preserve meaning and match the intended tone. Terse is not an excuse to drop content: tradeoffs, choices, and open decisions stay.

Your reply is a prose surface. So is a PR description, a commit body, an ADR, and a README.

## Process

1. Scan for the patterns below.
2. Rewrite.
3. Self-audit: "what makes this obviously AI generated?" Fix what is left.

## Content

- **Superficial -ing phrases.** "highlighting...", "ensuring...", "showcasing...", "fostering...". Delete, or replace with the concrete thing.
- **Vague attributions.** "Experts believe", "Industry reports suggest", "Some argue". Name the source or cut the sentence.
- **Restating the prompt** before answering. Answer.
- **Summary paragraphs that add nothing.** If the last paragraph repeats the first, delete it.

## Language

- **AI vocabulary.** additionally, crucial, delve, enhance, fostering, garner, interplay, intricate, landscape (abstract), leverage (as a verb), pivotal, robust, seamless, showcase, tapestry, testament, underscore, vibrant. Use plain words.
- **Fancy ways to say "is".** "serves as", "stands as", "boasts", "features". Say is or has.
- **"Not just X, but Y."** State the point directly.
- **Rule of three.** Forcing ideas into groups of three. Use the natural number.
- **Synonym cycling.** Pick one term for a thing and repeat it. Consistency beats variety in technical prose.
- **False ranges.** "from X to Y" where X and Y are not on a scale. List the things.
- **Hedging stacks.** "it may potentially be possible that". Say it or do not.

## Style

- **Em dash overuse.** Use periods or commas. If a thought needs separating, end the sentence.
- **Colon as a mid-sentence connector.** Colons are for lists and examples. Rewrite the sentence so it stands without one.
- **Boldface overuse.** Do not bold every proper noun or acronym.
- **Inline-header lists.** The tell is a bold label and colon that restates the line: "**Performance:** Performance improved". Convert to prose. A bold lead-in ending in a period that names the item and is followed by genuinely new detail is fine.
- **Title case headings.** Use sentence case.
- **Decorative emoji** in headings and bullets.

## For replies specifically

- Short declarative sentences, one thought each.
- Say who the work is for and what changes for them before any implementation detail.
- Never fabricate a link, citation, or file path. Link only what you produced or read this session.
- **No is an acceptable answer.** Asked whether to do something, give your real judgment. Decline or push back when that is the truth. Candour over agreement.
