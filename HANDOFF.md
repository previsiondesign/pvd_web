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
  the Built Environment"; static image replaced by a slideshow cycling project
  types with the subheadline (tagline) synced to the active slide (crossfade,
  clickable dots; taglines in data-tagline attrs). Per Adam: avoid "consulting"
  language; "sun/shadow" is the preferred term — note the copy doc still shows
  the old static hero copy.
- **Hero rebuilt on real project imagery (2026-07-28, option-b2-type-business
  only — the other variants still run the old portfolio slideshow).** Five
  *series* of **6 s each**, per Adam's masters in `projects/Headline Images`:

  | # | series | frames |
  |---|--------|--------|
  | 0 | Visual sims — Old Bayshore before/after | HL01 2s + HL02 4s |
  | 1 | Shadow studies — shadow-duration exhibits | HL03–08, 1s each |
  | 2 | Animation — SFMTA simulation (mp4) | HL09 6s |
  | 3 | Daylight/lighting analysis | HL10–15, 1s each |
  | 4 | Shadow shaping — insolation massing (placeholder) | HL16 6s |

  Per-frame hold times come from the `_#s` suffix in each filename and live in
  `data-dur` on each `.hero-frame`. Series 0 follows the before/after rule
  below. `scripts/build-hero-images.py` rebuilds the shipped derivatives
  (`website-mockups/shared/images/hero/`) from the masters: **137 MB of PNG →
  1.93 MB of WebP**, widths by role (photos 1800 / exhibits 1200 / daylight
  1800 wide, HL16 900 because that is its master). The masters stay local —
  `projects/` is gitignored.
  - **All five series are full-bleed** (`object-fit: cover`) per Adam
    (2026-07-28): legends, title blocks and captions crop away and the tagline
    carries the explanation. An earlier pass letterboxed the exhibits to the
    right — that is gone, along with `.fit-contain` / `.hero.is-contain`.
  - `--focus` sets the vertical crop; `.focus-upper` (42%) is on the shadow maps
    and the insolation tower, whose subjects sit above centre. Note
    `object-position` percentages offset the *overflow*, so 42% shows the band
    from 21% to 71% of the map's height, not 42% ± half.
  - `.hero-scrim` is two stacked gradients: a wash down the left (0.72 → 0 by
    62%) plus the bottom fade. The wash is what keeps white type readable over
    the near-white shadow maps without muddying the imagery on the right; a
    single stronger vertical gradient would flatten everything. At ≤768 px the
    text spans the full width, so that breakpoint swaps in a stronger vertical
    scrim (0.40 → 0.92) instead.
  - `.hero p.hero-tagline` reserves its tallest wrap so rotating taglines never
    shift the buttons — 2 lines on desktop, 3 at ≤768 px (`.hero p` specificity
    is needed to beat the base rule).
- **Mobile-only hero/stats/contact pass (2026-07-28, ≤768 px; desktop verified
  unchanged).** Per Adam, on phones only:
  - The two hero buttons move **out of the image into the grey stats bar**, side
    by side above the stats. `main.js` relocates the existing `.hero-actions`
    into `#stats-actions` on a `matchMedia('(max-width: 768px)')` listener and
    puts it back past the breakpoint — moved, not duplicated, so the labels have
    one source of truth. (Safe because the hero already needs JS to show
    anything.) `.stats-actions:empty` is hidden, so desktop sees nothing. This
    is why `.inner.stats-grid` was split into `.inner > .stats-actions +
    .stats-grid`; desktop renders identically.
  - Only **Projects Completed and Client Organizations** show, on one line —
    `.stat-item:nth-child(2)`/`(4)` (Years of Experience, Licensed Architect)
    are hidden. They still render on desktop. Their labels also shorten to
    **"Projects" / "Clients"** here (`.lbl-long` / `.lbl-short` spans, toggled by
    `display`, so the unused wording stays out of the accessibility tree).
    Desktop keeps the long labels — with four across, shortening two of them
    unbalances the row.
  - The headline block sits lower now that the buttons are gone: 222 px of the
    420 px hero is clear above the type, up from ~60 px. The mobile scrim was
    lightened at the top to suit (0.16 → 0.42 → 0.90) — the headline still
    measures 4.95:1 over near-white shadow-map paper, well past the 3:1 large
    text needs.
  - Contact page: the dashed drop zone collapses to a plain **Attach files
    button** (there is nothing to drag on a touch device). The file input,
    click, keyboard and drop handlers are untouched, so desktop drag-and-drop
    still works; the size/type limits move to a `.fd-note` line below the button
    (hidden on desktop, where the `<em>` inside the zone carries them). Vertical
    spacing tightened throughout: page hero 30/26, section 26/40, field gap 14,
    contact grid 28.
- **Discipline cards carry work snippets, not line icons (2026-07-28, both
  breakpoints).** Each of the five service cards has a 4.2:1 banner flush to the
  card's top edge, built from the masters in `projects/Disciplines` by
  `scripts/build-discipline-images.py` (25.4 MB → 107 KB of WebP in
  `website-mockups/shared/images/disciplines/`). The sixth card is the CTA and
  has no image, matching Adam's reference. The old `.service-icon` SVGs are gone.
  - Crops are stored as **normalised centre + width**, not pixels, so they
    survive a master being re-exported at a different size. Each is aimed at the
    recognisable part of the analysis, because a centred crop of a whole sheet
    reads as noise at 800×190. Note `daylighting.png` is **not** the same frame
    as hero HL10 — its subject is the warm shaft from the french doors, so a
    centred crop landed on blank floor; it is offset to 0.42/0.57.
  - Framing notes from review go in `NUDGE` **in rendered card pixels** (the
    338×80 desktop banner), so "down 31, left 38" can be typed in as given and
    the script converts into master coordinates — positive dx right, positive dy
    down, inverted internally because moving the content one way means moving the
    crop window the other. It warns if a nudge hits the edge of the master rather
    than silently clamping, which would look like the note was ignored.
    Adam's 2026-07-28 pass: shadow −38/+31, shaping 0/+12, daylight +4/−9,
    sims 0/+10, peer review unchanged.
  - 800 px wide covers the widest the banner ever gets (380 px on a phone,
    338 px in the 1180 px desktop frame) at just over 2× for retina.
  - Resting state is `grayscale(1) brightness(1.3) contrast(0.86)` (lightened
    from 1.08/0.94 per Adam, 2026-07-28 — candidates were rendered offline and
    1.42/0.80 washed the shadow map out entirely), rolling to full colour over
    550 ms, per card.
  - What singles a card out depends on the device. Hover devices use
    `:hover`/`:focus-within` inside `@media (hover: hover)`. **Touch devices have
    no hover, so `main.js` lights whichever card is nearest the middle of the
    viewport as you scroll** (`.is-lit`, rAF-throttled passive scroll listener,
    attached only when `hover: hover` does not match and torn down if it starts
    to). A threshold of 0.35 × viewport height means nothing is lit while the
    grid is away from the middle. Verified against simulated scroll offsets at
    430×932: nothing lit before the grid, each of the five cards lights in turn,
    nothing after; the CTA card is excluded since it has no snippet.
    `prefers-reduced-motion` drops the transition (colour still changes, just
    instantly).
  - Caveat on verification: the browser pane stopped compositing partway through
    this change, and **`filter` transitions run on the compositor** — so a frozen
    transition returns its start value from `getComputedStyle` and outranks even
    inline `!important`, which looks exactly like a broken cascade. It isn't.
    Geometry, loading and the authored rules were verified through the CSSOM, and
    both states were rendered offline to check the look; the hover roll itself was
    not confirmed on screen.
  - **Cross-fades stack rather than swap** (Adam asked for smooth transitions):
    the incoming series/frame fades in on a raised z-index while the outgoing
    layer stays fully opaque underneath until it is covered, so a transition
    never dips through the background the way two simultaneous opacity ramps
    do. Verified: 0% background visible across a whole transition. This is why
    `.hero-slides` needs `isolation: isolate` — without a stacking context those
    raised z-indexes escape and paint the imagery over the headline block.
    Frame fade defaults to 1 s after a ≥2 s hold and 600 ms between the 1 s
    study frames; `data-fade` on a frame overrides that, and the Bayshore
    before/after uses `data-fade="2000"` per Adam (2026-07-28) — so that series
    reads 2 s existing / 2 s cross-fade / 2 s proposed, superseding the older
    1s-1s-3s before/after rule for the hero. Series fade is 1 s (`SERIE_FADE`
    in main.js must stay in step with the CSS transition).
  - **Ken Burns** drift is on `.hero-serie`, not the individual frames, so the
    six shadow-duration steps stay registered with each other while they
    cross-fade — drifting them separately made the same base map jitter. Four
    keyframe variants (`kb-drift-a`…`d`) are assigned by `:nth-child`; the video
    is excluded via `.is-video`. Runs 9 s against a 6 s series so it is still
    moving through the hand-off and never snaps back on screen; paused unless
    the series is active; `show()` restarts it. Scale runs 1.08→1.16 (1.18 on
    the tower), which stays inside the 1800 px masters' headroom over a 1180 px
    hero, so nothing softens. Drift is capped well inside the overflow the scale
    creates — verified no edge can pull into frame at 1280 px or 375 px, worst
    case 9.3 px of slack. `prefers-reduced-motion` disables drift and fades.
    **`.hero-scrim` is `inset: -2px`, not 0, because of this drift**: the
    transform puts each series on its own compositing layer, and that layer's
    clip against `.hero`'s `overflow: hidden` rounds outward to whole device
    pixels, so a 1 px row of undimmed image bled through along the bottom edge
    (Adam spotted it, 2026-07-28). Overhanging the clip box covers the row;
    `.hero` clips the excess, so nothing outside the hero is darkened. Confirmed
    by A/B: the row disappears when the transform is removed.
  - `hl09-sfmta.mp4` is **compressed** (2026-07-28): 8.3 MB → 1.98 MB, H.264
    CRF 23 preset slow, audio dropped (the hero plays it muted), `+faststart`,
    trimmed to 6.05 s because the series only holds 6 s and `currentTime` resets
    to 0 each time. SSIM 0.970 against the master; CRF 26 saved another 600 KB
    but fell to 0.960, not worth it on the page's one moving element.
    `scripts/build-hero-images.py` now does this — it needs **ffmpeg on PATH**
    (installed here via `scoop install ffmpeg`) and skips the video with a
    notice rather than shipping the uncompressed master if ffmpeg is missing.
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

## Contact form — LIVE (2026-06-14)

B2-Business `contact.html` posts to **https://clients.previsiondesign.com/api/contact**
(Cloudflare Pages Function in the `clients` repo) which emails the inquiry via
**Resend** with reply-to set to the inquirer. Optional attachments: 3 files,
10 MB each / 20 MB total, delivered as email attachments.
Env vars on the CF `clients` project: `RESEND_API_KEY` (secret), `CONTACT_TO`,
optional `CONTACT_FROM`. `GET /api/contact` returns a boolean-only config check.

Two gotchas learned the hard way:
1. **"Retry deployment" did NOT bind new env vars** — a fresh commit/deployment
   was required. If the form 503s, check `GET /api/contact` then push a commit.
2. Resend's shared `onboarding@resend.dev` sender **only delivers to the Resend
   account's own address**, hence `CONTACT_TO=adam@previsiondesign.com` for now.

Sending domain **send.previsiondesign.com** verified in Resend 2026-07-27
(subdomain only — root SPF/MX for O365 untouched; DKIM/SPF/DMARC all align).
Sends as `website@send.previsiondesign.com` to `info@previsiondesign.com`.

**Uploads go to Dropbox, not email attachments** (changed 2026-07-27): files
land in `Apps/Prevision Clients/_Website Inquiries/<timestamp> <name>/` and the
notification carries a file list + a login-required Dropbox folder link (no
public share links). Falls back to email attachments if Dropbox is unreachable,
so an inquiry is never lost. Caps: 3 files, 10 MB each, 30 MB total (client and
server limits must stay in sync — js/main.js and functions/api/contact.js).

⚠️ **Deliverability is the weak link.** O365 quarantined a test as **High
Confidence Phish** — because the mail arrives externally From a subdomain of
previsiondesign.com addressed *to* previsiondesign.com, which reads as spoofing.
Auth is fine (SPF/DKIM/DMARC all pass); this is Defender heuristics.
Key gotcha: a **manually added** Tenant Allow/Block List entry only overrides
"upto regular confidence phish" and the scope is not editable. Only an allow
entry created via **Actions & submissions → Submissions → report false positive
→ "allow messages like this"** overrides high-confidence phish. Also consider
Anti-phishing policy → Trusted senders and domains.
Structural alternative if filtering keeps fighting: send the notification From a
domain that is NOT previsiondesign.com (removes the self-spoof signal entirely).

**Safety net:** every submission writes `inquiry.txt` into the same Dropbox
folder as the uploads, so a quarantined notification costs a delay, never the
lead. Verified 2026-07-27 with a no-attachment submission.

Verified 2026-06-14: direct POST and a real browser submission from
previsiondesign.github.io both returned ok with attachments.

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

In-browser preview added 2026-06-12: /api/view streams pdf/images/txt/video
inline (filename click opens a tab); other types fall back to download.

**Upgrades 2026-06-13 (all live, E2E 11/11):**
- Subfolder navigation: portal lists folders and lets clients drill in
  (breadcrumb back out), staying within the `To Client` subtree.
- **Access model changed to slug-based unique links.** CLIENTS_JSON is now
  keyed by URL slug; each project has an OPTIONAL `code`. No code → the link
  `clients.previsiondesign.com/<slug>` grants access (recommend unguessable
  slugs); `code` present → password-protected. `/api/login` replaced by
  `/api/access`; SPA `_redirects` serves the portal for any `/<slug>`.
- Adam's existing `TEST-0000` config entry still works as an open link.

Open request not yet done — **folders inside real project dirs (#1):** requires
switching the Dropbox app from App-folder to **Full Dropbox** access (recreate
app + new token + update 3 CF secrets + rewrite CLIENTS_JSON folder paths to
absolute). No code change needed — paths are already arbitrary. Tradeoff: token
gains full-Dropbox reach. Awaiting Adam's go/no-go on the security tradeoff.

Loose ends: the dead `files` → custom.smartfile.com record at Porkbun still
needs deleting; e2e test files accumulate in `TEST/From Client` (harmless).

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
