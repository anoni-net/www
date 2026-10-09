---
title: Writing Style
description: The writing rules shared by the anoni.net community site, the docs site and News, covering voice, terminology, headings, sentence patterns and writing about security and privacy. For contributors who write, translate or edit documentation.
---

The community site, the [docs site](docs:) and [News](news:) are written by different people, and readers should meet the same standard on all three. This page is the shared rule set for English, and the basis for each repository's own documentation. Formats and workflows specific to one site live elsewhere; for the docs site, see the [contributor handbook](docs:community/contributor-handbook/).

## What these rules cover

- Pages and community updates on the community site (`anoni-net/www`)
- English content on the docs site (`docs/en` in `anoni-net/docs`)
- English articles on News (`anoni-net/news`), whose length, structure and news-style opening are covered in that repository's `guides/posts.md`
- Each repository's explanatory files: `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md` and `NOTICE` at the root, plus the `README.md` in each subdirectory

Quoting someone else, including interviews and the original titles of outside sources, is exempt.

The mechanically checkable rules are implemented as a linter, `tools/docs_style_lint.py` in `anoni-net/docs`, which accepts `.md` and `.js` files. When checking a file in another repository, pass the full path. The linter picks its rule set from the `zh-TW`, `zh-CN` or `en` segment in the path, and a relative path can end up with the wrong one:

```bash
# run from the root of anoni-net/docs
python3 tools/docs_style_lint.py /path/to/www/pages/en/about.md
```

Rule documents quote the patterns they ban, so the linter exempts this page and the docs contributor handbook by filename. The docs site's CI triggers, and the flag that limits some rules to changed lines, are described in the handbook's "Writing style" section.


## English and Chinese have separate rule sets

Traditional Chinese (`docs/zh-TW`) is the source of truth for the site, and its style rules cover Chinese punctuation, classifier repetition, register, and translated terminology. Those rules do not transfer, and several are actively wrong when applied to English. Em dashes, for example, are banned in Chinese body text and are ordinary English typography.

What follows is the English rule set. If you are writing or reviewing Chinese, use the [Chinese writing style guide](https://anoni.net/join/writing-style/) (in Chinese) instead, which is the authority for `zh-TW` and `zh-CN`. Since 2026-08 the automated style linter in CI also covers `docs/en`, though only three of the English rules are mechanised so far (`bold-lead-sentence`, `title-colon`, `machine-field`). The rest of the English rules below rest on human review.

## Voice and positioning

The English site is written for international peers, researchers, journalists, and English-preferring readers across the Sinophone Asia-Pacific, by people working inside the region. The prose should sound like it.

- Write the name as `anoni.net`, all lowercase, including at the start of a sentence (`anoni.net Docs Project`). Never `Anoni.net`. URLs and email addresses keep their own form.
- Refer to ourselves as "we, a community based in Taiwan". Avoid "In Taiwan, we...", which addresses the reader as though they were also in Taiwan.
- Where a passage is specific to Taiwan, add the regional comparison rather than leaving Taiwan as the implied default. Mainland China, Hong Kong and Macau, Singapore, Malaysia, and the diaspora each have their own picture.
- Do not translate Chinese conceptual shorthand literally. Phrases like 在地脈絡 or 公民團體 turn into stilted English when carried across word for word. Say what is actually meant.

## Terminology

- Write regulatory short names out in full on first use: PDPA becomes "the Personal Data Protection Act of Taiwan", VASP becomes "the virtual asset service provider regime".
- Write institution names out in full: 金管會 becomes "the Financial Supervisory Commission (FSC)".
- Give technical names a short expansion on first use: Tor (onion routing network), Tails (amnesic live operating system), OONI (Open Observatory of Network Interference).
- Cite English-language primary sources in footnotes. Do not cite the Chinese translation of a piece that exists in English.

## Headings

- Write headings as noun phrases, not as sentences. Recast a heading built around a verb into a noun structure; where a second layer of information is needed, continue with a comma or leave it to the intro and the `summary`.
    - <i data-icon="close"></i> `What the docs site gained in the past two weeks`
    - <i data-icon="check"></i> `Docs site update review, September 2026`
- Do not use the "Topic: explanation" colon construction.
    - <i data-icon="close"></i> `Brave and GPU fingerprinting: uniformity and randomization in one release`
    - <i data-icon="check"></i> `Two opposite approaches to flattening GPU fingerprints in Brave`
- Do not let a non-human subject perform an action in a heading; the test is the same one used for animacy in body text.
    - <i data-icon="close"></i> `The sidebar groups the tools into five sets`
    - <i data-icon="check"></i> `The five utility groups`
- This applies to article titles and to section headings at every level.
- Keep an external source's original title as-is when the link text quotes it.
- Existing articles do not need retrofitting. Apply this to new articles and substantial rewrites.

## Paragraph voice

- Write like a community member who knows the subject explaining it, not like an encyclopedia entry.
- Do not end every paragraph with a summarizing sentence. Let paragraphs stop when they are finished.
- Avoid openers like "It is worth noting that", "In conclusion", and "All in all".
- Avoid the over-symmetrical three-part structure that reads as machine-generated. Two-part parallel pairs count too: "For people outside... For people inside..." has the shape of an argument without the content. Write the actual scale, numbers, or who is affected.
- If a point reads clearly as a full sentence, do not break it into a bullet list.
- Define a concept by stating it completely. Constructions like "what this is about is" or "this refers to" push the definition out of focus without adding anything.

## Narrative structure

- Keep dates, version numbers, PR numbers, and URLs out of the opening paragraph. Open with why the matter is important, and put the facts in the sections they belong to.
- Carry one argument through the piece and tie each section back to it, so the article does not read as a chronological event log.
- A timeline can list dates, but frame it: say why the work was worth doing before the list, and who benefits after it.
- In a call to action, say near the top who is invited, what they would do, and what to do instead if they cannot. Use an admonition (`!!! tip`) when it needs to stand out.

## No animacy for things that are not people

Non-human subjects do not take human actions. The common cases and their fixes:

| Case | <i data-icon="close"></i> | <i data-icon="check"></i> |
|---|---|---|
| Organizations speaking | `Brave said it would follow up later` | `Brave's announcement said it would follow up later` |
| Documents speaking | `The report points out the risk` | `The risk is in the report's conclusion` |
| Software perceiving | `The site sees an unfamiliar string` | `The string the site receives is not in its existing list` |
| Abstractions having intent | `The toggle's existence says the trade-off remains` | `Keeping the toggle means the trade-off remains` |

Two exceptions. An organization acting as an agent keeps the plain verb when the action is something it can actually do (`Brave shipped the protection`, `the Tor Project released a new version`, `OONI collects measurements`). Direct quotations keep their original wording.

## Cutting the machine-written texture

The edits that come up most in review:

- Delete the throat-clearing opener. `Let us first lay out the basics of CryptPad. It is...` becomes `CryptPad is...`. Start with the content instead of announcing what is coming.
- Cut filler transitions: "essentially", "in other words", "to put it plainly". Delete rather than replace where possible.
- Replace an abstract placeholder with the actual content. `The next section explains why that conclusion does not hold` becomes `The usage figures in the next section contradict it`.
- Use a metaphor once in a while at most. Do not carry a whole piece on one, and do not stack the same metaphor twice in a sentence. `Each new relay in Taiwan puts another entrance on the map` becomes `Each new relay in Taiwan gives people nearby one more unblocked way into Tor`.
- Drop intensifiers and emotional colour. `battle-tested under real-world pressure` becomes `has a record of production use`. Ordinary terms do not need quotation marks for emphasis.
- Do not open a paragraph with a bolded complete sentence. Promote parallel items to headings, and write standalone paragraphs as ordinary prose. `**Location.** OONI records the country and ASN...` becomes a `### Location` heading followed by the text. Bold words as sentence elements or list labels are fine (`the **control day** uses the same parameters`, `**Data source**: ...`). The test is whether the bolded text is a complete sentence ending in a period.

## Numbers and identifiers

Mark list numbers, IDs, and serial numbers as inline code (`10006`, `10298`), so a reader can see at a glance that they are identifiers rather than quantities.

## Writing about security and privacy

Anonymity and privacy are the subject of this site, and the writing has to hold the same line:

- Do not publish recipes that can be misused. Even where the data and APIs are public, we do not walk readers through full enumeration, bulk scraping, de-anonymization, or bypassing a security control. State the result instead: `we took a snapshot of the full list on a given day`, rather than printing the command that iterates every identifier.
- Do not expose individual operators' accounts or handles. Refer to someone's observations by region or role (`an observer in Thailand`), and name people only when they are already public and naming them is necessary.
- Material involving victims, unpublished research, or personal data goes through [Sending us sensitive material](/join/upload-sensitive/).

