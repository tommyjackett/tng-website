# TNG Website — System, Workflow & Plan

*The single readable record of how the TNG website process works, what we've built, where everything lives, and how we future-proof and replicate it. Written 13 Jul 2026. Plain-English on purpose — anyone should be able to read this top to bottom.*

> **How to use this doc:** Part 1 = current status (where we're up to). Part 2 = the episode lifecycle (explain to the team). Part 3 = where everything lives (local vs backed-up vs source-of-truth). Part 4 = the three skills we'll build. Part 5 = how link-sourcing actually works (technical, reproducible). Part 6 = the audio-only template (future). Part 7 = durability + the safe order to build. Part 8 = open threads.

---

## Part 1 — Current status (where we're up to, 13 Jul 2026)

- **Live site:** https://thenumbersgamepodcast.com.au (repo `tommyjackett/tng-website`, GitHub Pages). Local: `~/Desktop/TOMMY AI/repos/tng-website`.
- **Episode pages LIVE:** 243–285. Each has the video player + transcript/chapters/questions + the "Listen now" Spotify audio player + episode-specific Apple/Spotify/Subscribe buttons.
- **Platform links in Notion ("The Numbers Game episodes" DB):** EVERY published episode **1–285** has all its link properties filled:
  - `Apple episode URL`, `Spotify episode URL`, `Spotify embed URL` — on all 1–285.
  - `Website Page URL` — on 243–285 (the ones with built pages).
- **Back-catalogue (ep 1–242):** links are sourced + in Notion, but **pages are NOT built yet** (only 243+ have pages). Manifest of those links: `data/backcatalogue-links.json`.
- **Not yet published:** 286–298 (future) — source their links as each goes live.

**Known lesson banked:** ep 285's page first shipped with NO audio player, because it was built *before* the episode was live on the platforms (no links existed yet → the build's fallback dropped the player). Fixed. See "the one rule" in Part 2.

---

## Part 2 — The episode lifecycle (for the team)

Everything splits on one question: **is the episode public yet?**

**Pre-Phase 1 — Content prep** *(Tommy owns this; not website work)*
Record → edit → upload → schedule → transcribe → show notes. The episode exists but isn't public.

**Phase 1 — Build the page** *(before it's live)*
Transcript → run the schema → mine the "moments" → compile the data → build the episode page.
→ The page has everything **except the audio player**, because the episode isn't on Spotify/Apple yet, so there's nothing to embed.

**Phase 2 — Add the listen links** *(the moment it goes live)*
Episode publishes → source the Apple link, Spotify link + embed player → write to Notion **and** into the page → homepage flips to the new latest episode.

**THE ONE RULE:** *A page is not "done" until Phase 2 has run.* If a page goes live after Phase 1 only, its audio player slot is empty — which looks "broken" but isn't. Either hold the page until it's live + linked, or let the Phase-2 sweep fix it. This rule prevents the ep-285 situation forever.

---

## Part 3 — Where everything lives (local vs backed-up vs source-of-truth)

**The mental model:** *Local = the workshop (the master). GitHub = the safety backup AND the live shopfront. It must all run offline; GitHub is a mirror, not the brain.*

| What | Where it lives | Backed up if laptop lost? | Notes |
|---|---|---|---|
| Website **pages + data** (`episode-N.html`, `data/*.json`) | git repo → GitHub → live site | ✅ yes | Published snapshot; deployed by GitHub Actions |
| The **tools/scripts** (build, source, push) | `scripts/` in the repo | ⚠️ **NO — gitignored, local-only** | *Durability gap to fix* |
| The **content engine** (schema, mined moments, DEEP files, transcripts) | `Brain/Vidpod/clients/TNG/Website Build/` | ⚠️ **NO — local-only** | The content MASTER |
| The **link record** (Apple/Spotify/embed/page URLs) | Notion episodes DB | ✅ yes (Notion cloud) | The links MASTER |
| The **know-how** | Claude's memory (`project_tng_platform_links`) | Persists across chats | Not human-shareable on its own |
| **This document** | git repo → GitHub | ✅ yes | The readable plan/record |

**Two masters, one published copy:**
- **Content master = the engine (local).** It outputs 3 data files; a *copy* goes into the repo's `data/`, which builds the pages, which deploy to web. Flow is one-directional: **engine → repo `data/` → live web.** Golden rule: the repo's `data/` is always *regenerated* from the engine, never hand-edited — so the two copies never drift.
- **Links master = Notion.** Links flow from Notion (or the sourcing tools) into the page separately.

**The durability gap (the thing to fix first):** the *tools* (`scripts/`) and the *engine* are local-only. If the laptop dies, the website survives but the machinery to rebuild it doesn't. Fix = mirror the tools + a runbook into GitHub so "clone the repo → you have everything → run it offline" becomes true.

---

## Part 4 — The three skills (repeatable buttons over existing scripts)

A "skill" here = a small instruction file (like the existing `tng-shownotes`, `vidpod-website-push`) that runs the local scripts in order. Three, matching the lifecycle:

- **`build-episode-page`** *(Phase 1, local, offline)* — "Episode N is transcribed. Mine it → validate → compile data → build the page → verify." Runs entirely on the machine.
- **`sync-episode-links`** *(Phase 2, needs internet)* — "Episode N is live (or: check what's newly live). Source Apple + Spotify + embed → write to Notion → drop into the page → push live." **This is the Monday-8am scheduled-sweep candidate** (purely date-driven: an episode is either public or not).
- **`refresh-homepage`** — "Point the homepage at the latest live episode."

**Built as a template for OTHER CLIENTS:** every client is the same shape (a podcast + a Notion episodes DB + a website repo + the same schema & link-sourcing). Each skill takes a few per-client settings (Spotify show ID, Apple podcast ID, Notion DB, repo path); the rest is identical. Get it clean once for TNG → cloning for client #2 = filling in a settings file.

**Notion writing:** the Notion MCP connector is already connected — links are written straight through it, no manual clicking, no separate API key needed. (Only caveat: a fully-headless scheduled run with nobody present may not inherit that live connection — revisit if/when we automate the Monday sweep.)

---

## Part 5 — How link-sourcing actually works (technical, reproducible)

Everything derives from two IDs per episode: an Apple `trackId` and a Spotify 22-char episode `id`. All URLs are string templates:
- Spotify page: `open.spotify.com/episode/{id}`
- Spotify embed (AUDIO, no `/video`): `open.spotify.com/embed/episode/{id}?utm_source=generator` (render at `height="152"`)
- Apple page: `podcasts.apple.com/au/podcast/id1555566088?i={trackId}` (Universal Link → opens app on Apple devices)

**Apple sourcing:**
- Recent 200 episodes: iTunes Lookup API, no auth — `itunes.apple.com/lookup?id=1555566088&country=au&entity=podcastEpisode&limit=400`.
- Deep archive (older than ~Dec 2022, ep 1–84): iTunes caps at 200, so use Apple's internal **amp-api** — grab the bearer JWT from the podcasts.apple.com JS bundle (`/assets/index~*.js`, first `eyJ...` token), then `amp-api.podcasts.apple.com/v1/catalog/au/podcasts/1555566088/episodes?limit=100&offset=N` with `Authorization: Bearer <jwt>` + `Origin: https://podcasts.apple.com`. Paginates ALL episodes.

**Spotify sourcing:**
- Official Web API is DEAD for this — since May 2025 it requires the *app owner* to have Premium (our account is Free). Do NOT retry client-credentials.
- Use the **SpotifyScraper** pip library (`pip install --user spotifyscraper`) — reads the same public data the logged-out web player uses. `client.get_show('open.spotify.com/show/41SVe1eJhucikhF3fWD3NW').episodes` returns the newest ~50 (covers new episodes). For the full 284, use the pathfinder API fallback (`api-partner.spotify.com/pathfinder`, op `queryPodcastEpisodes`).

**Matching (the "never wrong" rule):** join platform episodes to the Notion/catalogue episode by **exact release date** (each episode has a unique date, so even the old twice-weekly stretches match cleanly). If dates are off by the usual ±1 day (AU vs UTC), fall back to a ±1-day window only when it's unique; disambiguate crowded windows by title similarity; flag anything ambiguous rather than guess. TNG rewords titles across platforms, so never match on title alone.

**Where the sourcing tools sit (LOCAL — `scripts/` is gitignored, so on the Mac but not GitHub-backed yet; that's the "make tooling durable" job in Part 7):**
- `scripts/podcast-link-sourcing/` (rescued from the vanishing scratchpad; has its own README):
  - `fetch-spotify-and-apple-episode-lists.py` — pull the full episode lists from both platforms.
  - `apple-deep-episode-pull-ampapi.py` — pull ALL Apple episodes via amp-api (reaches the old pre-Dec-2022 ones the iTunes API can't).
  - `match-episodes-to-platform-links.py` — match episodes to platform pulls by exact date; produce the links; flag anything uncertain.
- `scripts/enrich_platform_links.py`, `scripts/source_platform_links.py` — earlier sourcing versions (used for 243+).

**Script naming convention:** name every script by what it DOES — verb-first, domain-clear, hyphenated, understandable from the filename alone. ✅ `apple-deep-episode-pull-ampapi.py`  ❌ `apple_deep_pull.py`. (Example of a future one: `download-episode-audio-files.py` to fetch audio for ep 1–138 so they can be transcribed.)

**Spotify creds:** `.secrets/spotify-api_tng.txt` (only needed for the dead official-API path; the scraper needs nothing). **Never commit secrets.**

---

## Part 6 — The audio-only episode template (future, back-catalogue only)

TNG started **video at ~EP 139** (confirm exact cutover from data at build time). Episodes **≈1–138 are audio-only.**

- **Video episodes (139+, incl. everything loaded 243–285):** hero at top = YouTube video facade; chapter/question **seek runs on the YouTube player**. Spotify embed stays a passive "Listen" option. **Unchanged — do NOT add seek here.**
- **Audio-only episodes (≈1–138):** DIFFERENT template — the top hero slot (normally the YouTube thumbnail + play button) is **replaced by the Spotify audio player**, and that player gets **timecode seek** wired in via Spotify's official **iFrame API** (`open.spotify.com/embed/iframe-api/v1` → controller with `.seek(seconds)`/`.play()`). Tapping a chapter/question jumps the audio — the moment-jumping YouTube does on video eps. No video facade, no thumbnail.

**Seek alignment is CLEAN (confirmed):** NO dynamic ad insertion via Simplecast, and the audio-only transcript is cut from the exact Simplecast file Spotify serves → transcript timeline == Spotify player timeline → `seek(seconds)` is pinpoint, no per-episode test needed.

**Build-time note:** "has a YouTube link" ≠ "is a true video episode" (some old audio eps may have been re-uploaded to YouTube as static-image videos). Confirm the real cutover before applying the template.

---

## Part 7 — Durability + the safe order to build

**Principle:** local-first, offline-capable, mirrored to GitHub for backup + deploy. Each step below stands alone, is reversible, and does NOT touch the working live site.

1. **Durability first** — move the tools (`scripts/` + the scratch sourcing logic) into git, and keep this doc updated. Solves the "lost laptop / vanishing scratchpad" risk. *(Purely additive.)*
2. **Confirm the Notion write path** for automation (MCP works interactively; headless cron may need a token).
3. **Skill B — `sync-episode-links`** (the Monday sweep). The highest-value, cleanest-to-automate piece.
4. **Skills A + C** — `build-episode-page` and `refresh-homepage`, once B is proven.
5. **Audio-only template + seek** — when we start building the ≈1–138 back-catalogue pages.
6. **Generalise to a client template** — parameterise the skills for client #2.

---

## Part 8 — Open threads / next steps

- [ ] **Make the tooling durable** (Part 7, step 1) — the urgent one.
- [ ] Build **Skill B** (link sync) + decide on the Monday-8am schedule.
- [ ] Build the **back-catalogue pages** (1–242), then the **audio-only template** (≈1–138).
- [ ] Build **Skills A + C**.
- [ ] Generalise into a **reusable client template**.
- [ ] Source links for **286+** as each publishes (newest = top of iTunes lookup + SpotifyScraper `.episodes[0]`; match by exact title; verify; push to Notion; then it flows to the page).

---

*Companion docs in this repo: `PROCESS.md` (the step-by-step build pipeline), `HANDOFF.md` (session pickup), `EPISODE-PAGE-TEMPLATE.md` (the locked page spec). Companion Claude memory: `project_tng_platform_links` (the link-sourcing method + full status). This doc is the strategic/overview layer that ties them together.*
