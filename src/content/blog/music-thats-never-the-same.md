---
title: "Music That's Never the Same Twice"
description: >-
  Generating gentle ambient music at runtime from a pentatonic scale — and why
  that choice of scale means it can't really play a wrong note.
pubDate: 2026-07-24
category: 'Procedural'
tags: ['procedural generation', 'godot', 'audio']
heroAlt: 'A calm dusk scene; the kind of mood the ambient music is written for.'
---

The background music isn't a recording. There's no audio file. It's synthesised
as the game runs — notes chosen and sounded on the fly — so it never loops and
it's a little different every time. For an ambient world you wander through
indefinitely, that suits it better than a track that repeats every two minutes.

## Why it can't sound wrong

The notes are drawn from a major pentatonic scale. A regular scale has seven
notes; a pentatonic scale uses five, and the two that are left out are the ones
most likely to clash. The practical upshot is that any combination of pentatonic
notes sounds at least fine together. You can play them in any order, overlap them,
land on any one — it stays consonant.

This is a well-known party trick: the black keys on a piano form a pentatonic
scale, and you can mash them at random and it still sounds vaguely pleasant. That
property is exactly what you want when a program is choosing notes with no
composer checking them. The generator picks notes essentially at random from the
scale, and the scale guarantees the result is harmonious.

```gdscript
# C major pentatonic across three octaves; pick from these at random
var base := [261.63, 293.66, 329.63, 392.00, 440.00]   # C D E G A
```

<div class="shot">SCREENSHOT: this one's audio, so a calm representative scene works — somewhere you'd want this music playing. Or skip the image.</div>

## Making a note sound like a note

A raw sine wave is a dull electronic beep. A couple of touches make it a soft bell
instead.

- **Shape over time (the envelope).** A real struck note starts quickly and fades
  away slowly. Each note is given a soft attack and a long, decaying tail rather
  than switching on and off abruptly.
- **A harmonic.** Adding a quieter copy of the note an octave up gives it a
  bell-like timbre instead of a pure tone.

```gdscript
var env := (1.0 - exp(-t * 18.0)) * exp(-t * decay)   # quick in, slow fade
var tone := sin(TAU * f * t) + 0.35 * sin(TAU * f * 2.0 * t)  # + octave = bell
```

Underneath the bell notes sits a very quiet drone — a sustained low root and fifth
— which gives the whole thing a warm floor to rest on. Everything is run through a
reverb effect so the notes sound like they're in a space rather than right against
your ear.

## Reacting to the time of day

The music shifts with the world. There's a single "calm" value tied to the time of
day — covered in the lighting post — and at night the generator leaves longer
gaps between notes and favours the lower octaves. So the music thins out and
settles as it gets dark, matching the mood the lights and sky are setting.

That's the whole system: random notes from a scale that can't clash, shaped into
soft bells over a drone, easing with the time of day. Simple ingredients, and
because nothing is pre-recorded, you never hear the same minute twice.

The last two posts step back from individual systems — first the design rule
behind all of them, then what it's like to actually walk through the result in VR.
