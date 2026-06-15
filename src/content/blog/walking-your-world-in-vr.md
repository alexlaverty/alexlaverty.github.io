---
title: 'Walking Your Own World in VR'
description: >-
  Stepping inside the generated world on a Meta Quest 2: head-relative walking,
  teleporting, a comfort vignette, and a fly mode for seeing it from above.
pubDate: 2026-07-30
category: 'Procedural'
tags: ['godot', 'vr', 'meta quest 2']
heroAlt: 'A first-person VR view standing in the generated world at golden hour.'
---

The whole point of the project was to walk around these worlds in VR, so this last
post is about the part that puts you inside one. The target is a Meta Quest 2 used
as a PC headset. Everything in the series so far renders the world; the VR rig is
what lets you stand in it.

## A body and a head

In VR there are two things to track: where your body is in the world, and where
your head is looking. The rig handles them separately. The body is a simple
capsule that rests on the terrain and walks around — the same kind of physics the
flat-screen player uses. On top of it rides the headset's view, which tracks your
real head movement. So you can lean and look around freely while the body walks
beneath you.

<div class="shot">SCREENSHOT: a first-person in-headset view standing in the world. A golden-hour or night shot shows it off best.</div>

## Moving without feeling sick

Motion in VR is a comfort problem as much as a control one — moving the view in
ways your inner ear doesn't expect makes people queasy. The rig offers two ways
around, which most VR apps settle on:

- **Smooth walking** with the left stick, relative to where you're looking, kept
  slower than the flat-screen game on purpose.
- **Teleporting** with the right stick: push it forward to aim an arc, release to
  jump to where it lands. Because you blink to the new spot instead of sliding
  there, there's no motion to feel sick about.
- **Snap turning** — the view rotates in fixed steps rather than sweeping around,
  which is much easier on the stomach than smooth rotation.

There's also a comfort vignette: while you're moving, the edges of your view darken
slightly, narrowing what you see. It sounds odd but it noticeably reduces nausea,
and it eases off the moment you stop.

## Learning to fly

A world this size is worth seeing from above, so there's a fly mode — toggled with
a button on the controller. While flying, gravity is switched off and you hover:
the left stick moves you around, and pushing the right stick up or down lifts or
lowers you. It's the quickest way to appreciate the shape of the terrain, the
river network and the road layout all at once — the same systems from the rest of
the series, seen whole.

## Built from code, like everything else

In keeping with the rest of the project, the VR rig is assembled in script rather
than wired up by hand in the editor — the body, the camera, the controllers and
the teleport visuals are all created at runtime. That's the thread that ran
through the whole thing: the entire world and the way you move through it are
described in code, which is what made it possible to build with an AI assistant in
the first place.

That's the series. Sixteen systems, from Perlin noise terrain to fish that flock
to a pentatonic music generator, all aimed at one modest goal — a quiet,
good-looking world that's different every time, and that you can step into and
walk around. Thanks for reading.
