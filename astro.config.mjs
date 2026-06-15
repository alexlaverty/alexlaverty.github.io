// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// alexlaverty.github.io is a *user* GitHub Pages site, so it is served from the
// domain root — no `base` path needed.
export default defineConfig({
  site: 'https://alexlaverty.github.io',
  integrations: [sitemap()],
  markdown: {
    shikiConfig: {
      // Warm, low-contrast theme that fits the cosy palette.
      theme: 'rose-pine-dawn',
      wrap: true,
    },
  },
});
