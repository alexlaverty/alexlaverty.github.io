---
title: 'Painting the Land: Biomes with Voronoi'
description: >-
  Scattering a few seed points and assigning every spot to its nearest one — a
  Voronoi diagram — divides the map into biomes, with soft edges so they don't
  seam.
pubDate: 2026-06-18
category: 'Procedural'
tags: ['procedural generation', 'godot', 'voronoi', 'biomes']
heroAlt: 'A landscape showing a green meadow region meeting a sandy desert region.'
---

A world that's all one kind of ground gets boring quickly. Real landscapes have
regions: grassland here, forest there, desert further on. In this project those
regions are called biomes, and there are six — Meadow, Forest, Taiga, Swamp,
Desert, Snow. The question is how to divide the map up between them without it
looking arbitrary.

## Voronoi: nearest point wins

The method is a Voronoi diagram, which is simpler than the name suggests.

Scatter a handful of points on the map. Call them seeds. Now, for any spot on the
ground, find which seed is closest. That spot belongs to that seed's region.
Every spot gets assigned to its nearest seed, and the map naturally divides into
patches — one patch around each seed.

You see this pattern constantly in the real world. If you mark every town on a
map and ask "which town is closest from here," the country splits into territories
with straight-ish borders between neighbours. That's a Voronoi diagram. Mobile
phone coverage, the cells in a giraffe's coat, and the cracks in dried mud all
have the same structure.

<div class="shot">SCREENSHOT: the in-game minimap, which tints the terrain by biome — good for showing the patchwork of regions. Or an aerial view across two or three biomes.</div>

Each seed is given a biome type, so the patch around it becomes that biome:

```gdscript
# scatter `count` seeds, each tagged with a biome type
for k in range(count):
    seeds.append(Vector2(rng.randf_range(-inner, inner),
                         rng.randf_range(-inner, inner)))
    types.append(biome_types[k])

# the biome at any point is just the nearest seed's type
func nearest(p):
    # ...scan the seeds, keep the closest one
```

The number of seeds is configurable, so a world can have a few large biomes or
many smaller ones. The seeds are pulled toward the centre of the map rather than
the corners, since the corners are mostly ocean and would waste a region.

## What a biome actually changes

A biome here isn't a different set of plants and rocks — it's the same world
sampled differently. Each biome adjusts three things:

- **Ground colour.** A tint multiplied into the terrain — yellow-green for
  meadow, blue-grey for taiga, warm sand for desert, bright white for snow.
- **Terrain shape.** Small nudges to the relief and flatness from the previous
  post, so a swamp sits low and flat while a desert can be more rugged.
- **Vegetation density.** Each biome has a weight for every plant category.
  Desert grass weight is near zero; forest broadleaf weight is high. The
  scattering system reads these weights, so forests come out lush and deserts
  bare without any special-casing.

That's enough for regions to read clearly as you walk between them, even though
they're built from the same handful of generic assets.

## Avoiding the seam

Plain Voronoi has hard borders: step across the line between two seeds and the
ground colour would change instantly. That looks wrong.

The fix is to blend near the borders. For any point, the generator finds the
*two* closest seeds, not just one, and measures how much closer the nearest is.
Deep inside a region the nearest seed wins outright. Near a border the two are
almost tied, so the colour, shape and vegetation are mixed between them across a
narrow band. The result is a soft transition instead of a cut line.

```gdscript
# how far into a region we are: 0 on the border, 1 deep inside
var edge = (dist_second - dist_first) / (dist_second + dist_first)
var weight = 0.5 + 0.5 * smoothstep(0.0, blend, edge)
# then lerp colour/shape/veg between the two biomes by `weight`
```

So the whole biome system is really two ideas: nearest-seed assignment to carve
the map into regions, and a two-nearest blend to keep the seams soft.

Next: water. The generator works out where rivers should flow by simulating
water running downhill across the terrain.
