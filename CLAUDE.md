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
- Contact email: TBD — do not invent one. The `info@example.com`
  placeholders in `contact.html` and `js/script.js` remain until Keith
  supplies the real address.
- Canonical domain for JSON-LD `url` fields: TBD — leave `"#"` until
  Keith confirms which web property this site serves.
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

## QA checklist for site changes

1. Render QA: all pages in light, dark, mobile (~390px, nav toggle
   open), and forced-colors modes; zero console errors; no broken
   internal links or assets.
2. Content QA: grep the working tree against the canonical facts
   above; zero stale values (old license numbers, placeholder contacts
   the facts list has since resolved) before push.
