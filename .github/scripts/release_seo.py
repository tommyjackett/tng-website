#!/usr/bin/env python3
"""Release-day sitemap helper for The Numbers Game website.

Run by .github/workflows/scheduled-publish.yml straight after promote.py.
  default : add any listed episode that is missing from sitemap.xml (additive only)
  --check : fail loudly (exit 1) if a listed episode is missing from sitemap.xml, or if
            the sitemap lists a page that is not released.

Source of truth for "released" is data/catalogue.json (the listing), never the files on disk.
Only ever edits sitemap.xml. The new file is validated, then swapped in atomically,
so a crash can't leave a half-written sitemap. Standard library only.
"""
import json, os, re, sys, tempfile
import xml.dom.minidom

SITE = "https://thenumbersgamepodcast.com.au"
MAIN = ["/", "/episodes", "/adventure", "/about", "/contact",
        "/nick-reilly", "/jason-robinson", "/marty-vidakovic"]
SLUG_OK = re.compile(r'^[a-z0-9][a-z0-9-]*$')
LOC = re.compile(r"<loc>([^<]+)</loc>")


def warn(msg):
    print(f"::warning::release_seo: {msg}")


def read(path):
    return open(path, encoding="utf-8", newline="").read()


def atomic_write(path, text):
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".seo-tmp-")
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, path)


def load_catalogue():
    cat = json.load(open("data/catalogue.json", encoding="utf-8"))
    cat = cat if isinstance(cat, list) else cat["episodes"]
    out = []
    for e in cat:
        slug = (e.get("slug") or "").strip()
        if SLUG_OK.match(slug):
            out.append({"slug": slug, "date": e.get("date", ""), "ep": e.get("episodeNumber")})
        else:
            warn(f"EP {e.get('episodeNumber')} has no usable slug; skipped")
    return out


def add_to_sitemap(cat):
    sm = read("sitemap.xml")
    have = set(LOC.findall(sm))
    lines = sm.splitlines(keepends=True)
    main_urls = {SITE + p for p in MAIN}
    new_lines = []
    for e in sorted(cat, key=lambda x: x["date"], reverse=True):
        url = f"{SITE}/{e['slug']}"
        if url in have or not os.path.isfile(e["slug"] + ".html"):
            continue
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", e["date"]):
            warn(f"EP {e['ep']} has a bad date {e['date']!r}; skipped")
            continue
        new_lines.append(f"  <url><loc>{url}</loc><lastmod>{e['date']}</lastmod><priority>0.7</priority></url>\n")
        print(f"sitemap + EP {e['ep']}: {url}")
    if not new_lines:
        return 0
    # insert straight after the last main-page line (keeps the 8 pages first, newest episodes next)
    at = None
    for i, l in enumerate(lines):
        m = LOC.search(l)
        if m and m.group(1) in main_urls:
            at = i + 1
    if at is None:
        at = next(i for i, l in enumerate(lines) if "</urlset>" in l)
    out = "".join(lines[:at] + new_lines + lines[at:])
    xml.dom.minidom.parseString(out.encode("utf-8"))  # must parse
    locs = LOC.findall(out)
    assert len(locs) == len(have) + len(new_lines), "URL count mismatch"
    assert len(locs) == len(set(locs)), "duplicate URL"
    atomic_write("sitemap.xml", out)
    return len(new_lines)


def check(cat):
    errors = []
    slugs = {e["slug"] for e in cat}
    sm = read("sitemap.xml")
    try:
        xml.dom.minidom.parseString(sm.encode("utf-8"))
    except Exception as ex:
        errors.append(f"sitemap.xml is not valid XML: {ex}")
    locs = LOC.findall(sm)
    for e in cat:
        if os.path.isfile(e["slug"] + ".html") and f"{SITE}/{e['slug']}" not in locs:
            errors.append(f"EP {e['ep']} is released but missing from sitemap.xml")
    main_urls = {SITE + p for p in MAIN}
    for u in locs:
        if u not in main_urls and u[len(SITE) + 1:] not in slugs:
            errors.append(f"sitemap.xml lists {u}, which is not a released episode")
    if len(locs) != len(set(locs)):
        errors.append("sitemap.xml has duplicate URLs")
    print(f"INFO {len(cat)} released episodes, {len(locs)} sitemap URLs")
    for m in errors:
        print(f"::error::{m}")
    print("SEO CHECK: " + ("FAIL" if errors else "PASS"))
    return 1 if errors else 0


def main():
    cat = load_catalogue()
    if "--check" in sys.argv[1:]:
        return check(cat)
    try:
        n = add_to_sitemap(cat)
        print(f"release_seo: added {n} sitemap URL(s)")
        return 0
    except Exception as ex:
        warn(f"sitemap step failed, sitemap.xml left unchanged: {ex}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
