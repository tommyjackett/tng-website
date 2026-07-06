# TNG WEBSITE — HANDOFF (read this first to resume)

*Written 4 July 2026. This is the pickup point for the WEBSITE work. The content-ENGINE state lives in `Brain/Vidpod/clients/TNG/Website Build/ENGINE-STATE.md` (24 episodes 263–286 processed to the deep standard; 670 moments; site-data compiled).*

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

## OPEN / NEXT (updated 6 Jul 2026, evening)
1. ✅ DONE — all 22 released 2026 episodes live (generator + audit, see LIVE-PAGES.md).
2. **IN PROGRESS — Homepage (`index.html`)**: hero (podcast-art app icon + about + latest ep) and the moments feature ("Skip to the good bits", spec = `MOMENTS-FEATURE.md`) are built and iterated live with Tommy; NOT yet finished — continue refining with his notes (copy passes pending; top-of-page concept still open; heading block just switched black→purple).
3. **Episodes page** (search + topic filters) → **Contact** (form + voice-note component) → **About + host pages**.
4. Parked: direct Apple/Spotify show URLs; engine review list (EP 276 FBT/Company Setup mis-tag, weak moment descriptions Tommy spots); back-catalogue mining (all features auto-scale; moments payload optimisation trigger documented in MOMENTS-FEATURE.md §10).

## WORKING-STYLE REMINDERS (Tommy's, hard-won)
- Flag reasoning + intended action BEFORE consequential/irreversible steps (source-file edits, deploys). Don't build design without sign-off.
- Words before pixels; match the carousel exactly; be his eyes/ears on cross-episode threads.

## HOW TO RESUME
Start a new session in this project and say:
> "Read `repos/tng-website/HANDOFF.md` and `repos/tng-website/PROCESS.md`, then continue the TNG website roll-out."
