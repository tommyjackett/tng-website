# TNG Website — Status & Clean-URL Migration Plan
**Written 20 Jul 2026, before starting the clean-URL work. Nothing below is done yet unless marked ✅ LIVE.**

---

## PART 1 — Where everything stands right now (so we don't lose context)

### ✅ Done & LIVE on thenumbersgamepodcast.com.au
| Thing | State |
|---|---|
| **EP 286** (Pokemon Cards vs Bitcoin…) | Published live: video + Spotify player + Apple/Spotify links. Fixed the 404 that was on the home page. |
| **New site-wide footer** | Rolled out to **all 52 live pages** (44 episode pages + home, episodes, adventure, about, contact, nick-reilly, jason-robinson, marty-vidakovic). 3-col **Follow us on · Brought to you by · Produced by** + social icons + a subtle **☰ Menu** dropdown (opens to a row on desktop / stack on mobile). |
| **Footer spacing fix** | First rollout wrongly flattened each page's tuned footer top-margin (episodes 68px, about/contact 90px, adventure 100px, episodes-lib 80px, hosts 52px, home 0) → jammed the footer against content. **Fixed** by restoring each page's original margin/padding from git; only the inner footer content is new. |
| **Marty Vidakovic host page** | `marty-vidakovic.html` + his photo (`assets/Marty-Vidakovic-4.jpg`) are LIVE; Marty is in the footer menu site-wide. |
| Latest deploy | commit `98d1060`. GitHub Pages healthy. |

### ⏳ Built but NOT pushed — waiting on Tommy
**EP 138 — the first audio-only back-catalogue episode** ("Where Have All the Accountants Gone?"). Everything is built + gated green + verified locally, deliberately held for Tommy's review:
- **Page:** `where-have-all-the-accountants-gone.html` (untracked, local only — live URL is 404 by design). Spotify player hero + working chapter-seek, clean title-only URL.
- **Catalogue:** EP 138 added to **local** `data/catalogue.json` (audioOnly, slug, thumbnail) — NOT in the live catalogue.
- **Thumbnail:** `assets/tng-audio-only-thumbnail.webp` (the generic 3-host audio cover) — untracked.
- **episodes.html audio-wiring** (uses `e.thumbnail`/`e.slug`) IS already live (went out with the footer rollout) — harmless, nothing audio in the live catalogue yet.
- **To ship EP 138:** push the page + catalogue.json + the webp together (one deploy). Marty page already live.

### 🔒 Decisions locked this session
- **Audio-only thumbnail = ONE generic cover for every audio episode** = `assets/tng-audio-only-thumbnail.webp`. **Temporary** — Tommy will design a nicer one later; swap = drop the new image in at the same path, all audio eps update. Per-episode custom card is retired.
- **Clean title-only slug** is the URL standard (no `ep-N-` prefix).
- **Footer standard** as above; per-page footer outer spacing must always be preserved (never flattened).

### 🧵 Open threads (not started)
1. **Push EP 138** (pending Tommy's review).
2. **Clean-URL migration** ← this document (Part 2).
3. **Taxonomy gap:** EP 138 has 5 "advisory/storyteller" moments with no home — no *Advisory* subtopic under Business Finances. Decide at next taxonomy pass.
4. **Replicate audio-only across 1–138** (skip any title ending "the numbers game").
5. **`push-live.sh` bug:** it re-dispatches the deploy every 90s and can jam its own queue during a GitHub incident — worth hardening.

### 📂 Local uncommitted right now
- `data/catalogue.json` (M — has EP 138 audio entry + EP 286 platform links)
- `where-have-all-the-accountants-gone.html` (untracked — EP 138 page)
- `assets/tng-audio-only-thumbnail.webp` (untracked)
- scratch/mocks (`_mock-*.html`, `thumb-mockups/`, `_audio-only-template.html`) — disposable.

---

## PART 2 — Clean-URL migration (what we're about to do) — FOR SIGN-OFF

**Goal:** SEO-friendly, clean episode URLs that match the YouTube title / what people search, e.g.
`thenumbersgamepodcast.com.au/buying-commercial-property-with-your-super-in-2026`
(instead of `…/episode-285.html`).

### The slug rule (locked)
- **Full episode title → slug**, lowercased, every run of non-alphanumeric chars → a single `-`, trimmed.
  `re.sub(r'[^a-z0-9]+','-', title.lower()).strip('-')`
- **Drop a trailing branded tagline after a `|`** if it carries no search keywords (e.g. `… | What the Numbers Say`). Keep everything else, including stop-words (they match how people phrase searches).
- Example: *"Buying Commercial Property With Your Super in 2026 | What the Numbers Say"* → `buying-commercial-property-with-your-super-in-2026`.

### URL format (locked): CLEAN (no `.html`)
- Each episode becomes a **folder**: `buying-commercial-property-with-your-super-in-2026/index.html`, served at the bare `/buying-commercial-property-with-your-super-in-2026`.
- (GitHub Pages serves a folder's `index.html` at the extensionless URL; it won't strip `.html` from a flat file, hence the folder structure.)
- Canonical form = **no trailing slash** (`/slug`), applied consistently in canonical tags.

### Redirects — the safety net (nothing 404s)
- **Every old `episode-N.html` stays as a redirect stub** (never deleted): `<meta http-equiv="refresh" content="0; url=/slug">` + `<link rel="canonical" href="https://…/slug">`. This is the standard GitHub-Pages way to "301" and passes SEO to the new URL.
- Result: every Google-indexed URL and every shared link keeps working (forwards to the new clean URL). Even a missed internal link hits the old file and redirects — belt & suspenders.

### Everything that must be repointed to the new slugs
- **Home banner** — `index.html` JS builds `episode-N.html` from catalogue → build the slug.
- **Episodes library** — `episodes.html` JS builds card hrefs → build the slug.
- **Discover-more cards** — `build_episode.py` writes `episode-N.html` → write the slug.
- **catalogue.json** — each entry gets/uses its `slug` (audio-only eps already have one).
- **Per-page** `<link rel="canonical">`, `og:url`, and PodcastEpisode JSON-LD `url`.
- **sitemap.xml** — list the new clean URLs (drop or 301 the old).
- Footer menu links are to sections (index/episodes/about/…), not individual episodes — mostly unaffected; standalone links handled if we do Part-2 scope option B.

### Build tooling changes (so future episodes are clean automatically)
- `build_episode.py`: output `<slug>/index.html`, set canonical/og/JSON-LD to `/slug`, and **also emit the `episode-N.html` redirect stub**.
- `verify_episode.py`: check the new location + that the redirect stub exists and points correctly.

### How I guarantee it won't break live (the process)
1. **All local first.** Build the whole migration on disk.
2. **Automated link-checker:** crawl every page locally, assert **zero broken links**, and that **every old `episode-N.html` redirects to the right new URL**. Do not push until green.
3. **Pilot ONE episode (285):** migrate just it, push, and confirm on the LIVE site — new URL loads, old URL redirects, home + library links land on it. Prove the approach on production before touching the rest.
4. **Batch the other 43** only after the pilot is clean.
5. Push once, verify live (spot-check new URLs 200, old URLs redirect, sitemap valid).

### Open decisions (need Tommy's call before I start)
- **Scope:** (A) episodes only [SEO prize], or (B) episodes + standalone pages too (`about.html`→`/about`, `contact.html`→`/contact`, host pages, etc.) for full consistency.
- **Title-collision guard:** if two episodes ever share an exact title, the second slug needs disambiguation (append the ep number). Confirm that's acceptable.
- **Sitemap old URLs:** drop them entirely (rely on redirects) — recommended.

### NOT included / risks noted
- This does not change page content, the footer, or EP 138.
- Main risk = a missed internal link → mitigated by the redirect safety net + the link-checker + the pilot.
- `where-have-all-the-accountants-gone.html` (EP 138) already follows the clean-slug rule (it just needs to become a folder too when it ships).

---
**Next action after sign-off:** confirm scope (A or B), then I build locally → link-check → pilot EP 285 live → batch the rest. Nothing is touched until you approve this.

---
## UPDATE — end of session 20 Jul (supersedes the folder plan above)

**KEY FINDING:** GitHub Pages serves `.html` at the extensionless URL (`/episode-285` = 200). So clean URLs = **flat slug files, NO folders, no relative-path rework.** Much simpler/safer.

**APPROACH = REUSE, not rebuild.** Each existing `episode-N.html` is *copied* to `<slug>.html` with internal links rewritten; content (incl. EP 285's hand-added Spotify audio) is preserved. Only EP 138 (generated audio page) was rebuilt.

**STATUS: fully BUILT LOCALLY + link-checked GREEN. NOT PUSHED.** Awaiting Tommy's go.
- 45 `<slug>.html` pages (hook-only slug = title before ` | `). Pilot EP 285 already LIVE.
- Every `episode-N.html` → redirect stub → `/slug` (nothing 404s).
- Standalone canonical+links → extensionless; catalogue has `slug` on all; sitemap clean (138 excluded).
- Dynamic JS (index/episodes/adventure) builds `/`+slug from catalogue.
- `episode-master-template.html` = the build source (so 263 can be a stub). `build_episode.py` updated to output clean (slug page + stub + `/slug` canonical/discover/host).
- Link-checker `scratchpad/link_check.py`: 1951 links, **0 broken, all stubs valid**.

**WHEN PUSHING:** exclude EP-138 catalogue entry + `where-have-all-the-accountants-gone.html` + the webp (ship on the separate EP 138 approval). Everything else pushes together.

**FOLLOW-UPS:** (1) `verify_episode.py` needs matching hook-only-slug + read-slug-page + discover-regex tweak (only affects verifying FUTURE builds). (2) `push-live.sh` re-dispatch-during-outage bug.

**NOTHING is at risk in a new window** — all work is saved as files on disk + captured in memory (`project_tng_audio_only_build`). A new session reads that memory + this doc to continue.
