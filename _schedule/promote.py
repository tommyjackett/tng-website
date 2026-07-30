#!/usr/bin/env python3
"""Promote scheduled TNG episodes into the LIVE listing (catalogue + search-index)
on/after their release date, evaluated in Australia/Sydney local time (DST-aware).
Idempotent: an episode already in the catalogue is skipped. GitHub Pages redeploys on commit."""
import json, os
from datetime import datetime
from zoneinfo import ZoneInfo

REPO = os.environ.get("REPO_DIR", ".")
SCHED = os.environ.get("SCHED_DIR", "_schedule")
today = os.environ.get("TEST_TODAY") or datetime.now(ZoneInfo("Australia/Sydney")).strftime("%Y-%m-%d")

schedule = json.load(open(f"{SCHED}/schedule.json"))
cat_path, idx_path = f"{REPO}/data/catalogue.json", f"{REPO}/data/search-index.json"
cat = json.load(open(cat_path)); idx = json.load(open(idx_path))
listed = {e["episodeNumber"] for e in cat}
published = []
for s in schedule:
    if s["date"] > today:      continue     # not due (ISO date string compare)
    if s["ep"] in listed:      continue     # already live — idempotent
    entry = json.load(open(f"{SCHED}/{s['ep']}-cat.json"))     # list w/ 1 entry
    moments = json.load(open(f"{SCHED}/{s['ep']}-idx.json"))
    cat.extend(entry); idx.extend(moments)
    published.append(f"{s['ep']} ({s['slug']})")
if published:
    json.dump(cat, open(cat_path,"w"), ensure_ascii=False, indent=1); open(cat_path,"a").write("\n")
    json.dump(idx, open(idx_path,"w"), ensure_ascii=False, indent=1); open(idx_path,"a").write("\n")
    print("PUBLISHED: " + ", ".join(published))
else:
    print(f"nothing due (today Sydney = {today})")
