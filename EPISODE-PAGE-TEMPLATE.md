# EPISODE PAGE TEMPLATE — the locked spec

*Locked 5 July 2026 against `episode-263.html` (the master template file). Every new episode page is created by following THIS document — never by re-deciding anything. If a rule here conflicts with an older doc, this document wins. Change the rules only by changing this file first.*

**How a new page gets made:** copy `episode-263.html`, replace only the data slots listed below, run the validation checklist at the bottom, push via `scripts/push-live.sh`. No design decisions. No new CSS. No hand-written content.

---

## 0. DATA SOURCES (where everything comes from)

| Source | What it provides |
|---|---|
| Engine episode data (`episode-N-DEEP.json`, compiled into this repo's `data/*.json`) | episode number, title, date, youtubeId, duration, hosts, summary, moments (chapters, questions, timestamps, topics, standalone scores) |
| `data/catalogue.json` | per-episode card data for Discover More (title, date, youtubeId, thumbnail) |
| `data/search-index.json` | per-moment topic/subtopic tags that power Discover More matching |
| Fixed template constants | nav, listen links, SpeakPipe widget id, sponsor links, footer |

**Iron rule:** every episode-specific value on the page comes from the engine's verified data. Nothing is typed by hand — the engine's transcript-verified data is the single source of truth for all timestamps and text. (Notion feeds the engine; pages never take content from Notion directly.)

---

## 1. HEAD

- `<title>`: `EP {N} · {Full Title} | The Numbers Game`
- `<meta name="description">`: the episode summary, truncated at a sentence boundary at ≤160 characters.
- Fonts: Anton + Inter via Google Fonts (fixed block, do not touch).

## 2. NAV BAR (fixed template block)

- Logo left → `index.html`. Height 36px.
- Desktop (>720px): `HOME · EPISODES · ABOUT · CONTACT` inline right, uppercase Inter 13px/600, muted → white on hover, all on one baseline.
  - **About is a hover group**: dropdown with `The show` → `about.html`, `Nick Reilly` → `nick-reilly.html`, `Jason Robinson` → `jason-robinson.html`.
- Mobile (≤720px): hamburger button → solid overlay dropdown (`#180f4a`) listing Home / Episodes / About / (indented) Nick Reilly, Jason Robinson / Contact. Overlays content, never pushes it down.
- **HOME rule:** inner pages (all episode pages) include HOME; the homepage template omits it. Enforced by which template a page is stamped from.

## 3. EPISODE IDENTITY + TITLE LOCKUP

- **EP tag**: black `#0a0a0a` block, white Anton 13.5px, text `EP {N}`, overlapping the title's top-left corner (offset -6px left, -7px down). Data: episode number.
- **Title rule (automatic, never hand-picked) — every page is two-tone. Two modes:**
  - **Mode 1 — title has a natural break** (first ` | ` or `: `; else first `? ` or `. `, punctuation staying on the hook): front phrase = **hook** → `<h1>`, purple band, Anton `clamp(28px, 7vw, 52px)`, letter-spacing -0.5px; back phrase = **payoff** → mint band, dark text, Anton `clamp(16px, 4vw, 24px)`, 8px below.
  - **Mode 2 — no break in the title**: split at the word boundary nearest the title's character midpoint. First half → purple band; second half → mint band, dark text — **both at full hook size**, stacked with an 8px gap (markup: two `.hkrow` block spans inside the `<h1>`, second segment classed `mintseg`). The split is maths, so the same words are mint on every device.
  - A single-word title (back-catalogue edge case) renders purple only.
- Band mechanics (do not change): highlight is a background band trimmed to 87% (hook) / 88% (payoff) of line height, vertically centred; wraps per-line via `box-decoration-break: clone`; hook and payoff first letters align via the shared `--inx` inset.
- **Line balancing (`text-wrap: balance` on hook and payoff):** when a title wraps, the browser distributes words evenly across the lines — no one-word last lines (widows), at any viewport, for any length. Line breaks are never hand-picked; balancing is the only wrapping control.
- Verified across all 24 current titles: 23 render as a 1–2-line hook. Guidance for future title writing: keep the pre-break part under ~65 characters (only EP 283 exceeds it → 3 lines, still clean).

## 4. PLAYER

- Square corners, 16:9, full column width.
- Facade: `https://i.ytimg.com/vi/{youtubeId}/maxresdefault.jpg` + circular play button. The real YouTube player loads only on first interaction.
- Every chapter/question/facade tap calls `startAt(seconds)` → seeks THIS player. Scroll behaviour: nudge into view only if the player is off-screen — never yank to top.
- Data: `youtubeId`.

## 5. EXPLORE TABS (sticky mode switcher)

- Row of three: `SUMMARY` (default open) · `CHAPTERS · {count}` · `QUESTIONS · {count}`. Counts are computed from the data arrays, never typed.
- Style: Anton 14.5px; resting = purple bg / white text; active = mint bg / black text. Square corners.
- Sticky at `top: 58px` (under the nav) with blurred backdrop. Tapping swaps the visible panel in place — content above never moves.

### 5a. SUMMARY panel
1. Summary paragraph — the episode `summary`, verbatim from the data.
2. **Voice note ask**: mint pill button `SEND US A VOICE NOTE` (mic icon). Tapping reveals the purple recorder card:
   - Intro copy (fixed): *"We'd love to hear from you. You can leave up to a 90 second voice note for us to play on the show: a question, some feedback, or a topic you want covered."* + `×` close.
   - SpeakPipe inline iframe, widget id `hhq6kzggsx7zpcsvakgxfrzun3zidpde` (same on every page), height 200, full panel width.
3. **Facts block** (hairline above):
   - `RELEASE DATE` — format `9 February 2026` (D Month YYYY), from `date`.
   - `HOSTS` — names as mint links → `nick-reilly.html` / `jason-robinson.html`.
   - `GUEST` — row rendered ONLY when the episode has a guest; omitted otherwise.

### 5b. CHAPTERS panel
- Hint line (fixed copy): *"Jump straight to the part you need."*
- **Derivation rule:** group the episode's moments by their `chapter` name; each chapter's timestamp = the earliest `startSec` in its group; list chronologically; prepend `Intro` at `00:00` when the first chapter starts after 0s.
- Display: mint `MM:SS` + title per row; tap seeks the player.

### 5c. QUESTIONS panel
- Hint line (fixed copy): *"Real questions this episode answers. Tap one to hear the answer."*
- **Selection rule:** take all moments with a non-empty `questionAsked`; rank by `standalone` score (highest first); keep the top 10; display in chronological order. Question wording verbatim from the data.
- Tap seeks the player to that moment's `startSec`.
- (EP 263's live list is a grandfathered hand-polish from template development. All new pages use the rule above. Any future override must be noted in the page's commit message.)

### Timestamp integrity (the jumps-always-work rule)
1. **Single source of truth:** all seconds come from the engine's transcript-verified moment data.
2. **Build validation (hard gate):** every timestamp must be a number, `0 ≤ t < episode duration`, and each list (chapters, questions) strictly increasing in display order. Any violation = the page does not publish.
3. **Publish spot-check (human, ~10s):** on the live page, tap the FIRST and LAST chapter and confirm the video lands on the right words. Catches constant offset between transcript and the actual YouTube upload (trims, re-uploads) — the one failure automation can't see.

## 6. EPISODE TRANSCRIPT

- One collapsed square `details` row labelled `Episode transcript`, below the tabs.
- Content: the full verbatim transcript from the engine, one `<p>` per speaker turn: mint uppercase `SPEAKER · MM:SS` label + text.
- Always collapsed by default. Exists primarily for search engines; never remove it.

## 7. LISTEN ROW

- Desktop: `LISTEN ON` label + three pills, centred. Mobile: label hidden, three compact pills on ONE row (padding 10/13, font 11px, icons 16px).
- Pills: `SPOTIFY` (mint, Spotify mark) · `APPLE` (mint, Apple Podcasts app mark) · `SUBSCRIBE` (purple, YouTube mark).
- Links: Spotify/Apple currently search URLs — **TODO: replace with direct show URLs on every page the moment Tommy supplies them.** Subscribe → `https://www.youtube.com/@thenumbersgamepodcast?sub_confirmation=1`.

## 8. END-OF-EPISODE DIVIDER

Hairline + large gap after the listen row. Meaning: above = this episode, below = the show. Never remove.

## 9. DISCOVER MORE (recommendations)

- Header: `DISCOVER MORE` as a mint block (Anton 14.5px, same style family as tabs). No hint line.
- **Exactly 6 cards.** Selection algorithm, in order:
  1. **Eligible pool:** episodes with `date` ≤ today (released only), excluding this episode. Never an unreleased episode, never itself, never duplicates.
  2. **Fingerprint matches first:** score every eligible episode by moment-level subtopic overlap (cosine similarity of moment-count-per-subtopic vectors, from `search-index.json`). Episodes scoring **≥ 0.5** fill slots first, highest score first. Their mint footer line = `Also covers: {top shared subtopic}` (the subtopic with the largest overlap product).
  3. **Top-up with recency:** remaining slots take the newest released episodes not already picked. Their mint footer line = release date (`29 June 2026`).
  4. **The mint line only ever states a fact** — a genuinely shared topic or a real date. Never invent a connection. (Rationale: real matches in this catalogue score 0.85+, noise scores ≤0.15 — the 0.5 threshold has huge margin on both sides.)
- **Card anatomy (fixed):** thumbnail (`hqdefault.jpg`, 16:9 cover, square corners) → title (hook part only, before the title break) → footer row pinned to card bottom: **date/reason bottom-LEFT (mint), EP tag bottom-RIGHT (black block)**. Whole card links to `episode-{N}.html` — a PAGE, never a timecode, never YouTube.
- **Layout:** horizontal swipe strip on ALL screen sizes; cards `flex-basis 56%, max-width 232px`, scroll-snap. Mint position dots below, one per card, auto-hidden whenever the strip doesn't actually scroll. Dots track scroll position.

## 10. BROUGHT TO YOU BY

- Centred label + two logos (34px tall), 68px below Discover More, 48px above the footer line (line sits halfway to PRODUCED BY).
- Links (new tab): Inovayt → `https://www.inovayt.com.au/` · Future Advisory → `https://futureadvisory.com.au/`.

## 11. FOOTER

- `PRODUCED BY` + VIDPOD logo → `https://www.vidpod.com.au/` (new tab).
- `© {year} The Numbers Game`.

---

## LAYOUT CONSTANTS (global)

- Page frame `--wrap: 1280px`, side padding 36px (22px at ≤720px). Nav spans the full frame.
- Content column `main` capped at `--col: 960px`, centred (player renders ~888px wide on desktop).
- Single breakpoint: **720px** separates mobile and desktop behaviour everywhere.
- Colours: purple `#585af3`, mint `#7ad9a8`, black blocks `#0a0a0a`, nav/dropdown solid `#180f4a`. Fonts: Anton (display), Inter (body). Corners: square everywhere except pills (buttons) and the play button.

## MOBILE vs DESKTOP SUMMARY

| Element | Mobile (≤720px) | Desktop (>720px) |
|---|---|---|
| Nav | logo + hamburger overlay menu | logo + HOME EPISODES ABOUT(▾) CONTACT inline |
| Listen row | 3 compact pills, one row, no label | label + full-size pills, centred |
| Discover More | swipe strip + mint dots | same strip, ~3 cards visible, dots hide if it fits |
| Title | scales via vw clamps | caps at 52px/24px |
| Everything else | identical behaviour | identical behaviour |

## LINK MAP (every destination on the page)

| Element | Destination |
|---|---|
| Logo, HOME | `index.html` (homepage, future) |
| EPISODES | `episodes.html` (future) |
| About ▾ | `about.html`, `nick-reilly.html`, `jason-robinson.html` (future) |
| CONTACT | `contact.html` (future) |
| Host names in facts | `nick-reilly.html` / `jason-robinson.html` |
| Discover More cards | `episode-{N}.html` |
| Spotify / Apple | show URLs (TODO — currently search links) |
| Subscribe | YouTube channel with `?sub_confirmation=1` |
| Sponsors / VIDPOD | external sites, new tab |
| Chapters / questions / facade | the on-page player (seek), never external |

## NEW-PAGE CHECKLIST (run every time, in order)

1. Copy `episode-263.html` → `episode-{N}.html`. Replace ONLY: title tag, meta description, EP tag, hook/payoff, youtubeId (facade image + JS `VIDEO`), summary, CHAPTERS array, QUESTIONS array, transcript block, facts (date, hosts, guest-if-any), Discover More cards (run the selection algorithm), copyright year if changed.
2. Title split follows §3 exactly — no hand-chosen line breaks or mint words.
3. Chapters/questions derived by §5b/§5c rules — no hand-curation without a noted override.
4. Validation gate (§5, timestamp integrity #2): ranges + ordering pass, all links resolve to the patterns in the link map, exactly 6 Discover More cards, all from released episodes.
5. Push via `scripts/push-live.sh episode-{N}.html` (verifies live == local byte-for-byte).
6. Live spot-check: first + last chapter jump lands on the right words; swipe the Discover strip; open the voice recorder.

**Never:** em dashes in copy · invented "similar" claims · unreleased episodes in Discover More · timecode links that leave the page · hand-typed timestamps · new CSS per episode.
