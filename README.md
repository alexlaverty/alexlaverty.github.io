# How I Built a World in Code

The source for [alexlaverty.github.io](https://alexlaverty.github.io) — a blog
series on the procedural-generation techniques behind a cosy, procedurally
generated VR world for the Meta Quest 2, built in Godot with Claude Code.

Built with [Astro](https://astro.build) and deployed to GitHub Pages.

## Develop

```sh
npm install
npm run dev      # local dev server at http://localhost:4321
npm run build    # production build into dist/
npm run preview  # preview the production build
```

## Writing a post

1. Add a Markdown file to `src/content/blog/`. The file name (without `.md`) is
   the URL slug and **must match the matching `slug` in `src/series.ts`**.
2. Give it frontmatter: `title`, `description`, `pubDate` (see an existing post).
3. That's it — the post automatically becomes a live link on the homepage and in
   the series, and gets prev/next navigation. Until a post's file exists, the
   series shows it as "coming soon".

`src/series.ts` is the master plan: the full ordered list of all 17 posts,
grouped into sections. Edit it to change ordering, titles or blurbs.

## Deployment

Every push to `main` triggers `.github/workflows/deploy.yml`, which builds the
site and publishes it to GitHub Pages. Make sure the repo's
**Settings → Pages → Source** is set to **GitHub Actions**.
