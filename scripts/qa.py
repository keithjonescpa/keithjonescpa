#!/usr/bin/env python3
"""Content QA gate for keithjones.cpa site files.

Verifies the working tree against the canonical facts in CLAUDE.md.
Run from the repository root; exits non-zero on any violation so CI
blocks the merge.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LICENSE = "AC0028367"
PHONE = "844-888-1040"
DOMAIN = "https://keithjones.cpa"
EMAIL = "keith@keithjones.cpa"
DISCLAIMER = "not a guarantee"

# Values that must appear nowhere in tracked text files.
STALE = ["AC0029107", "info@example.com", '"url": "#"', "904-467-0868"]

CASE_COUNT_RE = re.compile(
    r"\b(?:over\s+)?\d[\d,]*\+?\s+(?:IRS(?:\s+and\s+Florida\s+DOR)?\s+)?cases?\b",
    re.I,
)
TEXT_GLOBS = ["*.html", "js/*.js", "css/*.css", "*.md", "*.xml", "*.txt"]

failures = []


def fail(msg):
    failures.append(msg)


def text_files():
    for pattern in TEXT_GLOBS:
        yield from ROOT.glob(pattern)


pages = sorted(p for p in ROOT.glob("*.html") if p.name != "404.html")

# 1. Stale values anywhere
for f in text_files():
    body = f.read_text(encoding="utf-8")
    for s in STALE:
        if s in body:
            fail(f"{f.name}: stale value {s!r} present")
    if re.search(r"\bwww\.keithjones\.cpa\b", body, re.I):
        fail(f"{f.name}: non-canonical www hostname present")
    if ("$15M+" in body or "70%+" in body or CASE_COUNT_RE.search(body)) and DISCLAIMER not in body.lower():
        fail(f"{f.name}: results claim without no-guarantee disclaimer")

# 2. Per-page canonical facts
for p in pages:
    body = p.read_text(encoding="utf-8")
    if LICENSE not in body:
        fail(f"{p.name}: license {LICENSE} missing")
    if PHONE not in body:
        fail(f"{p.name}: phone {PHONE} missing")
    if "<link rel='canonical'" not in body:
        fail(f"{p.name}: canonical link missing")
    m = re.search(r"<script type='application/ld\+json'>(.*?)</script>", body, re.S)
    if not m:
        fail(f"{p.name}: JSON-LD block missing")
    else:
        try:
            data = json.loads(m.group(1))
            for d in data:
                url = d.get("url", "")
                if url and not url.startswith(DOMAIN):
                    fail(f"{p.name}: JSON-LD url {url!r} not under {DOMAIN}")
        except json.JSONDecodeError as e:
            fail(f"{p.name}: JSON-LD invalid: {e}")
# 3. Contact email present where mail is sent
for name in ["contact.html", "js/script.js"]:
    if EMAIL not in (ROOT / name).read_text(encoding="utf-8"):
        fail(f"{name}: contact email {EMAIL} missing")

# 4. Internal links and assets resolve
link_re = re.compile(r"""(?:href|src)=['"]([^'"]+)['"]""")
for p in list(pages) + [ROOT / "404.html"]:
    if not p.exists():
        continue
    for target in link_re.findall(p.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
            continue
        if not (ROOT / target.split("#")[0]).exists():
            fail(f"{p.name}: broken internal reference {target!r}")

# 5. Sitemap covers every page and only real files
sitemap = ROOT / "sitemap.xml"
if not sitemap.exists():
    fail("sitemap.xml missing")
else:
    locs = re.findall(r"<loc>(.*?)</loc>", sitemap.read_text(encoding="utf-8"))
    for loc in locs:
        if not loc.startswith(DOMAIN):
            fail(f"sitemap.xml: {loc} not under {DOMAIN}")
        path = loc[len(DOMAIN):].lstrip("/") or "index.html"
        if not (ROOT / path).exists():
            fail(f"sitemap.xml: {loc} has no matching file")
    listed = {loc[len(DOMAIN):].lstrip("/") or "index.html" for loc in locs}
    for p in pages:
        if p.name not in listed:
            fail(f"sitemap.xml: {p.name} not listed")

if failures:
    print("CONTENT QA FAILED:")
    for msg in failures:
        print(f"  - {msg}")
    sys.exit(1)
print(f"Content QA passed: {len(pages)} pages checked against canonical facts.")
