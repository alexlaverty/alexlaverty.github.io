---
title: 'Schools of Fish That Think as One'
description: >-
  The boids algorithm: three simple rules each fish follows on its own add up to a
  school that moves, turns and scatters as a group.
pubDate: 2026-07-06
category: 'Procedural'
tags: ['procedural generation', 'godot', 'algorithms', 'boids']
heroAlt: 'A school of fish turning together underwater.'
---

A school of fish moves as if it were a single thing — turning, splitting around
obstacles, flowing back together. It's tempting to assume something is
choreographing the whole group. Nothing is. Each fish follows a few simple rules
based only on its nearby neighbours, and the group behaviour emerges from that.
This is the boids algorithm, devised by Craig Reynolds in 1986, and it's one of
the classic examples of simple rules producing complex-looking results.

## Three rules

Every fish looks at the others near it and steers by three urges:

- **Separation** — don't crowd. Steer away from neighbours that are too close.
- **Alignment** — go with the flow. Steer toward the average heading of your
  neighbours.
- **Cohesion** — stay with the group. Steer toward the average position of your
  neighbours.

That's it. No fish knows the shape of the school or where it's going. Each one
just balances "don't bump into anyone," "point roughly the way everyone else is
pointing," and "don't get left behind." Run that for every fish at once and a
school appears — moving, turning, reshaping — entirely as a side effect.

```gdscript
for neighbour in nearby:
    separation += (my_pos - neighbour.pos) / distance   # push apart
    alignment  += neighbour.velocity                     # match heading
    cohesion   += neighbour.pos                          # pull toward centre
# combine the three (weighted) into one steering force
```

The weights matter: separation is the strongest here, so fish never overlap, with
alignment and cohesion holding the group loosely together.

<div class="shot">SCREENSHOT: a school underwater, ideally mid-turn so the group shape is visible. A second shot of the school scattering away from the player or a boat.</div>

## Keeping them in the water

Boids alone would let the school wander out of its pond or up through the surface.
A few extra steering forces keep them honest:

- **Containment** — if a fish drifts beyond its home radius, it's nudged back
  toward the centre, so each school stays in its own body of water.
- **Depth** — a gentle pull toward a comfortable band between the seabed and the
  surface, so they don't beach themselves or fly out of the water. Their depth is
  also hard-clamped between the floor and the surface as a backstop.

These use the terrain and water data from earlier posts — the floor height comes
straight from the heightfield.

## Fleeing

The schools react to you. If the player or a boat comes within a fear radius, each
fish adds a strong push directly away from the threat, stronger the closer it is.
Because every fish feels this at once, the whole school bursts apart and reforms —
which, again, nobody coordinated. It falls out of each fish reacting on its own.

```gdscript
for threat in threats:
    if distance < fear_radius:
        steer += (my_pos - threat).normalized() * flee_strength
```

## One framework, several looks

The same code covers everything from a tight ocean shoal to a single pond koi —
a "school" of one is just a lone wanderer with the same rules and no neighbours to
flock with. Ocean schools are large and quick; ponds get a few slow koi; some
big solitary fish cruise on their own. At night a faint glow is added for
bioluminescence. None of that needs new logic — just different numbers fed into
the same three rules.

Next we go back on land to build the houses: cosy cottages generated from a set of
parameters.
