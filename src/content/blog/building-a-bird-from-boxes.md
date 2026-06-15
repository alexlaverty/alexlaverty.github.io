---
title: 'Building a Bird from Boxes'
description: >-
  A flying bird, with no model: a body, two flapping wings and a tail made from
  simple shapes, plus a bit of steering and banking to make the motion read.
pubDate: 2026-06-30
category: 'Procedural'
tags: ['procedural generation', 'godot', 'animation']
heroAlt: 'A low-poly bird in flight over water, wings mid-flap.'
---

The birds in this world have no 3D model. Each one is assembled at runtime from a
few basic shapes and then animated with some simple rules. Up close they're
clearly low-poly, but in flight at a distance they read as birds, and that's
enough. They're ambient — there to make the sky feel occupied, not to be
inspected.

## The shape

A bird is four parts:

- a small box for the body,
- two flat triangular wings, one on each side, each on its own pivot so it can
  rotate,
- a flat triangle for the tail.

The wings are built as a couple of triangles each and set to be visible from both
sides, since they're paper-thin and you often see them from below. That's the
entire model. Colour is rolled per bird — pale greys and whites for gulls, darker
browns and slate for the higher land birds.

```gdscript
var bm := BoxMesh.new()
bm.size = Vector3(0.12, 0.1, 0.5)   # the body
# each wing is two triangles on a pivot node, so rotating the
# pivot flaps the wing
```

<div class="shot">SCREENSHOT: a close-ish bird against the sky so the wing and tail shapes are visible, plus a wider shot of several birds in the distance.</div>

## The flap

Flapping is one line of maths. A sine wave moves smoothly back and forth between
-1 and 1 forever, so feeding the clock through a sine gives a value that rises and
falls. Use that to set the wing angle and the wings beat up and down. The two
wings use opposite signs so they mirror each other.

```gdscript
var flap := sin(time * flap_speed) * amplitude
wing_left.rotation.z = flap
wing_right.rotation.z = -flap
```

Each bird starts at a random point in the cycle so they don't all flap in unison,
and the flap speed varies per bird.

## Making the motion believable

A bird that flew in a straight line at a constant beat would look mechanical. A
few small touches fix that:

- **Wandering.** Each bird picks a random target point and steers toward it.
  When it gets close, it picks another. So it drifts around the map instead of
  flying off.
- **Turning gradually.** It doesn't snap to face a new target; it rotates toward
  the desired heading a little each frame, giving smooth curves.
- **Banking.** When it turns, it rolls into the turn — leaning like a real bird
  or an aircraft. The roll amount is taken from how sharply it's turning.
- **Flapping vs gliding.** It flaps harder when climbing and holds its wings
  still to glide when descending, which is what real birds do.
- **Holding altitude.** It aims to stay a set distance above whatever is below
  it — terrain or sea — so gulls skim low over the water while land birds circle
  higher.

None of these are complicated, but together they turn a flapping box into
something that moves like a bird. There's no flight simulation underneath — just a
handful of rules layered up.

To keep things cheap, a bird that's far from the player skips all of this and does
nothing until you're closer.

Next, a slower flier with a different feel: butterflies.
