# BUILD PLAN — finish the site (from Tommy's brief, 8 Jul 2026 11:22am)

*Source brief: `Brain/Vidpod/clients/TNG/Website Build/DELETE ME/site changes 8 july 1122am.md` (moved there after this plan was written). This file is the tracked execution plan — tick items as they ship. Every push follows the standard system: edit → verify → commit → push-live → live link + summary. Specs updated in the same push as any new rule.*

> **STATUS (end of 8 Jul session): MISSION ACCOMPLISHED — site LIVE at https://thenumbersgamepodcast.com.au, HTTPS enforced, all 29 pages, Stages 0-4 shipped.**
> **NEXT SESSION STARTS HERE:** 1) Tommy: add the domain in Google Search Console + submit /sitemap.xml (his Google login). 2) Email-capture v1 — Tommy's yes/no on Web3Forms. 3) Spotify/Apple show URLs -> subscribe buttons. 4) Tommy's voice pass over draft copy (banner sequence, cards, page intros). 5) Futures when ready: playlists, Instagram grid, guests facet (engine schema, during back-catalogue mining), back-catalogue ingestion.
> Local tooling note: scripts/push-live.sh (gitignored) now verifies against the NEW domain and follows redirects.

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

## STAGE 1 — Homepage quick wins ✅ SHIPPED 8 Jul (awaiting Tommy review)
- [x] Remove full stops in the banner sequence: "5 years" / "150+ hours" / "280+ episodes" (keep "but not as you know it!").
- [x] **GET INVOLVED IN THE SHOW** section under Ways to Explore: centred heading + short line, two buttons centred — **LEAVE US A VOICE NOTE** (episode-page SpeakPipe component, opens inline) and **SEND US A MESSAGE** (→ contact.html — 404 until Stage 2 ships it, hours away). Copy is draft for voice pass.
- [x] **Subscribe row v1** → revised per Tommy: three matching pill buttons across — voice note (mint) / message (purple) / SUBSCRIBE ON YOUTUBE (mint). Spotify/Apple ship when Tommy supplies show URLs.

## STAGE 2 — The page shell ×4 (the big stamp-out)
Order: contact → about → jason → nick (each one push, Tommy reviews live).
- [x] **contact.html** — SHIPPED 8 Jul. Band: IMG_8006 (optimised to assets/contact-band.jpg), bars GET IN / TOUCH, brief's copy, Web3Forms form live (key supplied by Tommy, redirect-back success note, honeypot), voice-note component as the second path.
- [x] **about.html** — SHIPPED 8 Jul. Band: IMG_7604 (Tommy swapped from IMG_6574; optimised to assets/about-band.jpg), bars ABOUT / THE NUMBERS GAME, layout per Tommy's example: artwork left (rounded, shadow), bio right (official show description, em dashes removed per house style), stat chips 5 YEARS / 280+ EPISODES / SINCE 2021.
- [x] **jason-robinson.html + nick-reilly.html** — SHIPPED 8 Jul, then EVOLVED to final locked pattern: NO video band; whole page fits ONE SCREEN (nav -> photo+bio -> footer, no scrolling on desktop); square head-centred photo (ANALYSE the frame before cropping), solid PURPLE offset shadow, photo stretches to bio height; NAME TAGS as purple/mint bars OVERLAPPING the photo bottom-LEFT (both hosts); Jason photo-left, Nick photo-right (mirrored); personal socials wired (logged below).
- **SOCIALS (logged, supplied by Tommy 8 Jul):** Jason IG https://www.instagram.com/jasonrobinson.cpa/ · Jason LinkedIn https://www.linkedin.com/in/jasonrobinsoncpa1/ · Nick IG https://www.instagram.com/nickreilly99/ · Nick LinkedIn https://www.linkedin.com/in/nickreilly/
- These four kill every remaining nav 404 (About dropdown + Contact already point at these filenames on all 24 live pages).
- [x] **Nav rule (Tommy, 8 Jul): the top-level ABOUT is NOT clickable** — hover/label only; the choosable items are The show / Nick Reilly / Jason Robinson (mobile menu shows About as a dim label with the three as sub-links). Applied across all 28 pages.

## STAGE 3 — episodes.html (the library) + nav rewire ✅ SHIPPED 8 Jul
**The two-layer data model (agreed with Tommy — determines the page's quality):**
- [x] Grid (locked card anatomy), 4 across, newest first, 12 + SHOW MORE (+12).
- [x] **Topic chips with counts** (primary topic from catalogue). Filtering returns TWO tiers: primary-topic episodes first, then episodes with GENUINE moment-level coverage (>=2 verified moments from search-index), ranked by depth and flagged "Also covers: {topic} · N moments" — same never-invent-a-connection law as Discover More.
- [x] **Question-level search** — matches title (100) > topic (50) > the 670 questionAsked/description texts (per-hit), relevance-ranked, cards annotated "Talked about inside · N mentions". Verified: "guarantor" finds Bank of Mum and Dad via 5 inside-mentions with no title match.
- [x] Sort toggle Newest/Oldest · adventure cross-link in header + empty-state · deep links ?topic= and ?q= supported (feeds the future playlist/share direction).
- [x] **Nav rewire on all 29 pages**: EPISODES is now an unclickable dropdown label → All episodes / Find moments (canonical nav in EPISODE-PAGE-TEMPLATE.md updated).
- [x] Homepage card 3 → episodes.html (YouTube interim retired).

## STAGE 4 — SEO + domain ✅ MOSTLY SHIPPED 8 Jul (domain = thenumbersgamepodcast.com.au)
- [x] Unique titles + meta descriptions (all 29) · favicon + apple-touch-icon (podcast art) · footer quick-links row on every page (the crawlable index).
- [x] Canonical tags + Open Graph/Twitter cards on all 29 pages (episode pages use their own YouTube thumbnails as og:image; others use assets/og-image.jpg 1200x630).
- [x] JSON-LD: PodcastSeries (home, with all show socials as sameAs), Person (both hosts), PodcastEpisode (all 22, from catalogue data).
- [x] sitemap.xml (29 URLs, domain-stamped) + robots.txt · contact-form redirect made domain-agnostic · push-live.sh curl now follows redirects (survives the move).
- [x] **DNS FLIP — DONE 8 Jul.** Site LIVE at https://thenumbersgamepodcast.com.au (HTTPS enforced, github.io 301s, www 301s, email untouched). NOTE for future: Pages runs build_type=workflow, so the custom domain needed BOTH the CNAME file AND `PUT /repos/tommyjackett/tng-website/pages {"cname":...}` via API (done). Original runbook kept below for reference:
  1. Tommy at the registrar: apex `thenumbersgamepodcast.com.au` → A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `www` → CNAME `tommyjackett.github.io`.
  2. AFTER records are set (and resolving): create one-line `CNAME` file in repo root containing `thenumbersgamepodcast.com.au`, commit, push. (Deliberately NOT committed yet — doing it before DNS = dark site.)
  3. GitHub Pages settings: wait for the DNS check, then tick **Enforce HTTPS** (cert auto-provisions, can take up to an hour).
  4. Verify https://thenumbersgamepodcast.com.au/ + confirm github.io 301s; submit sitemap in Google Search Console (property = the new domain).
- [ ] **Listener database v1 recommendation:** one-field email capture using the same Web3Forms account (no new vendor), submissions to Tommy's email; upgradeable later. Placement: small strip on contact page + homepage Get Involved. *(Decision for Tommy: OK to use Web3Forms for this v1?)*
- [ ] **Instagram feed: parked** — needs an embed service or manual grid decision; recommend a later phase (manual 6-tile grid linking to IG is the zero-dependency v1).
- [ ] Voice-note "appears on each page at different times": v1 = present on episode pages (already), contact, and homepage Get Involved. Roaming/timed appearance parked as a later experiment.

## GROWTH MODEL + FUTURES (agreed with Tommy, 8 Jul)
- **Self-growing facets:** episodes.html renders chips/counts from data at load — new topics from back-catalogue ingestion appear automatically (threshold-gated). Engine gates are the taxonomy quality control; the site trusts verified data. At ~20+ topics: chip row folds behind "+ more"; search becomes the primary tool.
- **Principle: add a field to the data, get a filter on the site.** Guests: add `guests[]` to the engine schema and capture it DURING back-catalogue mining (one pass); episodes page then gains guest facet + guest search for free (template already reserves a Guest fact slot). Same door for formats/series/years.
- **Playlists ("send yourself a playlist"):** v1 = URL-encoded lists (?list=281,273,266), zero backend, page rebuilds the queue from the URL; v1.5 = localStorage My List; v2 = "Email me this playlist" via the same Web3Forms account — which doubles as the listener-database capture. Also a hosts' marketing tool (curated playlist links said on air).

## Open items needing Tommy (updated end of day 8 Jul)
1. ~~Web3Forms key~~ SUPPLIED (ad399097-ad89-481c-a55b-31f074b176f6, live on contact.html).
2. **Spotify + Apple show URLs** — still needed (Get Involved subscribe row + future channels).
3. ~~Host socials~~ SUPPLIED + live. Show socials also live on about.html (IG/TikTok/LinkedIn/FB id=100071290388343/YT).
4. **Email-capture v1 via Web3Forms — yes/no** (Stage 4).
5. Tommy voice pass over all draft copy (banner sequence, cards, page intros) whenever ready.

## Standing context (per the brief, for any future session)
- The site is data-driven; treat design like a data scientist + expert UI dev. Everything must scale to the full back-catalogue (moments payload trigger documented in MOMENTS-FEATURE.md §10).
- TNG copy style + section look/feel are established — stay consistent (specs: EPISODE-PAGE-TEMPLATE.md, MOMENTS-FEATURE.md, HANDOFF.md).
- The whole system (engine data + pages + adventure product) is deliberately portable to other VIDPOD clients and product types — keep components self-contained and documented.
