# HOMEPAGE PLAN — locked design decisions (6 July 2026)

> **SUPERSEDED (6 Jul 2026, evening).** The homepage became a ROUTER after live iteration with Tommy: video banner (looping title sequence) → WAYS TO WATCH THE SHOW (three coloured cards: Latest episode / Choose your own adventure / Explore every episode) → about → footer. The moments feature moved to its own page `adventure.html` (spec: MOMENTS-FEATURE.md). The episodes grid below was built, shipped, then removed — its job moves to the future `episodes.html`; card 3 points at the YouTube channel until then. This file stays as the record of the two-column-hero era.

*Everything agreed with Tommy in the 5–6 Jul planning sessions. Build AFTER the 2026 episode batch. When built and iterated, this graduates into a locked spec like EPISODE-PAGE-TEMPLATE.md.*

**Scope note:** 2026 episodes only for now. Back-catalogue mining comes later — every count and queue below simply grows when it does; nothing here changes.

---

## The homepage's job

A visitor lands on a podcast site with 280+ episodes and thinks "where do I start?" The homepage answers it two ways at once: here's the latest (for returners), and here's a bespoke way in (for newcomers). It is NOT a marketing page — no welcome video (considered and ditched), minimal copy, drives straight into content.

## Layout — hero, two columns (desktop, full 1280 frame)

- **Left ~40%: LATEST EPISODE.** Deliberately the smaller partner. Thumbnail (square corners), black EP tag, title in the highlight treatment scaled down, date, single action → its episode page.
- **Right ~60%: NEW TO THE SHOW — the moments feature** (see below). The size asymmetry is the message: the moments experience is the thing nobody else has.
- **Mobile: stacked, moments feature FIRST, latest episode second.** (Tommy can flip — one-line swap.)
- **Below the hero: THIS YEAR'S EPISODES grid** — all released 2026 episodes, newest first, locked card anatomy (title under thumbnail, date bottom-left, EP tag bottom-right). Until the proper Episodes page exists, this grid IS the library and the nav's EPISODES points here; later it becomes a teaser row.
- Nav per template rules (homepage OMITS the HOME item), same footer, same palette/fonts. Building `index.html` also kills the root-404 and makes every logo/HOME link on the site work.

## The moments feature ("NEW TO THE SHOW") — the crown jewel

**Problem it solves:** onboarding into hundreds of hours. **It is a self-contained section** — build it so it can graduate to its own page and be productised for other VIDPOD clients (the pattern: content-engine data + interest picker + moment player + episode exits; Huddle was v1, this is v2).

### The walk-through (one possible action at a time)
- Header: plain white Anton **NEW TO THE SHOW?** (no mint block — mint means tappable).
- Sell line with LIVE counts computed from data: *"280+ episodes. 670 moments mapped across 13 topics. Pick what interests you and start watching."* (Counts auto-grow.)
- **01 · PICK WHAT INTERESTS YOU** — topic chips WITH counts ("Property · 17"). Lead with the 8 richest topics, "+ more" dropdown unfolds the rest. A chip only exists with 5+ substantial moments behind it (honesty rule; excludes Retirement today). Tap a topic → its subtopic chips unfold beneath with counts ("SMSF · 3"); pick specifics or leave for whole topic. Chips: purple resting, mint selected. Friendlier display labels allowed for internal topic names (cosmetic mapping only, taxonomy untouched).
- **02 · GET THE BEST BITS** — the mint button: **SHOW ME THE MOMENTS**. Player + cards do not exist until pressed (materialise below, page nudges down).
- **03 · WATCH. SWIPE. REPEAT.** — video language everywhere, never "listen". Fixed player on top (story-page pattern: big player, "Now playing" + title), numbered moment cards in a swipe carousel below; tap a card → loads in the player.

### Serve rules (the spec-to-be)
- **Eligibility:** standalone ≥ 80 AND duration ≥ 60s (the "substantial" pool — 114 moments today, median 75s). Short clips stay for social/quotes, not this player.
- **Serve size: 5**, best-first, **max 2 per subtopic** (variety cap — a serve must taste varied).
- **SHOW ME MORE** deals the next 5 by rank; session remembers — nothing repeats.
- **Chips stay live above the player** — re-picking re-serves instantly, never restarts.
- **Graceful bottom:** when a thin topic runs dry: "That's the best of X for now — try these" + adjacent topic chips. Never a dead end.
- **Moment card anatomy:** subtopic tag (black block, mint text) + the question it answers + duration (computed end−start). Answers "why would I watch this?" structurally.
- **What plays:** the EPISODE video cued at the moment's startSec, stopping at endSec (YouTube IFrame API — the proven Huddle mechanic). NOT the edited social exports.
- **Exits (optional, never pushed):** "Watch the full episode" → episode page. The player is the destination; exits are quiet doors.
- No autoplay-chaining v1 (swipe = tasting); can add a "keep playing" toggle later.

### Data grounding (all in repo `data/search-index.json`, computed client-side, no backend)
- 670 moments; 59 score 85+ (median 41s); 114 score 80+ AND ≥60s (median 75s, up to 2m46s).
- Inventory by topic (substantial pool): Property 17, Business Growth 13, Tax 12, Business Structures 11, Building Wealth 10, Personal Development 9, Business Finances 9, Economy 8, Technology 8, Superannuation 6 (SMSF 3, Contributions & Strategy 3), Leadership 5, Personal Finance 5, Retirement 1 (hidden).
- Reference implementations: `repos/help-at-hand-the-huddle-season-1` (seek+endSeconds player, moments schema) · vidpod.com.au/story (player + numbered thumbnail carousel layout).

### All copy above is DRAFT — Tommy does a voice pass at build time.

---

## Build order (agreed)

1. **BATCH the released 2026 episodes** (266–284 as of 6 Jul) — `build_episode.py N` + `verify_episode.py N` per episode, per PROCESS.md; update LIVE-PAGES.md; Tommy click-through.
2. **Homepage** (`index.html`) per this plan → iterate live → lock spec.
3. **Episodes page** (episodes.html): the real library — search + topic filter/sort, newest first.
4. **Contact** (form + reuse the voice-note component) · **About** (+ host pages nick-reilly.html / jason-robinson.html).
5. Later: back-catalogue mining; moments feature possibly graduates to its own page; direct Spotify/Apple show URLs still TODO from Tommy.
