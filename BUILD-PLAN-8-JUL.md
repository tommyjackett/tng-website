# BUILD PLAN — finish the site (from Tommy's brief, 8 Jul 2026 11:22am)

*Source brief: `Brain/Vidpod/clients/TNG/Website Build/DELETE ME/site changes 8 july 1122am.md` (moved there after this plan was written). This file is the tracked execution plan — tick items as they ship. Every push follows the standard system: edit → verify → commit → push-live → live link + summary. Specs updated in the same push as any new rule.*

**Mission: site finished today.** Cohesive, easy to navigate, the home for the show. Data-driven and scalable (back-catalogue will grow it 10x), SEO-conscious, and every pattern built portable for future VIDPOD clients/products.

---

## The reusable pattern this build stamps out (build once, use 4+ times)

**The "page shell":** nav (with Home + dropdowns) → cinematic image band (real photo, light blur + purple tint, purple/mint title bars, bottom fade — exactly the adventure.html header) → content → two-column footer. Contact, About, and both host pages are all this shell with different images/copy. This is Stage 2, and it is most of the site.

**Image assets** (all found, to be optimised ~1600px wide into `assets/`):
- Contact: `MEDIA/BTS IMAGES/IMG_8006.jpeg`
- About: `MEDIA/BTS IMAGES/IMG_6574.jpeg` (+ podcast artwork in content)
- Jason: `MEDIA/MEDIA/Q1_REC 2_1_Ep 273_v1.2_00_15_07_20.jpg`
- Nick: `MEDIA/MEDIA/Q1_REC 2_1_Ep 271_v1.1_00_01_10_07.jpg`

---

## STAGE 0 — Housekeeping (ships with this plan)
- [x] Desktop padding tightened under the explore cards + footer line pulled up (seamless full-scroll). Verified, pushed in this batch.
- [x] This plan committed to the repo (tracked in git); source brief moved to DELETE ME.
- [x] HANDOFF points here as the active work queue.

## STAGE 1 — Homepage quick wins
- [ ] Remove full stops in the banner sequence: "5 years" / "150+ hours" / "280+ episodes" (keep "but not as you know it!").
- [ ] **GET INVOLVED IN THE SHOW** section under Ways to Explore: centred heading + short line, two buttons centred — **LEAVE US A VOICE NOTE** (SpeakPipe widget, reusing the episode-page component) and **SEND US A MESSAGE** (→ contact.html). Built directly on the page, iterated live. Generous spacing per brief.
- [ ] **Subscribe/channels row** (brief's "push people to the other channels"): quiet row in the same section — YouTube (have URL) + Spotify/Apple (**need show URLs from Tommy — parked item**; buttons ship when URLs arrive).

## STAGE 2 — The page shell ×4 (the big stamp-out)
Order: contact → about → jason → nick (each one push, Tommy reviews live).
- [ ] **contact.html** — band: IMG_8006, bars "GET IN TOUCH" (purple) / mint payoff. Copy per brief (TNG voice pass): "We'd love to hear from you… use the form below." Web3Forms embed styled to brand. **BLOCKER: the Web3Forms access key/embed wasn't in the brief file and isn't in the brain — page ships with the form wired except the key; Tommy pastes the key, one push finishes it.** Voice-note button included as the second contact path.
- [ ] **about.html** — band: IMG_6574, bars around "ABOUT / THE NUMBERS GAME STORY". One strong SEO paragraph block (story + hosts + what the show covers) drawn from the TNG brain md files, podcast artwork placed in content. Nothing too crazy per brief.
- [ ] **jason-robinson.html** — band: Ep 273 still, bars = his name. TNG-tone bio from brain md files, Future Advisory mention + link, Instagram + LinkedIn (pull handles from brain; ask if absent). Meet-your-hosts feel.
- [ ] **nick-reilly.html** — same shell, Ep 271 still, Inovayt mention + link, socials.
- These four kill every remaining nav 404 (About dropdown + Contact already point at these filenames on all 24 live pages).

## STAGE 3 — episodes.html (the library) + nav rewire
**Proposed functionality (per brief's request for a recommendation, kept simple, all client-side from catalogue.json):**
- [ ] Grid of episode cards (locked card anatomy, already built once), 4 across desktop, newest first, 12 shown, **SHOW MORE** reveals +12.
- [ ] **Topic filter chips** across the top (each episode has a key topic in the data — chips with counts, same visual language as the adventure picker; one active at a time v1).
- [ ] **Search bar** — instant filter over titles + topics ("ATO" → the ATO episodes). Simple contains-match v1; can deepen to question-level search later using search-index.
- [ ] **Sort toggle** Newest/Oldest.
- [ ] Header explains the two ways in: small cross-link card/line to Choose Your Own Adventure ("looking for the best bits instead?").
- [ ] **Nav rewire everywhere** (index, adventure, 22 episode pages — batch swap like the footer rollout): EPISODES becomes a dropdown → All episodes (episodes.html) / Find moments (adventure.html).
- [ ] Homepage card 3: href flips from YouTube channel → episodes.html (label already says Explore episodes).

## STAGE 4 — SEO + extras
- [ ] Unique `<title>` + meta description on every new page; human URLs already good (about, contact, host names).
- [ ] `sitemap.xml` + `robots.txt`; JSON-LD (PodcastSeries on home, Person on host pages).
- [ ] Footer quick-links row (all pages): Episodes / Adventure / About / Contact — the crawlable "index" the brief wants, tidy in the footer.
- [ ] **Listener database v1 recommendation:** one-field email capture using the same Web3Forms account (no new vendor), submissions to Tommy's email; upgradeable later. Placement: small strip on contact page + homepage Get Involved. *(Decision for Tommy: OK to use Web3Forms for this v1?)*
- [ ] **Instagram feed: parked** — needs an embed service or manual grid decision; recommend a later phase (manual 6-tile grid linking to IG is the zero-dependency v1).
- [ ] Voice-note "appears on each page at different times": v1 = present on episode pages (already), contact, and homepage Get Involved. Roaming/timed appearance parked as a later experiment.

## Open items needing Tommy
1. **Web3Forms access key / embed snippet** (contact form + email capture).
2. **Spotify + Apple show URLs** (channels row; long-parked item).
3. Host **Instagram/LinkedIn handles** if not found in the brain.
4. Email-capture v1 via Web3Forms — yes/no.

## Standing context (per the brief, for any future session)
- The site is data-driven; treat design like a data scientist + expert UI dev. Everything must scale to the full back-catalogue (moments payload trigger documented in MOMENTS-FEATURE.md §10).
- TNG copy style + section look/feel are established — stay consistent (specs: EPISODE-PAGE-TEMPLATE.md, MOMENTS-FEATURE.md, HANDOFF.md).
- The whole system (engine data + pages + adventure product) is deliberately portable to other VIDPOD clients and product types — keep components self-contained and documented.
