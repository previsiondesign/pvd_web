# Handoff — Prevision Design Website

_Last updated: 2026-06-09_

## Project

Marketing-site mockups for **Prevision Design** (Adam Phillips, Licensed Architect, CA C-30995) — an architectural consulting firm in San Francisco, CA specializing in shadow analysis, visual simulation, daylight studies, peer review, and the proprietary Parasolv software.

Git repo, pushed to **https://github.com/previsiondesign/pvd_web** (public).
Live via GitHub Pages at **https://previsiondesign.github.io/pvd_web/** — root `index.html` is a hub page linking all mockup options (rebuilds automatically on push to main; `.nojekyll` present).

Hub conventions (per Adam, 2026-06-10):
- The **most-current iterations always go in the first section** of the hub page; demote earlier rounds below when adding a new round.
- **Highlight the selection trail**: the chosen card in each round gets
  `class="card selected"` + a `<span class="pick">Selected</span>` badge, and the
  "Selection path" chip strip at the top is extended with each new pick.
  Current path: B → B2 → B2 Autumn → Type Business.
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
  option-b2-type-business/  Type study, Inter throughout ("businessy") — Adam's
                            pick so far. Switched to AUTUMN palette 2026-06-10
                            (others remain Preppy). Lockup tuned per Adam: icon
                            37.4px (1.1x original), text 20.2px, gap 18px,
                            semibold on "vision" only, centered on the bar
  option-b2-type-sleek/     Type study on Preppy: Syne headings + Work Sans body
  option-b2-type-tech/      Type study on Preppy: Space Grotesk + IBM Plex Sans,
                            IBM Plex Mono for nav/stat/badge labels
                            (all three: header/footer logo is now a lockup —
                            icon-only SVG + lowercase "prevision design" as live
                            type; icon copies at shared/images/prevision_icon.svg
                            and _reverse.svg, generated from
                            images/logos/prevision_logo.svg)
  under-construction/    Branded "Site Under Construction" placeholder — Autumn
                         palette + Inter with the icon/lowercase lockup (matches
                         Type — Business). Fully self-contained single file
                         (inline CSS + inline icon SVG, no external assets except
                         Google Fonts); strip the .back-to-hub block for
                         production. Per Adam: no domain eyebrow, short lede,
                         footer is just firm name + San Francisco, CA
pallettes/               Palette sample JPGs (local only, gitignored — hex values
                         captured in the b2-* variant stylesheets)
Prevision_Site_Copy.docx All site copy (B2 home + option-b subpages) organized by
                         page/section in editable tables — for copy revision
docs/                    Resume + firm-profile reference PDFs
Prevision_Design_Firm_Overviews.docx
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
  no palette picked yet. Copy revision underway via Prevision_Site_Copy.docx —
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
- No favicon is set on any page — `images/logos/prevision_logo.svg` (icon-only 3D box, also copied to shared/images/prevision_icon.svg) is the natural candidate. (The old PrevisionP.png P-mark was removed 2026-06-10.)
- Email `info@previsiondesign.com` and "CA License C-30995" appear across all pages — verify before launch.

## Domain migration (in progress, 2026-06-10)

Moving previsiondesign.com: registrar Wild West Domains/secureserver.net
("Inexpensive Domains" reseller account) → Porkbun; web Wix → GitHub Pages;
email stays Office 365. Transfer initiated and approved at the losing
registrar; pending completion at Porkbun. DNS currently hosted by Wix
(ns10/ns11.wixdns.net) — **keep the Wix plan active until cutover**.

Production repo: **github.com/previsiondesign/site** (local clone D:\Dev\site)
— serves the under-construction page at **www.previsiondesign.com**.

**Cutover completed 2026-06-10:** domain at Porkbun (expiry 2027-06-20),
nameservers on Porkbun's current fleet (*.ns.porkbun.com), all 12 records
verified serving (O365 mail set + SmartFile files CNAME + GitHub Pages
apex A/www CNAME). Site confirmed live on the domain from GitHub.
Wrinkle hit on the way: Porkbun served a frozen imported zone (SOA serial
never incremented; panel edits ignored) — fixed by Porkbun support
("pushed out a new wave of propagation").

HTTPS: cert issued 2026-06-10 (needed a custom-domain remove/re-add nudge
after the DNS freeze); **Enforce HTTPS enabled**. Verified: https://www 200,
apex http+https 301 → https://www. (http://www → https redirect was still
propagating through GitHub's CDN at last check — expected within the hour.)

Remaining:
1. Adam: email round-trip test (send + receive on adam@previsiondesign.com).
2. After a few stable days: cancel the Wix site plan (LAST step — Wix DNS
   is dead weight now but harmless; nothing references Wix after this).

## Client portal — LIVE at https://clients.previsiondesign.com (2026-06-12)

Full E2E green (9/9) on the custom domain with TLS: login/sessions, Dropbox
auth, chunked upload committed to Dropbox, file-request fallback, cross-client
isolation 403, logout. Cloudflare Pages project "clients" (clients-ec3.pages.dev)
auto-deploys from the private repo on push to main; secrets live in the CF
project env. The live placeholder site footer links to the portal.

**Client onboarding runbook:** (1) add `"CODE": {"name": "...", "folder": "/Name"}`
to the CLIENTS_JSON env var in CF Pages settings → Retry deployment; (2) in
Dropbox create `Apps/Prevision Clients/<Name>/To Client` and `/From Client`;
(3) email the client their code + https://clients.previsiondesign.com.
Test with: `powershell -File scripts/e2e-test.ps1 -BaseUrl ... -Code ...`

Loose ends: download E2E still SKIP until a file is seeded in
`TEST/To Client` (then rerun the script); the dead `files` →
custom.smartfile.com record at Porkbun still needs deleting; e2e test
files accumulate in `TEST/From Client` (harmless, delete whenever).

## Client portal (built 2026-06-12, original notes)

**github.com/previsiondesign/clients** (private; local clone D:\Dev\clients) —
Dropbox-backed client file exchange for **clients.previsiondesign.com**.
Static UI (Autumn/Inter/lockup, matches production placeholder) + Cloudflare
Pages Functions. Per-client access codes → HMAC-cookie sessions; downloads via
Dropbox temporary links from `<Client>/To Client`; chunked in-page uploads
(~1 GB cap) into `<Client>/From Client`; Dropbox file request fallback for
multi-GB. Folder isolation enforced server-side; Dropbox refresh token only in
Cloudflare secrets. Full runbook in that repo's README.

Verified locally via wrangler: login good/bad/tampered, session round-trip,
cross-client path → 403, clean 502s on upstream failure. Remaining (Adam,
console steps per README): create Dropbox app + run scripts/get-refresh-token.js,
create Cloudflare Pages project + secrets, Porkbun `CNAME clients` →
`<project>.pages.dev` (and delete the dead `files` → custom.smartfile.com
record), then E2E test with TEST client and link "Client Area" from the live
site footer.

## Memory

Session memory at `C:\Users\AdamPhillips\.claude\projects\D--Dev-Prevision-Web\memory\` has `brand-logo-font-dependency.md` covering item 1–2 above.
