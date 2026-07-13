# Markdown cheatsheet

Quick reference for common Markdown syntax.

## Text formatting

```markdown
**bold**  *italic*  `inline code`  ~~strikethrough~~
```

**bold**  *italic*  `inline code`  ~~strikethrough~~

## Links and images

```markdown
[Link text](https://example.com)
[Link to another page](../guides/getting-started.md)
![Alt text](../assets/image.png)
```

Relative links between `.md` files are checked at build time, so broken
internal links fail the build instead of going live.

## Lists

```markdown
- Unordered item
    - Nested item (indent 4 spaces)

1. Ordered item
2. Another item
```

## Blockquotes

```markdown
> Quoted text.
```

> Quoted text.

## Horizontal rule

```markdown
---
```
