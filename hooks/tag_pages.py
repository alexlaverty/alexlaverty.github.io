"""MkDocs hook: a listing page per tag, and a tag index ordered by count.

Generates tags/<tag>.md for every tag found in page frontmatter, each
containing a scoped Material tags listing (only that tag's pages). The
pages are kept out of the left sidebar nav. Also replaces the
<!-- tag-index --> marker on tags.md with all tags ordered by page
count. Registered via `hooks:` in mkdocs.yml.
"""
import re
from pathlib import Path

from mkdocs.structure.files import File, InclusionLevel

_counts: dict[str, int] = {}

PAGE_TEMPLATE = """---
description: All pages on this site tagged {tag}.
robots: noindex, follow
search:
  exclude: true
---

# Tag: {tag}

<!-- material/tags {{ include: [{tag}], toc: false }} -->
"""


def _tags_of(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return []
    tags = []
    in_tags = False
    for line in match.group(1).splitlines():
        if re.match(r"^tags:\s*$", line):
            in_tags = True
        elif in_tags and (m := re.match(r"^\s+-\s+(\S+)", line)):
            tags.append(m.group(1))
        elif not line.startswith(" "):
            in_tags = False
    return tags


def on_files(files, config):
    _counts.clear()
    for file in list(files.documentation_pages()):
        for tag in _tags_of(Path(file.abs_src_path)):
            _counts[tag] = _counts.get(tag, 0) + 1

    for tag in _counts:
        page = File.generated(config, f"tags/{tag}.md",
                              content=PAGE_TEMPLATE.format(tag=tag))
        page.inclusion = InclusionLevel.NOT_IN_NAV
        files.append(page)
    return files


def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri != "tags.md":
        return markdown
    ordered = sorted(_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    index = "\n".join(
        f"- [{tag}](tags/{tag}.md) — {n} page{'s' if n != 1 else ''}"
        for tag, n in ordered
    )
    return markdown.replace("<!-- tag-index -->", index)
