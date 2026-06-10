# Handoff — PreVision Design Website

_Last updated: 2026-06-09_

## Project

Marketing-site mockups for **PreVision Design** (Adam Phillips, Licensed Architect, CA C-30995) — an architectural consulting firm in Marin County, CA specializing in shadow analysis, visual simulation, daylight studies, peer review, and the proprietary Parasolv software.

Git repo, pushed to **https://github.com/previsiondesign/pvd_web** (public).
Live via GitHub Pages at **https://previsiondesign.github.io/pvd_web/** — root `index.html` is a hub page linking all mockup options (rebuilds automatically on push to main; `.nojekyll` present).

Hub conventions (per Adam, 2026-06-10):
- The **most-current iterations always go in the first section** of the hub page; demote earlier rounds below when adding a new round.
- Every mockup page carries a fixed **"← All Mockups" button** (bottom-right, `.back-to-hub` in each option's styles.css) linking back to the live hub URL. Add it to any new mockup pages. Excluded via `.gitignore`: `images/projects/` (1.7 GB raw renders/video — exceeds GitHub limits; web-ready copies live in `website-mockups/shared/images/`) and `docs/` (references PDF contains third-party contact info — keep local).

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
  option-b4/             B variant "Gradient Studio" — dark SaaS-style page
                         (inspired by avoice.co landing): gradient mesh hero
                         panel w/ dot grid + serif-italic accents (Playfair
                         Display), framed Bayshore hero shot, mini service
                         cards, feature deep-dives w/ gradient image cards,
                         mock Parasolv UI window, gradient CTA band
  option-b2-autumn/      B2 color study — navy/slate + amber buttons, rust badges
                         (palette: 07111D 39444D 5D5D5D E5E5DF DB9941 AE2C11)
  option-b2-blues/       B2 color study — teal + charcoal/warm grays, monochrome
                         (palette: D9D4D1 BAB1AD AEC0C2 098698 3D444B 505A63)
  option-b2-preppy/      B2 color study — navy/steel + camel/sand accents
                         (palette: 071739 4B6382 A4B5C4 CDD5DB A68868 E3C39D)
  option-c/              "Narrative Scroll" — dark theme, single page, scroll-driven
  shared/images/         Logo copies + portfolio photos used by all options
pallettes/               Palette sample JPGs (local only, gitignored — hex values
                         captured in the b2-* variant stylesheets)
PreVision_Site_Copy.docx All site copy (B2 home + option-b subpages) organized by
                         page/section in editable tables — for copy revision
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

- Direction: **B2 "Boxed Canvas" selected** (2026-06-10). Three color studies
  (option-b2-autumn/blues/preppy) generated from palette samples in pallettes/;
  no palette picked yet. Copy revision underway via PreVision_Site_Copy.docx —
  when edits come back, apply them to the winning variant and clone B's
  subpages (services/portfolio/about/contact) into its style.
- Hero (B2 + color variants, 2026-06-10): headline simplified to "Analysis for
  the Built Environment"; static image replaced by a 5-slide slideshow cycling
  project types with the subheadline (tagline) synced to the active slide
  (5s interval, crossfade, clickable dots; taglines in data-tagline attrs).
  Per Adam: avoid "consulting" language; "sun/shadow" is the preferred term —
  note the copy doc still shows the old static hero copy.
- **Before/after rule (per Adam, 2026-06-10): any image with a before/after
  pair should be shown as a sequence — 1s on the before, 1s crossfade, 3s on
  the after.** Hero slides implement this via `.has-ba` (`.ba-before`/`.ba-after`
  imgs). Pairs in shared/images/portfolio: bayshore_page01→02 (page01 resized
  from images/projects/sims/Old Bayshore/FINAL_OldBayshore_VisSims_Page_01.jpg),
  61gough_before→after, sfport_view1→_after, sfport_view3→_after,
  sfport_view10→_after, mission_view1_before→after, ygnacio_before→after.
  Currently applied to hero slides 1 (Bayshore), 2 (61 Gough), 4 (SF Port);
  not yet to the Featured Work grid.
- Earlier exploration: B variants b1/b3/b4 (Bayshore hero per request, b4 styled
  after an avoice.co-inspired dark gradient look) remain live for reference.
- Option B is the only multi-page option; A and C are single-page index mockups.
- Contact form (option-b/contact.html) is a stub — `onsubmit` shows an alert; needs a real backend (e.g. Formspree) for production.
- `images/logos/PrevisionP.png` (P-mark) is unused in the mockups — possible favicon candidate; no favicon is set on any page.
- Email `info@previsiondesign.com` and "CA License C-30995" appear across all pages — verify before launch.

## Memory

Session memory at `C:\Users\AdamPhillips\.claude\projects\D--Dev-Prevision-Web\memory\` has `brand-logo-font-dependency.md` covering item 1–2 above.
