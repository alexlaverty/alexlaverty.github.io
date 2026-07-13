# Getting started

How to work on this site locally and add content.

## Prerequisites

You need Python 3.9+ installed. Everything else comes from `requirements.txt`.

## Run the site locally

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open <http://127.0.0.1:8000>. The site live-reloads as you edit
Markdown files, so you can preview changes instantly.

## Add a page

Create a new `.md` file under `docs/`:

```text
docs/
├── index.md              ← home page
├── guides/               ← "Guides" section in the left sidebar
│   ├── index.md          ← landing page for the section
│   └── getting-started.md
├── projects/             ← "Projects" section
└── reference/            ← "Reference" section
```

To add a whole new sidebar section, just create a new folder under `docs/`
with an `index.md` inside it.

## Publish

Commit and push to `main`:

```bash
git add .
git commit -m "Add new page"
git push
```

The **Deploy MkDocs to GitHub Pages** workflow runs automatically and the
change is live at <https://alexlaverty.github.io/> shortly after.
