# Prevision Design — Website Mockups

Marketing-site mockups for [Prevision Design](https://previsiondesign.com), an architectural consulting firm specializing in shadow analysis, visual simulation, daylight studies, and CEQA visual impact work.

## Options

| Option | Style | Structure |
|--------|-------|-----------|
| [A — Gallery-Forward](website-mockups/option-a/index.html) | Dark theme | Single page |
| [B — Corporate Professional](website-mockups/option-b/index.html) | Light theme | 5 pages (index, services, portfolio, about, contact) |
| [C — Narrative Scroll](website-mockups/option-c/index.html) | Dark theme | Single page, scroll-driven |

Shared brand assets (logos, portfolio photos) are in `website-mockups/shared/images/`. Master logo SVGs are in `images/logos/`.

## Preview locally

```sh
python3 -m http.server 8091 --directory website-mockups
```

Then open `http://localhost:8091/option-{a,b,c}/index.html`.

See [HANDOFF.md](HANDOFF.md) for project status and working notes.
