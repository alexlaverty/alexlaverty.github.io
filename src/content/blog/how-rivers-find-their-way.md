---
title: 'How Rivers Find Their Way'
description: >-
  Rivers are placed by simulating water running downhill: filling in pits so
  everything drains to the sea, then tracing flow from the high ground down.
pubDate: 2026-06-21
category: 'Procedural'
tags: ['procedural generation', 'godot', 'algorithms', 'hydrology']
heroAlt: 'A river winding down from high ground, widening as smaller streams join it.'
---

Rivers are one of the more satisfying systems in the project because they aren't
drawn by hand or scattered randomly — they're worked out from the terrain. Given
the heightfield, the generator figures out where water would actually collect and
flow, and puts rivers there. This kind of thing is called hydrology.

The whole approach rests on one rule everyone already knows: water flows
downhill. The challenge is turning that into something a program can follow
across thousands of grid cells.

## The problem with "just flow downhill"

The naive version is: from each point, step to the lowest neighbour, repeat. That
works until water reaches a pit — a low spot with no lower neighbour, like the
bottom of a bowl. Real water fills the bowl until it overflows the lowest part of
the rim, then carries on. The naive algorithm just gets stuck.

Perlin noise terrain is full of little pits like this. So before tracing any
rivers, the generator has to deal with them.

## Step one: fill the pits

The technique is called priority flood. The idea:

Start from the edges of the map — those drain to the sea. Work inward, always
processing the lowest unvisited cell next. When you reach a cell, you record that
its water leaves toward the cell you arrived from, and you raise its recorded
level to at least the level of where the water would have to spill. Pits get
"filled" up to their spill height, exactly like a bowl filling until it overflows.

Processing the lowest cell first is the important part. To do that efficiently the
generator keeps the frontier cells in a priority queue (a min-heap), which always
hands back the lowest one next. After this pass, two things are known for every
cell: a filled surface with no more stuck pits, and a pointer to where its water
goes next — its downstream cell. Follow those pointers from anywhere and you
reach the sea.

<div class="shot">SCREENSHOT: a river system seen from above or a high angle, showing several streams joining into a larger river heading to the coast.</div>

## Step two: trace the rivers

Now the generator picks a handful of starting points up in the high ground —
headwaters. From each, it follows the downstream pointers cell by cell, all the
way to the sea, adding one unit of "flow" to every cell it passes.

The nice consequence falls out for free: where two headwater streams happen to
merge onto the same path, that shared path has been walked twice, so its flow is
higher. River width is tied to flow, so the channel widens below each
confluence. Small streams up top, a broad river near the mouth — without any rule
that says so explicitly. It's just a count of how many sources drain through each
cell.

```gdscript
for source in sources:
    var c := source
    while c >= 0:
        accum[c] += 1.0            # one more source drains through here
        if filled[c] <= sea: break # reached the ocean
        c = downstream[c]          # step to the next cell downhill
```

## Carving, lakes and waterfalls

With flow known, three more things follow from the same data:

- **The channel** is carved into the terrain mesh by lowering the cells along
  each river, wider where flow is higher.
- **Lakes** are the filled pits that didn't fully drain — basins above a certain
  size are flattened to a water level and get a flat water surface.
- **Waterfalls** are simply river stretches where the drop is steep. The
  generator already knows each cell's height and its downstream cell's height; if
  that drop over that distance exceeds a threshold, the stretch is flagged as a
  waterfall and rendered as a falling sheet with spray.

Roads, buildings, ponds and scattered plants all check the river and lake maps so
they don't end up underwater — except roads, which are allowed to cross, and get
a bridge where they do. That's the subject of the next post: routing roads that
follow the terrain instead of fighting it.
