---
description: yts is a Python CLI tool that summarizes YouTube videos by downloading subtitles with yt-dlp and sending the transcript to Claude.
tags:
  - ai-coding
  - python
  - automation
summary: "yts is a Python command-line tool that summarizes YouTube videos by downloading their subtitles with yt-dlp and sending the transcript to Claude. The tool returns a summary paragraph that answers the video's title directly, then lists key points—a format that cuts through clickbait titles."
---

# Summarize YouTube videos with yt-dlp and Claude

yts is a small Python command-line tool I wrote that summarizes a
YouTube video without watching it. It downloads the video's subtitles
with yt-dlp, cleans them into plain text, and sends them to the Claude
CLI, which returns a short paragraph answering the video's title plus
a bullet list of key points. The whole thing is one file, about 170
lines. Source is at
[github.com/alexlaverty/yts](https://github.com/alexlaverty/yts).

The point of the summary format is dealing with clickbait titles. The
prompt tells Claude to first answer the title directly — if the video
is called "The one mistake killing your tomatoes", the first paragraph
of the summary states what the mistake actually is — and only then
list the takeaways.

## How it works

The script runs a five-step pipeline:

1. **Fetch metadata.** The yt-dlp Python API (`extract_info` with
   `download=False`) returns the video title and ID without
   downloading anything.
2. **Download subtitles.** A second yt-dlp call with
   `writesubtitles`, `writeautomaticsub`, and `skip_download` grabs
   English subtitles in WebVTT format into a temporary directory.
   Auto-generated captions are accepted, so it works on most videos,
   not just ones with hand-made subtitles.
3. **Clean the VTT.** Headers, timestamp lines, and inline tags are
   stripped, and duplicate lines are removed, leaving plain text.
4. **Save the transcript.** The cleaned text goes to
   `transcripts/<video-id>.txt` with the title, URL, and date at the
   top, so transcripts can be reused or searched later without
   re-downloading.
5. **Summarize.** The title and transcript are wrapped in a prompt and
   piped to `claude -p`, and the response prints to stdout.

Status messages go to stderr and only the summary goes to stdout, so
the output can be redirected to a file cleanly.

## Cleaning WebVTT captions

The cleanup step does more work than it looks like. YouTube's
auto-generated captions arrive as rolling cues: each caption block
repeats the previous line while the next one appears, so a naive
extraction produces every sentence two or three times. The script
handles this by keeping a set of lines already seen and dropping
repeats. It also strips the inline word-timing tags
(`<00:01:02.345>`, `<c>...</c>`) that YouTube embeds inside
auto-caption text, using a regex over each line.

The trade-off of set-based deduplication is that a line legitimately
said twice in the video is kept only once. For summarization that
loses nothing.

## Calling Claude from a script

The summary comes from the Claude Code CLI running in non-interactive
mode: `claude -p` reads a prompt, prints the response, and exits,
which makes it usable as a Unix-style text filter from any script. The
prompt is passed via stdin rather than as a command-line argument
because transcripts run to tens of thousands of characters and Windows
caps command-line length; stdin has no such limit (the CLI accepts
piped input up to 10 MB).

The default model is Haiku (`claude-haiku-4-5-20251001`), which is
cheap and fast and entirely adequate for "what does this video say".
A `-m`/`--model` flag switches models for videos worth a more careful
pass. Transcripts over 100,000 characters are truncated before
sending to stay under context limits — at roughly 150 words a minute
of speech that covers a couple of hours of video.

## Usage

Requirements are Python 3, `yt-dlp` (the only entry in
`requirements.txt`), and the Claude Code CLI installed and
authenticated.

```bash
pip install yt-dlp
python yts.py https://www.youtube.com/watch?v=lACQknq4sFI
python yts.py <url> -m claude-sonnet-5   # bigger model
```

Progress lines appear on stderr, then the summary:

```text
Fetching video info...
Title: The Memory of Mankind and what should be remembered?
Extracting subtitles...
Transcript saved: transcripts/lACQknq4sFI.txt
Summarizing with Claude (claude-haiku-4-5-20251001)...
```

## Limitations

- English subtitles only; the script exits if the video has neither
  manual nor auto-generated English captions.
- The summary is only as good as the captions. Auto-generated captions
  mangle names and technical terms, and carry no punctuation, though
  Claude copes with that better than expected.
- Anything shown on screen but not spoken — code, diagrams, slides —
  is invisible to the summary.

This same yt-dlp-plus-Claude approach generates the pages in this
site's [video summaries](../videos/index.md) section: the site's
`new-video.py` script uses the identical pipeline but writes a
formatted MkDocs page with the video embedded instead of printing to
the terminal.

## Sources

- [yts on GitHub](https://github.com/alexlaverty/yts) — source code
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — subtitle download options (`--write-auto-subs`, `--skip-download`)
- [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) — `claude -p` non-interactive mode and stdin piping
