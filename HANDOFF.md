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
  - `index.html` = the homepage, rebuilt 6 Jul late evening as ONE SCREEN: video banner with a play-once title sequence (logo pop → "5 years." → "150+ hours. 280+ episodes." → show lockup HOLDS) + pulsing scroll cue → WAYS TO EXPLORE THE SHOW (three coloured cards that pop in staggered: mint Latest episode / purple Choose your own adventure / black Explore every episode → YouTube channel until episodes.html exists) → footer. **LOCKED (Tommy): the video banner's bottom fade-out (mask-image, solid to 68%) must NEVER be removed.** No about section (lockup carries it); BTS photo band parked awaiting a photo from Tommy.
  - `adventure.html` = **Choose Your Own Adventure** (LIVE 6 Jul) — the moments feature as its own page/product (spec: `MOMENTS-FEATURE.md`). All 22 released 2026 episode pages live too.

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

## OPEN / NEXT (updated 6 Jul 2026, late evening)
1. ✅ DONE — all 22 released 2026 episodes live (generator + audit, see LIVE-PAGES.md).
2. ✅ DONE — Homepage restructured as the three-door ROUTER and `adventure.html` launched (Tommy's model: latest episode / choose your own adventure / explore every episode — siloed experiences). All copy on both pages is DRAFT pending Tommy's voice pass. Banner title-sequence wording ("5 years. 280+ episodes.") also draft.
3. **Episodes page** (`episodes.html`: search + topic filters, grid anatomy already proven) — when built: repoint homepage card 3 (currently → YouTube channel) and it fixes the nav EPISODES 404 on every page. Then **Contact** (form + voice-note component) → **About + host pages**. Tommy explicitly parked all of these on 6 Jul — do NOT start without his word.
4. Tommy wants to keep fleshing out the adventure page as a product (his words: "a real solid product"). Ideas discussed: topic deep-links (?topic=property), share-a-moment URLs, surprise-me button, ask-the-show search over questionAsked.
5. Parked: direct Apple/Spotify show URLs; engine review list (EP 276 FBT/Company Setup mis-tag, weak moment descriptions Tommy spots); back-catalogue mining (all features auto-scale; moments payload optimisation trigger documented in MOMENTS-FEATURE.md §10).

## WORKING-STYLE REMINDERS (Tommy's, hard-won)
- **Pushing after commit is STANDARD (Tommy, 6 Jul 2026):** edit → quick local sanity check only if visual/layout → commit → `scripts/push-live.sh <file>` immediately. Never stop at a local commit or ask whether to push — Tommy reviews on the LIVE site, not previews. Only hold if he explicitly says "don't push yet".
- One change live before the next, or batch several edits into a single push. If a deploy stalls the script handles it — never re-push to fix it.
- After each push: give the live link + a short summary of exactly what changed.
- Specs are law: EPISODE-PAGE-TEMPLATE.md, MOMENTS-FEATURE.md, PROCESS.md, this file. A new rule agreed with Tommy gets written into the relevant spec in the same push.
- Words before pixels; don't build design without sign-off; match the carousel exactly; be his eyes/ears on cross-episode threads.

## HOW TO RESUME
Start a new session in this project and say:
> "Read `repos/tng-website/HANDOFF.md` and `repos/tng-website/PROCESS.md`, then continue the TNG website roll-out."
