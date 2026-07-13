# Home

Welcome! This site is built with [MkDocs](https://www.mkdocs.org/) and the
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme,
and published automatically to GitHub Pages on every push to `main`.

## How this site works

Markdown files live in the `docs/` folder of the repository. The navigation
is generated automatically from the folder structure:

- **Top-level folders** under `docs/` become tabs in the top navigation bar.
- **Subfolders** become collapsible sections in the left sidebar.
- **Headings on each page** become the anchor menu in the right sidebar.

## Adding a new page

1. Create a Markdown file anywhere under `docs/`, e.g. `docs/guides/my-page.md`.
2. Start it with a single `# Heading` — that becomes the page title.
3. Commit and push to `main`.
4. GitHub Actions builds the site and deploys it to GitHub Pages in a minute or two.

## Sections

- [Guides](guides/index.md) — how-to articles and walkthroughs.
- [Projects](projects/index.md) — notes on things I'm building.
- [Reference](reference/index.md) — cheatsheets and quick lookups.
