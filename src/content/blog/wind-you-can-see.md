---
title: 'Wind You Can See'
description: >-
  Making grass and plants sway by bending each blade in the vertex shader, based
  on its height and position plus a global wind the weather controls.
pubDate: 2026-07-15
category: 'Procedural'
tags: ['godot', 'shaders']
heroAlt: 'Grass and plants leaning in the same direction under wind.'
---

Static grass looks dead. The moment it sways, the whole world feels like it has
air moving through it. The sway is done in a shader, on the graphics card, which
is what makes it affordable across an entire field at once.

## Bend the tips, keep the roots planted

When wind blows over grass, the base of each blade stays put and the tip leans the
most. Reproducing that is the core of the effect: push each point of the blade
sideways by an amount proportional to its height. Points at the bottom barely
move; points at the top move a lot.

This happens in the vertex shader — the part of a shader that runs once per point
of the mesh and can move that point before it's drawn. For each point it takes the
height, multiplies by the wind strength, and offsets the point in the wind's
direction.

```glsl
float bend = max(VERTEX.y, 0.0);     // taller points bend more, base stays put
float sway = wind_strength * flutter * bend;
VERTEX.x += wind_dir.x * sway;
VERTEX.z += wind_dir.z * sway;
```

<div class="shot">SCREENSHOT: hard to capture motion in a still, but a frame with grass clearly leaning, ideally with trees/plants leaning the same way. A short GIF would be better if you can.</div>

## Why it doesn't look uniform

If every blade bent by the same amount at the same instant, the field would move
like a single rigid sheet. Two things break that up.

First, the bend amount comes from a wave (a couple of sine waves added together,
as in earlier posts) so it grows and eases over time rather than snapping. Second
— and this is the important one — the wave is offset by each blade's world
position. Because the timing depends on *where* the blade is, a gust appears to
roll across the field: blades on one side lean a fraction before blades on the
other. That travelling ripple is what reads as real wind rather than a uniform
push.

```glsl
// the position term is what makes gusts roll across the field
float phase = TIME * 1.8 + world_pos.x * 0.25 + world_pos.z * 0.25;
float flutter = sin(phase) * 0.7 + sin(phase * 2.3 + 1.3) * 0.3;
```

## One wind for the whole world

The wind strength and direction are global values shared by every plant shader.
The weather system sets them: calm and gentle most of the time, stronger in a
storm, and exactly zero when there's no wind, which freezes everything perfectly
still. Because grass, flowers and bushes all read the same two values, they lean
together — the whole landscape responds to one wind, so a gust looks like it
passes over everything at once rather than each plant doing its own thing.

That shared, position-driven sway is the entire trick. It costs almost nothing
because the graphics card is already drawing each blade anyway; nudging the points
as it goes is nearly free.

Next, the sky: day, dusk, night, fog and god-rays.
