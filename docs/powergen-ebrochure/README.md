# Accelerating Time to Power — PowerGen e-brochure package

Southwire Power Generation Solutions. September 2026.

## Contents

| Path | What it is |
|---|---|
| `index.html` | The responsive e-brochure. Self-contained apart from the six images in `assets/`; fonts and data are embedded. Works offline from a folder or from any static host. |
| `assets/` | Six plant renders from the original engineering model (JPEG). |
| `PowerGen_eBrochure.pdf` | Email-ready brochure, 10 spreads, 16:10, clickable links. |
| `PowerGen_Technical_Appendix.pdf` | Zone cable packages (16), zone decisions, and the full catalog (29 core references + 24 expanded families), clickable links. |
| `source-and-asset-register.md` | What was used, what was not, what is unverified. |
| `CHANGELOG.md` | What was consolidated, removed, corrected, left unresolved. |
| `src/data.json` | Single source of truth for zones, catalog, services, cases, contacts. Edit here and rebuild. |
| `src/index.template.html`, `src/build.py` | Page template and build script (`python3 src/build.py` writes `index.html`, `pdf-main.html`, `pdf-appendix.html`). |
| `src/fonts/` | Nimbus Sans / Nimbus Sans Narrow, Latin subset, WOFF2 (URW base35, open licence). |

## Requirements

- **Offline:** open `index.html` directly; everything renders except the three films, which link to the online field guide.
- **Online:** the hero attempts the plant-flythrough film from the field guide and shows the still until it can play. External specification, product and case-study links open on southwire.com.
- No build step is needed to view. To regenerate the PDFs, render `pdf-main.html` and `pdf-appendix.html` at 1440 × 900 px per page with a Chromium-based browser (print backgrounds on, no margins).

## Levels

1. **Customer story**, sections 01–07: challenge, plant, cable offering, execution, applications, experience, conversation.
2. **Application exploration**: the plant map; select a zone for equipment, cable families, products, services, considerations and spec links.
3. **Technical reference**: the catalog at the end of the page, filterable by family and searchable; the appendix PDF for print.
