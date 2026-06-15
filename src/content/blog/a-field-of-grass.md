---
title: 'A Field of Grass Without Melting Your GPU'
description: >-
  Drawing tens of thousands of grass blades is fine if you do it in one batch and
  only near the player — the two ideas that keep the grass cheap enough for VR.
pubDate: 2026-07-12
category: 'Procedural'
tags: ['godot', 'performance', 'shaders']
heroAlt: 'A dense field of grass blades stretching toward hills.'
---

Grass is a performance problem before it's anything else. A convincing meadow
needs thousands upon thousands of blades, and VR is unforgiving — you're
rendering everything twice, once per eye, and a dropped frame is felt physically.
So the grass system is built around two ideas that keep the cost down: draw it all
at once, and only grow it where the player can see it.

## Drawing it all at once

The expensive thing in rendering isn't usually the number of triangles — it's the
number of separate *draw calls*. Every time you ask the graphics card to draw an
object, there's overhead. Ask it ten thousand times, once per grass blade, and the
overhead alone sinks you.

The fix is instancing. The blade is a tiny mesh — a few triangles. Instead of
drawing it ten thousand times, you hand the graphics card the blade once plus a
list of ten thousand positions, and it draws all of them in a single call. Godot's
MultiMesh does exactly this. One blade design, one draw call, a whole tile's worth
of grass.

```gdscript
var mm := MultiMesh.new()
mm.mesh = blade_mesh
mm.instance_count = blades.size()
for i in range(blades.size()):
    mm.set_instance_transform(i, blades[i])   # position, rotation, size
```

Each blade gets a random position, rotation, height and a slightly varied colour,
so the field doesn't look like a regular grid.

<div class="shot">SCREENSHOT: a dense grass field from ground level, showing the depth and variation. A second wider shot showing grass thinning into the distance.</div>

## Only near the player

Even with cheap drawing, covering an entire map in grass is wasteful — you can't
see most of it. So the grass exists only in a radius around the player, divided
into tiles. As you walk, tiles ahead of you are built and tiles behind you are
thrown away. The total amount of grass stays roughly constant no matter how big
the world is, because it's always just the patch around you.

To avoid a stutter when several tiles need building at once, only a few are built
per frame, nearest first. You might occasionally notice grass filling in just
ahead if you sprint, but the frame rate stays smooth, which matters far more in VR.

## Less detail further out

Within that radius, not all grass needs to be equally fancy. The system uses
rings: near tiles are dense and use a detailed curved blade; mid and far tiles get
progressively sparser and use a simpler flat blade. You can't tell the difference
at distance, but the saving is large. When a tile crosses from one ring to another
as you move, it's rebuilt at the new detail level. This idea — more detail up
close, less far away — is called level of detail, and it shows up all over the
project.

Finally, the grass respects the world: it follows each biome's grass density (lush
in meadows, almost none in desert) and skips roads, water and building pads, using
the same masks the earlier systems produced.

The grass also sways, which is the next post — wind, done entirely on the graphics
card.
