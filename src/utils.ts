import { getCollection, type CollectionEntry } from 'astro:content';

export type Post = CollectionEntry<'blog'>;

// Turn a display name ("Procedural Generation") into a URL slug ("procedural-generation").
export function slugify(s: string): string {
  return s
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// All published posts, newest first.
export async function getPublishedPosts(): Promise<Post[]> {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return posts.sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf(),
  );
}

// { displayName, slug, count } for every category, by post count.
export async function getCategories() {
  const posts = await getPublishedPosts();
  const map = new Map<string, { name: string; count: number }>();
  for (const p of posts) {
    const name = p.data.category;
    const key = slugify(name);
    const e = map.get(key) ?? { name, count: 0 };
    e.count++;
    map.set(key, e);
  }
  return [...map.entries()]
    .map(([slug, v]) => ({ slug, name: v.name, count: v.count }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
}

// { displayName, slug, count } for every tag, by post count.
export async function getTags() {
  const posts = await getPublishedPosts();
  const map = new Map<string, { name: string; count: number }>();
  for (const p of posts) {
    for (const name of p.data.tags) {
      const key = slugify(name);
      const e = map.get(key) ?? { name, count: 0 };
      e.count++;
      map.set(key, e);
    }
  }
  return [...map.entries()]
    .map(([slug, v]) => ({ slug, name: v.name, count: v.count }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
}
