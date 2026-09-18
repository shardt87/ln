# Accelerating Time to Power — PowerGen e-brochure package

Southwire Power Generation Solutions. September 2026.

## Contents

| Path | What it is |
|---|---|
| `index.html` | The e-brochure: hero film, four application sections, the interactive plant map, films, products and catalog, support, applications, cases, contact. Self-contained apart from the images in `assets/`; fonts and data are embedded. Works offline from a folder or from any static host. |
| `assets/` | Southwire logo (two variants) and eleven plant renders from the original engineering model (JPEG). |
| `PowerGen_eBrochure.pdf` | Email-ready brochure, 8 pages, 16:10, 60 clickable links. |
| `PowerGen_Technical_Appendix.pdf` | Zone cable packages (16), zone decisions, and the full catalog (29 core references + 24 expanded families), 16 pages, 137 clickable links. |
| `source-and-asset-register.md` | What was used, what was not, what is unverified, how the construction diagrams were made. |
| `CHANGELOG.md` | What was consolidated, removed, corrected, left unresolved, and the September 17 rebuilds. |
| `src/data.json` | Single source of truth for zones, catalog, services, cases, contacts. Edit here and rebuild. |
| `src/template.html`, `src/build.py` | Page template (data and fonts injected at build) and the builder: `python3 src/build.py` writes `index.html`, `pdf-main.html` and `pdf-appendix.html` next to `src/`. |
| `src/fonts/` | Inter 300/400/500/600, Latin subset WOFF2, inlined as `fonts-inline.css` (Google Fonts, open licence). |

## Requirements

- **Offline:** open `index.html` directly; everything renders. The hero shows the still; the three films link to the online field guide.
- **Online:** the hero attempts the plant-flythrough film from the field guide. External specification, product and case-study links open on southwire.com.
- No build step is needed to view. To regenerate the PDFs, render `pdf-main.html` and `pdf-appendix.html` at 1440 × 900 px per page with a Chromium-based browser (print backgrounds on, no margins).

## Sections

1. **Solutions**: five application sections (turbine hall, e-house and motor control, switchyard and GSU, plant to grid, battery storage), then the plant map (sixteen zones, one panel each) and the films.
2. **Products**: seven families, application boundaries, the catalog with family, core/expanded and zone filters and search.
3. **Support**: services by phase, the circuit record, lifecycle options.
4. **Applications beyond one configuration**, **documented experience**, **contact**.
