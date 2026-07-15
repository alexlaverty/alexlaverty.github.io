"""MkDocs hook: article header under the page H1.

Injects, in order, directly below the H1 of every content page:
the `summary:` frontmatter as a lede paragraph, an author/date meta
row (author from docs/.authors.yml, published/updated dates from git
history), and the `image:` hero set by new-hero.py — giving
Title -> Summary -> Meta row -> Hero -> content. The hero image also
becomes the og:image social preview via overrides/main.html.

Also stores ISO dates and a schema type in page.meta so
overrides/main.html can emit Article/BlogPosting JSON-LD. Daily posts
get the meta dates only — Material's blog templates already display
their author and date. Registered via `hooks:` in mkdocs.yml.
"""
import datetime
import html
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# Structural pages and generated views that never get the header
# (mirrors the exclusions in timeline.py)
EXCLUDED_PREFIXES = ("author/", "page/", "archive/", "category/", "tags/")
EXCLUDED_PAGES = ("index.md", "tags.md")

_git_dates: dict[str, tuple[str, str]] | None = None
_author: dict | None = None


def _git_dates_map() -> dict[str, tuple[str, str]]:
    """(first, last) commit ISO timestamp per repo-relative path, from a
    single git call. Newest commits come first, so the first time a path
    appears is its last modification and the final time is its creation."""
    global _git_dates
    if _git_dates is None:
        result = subprocess.run(
            ["git", "log", "--format=%x00%aI", "--name-only", "--", "docs"],
            capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
        )
        modified: dict[str, str] = {}
        created: dict[str, str] = {}
        ts = ""
        for line in result.stdout.splitlines():
            if line.startswith("\x00"):
                ts = line[1:]
            elif line.strip():
                path = line.strip()
                modified.setdefault(path, ts)
                created[path] = ts
        _git_dates = {p: (created[p], modified[p]) for p in modified}
    return _git_dates


def _author_info() -> dict:
    global _author
    if _author is None:
        with open(ROOT / "docs" / ".authors.yml", encoding="utf-8") as f:
            authors = yaml.safe_load(f)["authors"]
        key, info = next(iter(authors.items()))
        _author = {"name": info["name"], "avatar": info["avatar"],
                   "url": f"/author/{key}/"}
    return _author


def _display_date(iso: str) -> str:
    date = datetime.datetime.fromisoformat(iso)
    return f"{date.strftime('%B')} {date.day}, {date.year}"


def _wants_header(src: str, all_srcs: set[str]) -> bool:
    """Content pages only. A folder's landing index.md is excluded unless
    the folder has no other pages (then the index IS the content page)."""
    if src.startswith(("posts/",) + EXCLUDED_PREFIXES) or src in EXCLUDED_PAGES:
        return False
    if src.endswith("index.md"):
        folder = src[: -len("index.md")]
        if folder.count("/") <= 1:
            return False
        return not any(s != src and s.startswith(folder) for s in all_srcs)
    return True


def _meta_row(published_iso: str, modified_iso: str) -> str:
    author = _author_info()
    dates = (f'Published <time datetime="{published_iso[:10]}">'
             f"{_display_date(published_iso)}</time>")
    if modified_iso[:10] != published_iso[:10]:
        dates += (f' · Updated <time datetime="{modified_iso[:10]}">'
                  f"{_display_date(modified_iso)}</time>")
    return (
        '\n<div class="page-meta">\n'
        f'<img class="page-meta__avatar" src="{author["avatar"]}" '
        f'alt="{html.escape(author["name"])}">\n'
        f'<a class="page-meta__author" href="{author["url"]}">'
        f'{html.escape(author["name"])}</a>\n'
        f'<span class="page-meta__dates">{dates}</span>\n'
        "</div>"
    )


def on_page_markdown(markdown, page, config, files):
    file = page.file
    if file.abs_src_path is None:  # generated page (tag/blog views)
        return markdown
    src = file.src_uri

    # Resolve the hero image (frontmatter path is relative to the source
    # file's folder) to a site-root-relative path for og:image / schema
    if page.meta.get("image"):
        folder = src.rsplit("/", 1)[0] if "/" in src else ""
        page.meta["image_url"] = (
            f"{folder}/{page.meta['image']}" if folder else page.meta["image"]
        )

    today = datetime.date.today().isoformat()
    created, modified = _git_dates_map().get(f"docs/{src}", (today, today))

    if src.startswith("posts/"):
        # Post publish date comes from frontmatter; git gives the update
        date = page.meta.get("date")
        if isinstance(date, dict):  # blog plugin's date: created: form
            date = date.get("created")
        if hasattr(date, "isoformat"):
            created = date.isoformat()
        page.meta["date_published_iso"] = created
        page.meta["date_modified_iso"] = modified
        page.meta["schema_type"] = "BlogPosting"
        return markdown

    all_srcs = {f.src_uri for f in files.documentation_pages()}
    if not _wants_header(src, all_srcs):
        return markdown

    page.meta["date_published_iso"] = created
    page.meta["date_modified_iso"] = modified
    page.meta["schema_type"] = "Article"

    summary = page.meta.get("summary")
    image = page.meta.get("image")

    lines = markdown.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            inject = []
            if summary:
                inject.append(f'\n<p class="page-summary">{html.escape(summary)}</p>')
            inject.append(_meta_row(created, modified))
            if image:
                alt = line[2:].strip()
                inject.append(
                    f'\n![{alt}]({image})'
                    '{ .page-hero fetchpriority="high" loading="eager" }'
                )
            lines[i + 1:i + 1] = inject
            return "\n".join(lines)
    return markdown
