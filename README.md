# The Numbers Game — Website

A smart, searchable **financial-education library** built from *The Numbers Game* podcast (hosted by Nick Reilly and Jason Robinson, produced by VIDPOD). Every episode is broken into deep-linkable **moments** — a specific insight, tip, stat, or question-and-answer — so a listener can search a real question and jump to the exact second in the video where it's answered.

## What's here

- **`index.html`** — the site (self-contained static page, GitHub Pages hosted).
- **`data/`** — the data layer, compiled by the content-intelligence engine:
  - `catalogue.json` — one light record per episode (the browse shelf).
  - `search-index.json` — every moment, self-contained and deep-linkable to the video.
  - `entities.json` — every person, company, and place mentioned, aggregated across episodes (the SEO layer).

## The data

The live site is a full episode library — the front-end is **live and in active use**. Every moment carries a **verbatim quote** machine-verified against the transcript, a video deep-link + duration, a clip-readiness score, the questions it answers (for search), a topic/subtopic, a freshness flag, and the entities it names.

The data is generated locally by the engine, then compiled to `data/`. This repo is the **product**; the engine + all publishing tools/docs live in the VIDPOD working folder (`~/Desktop/TOMMY AI/Brain/Vidpod/clients/TNG/Website Build`).

## Status & how to work on this

⭐ **The single source of truth is `TNG-MASTER-STATUS.md`** in the Website Build folder (current live counts, standards, next actions, and **§8 = the verified tooling inventory**). To publish an episode, follow `PUBLISH-EPISODE-RUNBOOK.md`; live publish queue is `PUBLISH-TRACKER.md`. (Live episode counts drift — read the front-door doc, not this README, for the current number.)

---

*Produced by [VIDPOD](https://vidpod.com.au/). Brought to you by [Future Advisory](https://futureadvisory.com.au/) & [Inovayt](https://www.inovayt.com.au/).*
