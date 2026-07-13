# Video ideas

Working backlog of video ideas. Each idea gets a status, a rough shape of
what the video would show, and first steps. Update in place — move done
ones to the bottom.

Statuses: `idea` → `planning` → `in progress` → `published`

---

## YTS — YouTube summariser script

Status: `idea`

A script that takes a YouTube URL and produces a summary (transcript →
LLM). Video is a build/demo: what it does, how it works, run it live on a
real video.

- Show the pipeline: fetch transcript, chunk it, summarise, output format.
- Worth covering: videos with no captions, long videos, cost per summary.
- First step: get the script to a state where a single command produces a
  clean summary end to end.

## Procedural generation VR game

Status: `idea`

Building a VR game world with procedural generation — terrain, biomes,
vegetation. Likely a series rather than one video; each technique
(heightmaps, noise, object placement) is its own episode.

- Strong visual material: before/after of each generation pass.
- Decide engine (Godot/Unity/Unreal) before recording anything.
- First step: get a generated terrain viewable in a headset, however rough.

## Photo syncer

Status: `idea`

A tool that syncs photos from devices to central storage automatically.
Video covers the problem (photos scattered across phones/SD cards), the
setup, and it running unattended.

- Angle: the boring-but-solved version beats cloud subscriptions.
- Cover: dedupe, folder structure, what happens on failure.
- First step: write down the actual requirements before touching code.

## Permaculture swale simulator

Status: `idea`

Simulating water flow over terrain to work out swale placement before
digging. Crosses two topics (permaculture + coding), which is the hook.

- Show real property contours if possible — sim vs actual block.
- Could be simple: heightmap + water droplet simulation, top-down view.
- First step: find or capture elevation data for the block.

## VTuber exploration

Status: `idea`

Trying out the vtuber toolchain — avatar creation, face/motion tracking,
streaming setup. Video is a first-attempt log: what the software is, what
it costs, where it fell over.

- Honest "here's what this actually takes" angle, not a polished showcase.
- Decide up front: 2D (Live2D) or 3D (VRoid/VSeeFace) path.
- First step: get any avatar tracking a webcam locally.

## Python video generation

Status: `idea`

Generating videos programmatically with Python (moviepy/ffmpeg or
similar). Possible force multiplier: could automate parts of producing
the other videos on this list (intros, captions, b-roll assembly).

- Demo: script in, rendered video out, no editor opened.
- Worth testing early since it changes how the rest of the list gets made.
- First step: render a 30-second video with text, images, and audio from
  a single script.

## Memory of Mankind — ceramic tiles

Status: `idea`

Memory of Mankind is an archival project in Hallstatt, Austria that
stores information on ceramic tablets designed to last hundreds of
thousands of years. Video explores the project and attempts making a
tile — what's worth preserving, and can you do it at home.

- Angle: personal archive — what would I put on one tile?
- Research first: their process (laser-printed ceramic) vs what's
  achievable with a local kiln or pottery studio.
- First step: background research on the project and home-scale ceramic
  printing/engraving options.

---

Based on our past conversations, you have a pretty consistent set of interests. You tend to enjoy **building things**, **preserving knowledge**, **automation**, **self-sufficiency**, **AI**, and **long-term thinking**. Rather than chasing trends, you seem to enjoy documenting projects and learning in public.

Here are blog post ideas grouped into themes.

## AI & Automation

* Building an AI-powered daily YouTube news channel
* Creating a VTuber that speaks using text-to-speech
* Automatic lip-sync for AI-generated voices
* My workflow for AI-generated videos with Python
* Flux vs Stable Diffusion: which image model should you self-host?
* Open-source AI tools I actually use
* Running AI models locally on consumer hardware
* Automating Reddit content collection
* Building an AI research assistant for myself
* How I automated image generation for videos

---

## Python Projects

* Procedural generation VR game
* Python video generation
* Photo syncer
* Building a daily video creator with MoviePy
* Automatically converting photo albums into blog posts
* Generating thumbnails with Python
* Using Playwright for web automation
* Creating a personal life dashboard in Flask
* Tracking my health using only CSV files
* Building a personal analytics platform instead of using SaaS
* Why I prefer simple flat files over databases for personal projects

---

## Knowledge Preservation

* Memory of Mankind project ceramic tiles
* How to make information survive 10,000 years
* The best long-term storage media
* Could ceramic QR codes outlast hard drives?
* Creating a family archive for future generations
* Digital preservation in the AI age
* What should humanity preserve if civilization collapsed?
* Building my own "personal Memory of Mankind"

---

## Permaculture & Self Sufficiency

* Permaculture swale simulator
* Designing software to model water flow on land
* Passive hydroponics experiments
* Miscanthus as a future building material
* Earthships in Australia
* Could I become food independent on a small block?
* Mapping rainfall using GIS data
* Designing the perfect permaculture property
* Lessons from traditional agriculture
* My dream off-grid homestead

---

## Software Engineering

* Why I like Markdown over databases
* Building a knowledge base with MkDocs
* Organising thousands of notes
* My folder structure for a digital life
* Git as a personal archive
* Static websites that will still work in 30 years
* Why plain text wins
* Self-hosting everything I can
* Creating documentation people actually read

---

## Personal Data

* Building my own health dashboard
* Tracking exercise with Python
* Visualising years of Fitbit data
* My life quantified
* CSV vs SQLite for personal data
* Building dashboards without expensive software
* Tracking habits over decades
* What I've learned from years of personal metrics

---

## Photography

* Building a better photo management system
* Automatically tagging photo albums
* Drone photography around Sydney
* Manly Beach through the seasons
* Organising 100,000 photos
* Embedding maps into photo galleries
* Rating photos automatically with AI

---

## Home Server & Self Hosting

* My Ubuntu home server setup
* Automatic backups that actually work
* Self-hosting AI
* Building a private cloud
* Running Docker containers for everything
* Home server maintenance checklist
* Raspberry Pi projects worth building
* Why I moved away from cloud services

---

## Future Technology

* Could AI preserve civilisation?
* The future of humanoid robots
* Open-source AI vs closed AI
* How robotics will change agriculture
* Space colonisation through automation
* 3D printed homes
* The future of manufacturing
* Designing software for a post-AI world

---

## Finance

* Understanding Australian superannuation
* High Growth vs High Growth Index investments
* Building wealth through automation
* Tracking net worth with Python
* FIRE in Australia
* My personal finance dashboard

---

## Deep Dive Series

These could become recurring series:

* **Project Log** – weekly updates on whatever you're building.
* **Today I Learned** – one interesting thing each day.
* **Automation Journal** – every automation you create.
* **Interesting Papers** – summaries of scientific papers.
* **AI Experiments** – trying new models and documenting results.
* **Open Source Spotlight** – reviewing useful open-source software.
* **Permaculture Notes** – concepts you're learning.
* **Future Archive** – ideas worth preserving for future generations.
* **Data Diaries** – insights from your personal metrics.
* **Weekend Build** – small projects completed in a weekend.

## Ideas that fit your personality especially well

From everything we've discussed over the past few days, these stand out as topics you're likely to enjoy writing consistently:

1. Procedural generation VR game
2. AI-powered faceless YouTube automation
3. VTuber exploration
4. Python video generation
5. Photo syncer and automated gallery publishing
6. Memory of Mankind ceramic tile experiments
7. Permaculture swale simulator
8. Building a personal AI knowledge base
9. My self-hosted digital life
10. Flat-file software instead of cloud services
11. Long-term digital preservation
12. Quantified self dashboards
13. Home server projects
14. Open-source AI experiments
15. Building software that will still work in 30 years

A pattern I've noticed is that many of your ideas connect under a single theme: **using software and automation to preserve knowledge, improve self-sufficiency, and reduce dependence on proprietary services**. Framing your blog around that overarching mission would make a wide range of projects—from AI experiments to permaculture simulators to personal data dashboards—feel like parts of one coherent journey rather than unrelated posts.


