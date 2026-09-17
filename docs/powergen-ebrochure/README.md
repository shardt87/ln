# Accelerating Time to Power — PowerGen e-brochure package

Southwire Power Generation Solutions. September 2026. Plant-first build.

## Contents

| Path | What it is |
|---|---|
| `index.html` | The e-brochure: a full-screen interactive plant stage with zone pins, a zone panel and five content drawers. Self-contained apart from the images in `assets/`; fonts and data are embedded. Works offline from a folder or from any static host. |
| `assets/` | Eight plant renders from the original engineering model (JPEG). Drop an `assets/plant.glb` here to enable the 3D model viewer. |
| `PowerGen_eBrochure.pdf` | Email-ready brochure, 8 pages, 16:10, 60 clickable links. |
| `PowerGen_Technical_Appendix.pdf` | Zone cable packages (16), zone decisions, and the full catalog (29 core references + 24 expanded families), 16 pages, 137 clickable links. |
| `source-and-asset-register.md` | What was used, what was not, what is unverified. |
| `CHANGELOG.md` | What was consolidated, removed, corrected, left unresolved, and the September 17 rebuild. |
| `src/data.json` | Single source of truth for zones, catalog, services, cases, contacts. Edit here and rebuild. |
| `src/template.html`, `src/build.py` | Page template (data and fonts injected at build) and the builder: `python3 src/build.py` writes `index.html`, `pdf-main.html` and `pdf-appendix.html`. |
| `src/fonts/` | Instrument Sans and Geist Mono, Latin subset WOFF2, inlined as `fonts-inline.css` (Google Fonts, open licence). |

## Requirements

- **Offline:** open `index.html` directly; everything renders. The three films link to the online field guide.
- **Online:** external specification, product and case-study links open on southwire.com.
- No build step is needed to view. To regenerate the PDFs, render `pdf-main.html` and `pdf-appendix.html` at 1440 × 900 px per page with a Chromium-based browser (print backgrounds on, no margins).

## How it is organised

1. **The plant.** Six views on one stage. Drag to pan, scroll or pinch to zoom, double-click to zoom in. Sixteen pins; select one for the zone package.
2. **Drawers**, from the header: Cable (families, boundaries, catalog with filters and search), Execution, Applications, Cases, Start a review. Escape closes any panel or drawer.
3. **Print**: the email PDF for the first conversation, the appendix for the engineer.
