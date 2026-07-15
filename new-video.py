#!/usr/bin/env python3
"""Create a video summary page under docs/videos/ from a YouTube URL.

Fetches the video's subtitles with yt-dlp, has Claude write a factual title
and summary, and generates a page with the video embedded and the summary below it.
The videos landing page lists its pages automatically (article cards
rendered by overrides/main.html), so no index update is needed.

Usage:
    python new-video.py <youtube-url> [tag ...]

Tags are optional; if omitted, Claude suggests 1-3 based on the
transcript, preferring tags already used on the site.

Requires yt-dlp (pip install yt-dlp) and the claude CLI on PATH.
"""

import argparse
import datetime
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yt_dlp


DEFAULT_MODEL = "claude-haiku-4-5-20251001"

ROOT = Path(__file__).resolve().parent
VIDEOS_DIR = ROOT / "docs" / "videos"
DOCS_DIR = ROOT / "docs"

DELIMITERS = (
    "===TITLE===",
    "===DESCRIPTION===",
    "===TAGS===",
    "===SUMMARY===",
    "===KEY POINTS===",
)


def get_video_info(url: str) -> dict:
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
        try:
            return ydl.extract_info(url, download=False)
        except yt_dlp.utils.DownloadError as e:
            sys.exit(f"Error fetching video info: {e}")


def extract_subtitles(url: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        opts = {
            "quiet": True,
            "no_warnings": True,
            "writeautomaticsub": True,
            "writesubtitles": True,
            "subtitleslangs": ["en"],
            "subtitlesformat": "vtt",
            "skip_download": True,
            "outtmpl": str(Path(tmpdir) / "subs.%(ext)s"),
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                ydl.download([url])
            except yt_dlp.utils.DownloadError as e:
                sys.exit(f"Error downloading subtitles: {e}")

        vtt_files = list(Path(tmpdir).glob("*.vtt"))

        if not vtt_files:
            sys.exit("No English subtitles found for this video.")

        return clean_vtt(vtt_files[0].read_text(encoding="utf-8"))


def clean_vtt(vtt_text: str) -> str:
    """Strip VTT timestamps/headers and deduplicate lines."""

    seen = set()
    cleaned = []

    for line in vtt_text.splitlines():
        line = line.strip()

        if (
            not line
            or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE"))
            or "-->" in line
            or line.isdigit()
        ):
            continue

        line = re.sub(r"<[^>]+>", "", line).strip()

        if line and line not in seen:
            seen.add(line)
            cleaned.append(line)

    return " ".join(cleaned)


def existing_tags() -> list[str]:
    """Collect tags already used in frontmatter across the site."""

    tags = set()

    for md in DOCS_DIR.rglob("*.md"):
        text = md.read_text(encoding="utf-8")

        match = re.match(r"\A---\n(.*?)\n---", text, re.DOTALL)

        if not match:
            continue

        in_tags = False

        for line in match.group(1).splitlines():

            if re.match(r"^(tags|categories):\s*$", line):
                in_tags = True

            elif in_tags and (m := re.match(r"^\s+-\s+(\S+)", line)):
                tags.add(m.group(1))

            elif not line.startswith(" "):
                in_tags = False

    return sorted(tags)


def existing_page_for(video_id: str) -> Path | None:
    """Find a page already embedding this video, regardless of its title."""

    for md in VIDEOS_DIR.glob("*.md"):
        if f"embed/{video_id}" in md.read_text(encoding="utf-8"):
            return md

    return None


def summarize_with_claude(
    youtube_title: str,
    channel: str,
    subtitles: str,
    model: str,
) -> dict:

    tag_list = ", ".join(existing_tags()) or "(none yet)"

    prompt = f"""
You are writing a summary page for a personal knowledge site.

The original YouTube title is:
"{youtube_title}"

Channel:
"{channel}"

Important:
The YouTube title may be clickbait, exaggerated, vague, or designed
to get clicks. Do NOT copy it blindly.

Your job is to understand the actual video content from the subtitles
and create an accurate description of what the video is about.

Writing style:
- matter-of-fact
- plain language
- like explaining the video to a friend
- no hype
- no marketing language
- no exclamation marks
- no rhetorical questions

Only include information actually present in the subtitles.

Output EXACTLY these five sections, each starting with its delimiter
on its own line, with no other text before or after:

===TITLE===
A short accurate title (5-12 words) describing what the video is actually
about.

Write this like telling a friend what the video covers.

Good examples:
- How compost improves soil health
- Building a small home hydroponic system
- The history of reusable rockets

Bad examples:
- You won't believe this discovery
- This changes everything
- The shocking truth about farming

===DESCRIPTION===
One factual sentence, max 150 characters, saying what the video covers.

===TAGS===
1 to 3 lowercase kebab-case topic tags, one per line.

Prefer tags from this existing list when they fit:
{tag_list}

===SUMMARY===
A short paragraph (3-5 sentences) summarising the actual content.

===KEY POINTS===
A markdown bullet list of the key points and takeaways.

--- SUBTITLES ---
{subtitles}
--- END SUBTITLES ---
"""

    result = subprocess.run(
        ["claude", "-p", "--model", model],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",   # Windows defaults to cp1252, garbling em dashes etc.
    )

    if result.returncode != 0:
        sys.exit(f"Error calling Claude: {result.stderr}")

    return parse_sections(result.stdout.strip())


def parse_sections(text: str) -> dict:

    pattern = "|".join(re.escape(d) for d in DELIMITERS)

    parts = re.split(f"({pattern})", text)

    sections = {}

    for i, part in enumerate(parts):

        if part in DELIMITERS:

            key = part.strip("=").lower().replace(" ", "_")

            sections[key] = (
                parts[i + 1].strip()
                if i + 1 < len(parts)
                else ""
            )

    missing = [
        d
        for d in ("title", "description", "summary", "key_points")
        if not sections.get(d)
    ]

    if missing:
        sys.exit(
            f"Claude output missing sections: {missing}\n\n{text}"
        )

    return sections


def slugify(title: str, max_len: int = 60) -> str:

    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        title.lower()
    ).strip("-")

    if len(slug) > max_len:
        slug = slug[:max_len].rsplit("-", 1)[0]

    return slug


def yaml_quote(text: str) -> str:

    return (
        '"'
        + text.replace("\\", "\\\\")
        .replace('"', '\\"')
        + '"'
    )


def build_page(
    info: dict,
    sections: dict,
    tags: list[str],
) -> str:

    title = sections["title"]

    video_id = info["id"]

    channel = (
        info.get("uploader", "")
        or info.get("channel", "")
    )

    upload = info.get("upload_date", "")

    date_pretty = ""

    if upload:
        d = datetime.datetime.strptime(
            upload,
            "%Y%m%d",
        ).date()

        date_pretty = (
            f"{d.day} {d.strftime('%B %Y')}"
        )

    tag_lines = "\n".join(
        f"  - {t}"
        for t in ["videos", *tags]
    )

    esc_title = title.replace('"', "&quot;")

    source_bits = " — ".join(
        x for x in [channel, date_pretty]
        if x
    )

    return f"""---
description: {yaml_quote(sections["description"])}
tags:
{tag_lines}
---

# {title}

## Summary

{sections["summary"]}

<iframe src="https://www.youtube-nocookie.com/embed/{video_id}"
        title="{esc_title}"
        allowfullscreen
        style="width:100%;aspect-ratio:16/9;border:0;"></iframe>

[Watch on YouTube](https://www.youtube.com/watch?v={video_id}){f" — {source_bits}" if source_bits else ""}.

## Key points

{sections["key_points"]}

*Summary generated by AI from the video's subtitles.*
"""


def main():

    parser = argparse.ArgumentParser(
        description="Create a video summary page under docs/videos/."
    )

    parser.add_argument(
        "url",
        help="YouTube video URL",
    )

    parser.add_argument(
        "tags",
        nargs="*",
        help="topic tags (default: Claude suggests)",
    )

    parser.add_argument(
        "-m",
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )

    args = parser.parse_args()

    print("Fetching video info...", file=sys.stderr)

    info = get_video_info(args.url)

    youtube_title = info.get(
        "title",
        "Unknown Title",
    )

    print(
        f"YouTube title: {youtube_title}",
        file=sys.stderr,
    )

    existing = existing_page_for(info["id"])

    if existing:
        sys.exit(f"A page for this video already exists: {existing}")

    print(
        "Extracting subtitles...",
        file=sys.stderr,
    )

    subtitles = extract_subtitles(args.url)

    if len(subtitles) < 50:
        sys.exit(
            "Subtitles too short or empty — video may not have usable captions."
        )

    max_chars = 100_000

    if len(subtitles) > max_chars:
        subtitles = subtitles[:max_chars]

        print(
            f"Transcript truncated to {max_chars} characters.",
            file=sys.stderr,
        )

    channel = (
        info.get("uploader", "")
        or info.get("channel", "")
    )

    print(
        f"Summarizing with Claude ({args.model})...",
        file=sys.stderr,
    )

    sections = summarize_with_claude(
        youtube_title,
        channel,
        subtitles,
        args.model,
    )

    page_title = sections["title"]

    slug = slugify(page_title)

    path = VIDEOS_DIR / f"{slug}.md"

    if path.exists():
        sys.exit(f"Already exists: {path}")

    tags = args.tags or [
        t.strip().lstrip("-").strip()
        for t in sections.get("tags", "").splitlines()
        if t.strip()
    ][:3]

    path.write_text(
        build_page(info, sections, tags),
        encoding="utf-8",
        newline="\n",
    )

    print(f"Created: {path}")
    print(
        "Run: mkdocs build --strict"
    )


if __name__ == "__main__":
    main()