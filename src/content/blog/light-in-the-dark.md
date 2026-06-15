---
title: 'Light in the Dark'
description: >-
  Warm lamp posts along the roads, fireflies over the meadows, and windows that
  glow — the lights that make a dark world feel cosy instead of empty.
pubDate: 2026-07-21
category: 'Procedural'
tags: ['godot', 'lighting']
heroAlt: 'A road at night lit by warm lamp posts, with lit cottage windows nearby.'
---

The nights in this world are genuinely dark, which is a deliberate choice — it
makes the lights matter. A dark world with no warm light is bleak; a dark world
with lamp posts, lit windows and fireflies is cosy. This post is about placing
those lights.

## How "night" is measured

Everything here keys off one number: how night-like it currently is, derived from
the sun's elevation. When the sun is high it's 0; as the sun drops past the
horizon it eases up to 1. The lamp glow, the firefly spawning, and the glowing
windows from the houses post all scale off this same value, so the world lights up
together as the sun goes down.

```gdscript
static func night_factor(cfg) -> float:
    return 1.0 - smoothstep(8.0, 25.0, cfg.sun_angle)
```

There's also an "always on" override for worlds where you want the lights lit
regardless of time.

## Lamp posts along the roads

The roads from the earlier post left behind their centre-lines. The lamp system
walks along each road and places posts at even spacing, set just off to the side —
and it alternates which side, so the lamps zig-zag down the road like real
street lighting rather than lining up on one edge.

Each lamp is a thin pole with a glowing head and an actual light. The head's
emission and the light's brightness both scale with the night value, so the lamps
are dark by day and burn warm at night. The colour is a warm amber with a little
variation per lamp, so they're not all identical.

```gdscript
# even spacing along the road, alternating sides
for spot in resample(road, lamp_spacing):
    var side_offset := perpendicular * side
    spawn_lamp(spot.pos + side_offset)
    side = -side
```

<div class="shot">SCREENSHOT: a road at night lined with lit lamp posts, ideally with their light pooling on the ground and some god-rays. Lit house windows in frame would be a bonus.</div>

## Cost control: shadows on a budget

Lights are cheap until they cast shadows, and shadow-casting lights get expensive
fast. So shadows are optional and capped: only a limited number of lights are
allowed to cast them, handed out on a first-come basis. The rest still light the
scene, they just don't cast shadows. It's the kind of unglamorous limit that keeps
a night scene full of lamps from tanking the frame rate.

## Fireflies

In the lush biomes — Meadow and Forest — clusters of fireflies appear at night.
Each cluster is a patch of small glowing motes that drift slowly, plus a soft
green-tinted light so the swarm actually illuminates the grass beneath it. They're
placed by sampling the map for lush, dry spots, so you come across them in exactly
the places that already feel alive.

The motes use additive blending — their light adds onto whatever is behind them —
which is what gives them that glowing, floating-spark quality against the dark.

Together with the glowing house windows and the campfires, the lamps and fireflies
turn nightfall from something that hides the world into something that's worth
waiting for. Which is the right note to end the technical posts on, because the
next one is about the rule behind all of these choices.
