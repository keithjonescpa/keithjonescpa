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
FIRM_LICENSE = "AD0016958"
PHONE = "844-888-1040"
DOMAIN = "https://fdor.keithjones.cpa"
EMAIL = "keith@keithjones.cpa"
DISCLAIMER = "not a guarantee"
# Protected brand wording (Keith, 2026-08-05). The tagline is brand equity:
# every occurrence must match exactly, so no contributor or tool can quietly
# "improve" it. See CLAUDE.md.
TAGLINE = "Solving Bad Tax Problems for Good People"
TAGLINE_TM = TAGLINE + "\u2122"
# Every mark claimed in the README trademark notice. Asserting these verbatim is
# what catches an edit anywhere inside a mark — scanning for known-bad variants
# can never be exhaustive.
MARKS = [
    "TheCPATaxProblemSolver\u2122",
    TAGLINE_TM,
    "Helping Good People With Bad Tax Problems\u2122",
    "Florida Tax Guy\u2122",
    "Florida Tax Survival Engine\u2122",
    "FDOR Insider Advantage\u2122",
]
TAGLINE_DRIFT_RE = re.compile(
    r"Solving\s+Bad\s+Tax\s+Problems(?!\s+for\s+Good\s+People)", re.I
)

# Values that must appear nowhere in tracked text files.
STALE = [
    "AC0029107", "info@example.com", '"url": "#"', "904-467-0868",
    # fonts must be self-hosted (Brand System v5.0 + CSP default-src 'self')
    "fonts.googleapis.com", "fonts.gstatic.com",
]

CASE_COUNT_RE = re.compile(
    r"\b(?:over\s+)?\d[\d,]*\+?\s+(?:[A-Za-z][\w&.-]*\s+){0,4}cases?\b",
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
    if "™," in body:
        fail(f"{f.name}: comma immediately after ™ — list marks one per line instead")
    for m in re.finditer(re.escape(TAGLINE), body, re.I):
        if m.group(0) != TAGLINE:
            fail(f"{f.name}: tagline capitalisation altered — {m.group(0)!r} must be {TAGLINE!r}")
        elif body[m.end():m.end() + 1] != "\u2122":
            fail(f"{f.name}: tagline is missing its ™ symbol")
    for m in TAGLINE_DRIFT_RE.finditer(body):
        fail(f"{f.name}: tagline reworded — {m.group(0)!r} must read {TAGLINE!r}")

readme = ROOT / "README.md"
if not readme.exists():
    fail("README.md missing")
else:
    # The tagline must be used as the brand line, not merely listed in the
    # trademark notice — otherwise the brand line could be swapped for softer
    # wording while the notice alone keeps the check green.
    lines = readme.read_text(encoding="utf-8").splitlines()
    # Map the trademark-notice block so a mark listed there cannot, on its own,
    # satisfy the brand-line requirement. Detected case-insensitively and across
    # multiple lines, since the notice lists one mark per line.
    notice, in_notice = set(), False
    for i, line in enumerate(lines):
        if re.search(r"trademarks? of", line, re.I):
            in_notice = True
        if in_notice:
            notice.add(i)
        if in_notice and "</sub>" in line:
            in_notice = False
    notice_text = "\n".join(lines[i] for i in sorted(notice))
    body_text = "\n".join(l for i, l in enumerate(lines) if i not in notice)

    if TAGLINE_TM not in body_text:
        fail(f"README.md: tagline {TAGLINE_TM!r} must appear as the brand line, "
             "not only inside the trademark notice")
    if not notice:
        fail("README.md: trademark notice missing")
    for mark in MARKS:
        if mark not in notice_text:
            fail(f"README.md: trademark notice is missing or alters {mark!r}")

# 2. Per-page canonical facts
for p in pages:
    body = p.read_text(encoding="utf-8")
    page_url = DOMAIN + "/" if p.name == "index.html" else f"{DOMAIN}/{p.stem}"
    if f"<link rel='canonical' href='{page_url}'>" not in body:
        fail(f"{p.name}: canonical link missing or not {page_url}")
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
# 2a. Both credentials must be DBPR-verifiable LINKS in the footer of every
# page, 404 included. Raw license text alone is not verifiable by a visitor,
# so checking for the number is not enough — check the anchor and its target.
DBPR_URL = "https://www.myfloridalicense.com/wl11.asp"
anchor_re = re.compile(r"<a\s+([^>]*?)>\s*#([A-Z]{2}\d+)\s*</a>", re.I)
for p in sorted(ROOT.glob("*.html")):
    body = p.read_text(encoding="utf-8")
    linked = {num: f"href='{DBPR_URL}'" in attrs for attrs, num in anchor_re.findall(body)}
    if PHONE not in body:
        fail(f"{p.name}: phone {PHONE} missing")
    for num in (LICENSE, FIRM_LICENSE):
        if num not in body:
            fail(f"{p.name}: license #{num} missing")
        elif num not in linked:
            fail(f"{p.name}: license #{num} present but not a link")
        elif not linked[num]:
            fail(f"{p.name}: license #{num} link does not point at {DBPR_URL}")

# 2b. Typography per Brand System v5.0: Playfair headings, Inter body, self-hosted
css_path = ROOT / "css" / "style.css"
if not css_path.exists():
    fail("css/style.css: missing")
else:
    css = css_path.read_text(encoding="utf-8")
    for needle, msg in [
        ("'Playfair Display', Georgia, serif", "heading font stack missing"),
        ("'Inter', Arial, sans-serif", "body font stack missing"),
        ("assets/fonts/inter-latin.woff2", "self-hosted Inter face missing"),
        ("assets/fonts/playfair-display-latin.woff2", "self-hosted Playfair face missing"),
    ]:
        if needle not in css:
            fail(f"css/style.css: {msg}")
    if not re.search(r"h1\s*,\s*h2\s*,\s*h3\s*\{[^}]*font-family\s*:\s*var\(--font-heading\)", css):
        fail("css/style.css: h1-h3 not mapped to var(--font-heading)")
    if "Lora" in css:
        fail("css/style.css: retired font Lora referenced")
for fname in ["assets/fonts/inter-latin.woff2", "assets/fonts/playfair-display-latin.woff2"]:
    if not (ROOT / fname).exists():
        fail(f"{fname}: font file missing")

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
        path = target.split("#")[0].lstrip("/")
        if path == "":
            path = "index.html"
        elif "." not in path.rsplit("/", 1)[-1]:
            path += ".html"
        if not (ROOT / path).exists():
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
        if "." not in path.rsplit("/", 1)[-1]:
            path += ".html"
        if not (ROOT / path).exists():
            fail(f"sitemap.xml: {loc} has no matching file")
    def loc_file(loc):
        path = loc[len(DOMAIN):].lstrip("/") or "index.html"
        return path if "." in path.rsplit("/", 1)[-1] else path + ".html"
    listed = {loc_file(loc) for loc in locs}
    for p in pages:
        if p.name not in listed:
            fail(f"sitemap.xml: {p.name} not listed")

if failures:
    print("CONTENT QA FAILED:")
    for msg in failures:
        print(f"  - {msg}")
    sys.exit(1)
print(f"Content QA passed: {len(pages)} pages checked against canonical facts.")
