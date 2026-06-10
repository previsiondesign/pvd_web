# Handoff — PreVision Design Website

_Last updated: 2026-06-09_

## Project

Marketing-site mockups for **PreVision Design** (Adam Phillips, Licensed Architect, CA C-30995) — an architectural consulting firm in Marin County, CA specializing in shadow analysis, visual simulation, daylight studies, peer review, and the proprietary Parasolv software.

Git repo, pushed to **https://github.com/previsiondesign/pvd_web** (public).
Live via GitHub Pages at **https://previsiondesign.github.io/pvd_web/** — root `index.html` is a hub page linking all mockup options (rebuilds automatically on push to main; `.nojekyll` present). Excluded via `.gitignore`: `images/projects/` (1.7 GB raw renders/video — exceeds GitHub limits; web-ready copies live in `website-mockups/shared/images/`) and `docs/` (references PDF contains third-party contact info — keep local).

```
images/logos/            Master brand assets (source of truth, exported from Illustrator)
website-mockups/
  option-a/              "Gallery-Forward" — dark theme, single page
  option-b/              "Corporate Professional" — light theme, 5 pages
                         (index, services, portfolio, about, contact)
  option-b1/             B variant "Split Hero" — full width; text left / Bayshore
                         image right hero, utility bar, horizontal service cards
  option-b2/             B variant "Boxed Canvas" — NOT full width on desktop:
                         page sits on a centered 1180px white sheet over a gray
                         backdrop; Bayshore hero w/ scrim, sticky in-frame header
  option-b3/             B variant "Editorial" — full-bleed Bayshore hero with
                         overlapping white panel, centered-stack header, numbered
                         service index, alternating feature rows, light footer
  option-c/              "Narrative Scroll" — dark theme, single page, scroll-driven
  shared/images/         Logo copies + portfolio photos used by all options
docs/                    Resume + firm-profile reference PDFs
PreVision_Design_Firm_Overviews.docx
```

Each option has its own `css/styles.css` (shared palette: blue `#5188B5`, orange `#F18B01`, Montserrat headings / Roboto body via Google Fonts).

## Preview

`.claude/launch.json` defines server **"mockups"**: `python3 -m http.server 8091 --directory website-mockups`.
Pages live at `http://localhost:8091/option-{a,b,c}/index.html`.

## Recently completed: revised logo rollout (2026-06-09)

All mockups now use the revised brand logo (3D box icon + "PReviSION DESIGN" Bebas Neue wordmark). Done and verified in-browser — every placement on all 7 pages, no console errors.

Key facts a fresh session needs:

1. **The master logos are outlined SVGs** — `images/logos/prevision_logo_long.svg` (viewBox 0 0 1214.78 188.05) and `prevision_logo_compact.svg` (stacked). Wordmark text was converted to vector paths, so they're self-contained and safe in `<img>`, email, docs, etc.
   ⚠️ If the logo is ever re-exported from Illustrator: SVG Options → Fonts → Type → **Convert to Outlines**. An earlier export had live `<text>` in Bebas Neue, which renders in a fallback serif and clips when loaded via `<img>`.

2. **Two copies in `website-mockups/shared/images/`**, referenced as plain `<img class="pv-logo">`:
   - `prevision_logo.svg` — default dark-on-light. Used only in Option B's white header.
   - `prevision_logo_reverse.svg` — wordmark `#fff`, box face `#6d6d6d` (otherwise identical). Used everywhere else; every other placement is on a dark background. Generated from the master by swapping the `.st3`/`.st5` fills — regenerate the same way if the master changes.

3. **Sizing** lives in each option's `styles.css` under `.pv-logo` selectors (A: nav 28px / footer 20px; B: header 36px → 28px scrolled / footer 28px inline-styled; C: floating 24px / hero 40px / footer 20px).

4. Brand colors in the logo: box face `#231f20`, grays `#808285`, top `#fff`, blue cast shadow `#6fb9d8`, wordmark `#58595b`.

## State / open items

- Direction: B was judged closest (2026-06-09); three single-page B variants
  (b1/b2/b3, all using bayshore_page02.jpg as hero) were built for comparison.
  Variant nav links are in-page anchors; whichever wins gets B's subpages cloned.
- Option B is the only multi-page option; A and C are single-page index mockups.
- Contact form (option-b/contact.html) is a stub — `onsubmit` shows an alert; needs a real backend (e.g. Formspree) for production.
- `images/logos/PrevisionP.png` (P-mark) is unused in the mockups — possible favicon candidate; no favicon is set on any page.
- Email `info@previsiondesign.com` and "CA License C-30995" appear across all pages — verify before launch.

## Memory

Session memory at `C:\Users\AdamPhillips\.claude\projects\D--Dev-Prevision-Web\memory\` has `brand-logo-font-dependency.md` covering item 1–2 above.
