# The Numbers Game — Website

A smart, searchable **financial-education library** built from *The Numbers Game* podcast (hosted by Nick Reilly and Jason Robinson, produced by VIDPOD). Every episode is broken into deep-linkable **moments** — a specific insight, tip, stat, or question-and-answer — so a listener can search a real question and jump to the exact second in the video where it's answered.

## What's here

- **`index.html`** — the site (self-contained static page, GitHub Pages hosted).
- **`data/`** — the data layer, compiled by the content-intelligence engine:
  - `catalogue.json` — one light record per episode (the browse shelf).
  - `search-index.json` — every moment, self-contained and deep-linkable to the video.
  - `entities.json` — every person, company, and place mentioned, aggregated across episodes (the SEO layer).

## The data

Season 18 to date — **episodes 263–286 (24 episodes) · 670 moments**. Every moment carries a **verbatim quote** machine-verified against the transcript (zero hallucination), a video deep-link and duration, a clip-readiness score, the questions it answers (for search), a topic/subtopic (13 topics · 37 subtopics), a freshness flag, and the entities it names.

The data is generated locally by the engine, then compiled to `data/`. This repo is the **product**; the engine that builds the data lives in the VIDPOD working folder.

## Status

Repo scaffolding. The data layer is complete and web-ready; the front-end is in development.

---

*Produced by [VIDPOD](https://vidpod.com.au/). Brought to you by [Future Advisory](https://futureadvisory.com.au/) & [Inovayt](https://www.inovayt.com.au/).*
