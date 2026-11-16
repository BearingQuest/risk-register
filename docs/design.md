# Bearing Register: design

How Bearing Register uses the Bearing Quest design system. UI work in this repo follows this file (baseline UI-01). Written 15 Nov 2026 by Claude in Dusten's Claude project; approved by Dusten through the pull request that adds it. Requirements are in `docs/PRD.md`; where a screen and the PRD differ, the PRD wins.

## Source

- Design system: "Bearing Quest" design system artifact in Dusten's Claude account (private), version of 6 Nov 2026.
- `docs/design/tokens.json` is a byte-for-byte snapshot of that system's `tokens.json` (SHA-256 `18086c9cd35e6abf6429ff76b84cc28547a897b23d84176629651d06a4a8890c`, taken 15 Nov 2026; the same file the Bearing Quest site snapshotted on 14 Nov). Don't edit it here; when the design system changes, replace the snapshot in its own pull request and record the new hash.
- `docs/design/reference/bundle.css` is the design system's component stylesheet (`bq-btn`, `bq-field`, `bq-alert`, `bq-tier`, `bq-log`), for reference only. The site will generate its own CSS from the tokens.
- `docs/design/logos/` holds the design system's eight SVG marks, unchanged (hashes below).
- `docs/design/screens/` holds the accepted screens from the "Bearing Register Screens" design canvas, light theme only, rendered 15 Nov 2026 at the canvas's board sizes with the design system's own font files. Board 2 (a web-form concept) is left out: it was superseded on 6 Nov 2026.

## Bearing Register's layer

Every app in the family adds one accent and one motif to the shared base.

- **Accent:** `primary` (navy in light, pale slate in dark) is the action color in every data view. `accent` and `brand-orange` stay out of the register table, heat map, change summaries and reports, so nothing orange can be read as a tier (29 Oct 2026).
- **Motif:** the navigator's chart. The Register mark (three bearing lines crossing in a small triangle around a fix, approved 3 Nov 2026), a 1px `border` grid with degree-style ticks behind the heat map and charts, and the logbook (`bq-log`) for history.
- **Family identity:** the Bearing Quest mark beside the "Bearing Register" name in the site header (3 Nov 2026). Cinzel only for the wordmark.
- **Tier scale:** blue to violet, ordered by lightness, never orange or red (approved 3 Nov 2026). A tier color always appears with its tier word and, where quantified, its dollar figure (PRD R77).

| Tier | Fill token | Light | Dark | Text token |
|---|---|---|---|---|
| Low | `tier-low` | #D6E4F0 | #2E4A72 | `on-tier-low`, plus a `control` outline |
| Medium | `tier-medium` | #8DB0D9 | #6F93C4 | `on-tier-medium` |
| High | `tier-high` | #5E5BA8 | #A9A4EC | `on-tier-high` |
| Critical | `tier-critical` | #3B1E6B | #E2D2FB | `on-tier-critical` |
| Unquantified | `surface` | | | `heading`, italic, with a `control` outline and no dollar figure |

## Logos

| File | SHA-256 | Use |
|---|---|---|
| `bearing-register-mark-on-light.svg` | `03ec279e1d39ab65dad1753e6d3e2b075a775b7ff4d6d6fca050702b5f8a65c0` | Register mark on light grounds |
| `bearing-register-mark-on-dark.svg` | `9f4781b8c54d80d5a379f3378f5d6012c259af21efbc6db39d1af53438774021` | Register mark on dark grounds |
| `bearing-quest-mark-on-light.svg` | `4a62583464ca8a17b62973d9e90f46c7d82afcab89156ca6f30c433cb2ef22ac` | Family mark beside the name, light theme |
| `bearing-quest-mark-on-dark.svg` | `f6ac1cd9c1a823b85af350979f745b0957ab1e2119b97a5289093f25489da09a` | Family mark beside the name, dark theme |
| `bearing-quest-mark-mono-navy.svg` | `f5c49a2147808c902262b5ec2518730135178c97e782b8f454d1cfe20371b7c5` | Favicon |
| `bearing-quest-mark-mono-white.svg` | `b4a88eba8d5fd455499b22c515ee5968f5ae2a59a2c1dc487bb49e37809fc4b4` | Watermark on navy bands |
| `bearing-quest-lockup-on-light.svg` | `464c80c7ee3124dcd7e9fef0b9fbf216eb23a08b592bd10ffd506bec8388511c` | README banner, light |
| `bearing-quest-lockup-on-dark.svg` | `6a34f44ae1bd1880d9ff1e14628f7c4c3947a90a7113a81934e20ab7d08ea981` | README banner, dark |

Every mark sits beside the product name in text or has alt text; it is never the only label. The SVGs contain no scripts, event handlers or external references, and a test keeps it that way.

## Screens

| File | Canvas board | Shows |
|---|---|---|
| `01-brg-new-first-risk.png` | 1 | `brg new`: triage and the five answers for a first risk |
| `03-site-register.png` | 3 | Demo site: the register table |
| `04-site-risk-page.png` | 4 | Demo site: one risk (R-0042) |
| `05-site-heat-map.png` | 5 | Demo site: heat map |
| `06-change-summary.png` | 6 | brg's plain-language summary of a proposed change |
| `07-install-init-first-lint.png` | 7 | Install, `brg init` and the first lint |
| `08-lint-messages.png` | 8 | Lint messages: problem, why, fix |
| `09-issue-root-cause.png` | 9 | Issue path with root-cause prompts |
| `10-not-sure-finding.png` | 10 | Not sure path ending in a Finding |

All sample data is fictional (Lantern Bay Software). Known differences between the screens and PRD v1.0, where the PRD wins:

- **Heat map cells (board 5):** the canvas used a hand-drawn lookup table. The real table is generated by the rules in PRD section 6; on the sample edges its rows, Very high likelihood down, are L M H C C / L L M H C / L L M H C / L L M M C / L L L M H.
- **Likelihood labels (boards 1 and 5):** the screens show yearly percentages; the PRD anchors likelihood as loss events per year, with Very high capped at 3 a year.
- **"What could happen" (board 4):** the risk page splits it into cause, event and consequence. It is one sentence (29 Oct 2026; PRD OQ9), so the page shows the sentence.
- **FAIR ranges (board 4):** the note says ranges are 90% intervals; the PRD uses minimum, most likely and maximum with PERT distributions.
- **Closed records (board 3):** the register needs the count of closed and superseded records and the filter to show them (PRD R74).
- **Record IDs (board 3):** IDs wrap inside the table cell ("R-" then "0017"). IDs never wrap: `white-space: nowrap` on the `id` style.
- **Demo-only publishing:** the screens show the demo site. A live register's local build adds a "Confidential" banner on every page (PRD R105).
- **Dark theme:** not drawn. The first UI pull request adds dark screens.

## Rules for UI changes

- Generate CSS custom properties from `docs/design/tokens.json`; never paste raw hex into rules.
- Text 4.5:1 or better, focus rings and control edges 3:1 or better, in both themes; the token contrast test enforces it (PRD R79).
- Color is never the only signal: tier words, labels and icons carry meaning.
- Self-host fonts (Inter, IBM Plex Mono, Cinzel for the wordmark only) with their OFL licence files; no third-party requests (PRD R81).
- Escape all register text and run no inline scripts (PRD R72).
- New screens or a changed layout get new PNGs in `docs/design/screens/` in the same pull request.
- Recorded departures from the design system: none yet.
