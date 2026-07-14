"""MkDocs hook: auto-link unlinked section pages from landing pages.

Topic landing index.md pages hand-link their pages with short
descriptions. This hook is the safety net: at build time it appends a
"Pages" list of any page in the section that the landing page doesn't
already link, so new pages are always reachable even if the manual
link was forgotten. Source files are never modified; hand-written
links take precedence. Registered via `hooks:` in mkdocs.yml.
"""
import re
from pathlib import Path

# Sections whose landing pages are generated or special-cased
EXCLUDED_PREFIXES = ("posts/", "author/", "page/", "archive/", "category/", "tags/")


def _title_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else path.stem.replace("-", " ")


def on_page_markdown(markdown, page, config, files):
    src = page.file.src_uri
    if src == "index.md" or not src.endswith("index.md"):
        return markdown
    if src.startswith(EXCLUDED_PREFIXES):
        return markdown

    folder = src[: -len("index.md")]
    missing = []
    for file in files.documentation_pages():
        other = file.src_uri
        if other == src or not other.startswith(folder) or file.abs_src_path is None:
            continue
        rest = other[len(folder):]
        # Direct pages in this folder, plus subsection landing pages
        if "/" in rest and not rest.endswith("/index.md"):
            continue
        if rest in markdown:  # already linked (or mentioned) by hand
            continue
        missing.append((rest, _title_of(Path(file.abs_src_path))))

    if not missing:
        return markdown
    listing = "\n".join(f"- [{title}]({rest})" for rest, title in sorted(missing))
    return f"{markdown.rstrip()}\n\n## Pages\n\n{listing}\n"
