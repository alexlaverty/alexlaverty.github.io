"""MkDocs hook: render summary lede and hero image under the page H1.

Pages with `summary:` frontmatter get it as a lede paragraph directly
below the title; pages with `image:` (set by new-hero.py) get the hero
image below that, giving Title -> Summary -> Hero -> content. The image
also becomes the og:image social preview via overrides/main.html.
Registered via `hooks:` in mkdocs.yml.
"""
import html


def on_page_markdown(markdown, page, config, files):
    summary = page.meta.get("summary")
    image = page.meta.get("image")
    if not summary and not image:
        return markdown

    lines = markdown.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            inject = []
            if summary:
                inject.append(f'\n<p class="page-summary">{html.escape(summary)}</p>')
            if image:
                alt = line[2:].strip()
                inject.append(f"\n![{alt}]({image}){{ .page-hero }}")
            lines[i + 1:i + 1] = inject
            return "\n".join(lines)
    return markdown
