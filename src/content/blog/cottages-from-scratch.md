---
title: 'Cottages from Scratch'
description: >-
  Generating endless cottages from a handful of parameters: walls, one of four
  parametric roof types, a door, and windows that light up at night.
pubDate: 2026-07-09
category: 'Procedural'
tags: ['procedural generation', 'godot', 'buildings']
heroAlt: 'A small generated cottage with a pitched roof and lit windows at dusk.'
---

The houses in this world are generated, not modelled. Each one is built from
primitives at runtime based on a set of random parameters. Because the parameters
vary, you get a street of houses that are all clearly the same kind of building
but no two identical. The trick to making them look good rather than random is
fairly mundane, and I'll get to it at the end.

## A house as a set of numbers

A cottage is described by a few values rolled at build time: width, depth, number
of storeys, wall height, roof height, roof style, whether it has a chimney. From
those, the builder assembles:

- a foundation slab,
- a box of walls,
- a roof (more on this below),
- a door on the front, with a step,
- windows spaced along the walls,
- optionally a chimney, sometimes with smoke.

```gdscript
var w := rng.randf_range(4.5, 7.5)     # width
var d := rng.randf_range(4.5, 7.5)     # depth
var storeys := 1 if rng.randf() < 0.55 else 2
var roof := pick_roof(rng)             # gable / hip / pyramid / flat
```

Change those numbers and you get a different house. That's the whole idea — the
variety is in the parameters, not in separate models.

<div class="shot">SCREENSHOT: a few generated houses together showing different shapes and roof types. A close-up of one good cottage.</div>

## Parametric roofs

The roof is the part that most changes a house's character, so there are four
types, each built from the building's dimensions:

- **Gable** — the classic two-sloped roof with a triangular end wall.
- **Hip** — sloped on all four sides, meeting at a ridge.
- **Pyramid** — four triangular sides meeting at a single point.
- **Flat** — a low slab with a slight overhang.

Each is just a few triangles positioned from the width, depth and roof height.
Because they're computed from the same dimensions as the walls, the roof always
fits the house no matter what size it rolled.

## Windows that glow

The windows are the cosy part. By day they're dark glass. At night they glow
warm. This is driven by a single "how lit" value that comes from the sun's
position — covered properly in a later post on lighting — which runs from 0 in
daylight to 1 at night. The window material fades from dark glass toward a warm
colour by that value, and switches on emission (the surface gives off light) when
it's dark, so the windows actually glow and bloom rather than just changing
colour.

```gdscript
material.albedo_color = WINDOW_DAY.lerp(WINDOW_LIT, lit)
if lit > 0.02:
    material.emission_enabled = true   # the glass glows at night
```

A procedural house orients its door toward the nearest road, and the building
system also scatters driveways, fences, yard props and garden lights around it.

## The actual trick: curated palettes

Here's the part that makes them look charming instead of garish. The colours
aren't random. If you picked wall, roof and trim colours at random you'd get a lot
of ugly houses. Instead there's a short list of hand-picked colour combinations —
plaster walls with red-tile roof, ochre with slate, timber with brown, sage blue
with dark trim, and so on — and each house picks one combination as a set.

```gdscript
const PALETTES := [
    { "wall": ..., "roof": ..., "trim": ... },   # plaster / red tile
    { "wall": ..., "roof": ..., "trim": ... },   # ochre / slate
    # ...a handful of curated combinations
]
```

So the geometry is generated freely, but the colours are constrained to choices
known to look good together. That split — generate the structure, curate the
palette — is a recurring theme in the project, and it's the difference between
"procedural" looking cheap and looking deliberate.

Next: drawing a whole hillside of grass without the frame rate collapsing.
