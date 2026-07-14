# laverty.io

Personal site built with [MkDocs](https://www.mkdocs.org/) and
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/),
published to GitHub Pages at <https://laverty.io/>.

## How it works

- Markdown content lives under [`docs/`](docs/).
- Navigation is generated automatically from the folder structure:
  folders → collapsible left sidebar sections (collapsed by default),
  page headings → right sidebar anchor menu.
- Pushing to `main` triggers the
  [Deploy MkDocs to GitHub Pages](.github/workflows/deploy.yml) workflow,
  which builds the site and deploys it to GitHub Pages.

## Local development

Requires Python 3.x.

```bash
pip install -r requirements.txt   # once
mkdocs serve
```

Open <http://127.0.0.1:8000> — the site live-reloads as you edit.

If port 8000 is taken (`PermissionError: [WinError 10013]` or "address
already in use"), serve on another port:

```bash
mkdocs serve -a 127.0.0.1:8001
```

To run the same build as CI (fails on broken internal links):

```bash
mkdocs build --strict
```

The output lands in `site/` (git-ignored); it's a static site, so opening
it via `mkdocs serve` is only needed for live reload.

## Adding content

Drop a `.md` file anywhere under `docs/`, start it with a `# Heading`,
then commit and push. To add a new sidebar section, create a new folder
under `docs/` with an `index.md` inside.

For a daily log entry, scaffold today's post and fill it in:

```bash
python new-daily.py
```

To add a video summary page (embedded YouTube video with an AI-generated
summary below it; requires `pip install yt-dlp` and the `claude` CLI):

```bash
python new-video.py <youtube-url>
```

Folder structure, page conventions, and writing style are documented in
[CLAUDE.md](CLAUDE.md).
