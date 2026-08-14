# TASK: Award-quality executive brochure — "Protecting Time to Power" (Southwire × NRG)

You are building a print-ready executive brochure over multiple work sessions. Work autonomously,
iterate, and self-QA visually after every pass. Do not stop at "generated without errors" —
stop only when every page passes the QA gates below.

---

## 0. Setup — skills and tools

- READ FIRST, before writing any code: the `pdf` skill and the `canvas-design` skill
  (design philosophy for static print pieces). If a `frontend-design` skill is present, read it
  too for typography/spacing discipline. Follow canvas-design's guidance on grids, restraint,
  and composition — this is a print object, not a slide deck.
- No connectors or external services are needed. Everything is local Python:
  `reportlab` (layout), `pypdfium2` (rasterize for QA and asset extraction), `pikepdf`/`pypdf`
  (assembly), `Pillow` (image prep).
- Web search (only if available): use it ONLY to re-verify the two public facts in §4.
  Do not import any other web content.
- Do NOT use AI image generation. All imagery comes from the source PDFs listed below.

## 1. Inputs (place in working directory before starting)

- `Power_Gen_Southwire_NRG_Teaser_3.pdf` — latest content source (copy + structure)
- `Power_Gen_Southwire_NRG_Teaser_Rev10.pdf` — the CORRECTED wording reference. Where Teaser_3
  and Rev10 disagree on wording, Rev10 wins (Teaser_3 was exported from the uncorrected
  PowerPoint source and reintroduced known errors).
- `Print_Test.pdf` (if present) — hexagon cover texture source

Extract raster assets at 300 dpi minimum with pypdfium2 (`scale ≥ 4.2`):
the 3×1 plant-zone isometric render, the cover plant render, the staging-yard/reel render,
and the hexagon texture. Crop generously; never upscale.

## 2. Deliverable

`Southwire_PowerGen_Brochure_NRG_Rev01.pdf`
- 8 pages, saddle-stitch imposition NOT required — deliver reader spreads: 8 sequential
  Letter pages (8.5×11 portrait? NO — use **Letter landscape 11×8.5** to match the render
  aspect), each with **0.125 in bleed on all sides** (final trim 11×8.5, page box 11.25×8.75).
- Also output `proof_sheet.png` — all 8 pages tiled small for one-glance review.
- Metadata: Author `Stephan Hardt`, Title `Protecting Time to Power — NRG | Southwire
  Power Generation Solutions`, Subject `SWR-PG-BROCHURE-NRG Rev 01`.

## 3. Structure — one sayable idea per page, ≤400 words TOTAL across the brochure

1. **Cover** — dark hexagon texture, NRG | Southwire PGS lockup, "PROTECTING *TIME TO POWER*",
   nothing else except the credit line (see §6).
2. **Why now** — "NRG's growth agenda creates three electrical-delivery environments."
   1.5 GW TEF / 5.4 GW newbuild / 25.8 GW fleet, one line each, plus the black band:
   "Different asset states. One requirement: preserve schedule certainty through energization."
3. **The thesis** — full-bleed 3×1 plant render as hero. Single overlaid line:
   "Time to power is an electrical execution problem before it is a cable-buying problem."
4. **The three risks** — labor & demand pressure / material + installation fit / fragmented
   coordination, one line each. Closing band: "Late handoffs become schedule and commissioning
   exposure."
5. **The system** — the 6-step coordinated delivery flow (Plan → Field Support + Turnover) as
   one horizontal diagram, subline "without changing project accountability", kicker
   "Field-engineer what is unique. Prefabricate what repeats."
6. **The honesty page** — this is the differentiator; give it room. Two boxes verbatim in
   spirit: "Adjacent experience indicates where to test — not what NRG will save." and
   "No presumption that the answer is prefab — or that Southwire belongs in the solution."
   NO numbers on this page (see §4).
7. **Who we are** — family-held since 1950, copper rod to finished cable; stat row
   1950 · 9,000+ employees · $9.7B 2025 revenue (Forbes) · 12 industries · 7 Copper Mark sites.
8. **The ask (back)** — dark. "ONE SITE WALK. ONE HOUR. NO SALES PRESENTATION."
   Input / Output / Decision rows, "No pricing exercise. No broad commercial commitment.",
   contact block.

## 4. Fact hygiene — hard rules, non-negotiable

- **Revenue is $9.7B (2025, per Forbes).** The "$13B" figure circulating in the source decks is
  the Richards FAMILY net worth, not Southwire revenue. Never print $13B as revenue.
- Never sum the GW figures (1.5 / 5.4 / 25.8 / ~1-2) — different asset states, they overlap.
- **Exclude entirely:** the 4,400→880 hour benchmark, all derived dollar math ($418K / $83.6K /
  $334K / $33.4M), spine-count extrapolations, Cedar Bayou project details, Bloom/fuel-cell
  naming, and anything marked internal/confidential. A brochure travels; it gets only what can
  be public forever.
- Corrected wording (Rev10 baseline): "Simple Cycle" (not Cyle), "GENERATION ISLAND + BOP",
  "OPTIONAL + AUXILIARY + BOP", "3×1" (never 3x1x1), "owner lens" phrasing, "OEM, Contractor
  or Channel accountability or preference."

## 5. Design system

- Warm white `#F6F3EE` body pages; graphite `#171920` dark pages (cover, ask); copper accents
  `#C67A43` (light on dark: `#E3A06D`, deep: `#9D4E24`). Copper is a SPOT accent — rules,
  kickers, one number — never large fills.
- Helvetica only, three sizes per page maximum. Headlines 28–40 pt, body ≥10 pt, kickers
  7–8 pt tracked caps. Real margins: ≥0.6 in inside trim; let pages breathe.
- Renders run full-bleed or not at all — no floating boxed screenshots. Vignette/fade edges
  where a render meets a text field.
- 5-second test on every page: rasterize it, look at it, and ask "can I say the takeaway
  aloud?" If a page needs study, cut words.

## 6. Attribution — required on the artifact itself

- Cover and back page: `Stephan Hardt  |  Director, Power Generation Solutions  |
  stephan.hardt@southwire.com  |  +1 470-439-8488` (back, full) and a short credit on the cover.
- Every interior page: small footer `Stephan Hardt  |  Power Generation Solutions`.
- Credit must be drawn into the PDF content (burned in), not metadata-only — though metadata
  author is also set per §2.

## 7. Work loop (repeat until all gates pass)

1. Build → 2. Rasterize every page at 150 dpi → 3. Inspect each image yourself →
4. Log faults (overlap, orphan words, cramped margins, low-contrast text on renders,
   banding/pixelation) → 5. Fix → repeat. Expect 3–5 full passes; budget your time for them.

**QA gates:** zero text overlaps or clipped lines; no orphaned single words on their own line;
word count ≤400; every §4 rule verified by text-extracting the final PDF and grepping for the
banned strings (`13 B`, `4,400`, `880`, `334`, `3x1x1`, `Cyle`, `ISLAN`, `Cedar Bayou`,
`Bloom`); credit present on all 8 pages; images ≥300 dpi effective; proof sheet generated.

When done, write `BUILD_NOTES.md`: what you changed between passes, any judgment calls on
copy, and anything that needs Stephan's decision before print.
