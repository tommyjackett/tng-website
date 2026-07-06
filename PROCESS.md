# FULL PROCESS — from new episode to live page

*The end-to-end pipeline, so it never lives only in anyone's head. Last updated: 6 July 2026.*

**Reading order note (fixes the two-READMEs confusion):** in `Brain/Vidpod/clients/TNG/Website Build/` there are two overview docs — **`RESUME.md` is the pickup point and wins on any conflict**; `README.md` is older background (mission + early decisions) kept for context only. Per-episode mining steps live in `schema/EPISODE-PROCESSING-GUIDE.md`.

---

## Stage 1 — Source content (per new episode)

1. Show notes confirmed in Notion (titles, chapters — the episode's editorial layer).
2. Full transcript appended to `Brain/Vidpod/clients/TNG/Mine/tng-transcripts.md` under a `## EP N | Title | Date` header.
   - If a transcript section looks thin/compressed (the EP 274 case): pull the audio from Drive → AssemblyAI → replace that section with the true verbatim transcript.

## Stage 2 — Mine the episode (the content engine, in `Website Build/`)

Follow `schema/EPISODE-PROCESSING-GUIDE.md` + `schema/EXTRACTION-RULES.md`. In short:

1. Extract deep moments from the transcript → `episodes/episode-N-DEEP.json` (schema 2.0). Transcript is the entry point; Notion chapters are a cross-check, not the boundary.
2. Gates, in order — ALL must pass (they replace per-episode sign-off):
   - `schema/normalize.py` (uniform shape)
   - `schema/validate.py` (shape gate, hard-fail)
   - `schema/voice_lint.py` (verbatim quotes + house style, hard-fail)
   - `schema/health_check.py` (report card + taxonomy health + tag integrity)
3. Go-live gate: 0 homeless, 0 invented tags, 0 doppelgängers, coherence flags reviewed.

## Stage 3 — Compile site data

1. `python3 schema/build_site_data.py` → regenerates `site-data/catalogue.json`, `search-index.json`, `entities.json`.
2. Copy the three JSONs into this repo's `data/` folder.

## Stage 4 — Generate the page (this repo)

1. `python3 scripts/build_episode.py N` — builds `episode-N.html` from the master template (`episode-263.html`) applying every rule in `EPISODE-PAGE-TEMPLATE.md` (title modes, chapters, questions, discover-more selection, transcript). It validates before writing and refuses on any violation.
2. Quick local preview if the change warrants it.

## Stage 5 — Ship

1. `git add episode-N.html && git commit`
2. `./scripts/push-live.sh episode-N.html` — pushes, waits for the Actions deploy (auto-retries), verifies live == local byte-for-byte.

## Stage 6 — Review

1. Add the page to `LIVE-PAGES.md` (with today's date) and give Tommy the live link.
2. Tommy's ten-second spot-check: tap the FIRST and LAST chapter — the video must land on the right words (catches transcript-vs-upload offset, the one failure automation can't see).

---

**Key repo files:** `EPISODE-PAGE-TEMPLATE.md` (the locked page spec) · `scripts/build_episode.py` (generator) · `scripts/push-live.sh` (ship + verify) · `LIVE-PAGES.md` (review list) · `HANDOFF.md` (session pickup).
