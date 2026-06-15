---
title: 'Making Water Look Wet'
description: >-
  A flat surface reads as water once you add a few things: moving waves, a colour
  that deepens with depth, foam at the shoreline, and brighter reflections at
  grazing angles.
pubDate: 2026-06-27
category: 'Procedural'
tags: ['godot', 'shaders', 'water']
heroAlt: 'Ocean water meeting a sandy shore, with foam at the waterline.'
---

The ocean, lakes and ponds are all flat surfaces. What sells them as water is a
shader — a small program that runs on the graphics card and decides the colour
and shape of every pixel of the surface as it's drawn. Four effects do most of
the work, and none of them are expensive.

## Moving waves

A still surface looks like glass, not water. The shader gives the surface a
rolling shape by adding several sine waves together and shifting them over time.
Each wave is a simple ripple; a few of them at different sizes and directions,
summed, make an irregular swell that never quite repeats. Because it's driven by
the clock, it animates.

```glsl
float h = 0.0;
h += sin(p.x * 1.0 + t * 1.1) * 0.6;
h += sin(p.y * 1.3 - t * 0.9) * 0.5;
h += sin((p.x + p.y) * 0.7 + t * 0.7) * 0.4;
// ...a few more, then push the surface up by h
```

The same wave field is reused at a smaller scale to wrinkle the surface for fine
sparkle, without adding any actual geometry — the wrinkles only affect how light
bounces, not the shape.

<div class="shot">SCREENSHOT: open water with visible wave motion and some sun sparkle. A still frame from a spot with a good reflection.</div>

## Colour by depth

Real water is lighter where it's shallow and darker where it's deep. The shader
works out the water's depth at each pixel by comparing the distance to the water
surface with the distance to the terrain behind it (the engine provides that
behind-the-surface distance). A small gap means shallow water; a large gap means
deep. The colour fades from a light shade in the shallows to a dark one in the
depths based on that gap. This is what gives shorelines their gradient and makes
the water read as a volume rather than a flat sheet.

## Foam at the shoreline

Where water meets land — where that depth is very small — the shader mixes in
white foam. A clean white band would look fake, so the foam edge is broken up
using the same wave field, giving it a ragged, shifting line that looks like surf.

## Reflections at a glancing angle

Look straight down into water and you see into it; look across it at a low angle
and it turns mirror-like and bright. That angle-dependent effect is called
fresnel, and it's a big part of why water looks like water. The shader computes
how grazing the viewing angle is and blends in a brighter sky tint as the angle
gets shallower, and makes the surface smoother (more mirror-like) there too. The
engine's screen-space reflections then paint nearby scenery onto that surface.

Put together — animated waves, depth colouring, broken-up foam, and a fresnel
sky tint — a plain flat plane reads convincingly as water. Each generated world
feeds its own colours and wave settings in, so one world's sea can be a calm
teal and another's a deep storm-grey.

The same shader, with gentler waves, is reused for lakes and ponds. Next we leave
the landscape behind and start adding life, beginning with birds built out of
boxes.
