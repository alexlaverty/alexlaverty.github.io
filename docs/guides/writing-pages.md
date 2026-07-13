# Writing pages

A tour of the Markdown features enabled on this site. View this page's
source in `docs/guides/writing-pages.md` to see how each one is written.

## Headings and the anchor menu

Every `##` and `###` heading on a page appears in the right-hand anchor
menu automatically, and each heading gets a clickable ¶ permalink.

## Code blocks

Fenced code blocks get syntax highlighting and a copy button:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("world"))
```

## Admonitions

Callout boxes for notes, tips, and warnings:

!!! note
    This is a note admonition.

!!! tip
    This is a tip. There are also `warning`, `danger`, `info`, and more.

??? question "Collapsible admonition (click to expand)"
    Use `???` instead of `!!!` to make it collapsible.

## Content tabs

=== "Windows"

    ```powershell
    pip install -r requirements.txt
    ```

=== "Linux / macOS"

    ```bash
    pip3 install -r requirements.txt
    ```

## Tables

| Feature        | Where it shows up                     |
| -------------- | ------------------------------------- |
| Folders        | Collapsible left sidebar sections     |
| Page headings  | Right sidebar anchor menu             |

## Task lists

- [x] Set up MkDocs
- [x] Configure GitHub Actions deploy
- [ ] Write more content
