import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Blog posts live as Markdown in src/content/blog/. The file name (without the
// .md) is the post id / URL slug, and must match the slug in src/series.ts.
const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    // One broad category per post; many specific tags.
    category: z.string().default('Uncategorised'),
    tags: z.array(z.string()).default([]),
    // Hero image (optional) lives in /public and is referenced by absolute path.
    heroImage: z.string().optional(),
    heroAlt: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
