// The master plan for the whole series. This is the single source of truth for
// ordering and grouping. A post becomes a live link the moment a matching
// Markdown file (id === slug) lands in src/content/blog/; until then it renders
// as "coming soon". That lets us publish one post at a time without dead links.

export type SeriesItem = {
  num: number;
  slug: string;
  title: string;
  blurb: string;
};

export type SeriesSection = {
  section: string;
  items: SeriesItem[];
};

export const SERIES: SeriesSection[] = [
  {
    section: 'Start here',
    items: [
      {
        num: 1,
        slug: 'welcome-how-i-built-a-world-in-code',
        title: 'Procedurally Generated VR Worlds, Built with Claude Code',
        blurb:
          'What the project is, why it is generated from code, and an index of the posts that explain each part.',
      },
    ],
  },
  {
    section: 'Foundations',
    items: [
      {
        num: 2,
        slug: 'terrain-from-perlin-noise',
        title: 'Mountains from Noise',
        blurb:
          'How a grid of smooth random numbers — Perlin noise — turns into rolling hills, valleys and peaks.',
      },
      {
        num: 3,
        slug: 'biomes-with-voronoi',
        title: 'Painting the Land: Biomes with Voronoi',
        blurb:
          'Scattering seed points and letting "nearest one wins" carve the world into meadows, forests, deserts and snow.',
      },
    ],
  },
  {
    section: 'Water & shaping the land',
    items: [
      {
        num: 4,
        slug: 'how-rivers-find-their-way',
        title: 'How Rivers Find Their Way',
        blurb:
          'Simulating water flowing downhill — filling in pits, merging streams into rivers, and spilling over waterfalls.',
      },
      {
        num: 5,
        slug: 'roads-that-follow-the-land',
        title: 'Roads a Car Could Actually Drive',
        blurb:
          'Connecting the houses with paths that hug the contours instead of charging straight up cliffs.',
      },
      {
        num: 6,
        slug: 'making-water-look-wet',
        title: 'Making Water Look Wet',
        blurb:
          'The little shader tricks — ripples, reflections and depth — that make a flat blue plane read as an ocean.',
      },
    ],
  },
  {
    section: 'The living world',
    items: [
      {
        num: 7,
        slug: 'building-a-bird-from-boxes',
        title: 'Building a Bird from Boxes',
        blurb:
          'A flying bird with flapping wings, assembled from a few simple shapes and a bit of banking.',
      },
      {
        num: 8,
        slug: 'butterflies-that-wander',
        title: 'Butterflies That Wander',
        blurb:
          'Gentle, ground-hugging drift and the occasional rest — the small touches that make a meadow feel alive.',
      },
      {
        num: 9,
        slug: 'fish-that-flock',
        title: 'Schools of Fish That Think as One',
        blurb:
          'The famous "boids" rules: three simple instincts that add up to a shimmering, swirling school.',
      },
      {
        num: 10,
        slug: 'cottages-from-scratch',
        title: 'Cottages from Scratch',
        blurb:
          'Endless cosy houses from a handful of dials — walls, parametric roofs, and windows that glow at night.',
      },
    ],
  },
  {
    section: 'Atmosphere & polish',
    items: [
      {
        num: 11,
        slug: 'a-field-of-grass',
        title: 'A Field of Grass Without Melting Your GPU',
        blurb:
          'Drawing a hillside of thousands of grass blades in a single go, and only where the player can see.',
      },
      {
        num: 12,
        slug: 'wind-you-can-see',
        title: 'Wind You Can See',
        blurb:
          'Making grass and trees sway by turning position and time into motion — all on the graphics card.',
      },
      {
        num: 13,
        slug: 'golden-hour-on-demand',
        title: 'Golden Hour on Demand',
        blurb:
          'Day, dusk and pitch-black night — with fog, god-rays, stars and the occasional aurora.',
      },
      {
        num: 14,
        slug: 'light-in-the-dark',
        title: 'Light in the Dark',
        blurb:
          'Warm lamp posts, drifting fireflies and glowing windows: how the world stays cosy after sunset.',
      },
      {
        num: 15,
        slug: 'music-thats-never-the-same',
        title: "Music That's Never the Same Twice",
        blurb:
          'Gentle ambient music invented on the fly — and the reason it can never quite hit a wrong note.',
      },
    ],
  },
  {
    section: 'Wrap-up',
    items: [
      {
        num: 16,
        slug: 'designing-for-wonder',
        title: 'Make It Beautiful',
        blurb:
          'The one rule behind every decision in the project: when in doubt, choose the prettier option.',
      },
      {
        num: 17,
        slug: 'walking-your-world-in-vr',
        title: 'Walking Your Own World in VR',
        blurb:
          'Stepping inside the world on a Meta Quest 2 — comfortable movement, teleporting, and learning to fly.',
      },
    ],
  },
];

// Flat, ordered list — handy for prev/next links and lookups.
export const SERIES_FLAT: SeriesItem[] = SERIES.flatMap((s) => s.items);
