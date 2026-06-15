---
title: 'Golden Hour on Demand'
description: >-
  A procedural sky that runs from day through sunset to a dark, starry night, plus
  the fog and post-processing that give every world a consistent, art-directed
  look.
pubDate: 2026-07-18
category: 'Procedural'
tags: ['godot', 'shaders', 'lighting']
heroAlt: 'A sunset sky with warm colours near the horizon fading to deep blue overhead.'
---

The time of day does more for the mood of a scene than almost anything else. The
same valley is cheerful at noon, striking at sunset and quiet at night. So the sky
is fully procedural — there's no skybox photo — and it's driven by a single sun
direction, which also drives the actual sunlight and shadows so they always agree.

## The sky is a shader

The sky is computed per pixel in a shader, based on the direction you're looking
and where the sun is. A few layers stack up:

- **A vertical gradient** from a light horizon to a deeper blue overhead. When the
  sun is low, the horizon colour shifts warm — the orange of sunrise and sunset.
- **A glow around the sun**, warm and broad when the sun is near the horizon.
- **A fade to night.** As the sun drops below the horizon, the whole sky is
  blended toward a near-black night colour.
- **The sun disk itself**, a bright spot with a halo.

```glsl
float day = smoothstep(-0.08, 0.22, sun_height);  // 0 night .. 1 day
vec3 horizon = mix(sunset_color, day_color, ...);  // warm when the sun is low
col = mix(night_color, col, day);                  // fade out after sundown
```

Because it's all derived from the sun height, moving the sun smoothly carries the
sky from midday through golden hour to dark.

<div class="shot">SCREENSHOT: a sunset and a daytime shot side by side if possible, to show the range. Golden hour is the money shot.</div>

## Night: stars, a moon, and sometimes an aurora

When it's dark, more of the shader switches on. A sparse, faintly twinkling
starfield appears overhead. A moon disk with a soft halo sits where its direction
points. And occasionally — when a world rolls it — ribbons of aurora hug the
horizon, built from drifting noise and coloured green shading to blue. These only
appear at night, so they're a treat you get in the worlds that have them.

## Clouds

Drifting clouds are layered on using fractal noise — the same kind of
many-scaled noise the terrain uses, but in 2D and slowly moving — projected onto
the sky above the camera. Cloud coverage is a parameter, so some worlds are clear
and others overcast.

## The consistent look

Two more things make every world feel art-directed rather than raw.

**Fog**, including volumetric fog — fog that fills space rather than just tinting
the distance. Light passing through it becomes visible as shafts (god-rays) from
the sun, or from the lamp posts at night. Storms thicken it for a moodier feel.

**Post-processing.** After the scene is rendered, it's run through a filmic
tonemap — the same kind of curve film and cinema cameras use to handle bright and
dark areas gracefully — plus a slight bump to contrast and saturation, gentle
ambient shadowing in the creases, and reflections on the water. This grade is
applied to every world, which is what gives them a common, slightly cinematic
character no matter how different the terrain.

The nights are deliberately very dark — which is exactly why the next post exists:
the warm lights that make a dark world cosy instead of bleak.
