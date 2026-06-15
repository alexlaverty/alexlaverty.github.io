---
title: 'Mountains from Noise'
description: >-
  How a grid of smooth random numbers — Perlin noise — becomes terrain, and the
  handful of parameters that turn it into hills, plains or mountains.
pubDate: 2026-06-16
category: 'Procedural'
tags: ['procedural generation', 'godot', 'perlin noise', 'terrain']
heroAlt: 'Generated terrain showing hills, a flat plain and higher rocky peaks.'
---

Everything in this world sits on the terrain, so it's the first thing the
generator builds. The terrain is a heightfield: a grid of points, each with a
height. Connect neighbouring points into triangles and you have a surface. The
only real question is where the heights come from.

If you used plain random numbers — a different random height at every point —
you'd get static, like an untuned TV. Useless as a landscape. What makes terrain
look like terrain is that nearby points have *similar* heights. The ground rises
and falls gradually. That property is called coherence, and it's exactly what
Perlin noise gives you.

## What Perlin noise is

Perlin noise (and its relatives) is a function that takes a coordinate and
returns a smoothly varying value. Ask it for the value at two nearby points and
you get two nearby results; ask at distant points and the results are unrelated.
Plotted as height, it looks like soft, rolling hills.

You can picture it as a landscape of random bumps where the bumps blend into each
other instead of jumping. There's no randomness visible at the small scale —
just gentle slopes — but zoom out and the whole thing wanders up and down.

<div class="shot">SCREENSHOT: a top-down or angled view of bare terrain with no features yet, just the noise shape. Show the smooth rolling quality.</div>

In Godot this is a few lines. The engine has a built-in noise generator; you set
the seed and a few parameters and then sample it across the grid:

```gdscript
var noise := FastNoiseLite.new()
noise.noise_type = FastNoiseLite.TYPE_PERLIN
noise.seed = cfg.seed
noise.frequency = cfg.frequency
noise.fractal_octaves = cfg.octaves
# ...then for each grid point:
var raw := noise.get_noise_2d(x, z)   # roughly -1..1
var height := raw * 0.5 + 0.5         # rescaled to 0..1
```

## Octaves: detail at different scales

A single layer of Perlin noise is smooth but a bit featureless — all gentle
hills, no fine detail. Real terrain has structure at many scales: big mountain
masses, ridges on the mountains, bumps on the ridges.

The standard trick is to add several layers of noise at different sizes. A big,
slow layer sets the broad shape. A second, smaller layer at lower strength adds
medium variation. A third adds fine roughness. Each added layer is called an
octave, and stacking them is "fractal" noise. The generator here uses a few
octaves, which is enough to read as natural without looking busy.

## Turning the dial from plains to mountains

Raw noise gives you one particular look. A few simple operations applied to the
0–1 height reshape it into different kinds of terrain.

**Relief.** Raising the height to a power pushes values toward the low end or
the high end. Values below 1 stay closer to flat with occasional peaks (plains
with the odd hill); the world can lean the other way for rugged terrain. One
exponent controls the overall ruggedness.

```gdscript
height = pow(height, relief_exponent)
```

**A ceiling.** Clamping the maximum height flattens off the tops, which gives
mesa-like plateaus instead of sharp peaks.

**An island falloff.** Multiplying the height by a value that's 1.0 at the centre
of the map and drops to 0 at the edges sinks the borders below sea level, so the
land becomes an island surrounded by ocean rather than terrain that runs off the
edge of the world.

```gdscript
# d is distance from centre, 0 at middle, 1 at the corners
height *= 1.0 - pow(d, falloff_strength)
```

None of these are complicated on their own. The variety comes from combining
them and letting each generated world pick slightly different values.

## The seed, again

All of this is driven by the seed. The seed sets the noise pattern, and the same
seed always produces the same heights. That's what makes a whole world
reproducible from one number, and it's why the rest of the systems — rivers,
roads, where the houses go — can be layered on top deterministically. Change the
seed and you get a different but equally valid landscape from the same rules.

Once the heights exist, they drive two things: the visible mesh you walk on, and
an invisible collision surface built from the same numbers, so what you see and
what you bump into always match.

The next post takes this bare terrain and divides it into regions — meadow,
forest, desert, snow — using a different idea entirely: Voronoi cells.
