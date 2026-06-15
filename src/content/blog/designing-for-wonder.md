---
title: 'Make It Beautiful'
description: >-
  The single design rule the whole project was built around, and the practical
  decisions that followed from taking "make it beautiful" literally.
pubDate: 2026-07-27
category: 'Procedural'
tags: ['procedural generation', 'game design']
heroAlt: 'A particularly striking generated scene at dusk.'
---

Across all the systems in this series there's one rule that decided most of the
arguments: when there's a choice to make, pick whichever option looks better. Not
the most realistic option, not the most technically interesting one — the prettier
one. That sounds obvious, but taking it literally and consistently changes a lot of
small decisions, and the small decisions are what add up.

## Beauty as the spec, not the polish

It's normal to build something functional first and make it look nice later. This
project inverted that: how good it looks was the actual goal, and correctness was
in service of it. A river system isn't there because simulating hydrology is neat;
it's there because rivers and waterfalls make a landscape worth looking at. The
question for any feature was always "does this make the world more pleasant to be
in," and if the answer was no, it didn't matter how clever it was.

<div class="shot">SCREENSHOT: the single most beautiful screenshot you have. This post is the place for it.</div>

## What the rule actually changes

Stated as a principle it's vague, so here's how it showed up in practice:

- **Bias the random ranges toward good-looking results.** Procedural generation
  rolls a lot of dice. Wherever it does, the ranges are tuned so the likely
  outcomes look good, rather than allowing the full range and accepting that some
  worlds come out ugly.
- **Make the striking conditions common enough to actually see.** Sunsets, night,
  fog, fireflies, glowing water — if these only happened rarely you'd never
  experience them. They're tuned to occur often. A feature you don't see might as
  well not exist.
- **Curate where raw randomness looks cheap.** The house colours come from
  hand-picked palettes, not random RGB. The notes come from a scale that can't
  clash. Generate the structure freely, but constrain the parts where random
  choices tend to look bad.
- **Prefer smooth to sharp.** Soft transitions between biomes, blended foam lines,
  gusts that roll across a field instead of snapping. Hard seams read as
  artificial; gradients read as natural.
- **Spend a little more when it clearly pays off.** If something can be made
  noticeably nicer for a modest extra cost, do it. Volumetric fog for god-rays,
  reflections on the water, a curved grass blade up close — none essential, all
  worth it.

## Why a rule helps

The value of having one stated principle is that it settles trade-offs quickly and
consistently. Faced with two ways to do something, you don't relitigate your
priorities each time — you ask which looks better and move on. Over hundreds of
those small decisions, a consistent bias toward the prettier option is most of
what separates a tech demo from somewhere you actually want to spend time.

It also kept the project honest about what it was. This was never meant to be a
realistic terrain simulator or an efficient engine showcase. It was meant to be a
nice place to walk around. Keeping that front and centre is the reason all the
systems in this series point in the same direction.

The last post is about the payoff: stepping inside one of these worlds in VR.
