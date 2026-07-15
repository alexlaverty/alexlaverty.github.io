---
name: write-article
description: Write a researched article page for this site on a given topic. Creates the markdown file in the right topic folder under docs/, tags it, and generates the hero image and summary lede via new-hero.py (topic landing pages list their articles automatically). Use when Alex asks to write, create, or draft an article, page, or write-up about a topic.
---

# Write an article page

The argument is the topic, e.g. `/write-article how heat pumps work`.
Everything below follows the conventions in CLAUDE.md — structure,
frontmatter, writing style, and SEO checklist all apply.

## 1. Choose the location and slug

- List the top-level topic folders under `docs/` (ignore `posts/`,
  `videos/`, `author/`, `tags.md`, and generated content). Pick the
  folder the topic belongs to.
- If no existing folder fits, create a new top-level kebab-case topic
  folder named for the term someone would search, plus its `index.md`
  landing page (frontmatter `description` + one or two sentences saying
  what the section covers). Create it directly — no need to ask.
- Filename is the URL slug: kebab-case, keyword-bearing, the term
  someone would actually search. Getting it right matters; renames
  break URLs.

## 2. Research the topic on the web

- Use WebSearch, then fetch 2–4 solid sources (official documentation,
  Wikipedia, reputable publications) with WebFetch.
- Cross-check the key facts. Where sources disagree, resolve it or
  state the spread explicitly ("figures cited range from X to Y") —
  never silently pick one.
- Keep the source URLs for a Sources section.

## 3. Write the page

- Target 600–900 words.
- Frontmatter: `description` (~150 chars, factual, for search
  snippets) and 1–4 lowercase kebab-case `tags`. Reuse existing tags
  (grep the frontmatter across `docs/`) before inventing new ones;
  prefer tag names matching topic folder names.
- One `#` H1 with the searchable title, then descriptive `##` headings.
- **Voice — hard rules.** Write in the neutral informational register
  of `docs/deep-time/memory-of-mankind/index.md`, not first person.
  Never fabricate personal experience, projects, purchases, costs,
  dates, or opinions — the site's credibility rests on its first-person
  content being true. If Alex's prompt supplies an experience or
  opinion, include it faithfully and only then use first person.
- All CLAUDE.md writing-style bans apply: no hype vocabulary, no
  contrast-pivot constructions, no rhetorical questions, no exclamation
  marks, no summary conclusions, no calls to action.
- End with a `## Sources` section listing the references as markdown
  links. Attribute claims that came from a specific source.
- Link at least one related page on this site if one exists.

## 4. Hero image and summary lede

Run:

```
python new-hero.py <path-to-new-page>
```

This generates the hero image with ComfyUI and fills in the `summary:`
frontmatter in one step. If it fails because ComfyUI is not reachable,
fall back to summaries only:

```
python new-hero.py --summary <path-to-new-page>
```

and tell Alex the hero can be added later by re-running
`python new-hero.py <path>` with ComfyUI running.

## 5. Verify and report

- `mkdocs build --strict` must pass.
- Leave everything uncommitted for Alex to review.
- Report: file path and final URL, chosen tags, whether the hero was
  generated (and in which style — see `image_style:` in the page
  frontmatter), and which sources were used.
