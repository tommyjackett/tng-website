#!/usr/bin/env python3
"""Render an optional Sources block from data/catalogue.json.

scripts/build_episode.py is the local page generator. It is gitignored and is
not in this repository, and catalogue.json has no sources field of its own.
This is the committed renderer for an optional per-episode "sources" list so a
later episode can reuse it.

Each item is {"text": "...", "links": [{"label": "...", "href": "..."}]}.
"links" is optional. Each label must occur in that item's text; it becomes an
anchor with target="_blank" and rel="noopener". The block is inserted under the
summary and above the voice note (and therefore above the transcript), using
the existing .summary-body paragraph style. Pages with no sources list are not
written.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

MARK_START = "        <!-- SOURCES:START -->"
MARK_END = "        <!-- SOURCES:END -->"
BLOCK_RE = re.compile(
    re.escape(MARK_START) + r"\n.*?" + re.escape(MARK_END) + r"\n",
    re.S,
)
INSERT_RE = re.compile(
    r'(        <div class="summary-body">\n(?:.*\n)*?        </div>\n)'
    r'(        <div class="vask">)'
)


def _apos(s: str) -> str:
    return s.replace("'", "\u2019").replace("\u2019", "\u2019")


def paragraph_html(item: dict) -> str:
    text = html.escape(_apos(item["text"]), quote=False).replace("\u2019", "&rsquo;")
    for link in item.get("links") or []:
        label = html.escape(_apos(link["label"]), quote=False).replace("\u2019", "&rsquo;")
        href = html.escape(link["href"], quote=True)
        if label not in text:
            raise SystemExit(f"sources link label not found in paragraph: {link['label']!r}")
        anchor = f'<a href="{href}" target="_blank" rel="noopener">{label}</a>'
        text = text.replace(label, anchor, 1)
    return text


def render_block(sources: list) -> str:
    lines = [
        MARK_START,
        '        <div class="summary-body">',
        "          <p><strong>Sources</strong></p>",
    ]
    for item in sources:
        lines.append(f"          <p>{paragraph_html(item)}</p>")
    lines.append("        </div>")
    lines.append(MARK_END)
    return "\n".join(lines) + "\n"


def apply_html(page: str, sources: list) -> str:
    block = render_block(sources) if sources else ""
    if BLOCK_RE.search(page):
        return BLOCK_RE.sub(block, page, count=1)
    if not sources:
        return page
    match = INSERT_RE.search(page)
    if not match:
        raise SystemExit("episode page has no summary block to attach sources to")
    return page[: match.end(1)] + block + page[match.start(2) :]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repo root (default: cwd)")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    catalogue = json.loads((root / "data" / "catalogue.json").read_text(encoding="utf-8"))
    changed = []
    for entry in catalogue:
        sources = entry.get("sources") or []
        slug = entry.get("slug")
        if not slug:
            continue
        path = root / f"{slug}.html"
        if not path.is_file():
            if sources:
                print(f"skip (no page): {slug}", file=sys.stderr)
            continue
        original = path.read_text(encoding="utf-8")
        updated = apply_html(original, sources)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(slug)
    print(f"sources: {len(changed)} page(s) updated")
    for slug in changed:
        print(f"  {slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
