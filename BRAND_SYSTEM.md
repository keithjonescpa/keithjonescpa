# TheCPATaxProblemSolver™ — Brand System v5.0 (typography)

Adopted by Keith 2026-07-23 (relayed in Claude Code session). This file
is the repo-local reference; the full brand system lives in the Figma
file "🎨 Brand System — TheCPATaxProblemSolver".

## Typography rule

- **Operational assets** (hubs, SOPs, dashboards, internal sites):
  Inter only.
- **Marketing assets** (keithjones.cpa, landing pages, webinar pages,
  lead magnets — **this site is a marketing asset**): Playfair Display
  for headings, Inter for body.
- **Retired:** Lora — do not use anywhere.

## Implementation in this repo

Fonts are **self-hosted** (`assets/fonts/*.woff2`, latin subset,
variable weight 400–700) rather than loaded from Google Fonts, so the
site's strict `Content-Security-Policy: default-src 'self'` stays
intact and no third-party request is made.

```css
--font-heading: 'Playfair Display', Georgia, serif;  /* h1, h2, h3 */
--font-body: 'Inter', Arial, sans-serif;             /* everything else */
```

## Type scale

| Token   | Size | Weight  | Use               |
|---------|------|---------|-------------------|
| H1      | 40px | Bold    | Page titles       |
| H2      | 30px | Bold    | Section headings  |
| H3      | 24px | Bold    | Subsections       |
| Body    | 16px | Regular | Default text      |
| Small   | 14px | Regular | Secondary text    |
| Caption | 12px | Regular | Labels, metadata  |
