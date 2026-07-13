# alexlaverty.github.io

Personal site built with [MkDocs](https://www.mkdocs.org/) and
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/),
published to GitHub Pages at <https://alexlaverty.github.io/>.

## How it works

- Markdown content lives under [`docs/`](docs/).
- Navigation is generated automatically from the folder structure:
  top-level folders → top nav tabs, subfolders → left sidebar sections,
  page headings → right sidebar anchor menu.
- Pushing to `main` triggers the
  [Deploy MkDocs to GitHub Pages](.github/workflows/deploy.yml) workflow,
  which builds the site and deploys it to GitHub Pages.

## Local development

```bash
pip install -r requirements.txt
mkdocs serve
```

Open <http://127.0.0.1:8000> — the site live-reloads as you edit.

## Adding content

Drop a `.md` file anywhere under `docs/`, start it with a `# Heading`,
then commit and push. To add a new top-nav tab, create a new top-level
folder under `docs/` with an `index.md` inside.
