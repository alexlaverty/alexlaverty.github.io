#!/usr/bin/env python3
"""Create today's daily log post under docs/posts/.

Usage:
    python new-daily.py [category ...]

Categories are optional and should match top-level topic folder names
under docs/ (e.g. permaculture, ai-coding). If today's post already
exists, prints its path and exits without touching it.
"""
import sys
from datetime import date
from pathlib import Path

POSTS_DIR = Path(__file__).resolve().parent / "docs" / "posts"


def main() -> None:
    today = date.today()
    path = POSTS_DIR / f"{today.isoformat()}.md"
    if path.exists():
        print(f"Already exists: {path}")
        return

    lines = [
        "---",
        f"date: {today.isoformat()}",
        "authors:",
        "  - alex",
    ]
    categories = sys.argv[1:]
    if categories:
        lines.append("categories:")
        lines.extend(f"  - {c}" for c in categories)
    lines += [
        "---",
        "",
        f"# {today.day} {today.strftime('%B %Y')}",
        "",
        "",
    ]

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"Created: {path}")


if __name__ == "__main__":
    main()
