#!/usr/bin/env python3
"""Apply the unique episode summaries in data/summary-overrides.json to the live pages.

data/summary-overrides.json is {"<episode number>": "<2 to 4 sentence summary>"}. It is the
source of truth for those summaries: scripts/build_episode.py and scripts/build_audio_lite.py
read it too (it wins over the DEEP / Notion summary), so a rebuild of an episode emits the
same text.

Why this does not run the page builders: a full rebuild re-picks Discover More, re-pulls the
transcript and drops hand-added blocks (for example EP 304's Sources credit). This script
changes ONLY the three places the summary appears on a page:
  1. the first <div class="summary-body"><p>...</p> (the SUMMARY tab)
  2. <meta name="description">
  3. <meta property="og:description">
and, for audio-era episodes that carry a "summary" in data/catalogue.json (used by the
library search), that one field. Nothing else is touched.

Usage:
  python3 .github/scripts/apply_summaries.py            # apply
  python3 .github/scripts/apply_summaries.py --check    # validate + report, write nothing

Standard library only. Validates every summary first and refuses to write anything if any fails.
"""
import html
import json
import os
import re
import sys
import tempfile

OVERRIDES = "data/summary-overrides.json"
BAD_START = re.compile(r"^\s*(welcome|in this episode|on today'?s show|today we)\b", re.I)
BAD_CHARS = re.compile("[—–⁠​*\\[\\]<>`#]|--")
BODY_RE = re.compile(r'(<div class="summary-body">\s*<p>)(.*?)(</p>)', re.S)
META_RE = re.compile(r'(<meta name="description" content=")[^"]*(">)')
OG_RE = re.compile(r'(<meta property="og:description" content=")[^"]*(">)')


def sentences(t):
    return len(re.findall(r"[.!?]+[\"')”]*(?=\s|$)", t.strip()))


def meta_text(s):
    """<= 160 chars, cut at a sentence boundary (same rule as build_episode.py); word cut + ellipsis as a fallback."""
    if len(s) <= 160:
        return s
    ends = [m.end() for m in re.finditer(r"[.!?](?=\s|$)", s[:161]) if m.end() <= 160]
    if ends and max(ends) >= 40:
        return s[:max(ends)]
    cut = s[:157].rsplit(" ", 1)[0].rstrip(",;: ")
    return cut + "…"


def esc_body(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def esc_attr(t):
    return esc_body(t).replace('"', "&quot;")


def validate(ov):
    errs, seen = [], {}
    for k, v in ov.items():
        n = sentences(v)
        if not 2 <= n <= 4:
            errs.append(f"EP {k}: {n} sentences (need 2 to 4)")
        if BAD_START.search(v):
            errs.append(f"EP {k}: boilerplate opener")
        if BAD_CHARS.search(v):
            errs.append(f"EP {k}: em/en dash, markdown or invisible character")
        if re.search(r"fonterra", v, re.I):
            errs.append(f"EP {k}: mentions a banned name")
        if len(v) > 700 or len(v) < 80:
            errs.append(f"EP {k}: length {len(v)} outside 80..700 characters")
        if re.search(r"\bnumbers game\b", v, re.I) and not re.search(r"The Numbers Game", v):
            errs.append(f"EP {k}: show name not written in full")
        if v in seen:
            errs.append(f"EP {k}: identical to EP {seen[v]}")
        seen[v] = k
    return errs


def atomic_write(path, text):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(path)) or ".", prefix=".sum-tmp-")
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, path)


def main():
    check = "--check" in sys.argv[1:]
    ov = json.load(open(OVERRIDES, encoding="utf-8"))
    errs = validate(ov)
    cat_text = open("data/catalogue.json", encoding="utf-8", newline="").read()
    cat = json.loads(cat_text)
    by_ep = {e["episodeNumber"]: e for e in cat}
    plan = {}
    for k, new in ov.items():
        e = by_ep.get(int(k))
        if not e:
            errs.append(f"EP {k}: not in data/catalogue.json (not released); refusing to touch it")
            continue
        path = e["slug"] + ".html"
        if not os.path.isfile(path):
            errs.append(f"EP {k}: {path} missing")
            continue
        page = open(path, encoding="utf-8", newline="").read()
        if len(BODY_RE.findall(page)) < 1 or len(META_RE.findall(page)) != 1 or len(OG_RE.findall(page)) != 1:
            errs.append(f"EP {k}: {path} does not have exactly one summary-body / description / og:description")
            continue
        out = BODY_RE.sub(lambda m: m.group(1) + esc_body(new) + m.group(3), page, count=1)
        md = esc_attr(meta_text(new))
        out = META_RE.sub(lambda m: m.group(1) + md + m.group(2), out, count=1)
        out = OG_RE.sub(lambda m: m.group(1) + md + m.group(2), out, count=1)
        plan[path] = out
    new_cat = cat_text
    changed_cat = 0
    for k, new in ov.items():
        e = by_ep.get(int(k))
        if e and "summary" in e and e["summary"] != new:
            old_j, new_j = json.dumps(e["summary"], ensure_ascii=False), json.dumps(new, ensure_ascii=False)
            if new_cat.count('"summary": ' + old_j) != 1:
                errs.append(f"EP {k}: could not locate its catalogue summary exactly once")
            else:
                new_cat = new_cat.replace('"summary": ' + old_j, '"summary": ' + new_j, 1)
                changed_cat += 1
    for m in errs:
        print(f"ERROR {m}")
    if errs:
        print(f"apply_summaries: FAILED ({len(errs)} problems), nothing written")
        return 1
    if check:
        print(f"apply_summaries --check: {len(ov)} summaries valid; would rewrite {len(plan)} pages and {changed_cat} catalogue summaries")
        return 0
    for path, text in plan.items():
        atomic_write(path, text)
    if changed_cat:
        json.loads(new_cat)  # must still parse
        atomic_write("data/catalogue.json", new_cat)
    print(f"apply_summaries: rewrote {len(plan)} pages, {changed_cat} catalogue summaries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
