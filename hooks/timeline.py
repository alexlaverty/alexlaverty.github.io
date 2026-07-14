"""MkDocs hook: unified home page timeline with pagination.

Merges blog posts (by publish date) and content pages (by last git
commit date) into one newest-first list, exposed to templates as the
`timeline` global. overrides/blog.html renders ten entries per page:
the first ten on the home page, the rest on generated /page/N/ pages.
Registered via `hooks:` in mkdocs.yml.
"""
import datetime
import re
import subprocess
from pathlib import Path

from mkdocs.structure.files import File, InclusionLevel

PER_PAGE = 10
ROOT = Path(__file__).resolve().parent.parent

PAGE_TEMPLATE = """---
title: Page {n}
template: blog.html
timeline_page: {n}
search:
  exclude: true
---
"""

# Structural pages and generated views that don't belong in the timeline
EXCLUDED_PREFIXES = ("posts/", "author/", "page/", "archive/", "category/", "tags/")
EXCLUDED_PAGES = ("index.md", "tags.md")


def _sources(files) -> set[str]:
    return {f.src_uri for f in files.documentation_pages()}


def _eligible(src: str, all_srcs: set[str]) -> bool:
    """Content pages only. A folder's landing index.md is excluded unless
    the folder has no other pages (then the index IS the content page)."""
    if src.startswith(EXCLUDED_PREFIXES) or src in EXCLUDED_PAGES:
        return False
    if src.endswith("index.md"):
        folder = src[: -len("index.md")]
        # Top-level index.md is always a topic landing page
        if folder.count("/") <= 1:
            return False
        return not any(
            s != src and s.startswith(folder) for s in all_srcs
        )
    return True


def _git_dates() -> dict[str, int]:
    """Last commit timestamp per repo-relative path, one git call."""
    result = subprocess.run(
        ["git", "log", "--format=%x00%ct", "--name-only", "--", "docs"],
        capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
    )
    dates: dict[str, int] = {}
    ts = 0
    for line in result.stdout.splitlines():
        if line.startswith("\x00"):
            ts = int(line[1:])
        elif line.strip():
            dates.setdefault(line.strip(), ts)
    return dates


def _frontmatter(text: str) -> str:
    match = re.match(r"\A---\n(.*?)\n---", text, re.DOTALL)
    return match.group(1) if match else ""


def _post_date(text: str) -> datetime.datetime | None:
    match = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", _frontmatter(text), re.MULTILINE)
    if match:
        return datetime.datetime.strptime(match.group(1), "%Y-%m-%d")
    return None


def _snippet(text: str, max_words: int = 40) -> str:
    """Meta description if present, else the first body paragraph as
    plain text."""
    meta = _frontmatter(text)
    match = re.search(r"^description:\s*(.+)$", meta, re.MULTILINE)
    if match:
        return match.group(1).strip().strip('"')

    body = re.sub(r"\A---\n.*?\n---", "", text, flags=re.DOTALL)
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        # Skip headings, embeds, images, and other non-prose blocks
        if not block or block.startswith(("#", "<", "!", "-", "*", "|", "```")):
            continue
        block = re.sub(r"\[([^]]*)\]\([^)]*\)", r"\1", block)   # links -> text
        block = re.sub(r"[*_`]", "", block)
        words = block.split()
        if len(words) > max_words:
            return " ".join(words[:max_words]) + " …"
        return " ".join(words)
    return ""


def on_files(files, config):
    srcs = _sources(files)
    total = sum(
        1 for s in srcs if s.startswith("posts/") or _eligible(s, srcs)
    )
    for n in range(2, (total + PER_PAGE - 1) // PER_PAGE + 1):
        page = File.generated(config, f"page/{n}.md",
                              content=PAGE_TEMPLATE.format(n=n))
        page.inclusion = InclusionLevel.NOT_IN_NAV
        files.append(page)
    return files


def on_env(env, config, files):
    git_dates = _git_dates()
    srcs = _sources(files)
    docs_dir = Path(config["docs_dir"])
    entries = []

    for file in files.documentation_pages():
        # Generated files (tag pages, blog views, /page/N/) have no
        # source path and never belong in the timeline
        if file.page is None or file.abs_src_path is None:
            continue
        src = file.src_uri
        path = Path(file.abs_src_path)

        if src.startswith("posts/"):
            kind = "post"
            date = _post_date(path.read_text(encoding="utf-8"))
            if date is None:
                date = datetime.datetime.fromtimestamp(path.stat().st_mtime)
        elif _eligible(src, srcs) and path.is_relative_to(docs_dir):
            kind = "page"
            ts = git_dates.get(f"docs/{src}") or int(path.stat().st_mtime)
            date = datetime.datetime.fromtimestamp(ts)
        else:
            continue

        text = path.read_text(encoding="utf-8")
        entries.append({
            "kind": kind,
            "title": file.page.title,
            "url": file.page.url,
            "ts": date.timestamp(),
            "date": f"{date.strftime('%B')} {date.day}, {date.year}",
            "text": _snippet(text),
        })

    entries.sort(key=lambda e: -e["ts"])
    env.globals["timeline"] = entries
    env.globals["timeline_per_page"] = PER_PAGE
    return env
