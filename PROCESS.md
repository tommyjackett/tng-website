# FULL PROCESS — from new episode to live page

*The end-to-end pipeline, so it never lives only in anyone's head. Source+mine stages current; **publish half rewritten 23 Jul 2026** (now additive / clean-URL — see `PUBLISH-EPISODE-RUNBOOK.md`).*

**Docs:** front door + state + §8 tooling = **`Website Build/TNG-MASTER-STATUS.md`**. Mining = `schema/EPISODE-PROCESSING-GUIDE.md` + `ENGINE-STATE.md`. Publishing = **`PUBLISH-EPISODE-RUNBOOK.md`**.

## TWO FLOWS — new episode vs. old back-catalogue (this is the confusion, resolved)
- **NEW episode (the weekly drop):** run the FULL pipeline — **Stage 1** (source: show notes + transcript) → **Stage 2** (mine through the schema → `episode-N-DEEP.json`, gated green) → **Stage 3** (publish, additive).
- **OLD / back-catalogue episode:** the transcript + DEEP are ALREADY mined → **SKIP Stages 1–2, go straight to Stage 3** (publish). That's the back-catalogue batching (56/60 done this way).
- **Both share the identical Stage 3.** The only extra for a new episode: Stages 1–2 first, plus sourcing its platform links (old eps' links were already logged).

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

## Stage 3 — Publish to the live site (ADDITIVE — REPLACES the old "compile + generate + ship")

⛔ The old approach (`build_site_data.py` → copy all 3 JSONs → `episode-N.html`) is **BANNED against live** now: `build_site_data.py` recompiles EVERY episode and 404s the library. Publishing is **per-episode additive**. Follow **`PUBLISH-EPISODE-RUNBOOK.md`** — in short:

1. `scripts/check_transcript.py N` — transcript-quality GATE (coarse timecodes ≥45s median / >15% Unknown → re-transcribe, don't publish).
2. `scripts/merge_episode.py N` — **ADDITIVE** merge of just N into `data/catalogue.json` + `search-index.json` + `entities.json` (preserves every other episode; NEVER `build_site_data.py`).
3. `scripts/enrich_platform_links.py --ep N --write` — source N's Spotify+Apple links onto the catalogue (new episodes only — old eps' links auto-attach; skip for the "publish fast, backfill later" speed play).
4. `scripts/build_episode.py N` — builds **`{slug}.html`** (clean URL) + `episode-N.html` redirect stub from the master template (`episode-master-template.html`); hosts auto-link; validates + refuses on violation.
5. `scripts/verify_episode.py N` → `scripts/link_check.py` → `scripts/push-live.sh {slug}.html`.

**Automatic (no extra steps) — these all derive from the Stage-3 data merge:**
- **Choose-Your-Own-Adventure** — `adventure.html` pools the episode's top moments from `search-index.json`. Nothing to do.
- **Topic/subtopic filters + Guests filter + guest byline + SEO entity pages** — all data-driven from the merge.

## Stage 4 — Review + record

1. Tommy's spot-check: tap the FIRST and LAST chapter — the video must land on the right words (catches transcript-vs-upload offset, the one failure automation can't see).
2. Update `TNG-MASTER-STATUS.md` §2 (count + `origin/main` hash) and tick the episode in `PUBLISH-TRACKER.md`.

---

**Key files:** `PUBLISH-EPISODE-RUNBOOK.md` (publish how-to) · `TNG-MASTER-STATUS.md` §8 (every tool, verified) · `EPISODE-PAGE-TEMPLATE.md` (page spec) · `schema/EPISODE-PROCESSING-GUIDE.md` (mining).
