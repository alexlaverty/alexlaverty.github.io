---
title: 'Procedurally Generated VR Worlds, Built with Claude Code'
description: >-
  An overview of a procedurally generated VR world built in Godot, and an index
  of the posts that explain how each part works.
pubDate: 2026-06-15
category: 'Procedural'
tags: ['procedural generation', 'godot', 'vr', 'meta quest 2', 'claude code']
heroAlt: 'A view across procedurally generated hills, a river and a small cottage at dusk.'
---

This is the first post in a series about a small project: a procedurally
generated world you can walk around in VR. It runs on a Meta Quest 2. Every time
it loads, the terrain, water, plants, buildings and weather are arranged
differently.

The series explains how the various parts work — terrain, rivers, biomes,
animals, lighting, and so on. Each post covers one system. They're written for
people who are curious about how this kind of thing is done but don't
necessarily write code, so I've kept the maths informal and the jargon to a
minimum.

This post sets out what the project is and links to the rest.

<div class="shot">SCREENSHOT: a wide establishing shot — hills, a river, a cottage. Something that shows the overall look of a generated world.</div>

## What the project is

The goal was a world I could walk through in VR that's different each time I load
it, rather than a single hand-built level. I wanted it to look reasonable — like
a place, not like random noise — without me placing every tree and hill by hand.

The target hardware is the Meta Quest 2, a standalone headset. The tone is
deliberately quiet: no combat or objectives, just somewhere to walk around. A
fish jumping in a pond is about as eventful as it gets.

## Why it's generated from code

None of the landscape is hand-authored. There's no level I sculpted in an
editor, no hand-placed houses, no painted grass. The world is generated from
code each time it loads. This is what "procedural generation" means: you write
the rules for building something, add some controlled randomness, and let the
program produce the result.

I used [Godot](https://godotengine.org), a free, open-source game engine. One
decision shaped the whole project: I wrote the entire game in script rather than
building scenes by hand in the editor. Terrain, water, buildings, animals,
lighting and music are all created in code at runtime.

I worked on it with [Claude Code](https://claude.com/claude-code), an AI coding
assistant. Building everything in code rather than through the editor's UI made
that practical — the whole game is text, so I could describe a change and have it
written, then run it in Godot to see the result. A fair amount of this series is
also about what that working process was like.

## What "procedurally generated" means here

The basic idea:

> A set of rules, plus some randomness, plus a starting number called the seed.

The rules are constraints like "terrain should be smooth," "rivers flow
downhill," and "houses sit on flat ground near a road." The randomness is what
makes each world different. The seed is a single number that determines how that
randomness plays out.

The useful property of the seed is that the same seed always produces the same
world. Change the seed and you get a different world from the same rules. That
makes results reproducible, which matters when you're debugging — you can
regenerate the exact world that looked wrong. The next post relies on this.

<div class="shot">SCREENSHOT: two or three small worlds from different seeds, side by side, to show how much they vary.</div>

## The posts

Each part of the world has its own post. You can read them in order, or skip to
whatever you're interested in.

**Foundations**

- Mountains from Noise *(coming soon)* — turning a grid of smooth random numbers
  into hills and valleys. This is the basis for most of what follows.
- Painting the Land: Biomes with Voronoi *(coming soon)* — dividing the map into
  meadow, forest, desert and snow, with soft transitions between them.

**Water and shaping the land**

- How Rivers Find Their Way *(coming soon)* — simulating water flowing downhill
  so streams merge into rivers and fall over edges.
- Roads That Follow the Land *(coming soon)* — routing paths that go around hills
  instead of straight over them.
- Making Water Look Wet *(coming soon)* — the shader tricks that turn a flat
  surface into water.

**The living world**

- Building a Bird from Boxes *(coming soon)* — a bird with flapping wings, made
  from simple shapes.
- Butterflies That Wander *(coming soon)* — slow, low flight for ambient detail.
- Schools of Fish That Think as One *(coming soon)* — the boids algorithm: three
  simple rules that produce flocking.
- Cottages from Scratch *(coming soon)* — generating houses from a set of
  parameters, with windows that light up at night.

**Atmosphere and performance**

- A Field of Grass Without Melting Your GPU *(coming soon)* — drawing a lot of
  grass blades efficiently, and only near the player.
- Wind You Can See *(coming soon)* — making vegetation sway.
- Golden Hour on Demand *(coming soon)* — day, dusk and night, with fog and
  god-rays.
- Light in the Dark *(coming soon)* — lamp posts, fireflies and lit windows
  after sunset.
- Music That's Never the Same Twice *(coming soon)* — generating ambient music
  at runtime.

**Wrap-up**

- Make It Beautiful *(coming soon)* — the design rule the project was built
  around.
- Walking Your Own World in VR *(coming soon)* — movement, teleporting and flying
  on the Quest 2.

## Next

The place to start is the terrain, since most other systems build on it:
Mountains from Noise.
