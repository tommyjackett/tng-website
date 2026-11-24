#!/usr/bin/env python3
"""Backfill direct Spotify and Apple episode links onto the TNG site.

Episode pages fall back to a show-wide search URL when catalogue.json has no
appleUrl / spotifyUrl (see the LISTEN block written by build_episode.py). This
script fills those fields from the public RSS feed, the Apple lookup API, and
the Spotify show episode list, then rewrites the matching episode HTML.

Only verified matches are written: RSS episode number must equal the catalogue
number, Apple is matched by episode GUID (or exact title), and Spotify is
matched by exact title. Nothing is guessed.

Designed for local use and for the scheduled-publish workflow. Stdlib only.
Does not commit, push, or deploy.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

APPLE_SHOW_ID = 1555566088
SPOTIFY_SHOW_ID = "41SVe1eJhucikhF3fWD3NW"
RSS_URL = "https://feeds.simplecast.com/1EHEYhtl"
APPLE_LOOKUP = (
    f"https://itunes.apple.com/lookup?id={APPLE_SHOW_ID}"
    "&entity=podcastEpisode&limit=300&country=AU"
)
APPLE_URL_TMPL = f"https://podcasts.apple.com/au/podcast/id{APPLE_SHOW_ID}?i={{track_id}}"
SPOTIFY_URL_TMPL = "https://open.spotify.com/episode/{eid}"
SPOTIFY_EMBED_TMPL = "https://open.spotify.com/embed/episode/{eid}?utm_source=generator"
SPOTIFY_EMBED_SHOW = f"https://open.spotify.com/embed/show/{SPOTIFY_SHOW_ID}"
PATHFINDER_URL = "https://api-partner.spotify.com/pathfinder/v1/query"
PATHFINDER_HASH = "06046f9b939d56c8eb7cdbb687da938de1164c006871aec91dc26e4dc7d8eb08"
UA = "TNG-enrich-episode-links/1.0 (+https://thenumbersgamepodcast.com.au)"
SEARCH_SPOTIFY = "https://open.spotify.com/search/the%20numbers%20game%20podcast"
SEARCH_APPLE = "https://podcasts.apple.com/search?term=the%20numbers%20game"
ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"

LISTEN_NOW = """    <section class="listen-now">
      <div class="ln-head">
        <span class="ln-title">Listen now</span>
      </div>
      <div class="audio-embed">
        <iframe src="{embed_url}"
          width="100%" height="152" loading="lazy" allowfullscreen
          allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
          title="Spotify — {title}"></iframe>
      </div>
    </section>

"""


def http_json(url: str, headers: dict[str, str] | None = None, timeout: int = 30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def http_text(url: str, headers: dict[str, str] | None = None, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_rss() -> list[dict]:
    text = http_text(RSS_URL, timeout=45)
    root = ET.fromstring(text)
    items = []
    for item in root.find("channel").findall("item"):
        ep_el = item.find(f"{{{ITUNES_NS}}}episode")
        if ep_el is None or not (ep_el.text or "").strip().isdigit():
            continue
        items.append(
            {
                "episodeNumber": int(ep_el.text.strip()),
                "title": (item.findtext("title") or "").strip(),
                "guid": (item.findtext("guid") or "").strip(),
            }
        )
    return items


def fetch_apple() -> list[dict]:
    data = http_json(APPLE_LOOKUP, timeout=45)
    out = []
    for r in data.get("results") or []:
        if r.get("kind") != "podcast-episode":
            continue
        track_id = r.get("trackId")
        title = (r.get("trackName") or "").strip()
        if not track_id or not title:
            continue
        out.append(
            {
                "trackId": int(track_id),
                "title": title,
                "guid": (r.get("episodeGuid") or "").strip(),
            }
        )
    return out


def _spotify_token_from_embed() -> str:
    html = http_text(SPOTIFY_EMBED_SHOW, timeout=30)
    m = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        html,
        re.S,
    )
    if not m:
        m = re.search(r'<script[^>]*>(\{"props".*?)</script>', html, re.S)
    if not m:
        raise RuntimeError("Spotify embed page had no NEXT_DATA")
    data = json.loads(m.group(1))
    token = (
        data.get("props", {})
        .get("pageProps", {})
        .get("state", {})
        .get("settings", {})
        .get("session", {})
        .get("accessToken")
    )
    if not token:
        raise RuntimeError("Spotify embed page had no access token")
    return token


def _walk_episodes(node, found: list[dict]) -> None:
    if isinstance(node, dict):
        uri = node.get("uri") or node.get("_uri") or ""
        name = (node.get("name") or node.get("title") or "").strip()
        data = node.get("data") if isinstance(node.get("data"), dict) else None
        if data and not name:
            name = (data.get("name") or data.get("title") or "").strip()
            uri = uri or data.get("uri") or ""
        if isinstance(uri, str) and uri.startswith("spotify:episode:") and name:
            found.append({"id": uri.rsplit(":", 1)[-1], "title": name})
        for v in node.values():
            _walk_episodes(v, found)
    elif isinstance(node, list):
        for v in node:
            _walk_episodes(v, found)


def fetch_spotify(limit: int = 80) -> list[dict]:
    token = _spotify_token_from_embed()
    variables = json.dumps(
        {"uri": f"spotify:show:{SPOTIFY_SHOW_ID}", "offset": 0, "limit": limit},
        separators=(",", ":"),
    )
    extensions = json.dumps(
        {"persistedQuery": {"version": 1, "sha256Hash": PATHFINDER_HASH}},
        separators=(",", ":"),
    )
    url = PATHFINDER_URL + "?" + urllib.parse.urlencode(
        {
            "operationName": "queryPodcastEpisodes",
            "variables": variables,
            "extensions": extensions,
        }
    )
    data = http_json(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "App-Platform": "WebPlayer",
        },
        timeout=30,
    )
    found: list[dict] = []
    _walk_episodes(data, found)
    # de-dupe, keep order
    seen: set[str] = set()
    out = []
    for ep in found:
        if ep["id"] in seen:
            continue
        seen.add(ep["id"])
        out.append(ep)
    if not out:
        raise RuntimeError("Spotify pathfinder returned no episodes")
    return out


def apple_url(track_id: int) -> str:
    return APPLE_URL_TMPL.format(track_id=track_id)


def verify_spotify_oembed(episode_id: str, expected_title: str) -> bool:
    url = "https://open.spotify.com/oembed?url=" + urllib.parse.quote(
        SPOTIFY_URL_TMPL.format(eid=episode_id), safe=""
    )
    try:
        data = http_json(url, timeout=20)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return False
    return (data.get("title") or "").strip() == expected_title


def match_links(catalogue: list[dict], rss: list[dict], apple: list[dict], spotify: list[dict]) -> list[dict]:
    rss_by_n = {r["episodeNumber"]: r for r in rss}
    apple_by_guid = {a["guid"]: a for a in apple if a["guid"]}
    apple_by_title = {}
    for a in apple:
        apple_by_title.setdefault(a["title"], []).append(a)
    spotify_by_title = {}
    for s in spotify:
        spotify_by_title.setdefault(s["title"], []).append(s)

    matches = []
    for entry in catalogue:
        n = entry.get("episodeNumber")
        if n not in rss_by_n:
            continue
        rss_item = rss_by_n[n]
        title = rss_item["title"]
        apple_hit = None
        if rss_item["guid"] and rss_item["guid"] in apple_by_guid:
            apple_hit = apple_by_guid[rss_item["guid"]]
        elif title in apple_by_title and len(apple_by_title[title]) == 1:
            apple_hit = apple_by_title[title][0]
        spotify_hit = None
        if title in spotify_by_title and len(spotify_by_title[title]) == 1:
            cand = spotify_by_title[title][0]
            if verify_spotify_oembed(cand["id"], title):
                spotify_hit = cand
        if not apple_hit and not spotify_hit:
            continue
        matches.append({"entry": entry, "rss_title": title, "apple": apple_hit, "spotify": spotify_hit})
    return matches


def needs_update(entry: dict, apple_hit, spotify_hit) -> bool:
    if apple_hit:
        want_url = apple_url(apple_hit["trackId"])
        if entry.get("appleTrackId") != apple_hit["trackId"] or entry.get("appleUrl") != want_url:
            return True
    if spotify_hit:
        eid = spotify_hit["id"]
        if (
            entry.get("spotifyId") != eid
            or entry.get("spotifyUrl") != SPOTIFY_URL_TMPL.format(eid=eid)
            or entry.get("spotifyEmbedUrl") != SPOTIFY_EMBED_TMPL.format(eid=eid)
        ):
            return True
    return False


def apply_catalogue(entry: dict, apple_hit, spotify_hit) -> None:
    if apple_hit:
        entry["appleTrackId"] = apple_hit["trackId"]
        entry["appleUrl"] = apple_url(apple_hit["trackId"])
    if spotify_hit:
        eid = spotify_hit["id"]
        entry["spotifyId"] = eid
        entry["spotifyUrl"] = SPOTIFY_URL_TMPL.format(eid=eid)
        entry["spotifyEmbedUrl"] = SPOTIFY_EMBED_TMPL.format(eid=eid)


def patch_html(path: Path, entry: dict) -> bool:
    if not path.is_file():
        return False
    text = path.read_text()
    if "LISTEN:START" not in text or "LISTEN:END" not in text:
        return False
    original = text
    apple = entry.get("appleUrl")
    spotify = entry.get("spotifyUrl")
    embed = entry.get("spotifyEmbedUrl")
    title = entry.get("title") or ""
    if apple:
        text = text.replace(SEARCH_APPLE, apple)
        # also rewrite a stale direct Apple URL if present
        text = re.sub(
            r'(<a href=")https://podcasts\.apple\.com/[^"]+(" target="_blank" rel="noopener" aria-label="Listen to this episode on Apple Podcasts")',
            rf"\1{apple}\2",
            text,
            count=1,
        )
    if spotify:
        text = text.replace(SEARCH_SPOTIFY, spotify)
        text = re.sub(
            r'(<a href=")https://open\.spotify\.com/[^"]+(" target="_blank" rel="noopener" aria-label="Listen to this episode on Spotify")',
            rf"\1{spotify}\2",
            text,
            count=1,
        )
    if embed and 'class="listen-now"' not in text and "LISTEN:START" in text:
        block = LISTEN_NOW.format(embed_url=embed, title=_html_escape(title))
        text = re.sub(
            r"(<!-- LISTEN:START[^\n]*-->\n)(\s*<div class=\"listen\">)",
            rf"\1\n{block}\2",
            text,
            count=1,
        )
    elif embed and 'class="listen-now"' in text:
        text = re.sub(
            r'(<iframe src=")https://open\.spotify\.com/embed/episode/[^"]+(")',
            rf"\1{embed}\2",
            text,
            count=1,
        )
        text = re.sub(
            r'(<iframe src="https://open\.spotify\.com/embed/episode/[^"]+"[\s\S]*?title=")[^"]*("></iframe>)',
            rf"\1Spotify — {_html_escape(title)}\2",
            text,
            count=1,
        )
    if text == original:
        return False
    path.write_text(text)
    return True


def _html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repo root (default: cwd)")
    parser.add_argument(
        "--only-missing",
        action="store_true",
        default=True,
        help="Only fill catalogue entries missing a Spotify or Apple URL (default)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Consider every catalogue episode (still only writes verified matches)",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    cat_path = root / "data" / "catalogue.json"
    catalogue = json.loads(cat_path.read_text())

    print("Fetching RSS, Apple lookup, and Spotify episode list…", flush=True)
    try:
        rss = fetch_rss()
        apple = fetch_apple()
        spotify = fetch_spotify()
    except Exception as e:
        print(f"ERROR: could not fetch platform data: {e}", file=sys.stderr)
        return 1
    print(f"  RSS {len(rss)}  Apple {len(apple)}  Spotify {len(spotify)}")

    only_missing = not args.all
    targets = []
    for entry in catalogue:
        if only_missing and entry.get("appleUrl") and entry.get("spotifyUrl"):
            continue
        targets.append(entry)

    matches = match_links(targets if only_missing else catalogue, rss, apple, spotify)
    changed_cat = 0
    changed_html: list[str] = []
    skipped = []
    for m in matches:
        entry = m["entry"]
        n = entry["episodeNumber"]
        if not m["apple"] or not m["spotify"]:
            skipped.append((n, "incomplete", m["apple"] is not None, m["spotify"] is not None))
            # still apply whichever side is verified, if something is missing
        if not needs_update(entry, m["apple"], m["spotify"]) and (
            not m["spotify"]
            or 'class="listen-now"' in (root / f"{entry['slug']}.html").read_text()
            if (root / f"{entry['slug']}.html").is_file()
            else True
        ):
            # may still need HTML player restored
            html_path = root / f"{entry['slug']}.html"
            if html_path.is_file() and m["spotify"] and 'class="listen-now"' not in html_path.read_text():
                apply_catalogue(entry, m["apple"], m["spotify"])
                if patch_html(html_path, entry):
                    changed_html.append(str(html_path.relative_to(root)))
            continue
        apply_catalogue(entry, m["apple"], m["spotify"])
        changed_cat += 1
        html_path = root / f"{entry['slug']}.html"
        if patch_html(html_path, entry):
            changed_html.append(str(html_path.relative_to(root)))
        print(
            f"  EP {n}: Apple={'yes' if m['apple'] else 'no'} "
            f"Spotify={'yes' if m['spotify'] else 'no'}  {entry.get('slug')}"
        )

    if changed_cat:
        cat_path.write_text(json.dumps(catalogue, indent=1, ensure_ascii=False) + "\n")

    print(f"Updated catalogue entries: {changed_cat}")
    print(f"Updated HTML pages: {len(changed_html)}")
    for p in changed_html:
        print(f"  {p}")
    if skipped:
        print("Incomplete (left unverified side unchanged):")
        for row in skipped:
            print(f"  EP {row[0]} apple={row[2]} spotify={row[3]}")
    if changed_cat == 0 and not changed_html:
        print("No changes.")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
