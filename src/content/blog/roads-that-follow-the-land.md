---
title: 'Roads That Follow the Land'
description: >-
  Connecting the houses with a road network that winds around hills instead of
  going straight over them, using a minimum spanning tree and A* pathfinding.
pubDate: 2026-06-24
category: 'Procedural'
tags: ['procedural generation', 'godot', 'algorithms', 'pathfinding']
heroAlt: 'A dirt road curving along the contours of a hillside between two houses.'
---

Once the world has houses on it, they need to be connected by roads. Two
questions come up: which houses connect to which, and what route each road takes
across the terrain. The project answers them with two well-known algorithms.

## Which houses connect: a minimum spanning tree

You could connect every house to every other house, but that's a tangle. You want
the smallest network that still links everything together. That's a minimum
spanning tree.

Picture the houses as dots. A spanning tree is a set of connections that joins all
the dots with no redundant loops. The *minimum* spanning tree is the one where the
total length of all the connections is as short as possible. It's the cheapest way
to wire everything up so you can still get from any house to any other.

A useful side effect: a tree branches. Roads fork off to reach outlying houses
rather than forming one long chain, which looks more like a real road network.
Campfire sites are added to the same network, so paths fork out to reach them too.

```gdscript
# Prim's algorithm: grow the tree by repeatedly adding the
# shortest connection from the tree to a house not yet in it.
```

<div class="shot">SCREENSHOT: an aerial or minimap view showing the road network linking several houses, ideally with a fork or two.</div>

## What route each road takes: A* with a grade limit

Knowing two houses should connect doesn't tell you the path between them. A
straight line would plough through hills and cliffs. A real road winds to keep the
slope gentle. To get that, the project uses A* pathfinding.

A* finds the lowest-cost path between two points across a grid. It's the standard
algorithm game characters use to walk around walls. The clever part here is what
"cost" means.

The terrain is covered with a coarse grid of nodes. Crucially, each node's
position includes its height, exaggerated vertically. Because height is baked into
the node positions, going up a slope is literally a longer distance in the
algorithm's eyes than going around. A* prefers the shorter total distance, so it
naturally favours routes that stay level and curve around high ground.

On top of that, any connection between two nodes steeper than a maximum grade
isn't created at all. So A* can't even consider a route up a cliff — there's no
link there to use. The result is a road a vehicle could plausibly drive: it
contours around hills, takes the gentle saddle between two peaks, and only climbs
where it must.

```gdscript
# each node sits at (x, height * climb_weight, z); steep links are skipped
var rise = abs(a.y - b.y) / climb_weight
if rise / run > max_grade:
    continue              # too steep — don't connect these nodes
astar.connect_points(a_id, b_id)
```

## Carving and crossing

The routed path is a polyline — a series of points. The generator flattens a
strip of terrain along it to make the road surface, smoothing the heights a little
so the road doesn't ripple, and marks those cells so plants and buildings keep
off the road.

Where a road's path crosses a river, the terrain there was carved into a channel
by the river system. Rather than dip the road into the water, the generator raises
that span back up to bank level and records a bridge, which gets built as a set of
planks spanning the gap. The road treats the river cell as flat ground at bank
height while routing, so A* is willing to cross it occasionally instead of always
detouring around.

Two algorithms, then: a minimum spanning tree to decide the connections, and A*
with a slope limit to route each one. Next, a change of subject — the shader
tricks that make water look like water.
