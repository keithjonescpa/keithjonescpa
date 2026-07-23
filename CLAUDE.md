# CLAUDE.md — keithjonescpa/keithjonescpa

Guidance for AI-assisted sessions working in this repository.

## Canonical facts — source of truth for all site copy

Every page must match these values. Content QA greps the working tree
against this list before any push; a render pass alone cannot catch a
wrong fact.

- Firm name: Keith L. Jones, CPA
- Florida CPA license: **AC0028367** (verified against keithjones.cpa
  2026-07-07; DBPR is the authoritative registry if any doubt)
- Phone: 844-888-1040
- Contact email: keith@keithjones.cpa (confirmed by Keith 2026-07-07)
- Canonical domain for THIS SITE: **https://fdor.keithjones.cpa**
  (decided 2026-07-16). The apex https://keithjones.cpa serves Keith's
  main ~290-URL content property and is NOT replaced by this repo —
  this site is an FDOR-defense campaign funnel on the subdomain.
  Never point the apex at this repo. URLs are extensionless (Workers
  clean URLs): canonical/OG/JSON-LD/sitemap use `/about`, not
  `/about.html`. JSON-LD `url` fields use the root for
  ProfessionalService and the page's own URL for page-level schema
  types.
- Hosting (decided 2026-07-16): Cloudflare Workers static assets,
  Git-connected to this repo — production deploys from `main` on
  every push. Staging URL:
  https://keithjonescpa.thecpataxproblemsolvers.workers.dev
- Typography (Brand System v5.0, adopted 2026-07-23): this site is a
  MARKETING asset — headings use Playfair Display, body uses Inter,
  Lora is retired everywhere. Fonts are self-hosted in `assets/fonts/`
  (never loaded from Google Fonts — keeps CSP `default-src 'self'`).
  Full rules: `BRAND_SYSTEM.md`.
- Any results claim ($15M+, 70%+, case counts) must carry the
  no-guarantee disclaimer ("Past results are not a guarantee of future
  outcomes.").

## Repository rules

- This is a PUBLIC repository. Never include client PII, TINs, client
  entity names, or matter facts in any file, commit message, branch
  name, issue, or pull request.
- 2026-07-07: GitHub approved by Keith for public-facing web assets
  and version control (dated decision recorded via Claude Code
  session).

## Workflow rules

- All changes reach `main` via pull request. Keith merges, or
  explicitly delegates the merge in writing.
- CI (`.github/workflows/qa.yml`) runs `scripts/qa.py` on every pull
  request and push to `main`; it must pass before merge.
- After merging, verify `main` contains the branch's latest commit —
  a stale-head merge silently dropped a commit here on 2026-07-07.
- Keep pull requests small and short-lived; delete branches after
  merge.
- New dated decisions land in this file within 15 minutes of being
  made.

## QA checklist for site changes

1. Render QA: all pages in light, dark, mobile (~390px, nav toggle
   open), and forced-colors modes; zero console errors; no broken
   internal links or assets.
2. Content QA: grep the working tree against the canonical facts
   above; zero stale values (old license numbers, placeholder contacts
   the facts list has since resolved) before push.
