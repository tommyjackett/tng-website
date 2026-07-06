# TNG WEBSITE — HANDOFF (read this first to resume)

*Written 4 July 2026. This is the pickup point for the WEBSITE work. The content-ENGINE state lives in `Brain/Vidpod/clients/TNG/Website Build/RESUME.md` (24 episodes 263–286 processed to the deep standard; 670 moments; site-data compiled).*

---

## WHERE WE ARE
- **Repo:** `tommyjackett/tng-website` (public, GitHub Pages, deploy-from-branch `main` / root). Local: `~/Desktop/TOMMY AI/repos/tng-website`.
- **EP 263 is the FIRST live episode-page template (v2, approved-in-progress).**
  - Live: **https://tommyjackett.github.io/tng-website/episode-263.html**
  - File: `episode-263.html` — self-contained (styles + inline episode data + JS). This IS the template; other episodes become data swaps.
  - `assets/`: `tng-logo.png` (trimmed to 2.44:1 — full "THE NUMBERS game"), `inovayt-white.png`, `future-advisory-white.png`, `vidpod-white.png`, `numbers-wordmark.png`.
  - `data/`: `catalogue.json`, `search-index.json`, `entities.json` (263–286).
  - No `index.html` at root yet (Tommy's call — no homepage until we design it).

## THE TEMPLATE (what's built in episode-263.html)
**LOCKED 5 Jul 2026 — the full spec with strict per-element rules lives in `EPISODE-PAGE-TEMPLATE.md`. New pages follow that document, never re-decide.** Summary of what's on the page:
Sticky navbar (logo + "All episodes") → **carousel-exact hook title** (purple setup bars + one mint payoff bar, from `design.md`) → **clean YouTube facade** (thumbnail + semi-transparent play button, NO YouTube chrome; loads real player on tap) → meta (date + host tags) → Listen buttons (YouTube/Spotify/Apple) → **collapsible dropdowns**: Summary, What this episode answers, Chapters, Full transcript → tapping a chapter/question **seeks the player WITHOUT yanking to top** (only nudges if off-screen) → CTA ("Get in touch") → footer (Brought to you by Inovayt + Future Advisory, Produced by VIDPOD).

## BRAND (source of truth: `Brain/Vidpod/clients/TNG/Carousel/design.md`)
- Gradient **#585af3 → #2c1b8a**; accent mint **#7ad9a8** (one accent, restraint).
- Fonts: **Anton** (display/headline) + **Inter** (body) — the closest free web match to Helvetica Neue Black Condensed (their reel font; no web kit exists). Loaded via Google Fonts CDN.
- No em dashes. Numbers-forward. Dark/premium = YouTube-thumbnail energy.

## OPERATIONAL (so pushing/previewing just works)
- **Token:** `~/Desktop/TOMMY AI/.secrets/TNG WEBSITE_github-token.txt` (classic PAT, `public_repo` + `workflow` scopes).
- **Ship a change:** commit, then run `scripts/push-live.sh` (local tooling, gitignored). It pushes, polls the live URL until it matches the local file byte-for-byte, and re-dispatches the deploy workflow if a deploy stalls. Never re-push to fix a stuck deploy.
- **Deploys run through OUR workflow** `.github/workflows/deploy-pages.yml` (Pages build_type=workflow since 5 Jul 2026). It queues deploys and auto-retries transient failures inside the run — the old branch-based pipeline's "Deployment failed, try again later" emails are gone. The site always keeps the last good deploy (never goes down).
- **Preview:** `preview_start "tng-site"` (config in `Brain/Vidpod/clients/TNG/.claude/launch.json`, serves the repo on :8137) → open `/episode-263.html`. Or Tommy's `Tools/Desktop Phone Preview/preview.html` (paste the live URL; shows desktop + iPhone).

## OPEN / NEXT (in order)
1. **Tommy reviews EP 263 on mobile** and gives notes → apply them.
2. Parked details to wire: **direct Apple/Spotify show links**; **"Get in touch" destination** (contact page TBD); the **mint-highlight rule** for the title (which words go mint per episode — needs a system so it's consistent, not per-hand).
3. **Templatise:** externalise the inline episode data → `data/episodes/263.json`; make one generic `episode.html?ep=N` that reads it; extend `build_site_data.py` to emit per-episode page JSONs (summary + chapters + questions + transcript). Then roll across 264–286.
4. **Later:** the dynamic homepage (topic search + custom moment collections that build YouTube playlists) — v1's moment-and-seek mechanic is the seed.

## WORKING-STYLE REMINDERS (Tommy's, hard-won)
- Flag reasoning + intended action BEFORE consequential/irreversible steps (source-file edits, deploys). Don't build design without sign-off.
- Words before pixels; match the carousel exactly; be his eyes/ears on cross-episode threads.

## HOW TO RESUME
Start a new session in this project and say:
> "Read `repos/tng-website/HANDOFF.md` and `Brain/Vidpod/clients/TNG/Website Build/RESUME.md`, then continue the TNG website — EP 263 template review + roll-out."
