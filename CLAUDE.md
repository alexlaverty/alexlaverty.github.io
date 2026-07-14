# CLAUDE.md

Personal knowledge site for Alex Laverty, built with MkDocs Material and
deployed to GitHub Pages at https://laverty.io/ on every push to
`main`. Markdown lives under `docs/`; navigation is generated from the
folder structure (no `nav:` in mkdocs.yml — keep it that way).

## Commands

```bash
pip install -r requirements.txt   # once
mkdocs serve                      # live preview at http://127.0.0.1:8000
mkdocs build --strict             # what CI runs; broken internal links fail the build
python new-daily.py [category …]  # scaffold today's daily log post
python new-video.py <url> [tag …] # generate a video summary page (needs yt-dlp + claude CLI)
```

Always run `mkdocs build --strict` before committing content changes.

## Folder structure rules

Topic-first, not type-first. Top-level folders under `docs/` are topics
(`permaculture/`, `ai-coding/`), never content types (`guides/`,
`tutorials/`). Two sanctioned exceptions: `docs/posts/` (the daily log —
see "Daily log vs project pages") and `docs/videos/` (video summaries —
see "Video summary pages").

1. **One folder per topic**, kebab-case, named for the term someone would
   search for: `real-estate/`, not `property-stuff/`.
2. **Every folder has an `index.md`** — a short landing page that says what
   the section covers and links to its pages. It renders as the section's
   clickable entry in the sidebar (`navigation.indexes`).
3. **Stay flat until it hurts.** Pages go directly in the topic folder.
   Only add a subfolder when a distinct sub-topic has 3+ pages (e.g.
   `ai-coding/claude-code/`). Maximum depth: 3 levels below `docs/`.
4. **New interest = new top-level folder.** Don't shoehorn a new topic into
   an existing one. When unsure where a page belongs, put it in the closest
   topic folder and give it tags — don't create a `misc/` folder.
5. **Filenames are URL slugs.** Kebab-case, descriptive, keyword-bearing:
   `worm-farm-setup.md` → `/permaculture/worm-farm-setup/`. Never
   `page1.md`, `notes.md`, `untitled.md`, or dates in filenames.
6. **Moving/renaming a published page breaks its URL.** Prefer getting the
   name right first. If a move is genuinely needed, flag it to Alex — it
   may warrant adding the mkdocs-redirects plugin.

## Daily log vs project pages

Two kinds of content with different lifecycles:

- **Daily log posts** (`docs/posts/YYYY-MM-DD.md`) are append-only
  journal entries: what happened today, written once, not edited later.
  Handled by the Material blog plugin with `blog_dir: .` — the home page
  (`docs/index.md`) is the blog index; posts don't appear in the sidebar
  nav. The front page shows a unified timeline (built by
  `hooks/timeline.py`, rendered by `overrides/blog.html`): blog posts by
  publish date merged with content pages by last git commit date, newest
  first, ten per page with extra pages at `/page/N/`. Topic landing
  `index.md` pages are excluded from the timeline.
- **Project pages** (topic folders like `permaculture/`) are evergreen
  reference pages, updated in place as the project evolves.

The rule connecting them: the daily post records what happened; anything
durable gets distilled into the relevant topic page, and the post links
to it (from a post the path is `../permaculture/worm-farm-setup.md`).
Don't let reference material accumulate in the blog.

Scaffold today's post with `python new-daily.py [category …]`. Posts are
the one exception to the "no dates in filenames" rule and use their own
frontmatter (no `description`/`tags` needed):

```markdown
---
date: 2026-07-14
authors:
  - alex
categories:
  - permaculture
---

# 14 July 2026

Moved the worm farm into shade; midday temps were cooking it. Details in
[worm farm setup](../permaculture/worm-farm-setup.md).
```

- `date` is required and drives the URL (`/2026/07/14/…`).
- `authors` keys come from `docs/.authors.yml`.
- `categories` are optional, must match top-level topic folder names, and
  give a per-topic chronological view of the work.
- The writing style rules below apply to posts too. Short is fine — two
  sentences is a valid daily post.

## Video summary pages

`docs/videos/` holds one page per YouTube video worth sharing: the video
embedded up top, an AI-generated summary and key points below. Pages are
generated, not hand-written:

```bash
python new-video.py <youtube-url> [tag ...]   # requires yt-dlp + claude CLI
```

The script fetches subtitles, has Claude write the summary, creates
`docs/videos/<title-slug>.md`, and appends a link to `docs/videos/index.md`.
Every video page gets the `videos` tag plus 1–3 topic tags (supplied as
arguments, or suggested by Claude from the site's existing tags). Tags are
how videos connect to topics — a permaculture video is tagged
`permaculture`, not filed in `permaculture/`. Keep the AI-disclosure line
the script adds at the bottom of each page.

How the three categorisation mechanisms divide up: topic folders say what
a page is about (navigation), frontmatter tags collect cross-topic threads
across all page types (the site-wide index), and blog `categories` only
filter the daily log chronologically. Prefer tag names that match topic
folder names so the threads line up.

## Page conventions

Every page starts with frontmatter, then a single `#` H1:

```markdown
---
description: One factual sentence, ~150 chars, for search result snippets.
tags:
  - permaculture
  - composting
---

# Worm farm setup

What this page is about in one or two sentences, then straight into it.
```

- `description` is required — it becomes the meta description.
- `tags` are lowercase kebab-case, 1–4 per page. Reuse existing tags
  (check the rendered `/tags/` page, which shows counts, or grep the
  frontmatter) before inventing new ones. Tags are for cross-topic
  threads (e.g. `automation` appearing in both `ai-coding/` and
  `real-estate/`). Each tag gets its own listing page at `/tags/<tag>/`,
  generated at build time by `hooks/tag_pages.py` — never create tag
  pages by hand. The same hook fills the count-ordered index on
  `docs/tags.md`, and a widget in `overrides/main.html` shows all tags
  with counts in the right sidebar.
- Exactly one H1 per page. Use `##`/`###` for structure — they feed the
  right-hand anchor menu. Don't skip levels.
- Images go in an `img/` folder next to the page, with descriptive
  filenames and alt text.
- Link related pages on this site with relative links to the `.md` file
  (`[worm farms](../permaculture/worm-farm-setup.md)`) — internal linking
  helps readers and SEO, and `--strict` verifies the targets exist.

## Writing style

The voice is an engineer documenting their own projects — primarily for
their future self, secondarily for a reader who found the page via search.
Matter-of-fact, specific, and plain. It should read like a good lab
notebook or an internal engineering wiki, not a blog chasing traffic.

**Do:**

- Write in first person singular. "I planted the bed in March" not "we"
  or "one" or passive voice.
- Open with what the thing is. First paragraph states the subject and the
  outcome or current status. No scene-setting, no "why this matters"
  preamble.
- Use real specifics: dates, costs, quantities, model numbers, error
  messages, version numbers. "$140 of sleepers from Bunnings" beats
  "affordable materials".
- Record what failed and what it cost. Dead ends are often the most
  useful content on a page.
- State opinions as opinions, plainly: "I think X is overkill for this"
  — then move on. No hedging paragraphs, no "your mileage may vary".
- Let short pages be short. A 150-word page that answers one question is
  finished. Do not pad.
- Use ordinary words. "Use" not "utilize", "buy" not "invest in",
  "problem" not "pain point".

**Never (these are the AI tells — treat as hard bans):**

- Contrast-pivot constructions: "It's not just X — it's Y", "This isn't
  about X, it's about Z", "X isn't the goal; Y is."
- Hype vocabulary: game-changer, supercharge, unlock, unleash, elevate,
  seamless, effortless, powerful, robust, delve, dive in, journey,
  landscape (metaphorical), leverage (as a verb).
- Flattering or coaching the reader: "you're already ahead of most
  people", "here's the secret", "trust me".
- Rhetorical questions as transitions or openers: "So what does this
  mean?", "Ever wondered why…?", "The best part?"
- Clickbait framing in titles or headings. Headings describe content:
  "Irrigation costs" not "The irrigation mistake that cost me $400".
- Exclamation marks.
- Punchy sentence fragments for drama. "No fluff. Just results." — never.
- Rule-of-three flourishes and em-dash crescendos ("faster, cheaper, and
  — best of all — free").
- Bolding random phrases mid-sentence for emphasis.
- Summary conclusions that restate the page ("In conclusion…", "To wrap
  up…"). When the information ends, the page ends.
- Calls to action ("give it a try!", "let me know in the comments").
- Filler transitions: "Let's take a look", "Without further ado", "It's
  worth noting that", "At the end of the day".

**Calibration example.**

Bad (AI-flavoured):

> Composting isn't just about reducing waste — it's about transforming
> your garden. In this guide, we'll dive into how I built a thriving worm
> farm that supercharges my soil. The best part? It took just one weekend!

Good (target voice):

> I built a two-tier worm farm out of old broccoli boxes in March 2026.
> Total cost was about $25 plus 1000 compost worms ($45 from an eBay
> seller). Six weeks in it processes roughly 2 kg of scraps a week. The
> first attempt failed — details below.

## SEO checklist (applies to every new topic page; daily posts exempt)

- Slug and H1 contain the term someone would actually search.
- `description` frontmatter present, factual, ~150 chars.
- At least one internal link to a related page on this site, and a link
  from the topic's `index.md` to the new page.
- Headings are descriptive (they're what Google shows as jump links).
- Alt text on images.
- Don't keyword-stuff. Write normally; the structure does the SEO work.

## Publishing workflow

1. Add or edit pages under `docs/`.
2. If a new page was added, link it from its topic's `index.md`.
3. `mkdocs build --strict` — must pass.
4. Commit with a plain message describing the content change; push to
   `main`. GitHub Actions (`.github/workflows/deploy.yml`) builds and
   deploys automatically. The "last updated" date on pages comes from git
   commit history (git-revision-date-localized plugin), so no manual
   date maintenance.
