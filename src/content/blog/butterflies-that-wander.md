---
title: 'Butterflies That Wander'
description: >-
  Slow, erratic, ground-hugging flight and the occasional rest — the small
  ambient detail that makes a meadow feel inhabited.
pubDate: 2026-07-03
category: 'Procedural'
tags: ['procedural generation', 'godot', 'animation']
heroAlt: 'A colourful butterfly fluttering low over meadow grass.'
---

Butterflies are pure atmosphere. They don't react to the player, they don't do
anything useful — they just drift around lush areas close to the ground and
occasionally land. But a meadow with a few butterflies in it feels alive in a way
an empty one doesn't, which is the whole point.

Like the birds, they have no model. Each is a small body with two pairs of wings —
fore and hind — plus a little accent spot, built from flat shapes and given a
colour scheme rolled from a list of real butterfly palettes (monarch, blue morpho,
cabbage white, and so on).

<div class="shot">SCREENSHOT: one or two butterflies over grass, close enough to see the wing colours. A second shot of one resting on the ground would be nice.</div>

## Fluttering, not flying

A bird moves in smooth arcs. A butterfly does the opposite — it bobs and weaves
unpredictably. Getting that erratic quality is the interesting part.

The butterfly heads toward a target point, but its path there isn't straight. On
top of the forward motion, it's pushed side to side by a weaving signal made of
two sine waves at different rates added together. Two waves that don't line up
produce a wobble that never settles into an obvious rhythm, which is what makes
the flight look unplanned rather than mechanical.

```gdscript
# side-to-side weave: two out-of-step waves, so it never repeats cleanly
var weave := sin(t * 6.0 + phase) * 0.6 + sin(t * 11.0 + phase * 1.7) * 0.3
var velocity := forward * speed + sideways * weave
```

It also bobs up and down slightly and stays a short, randomised height above the
ground, so the whole swarm hugs the terrain. The wings clap quickly — the same
sine-wave flap as the birds, but faster and through a wider angle.

## Resting

Every so often, instead of picking a new target, a butterfly lands. It drops to
the ground and switches to a resting state, where it slowly opens and closes its
wings — a much slower version of the flap — for a few seconds before taking off
again. That pause and the slow wing-fan are a big part of what makes them read as
butterflies rather than just colourful motes.

```gdscript
# while resting: a slow open/close instead of the fast flight clap
var angle := base + spread * (0.5 + 0.5 * sin(t * 2.5))
```

## Only where it makes sense

Butterflies are spawned in clusters, and only in the lush biomes — Meadow and
Forest. You won't find them over the desert or the sea. That restriction is just
a check against the biome map from the earlier post: spawn here only if this spot
is a lush biome. It keeps them where they belong and makes coming across a cloud
of them feel like a feature of that place.

As with the birds, a butterfly that's far from the player does nothing until you
approach.

Next is the system I find most satisfying: fish that move as a school, using three
simple rules that produce flocking.
