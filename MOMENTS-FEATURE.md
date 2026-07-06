# MOMENTS FEATURE — product spec ("Skip to the good bits")

*Documented 6 July 2026. Deployed as its own page, `adventure.html` ("Choose Your Own Adventure"), since the 6 Jul homepage restructure; the homepage carries an entry card. This is a portable VIDPOD product: **content-engine data + interest picker + moment player + episode exits**. The Huddle (Help at Hand) was v1; this is v2. Change behaviour only by changing this spec first.*

**What it does:** a visitor lands on a show with hundreds of episodes. They pick the topics they're into; the feature pulls up the standout moments on exactly those topics and plays them right there — jumping to the exact seconds inside episodes, not to episode lists. It serves both newcomers (taste the show) and existing listeners (mine the back catalogue).

---

## 1. Data contract (what any show must supply)

Two static JSON files, fetched client-side. No backend, no database.

| File | Required fields |
|---|---|
| `catalogue.json` (one row per episode) | `episodeNumber`, `title`, `date` (ISO), `youtubeId` (the full episode video) |
| `search-index.json` (one row per moment) | `momentId`, `episodeNumber`, `youtubeId`, `startSec`, `endSec`, `durationSec`, `topic`, `subtopic`, `standalone` (0–100 quality score), `questionAsked`, `description` |

**Quality prerequisites (upstream, non-negotiable):** timestamps machine-verified against transcripts; `questionAsked` = *what the moment answers* (framing, but the answer must genuinely be at that timestamp); `description` = factual summary of what's said; both through house-style gates. The feature's honesty is only as good as this data.

## 2. Tunable constants (per deployment)

```
MIN_SCORE = 80    // moment quality floor
MIN_DUR   = 60    // seconds — substantial moments only (short clips are for social, not this player)
CHIP_MIN  = 5     // a topic earns a chip only with this many qualifying moments
LEAD_CHIPS= 8     // topics shown before "+ more"
SERVE     = 5     // moments per deal
PER_SUB   = 2     // variety cap per subtopic within a deal
```

## 3. How it functions, step by step

1. **Load:** fetch both JSONs → the *pool* = moments with `standalone ≥ MIN_SCORE` AND `durationSec ≥ MIN_DUR` AND from **released** episodes (`date ≤ today`, browser-local). Unreleased episodes never surface anywhere.
2. **Topic chips:** pool grouped by topic. A topic gets a chip only with `CHIP_MIN`+ moments (never let anyone pick into an empty plate). Chips ranked by inventory, each showing its count (`PROPERTY · 17`). Top `LEAD_CHIPS` visible, rest behind `+ more topics`. Mint resting / purple selected.
3. **Get specific:** selecting a topic unfolds its subtopic chips (only when it has 2+), with counts. Picking none = the whole topic. Outline resting / purple selected.
4. **Serve (the button):** eligible = pool ∩ selected topics/subtopics, minus everything already served this session. Rank by `standalone` desc. Deal up to `SERVE`, capping `PER_SUB` per subtopic **except** subtopics the user explicitly selected (you asked for that dish, you get the whole dish).
5. **Display swap:** the resting placeholder (see §5) swaps for the real player + cards on first serve. **Card anatomy:** number `01` → the question (the hook: *what this moment answers*) → footer: subtopic tag + duration. **Now Playing line:** `Now playing 01 · 1m 18s · From EP 266 — watch the full episode →` with the moment's `description` beneath in white (context once committed).
6. **Player mechanics (the chrome-stripping trick):** no YouTube exists until play intent. Resting: our facade showing the current moment's episode thumbnail + mint play. First real tap creates the `YT.Player`; every moment plays via `loadVideoById({videoId, startSeconds, endSeconds})` — user-gesture = autoplay allowed, playback stops at `endSec`. Never `cueVideoById` after the facade exists (cueing shows YouTube's chrome).
7. **Show me more:** APPENDS the next `SERVE` by rank — numbering continues (06, 07…), the playing moment is untouched, nothing ever repeats (session memory). When the selection runs dry: button hides, note reads "That's the best of it for now. Try another topic."
8. **Live re-picking:** chips stay active above the player; changing them re-deals immediately.
9. **Clear and start again:** the serve button is a two-state machine — mint `SHOW ME THE MOMENTS` (pick state) → outline `Clear and start again` (active state). Clear resets selection, session memory, queue; destroys the player; restores the placeholder. Deselecting the last chip does the same.

## 4. State summary

| State | What's visible |
|---|---|
| Resting | placeholder mock (screen + caption + ghost cards); button disabled |
| Picking | chips selected (purple); subchips unfolded; button live (mint) |
| Served | player + N cards; button = Clear (outline); Show me more if pool remains |
| Extended | appended cards, numbering continues |
| Dry | more-button hidden, "best of it for now" note |
| Cleared | back to Resting |

## 5. The placeholder (resting state = exact preview)

Deliberately minimal (simplified with Tommy, 6 Jul): a 16:9 screen using the hosts still under the purple tint, **heavily blurred** (image + tint fused in ONE layer so edges can't mismatch; the strong blur both says "placeholder" and differentiates from the page banner, which uses the same still lightly blurred), with a **single centred caption** in plain sans: `YOUR MOMENTS WILL PLAY HERE`. Nothing else — no play indicator, no ghost cards, no explainer line.

## 6. Layout

- **Desktop:** two even panes. Left = titled control column (black-block heading `SKIP TO THE GOOD BITS`, sell copy, steps 01 SELECT A TOPIC / 02 GET SPECIFIC / 03 GET YOUR MOMENTS + button). Right = the screen. Nothing spans both panes.
- **Mobile:** single stack in the same DOM order — title, sell, 01, 02, 03, button, then the screen and cards below.
- Grid items carry `min-width:0` (the card strip otherwise blows the column wide).

## 7. Honesty rules (the product's soul)

Released episodes only · chips only with real inventory behind them · every count and mint line states a fact · questions must genuinely be answered at their timestamp (upstream gates) · no dead ends — dry states degrade gracefully · the browsing experience doubles as a data audit (mis-tags and weak descriptions get SEEN — log them for engine review, e.g. the EP 276 FBT/Company Setup tag).

## 8. Porting to another show

1. Produce the two JSONs from that show's content engine (schema in §1) — this is the hard part and the moat.
2. Swap: brand tokens (colours/fonts), constants (§2), the placeholder still, copy strings, channel links.
3. Episode exits: link to episode pages if the show has them; otherwise point at YouTube timestamps or hide the exit.
4. The section is self-contained (HTML + CSS + JS in one block) — it lifted cleanly out of `index.html` into its own page (`adventure.html`, 6 Jul 2026), proving the portability claim.

## 9. Known limits

- YouTube's minimum player chrome shows *during* playback (their terms; pre-play is fully ours).
- No autoplay-chaining between moments in v1 (a "keep playing" toggle is possible later — chain `loadVideoById` on the `ENDED` event).
- On the release day of a new episode, its moments/counts appear automatically — but its episode page must be built the same day or exits 404 (the page-build step in PROCESS.md).

## 10. Scale plan (back-catalogue growth)

Everything adapts automatically as episodes are mined — chips, counts, subtopics, serve depth all recompute at load; new topics appear when they cross `CHIP_MIN`. The only manual step is PROCESS.md stage 3 (copy refreshed JSONs into `data/` and push). **One planned optimisation:** `search-index.json` is 129KB gzipped at 24 episodes but ~1.5MB at 280. Before that bites (trigger: gzipped size passes ~300KB), add a build step emitting `moments-lite.json` with only this feature's 11 fields (49KB now, ~570KB at full scale; can be split per-topic and lazy-loaded if needed). No design change required.
