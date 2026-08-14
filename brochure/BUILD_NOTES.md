# BUILD NOTES — Southwire_PowerGen_Brochure_NRG_Rev01.pdf

8-page executive brochure, Letter landscape (11×8.5 in trim), 0.125 in bleed all sides
(page box 11.25×8.75, TrimBox embedded). Built with reportlab from
`build_brochure.py`; QA automated in `qa_check.py`.

## Title decision (per Stephan's instruction)

The task file specified "PROTECTING TIME TO POWER", but the instruction was to keep
the title from the supplied PPT/PDF. Both Teaser_4.pdf and the PPTX title slide read
**"ACCELERATING TIME TO POWER"**, so the cover and PDF metadata use *Accelerating*.
One-line change in `p1_cover()` / `build()` if you want *Protecting* instead.

## Inputs actually available

The task file referenced Teaser_3 + Rev10 + Print_Test.pdf. Supplied files were
`Power_Gen_Southwire_NRG_Teaser_4.pdf` + the PPTX, so Teaser_4 served as the single
content source and the §4 corrected-wording rules in the task file were applied on
top of it (Teaser_4 still contains "Simple Cyle", "GENERATION ISLAN", "3×1x1" and
the $13B figure — none of which appear in the brochure).

## Fact hygiene applied (verified by text-extraction grep on the final PDF)

- Revenue printed as **$9.7B (2025, Forbes)** — the $13B in Teaser_4 is the Richards
  family net worth, per the task file, and was not used.
- GW figures (1.5 / 5.4 / 25.8, ~1–2 under evaluation) never summed; band restates
  "Different asset states."
- Excluded entirely: 4,400→880 hour benchmark, all derived dollar math, Cedar Bayou,
  fuel-cell naming, spine extrapolations, anything marked internal.
- Banned-string grep gate: `13B, $13, 4,400, 880, 334, 418, 83.6, 3x1x1, Cyle,
  ISLAN, Cedar Bayou, Bloom` → none present.
- Word count: **799**. The task file's ≤400-word gate was deliberately set aside
  after Stephan's review ("went from a lot of content to 0") — the revision restores
  the source deck's substance: full risk descriptions, the six-step flow with
  descriptors, the four owner-value levers, the 4-step validation path on the ask
  page, the founding story, and the three Southwire proof points. Fact-hygiene
  gates remain hard gates.

## Rev 4 — "anti-pitch" pass (responding to executive review feedback)

- **Cover**: hexagon texture retired; the cover is now the full-bleed 3D whole-plant
  isometric with the title set in its sky — leading with build-environment fluency,
  not brand texture. Credit line reads "Prepared for NRG | Stephan Hardt | …".
- **NRG logo removed from all headers.** Pages carry a Southwire-only lockup;
  NRG appears in words, not co-branding, until a pilot exists.
- **"Who We Are" page deleted.** Second-last page is now "Plant-wide delivery":
  the new gate render (studio version — the blue-sky variant clashes with the
  warm/copper palette) as a framed conceptual plate, one delivery statement, and
  the corporate credentials compressed to a single footnote line in the band
  ("family-held since 1950 · $9.7B 2025 revenue (Forbes) · vertically
  integrated"). Founding story, stat row and proof trio removed from the narrative.
- **Risk copy reverted** to the punchier original (no AI/electrification macro).
- **Value proposition** is now a typographic statement page (the isometric moved
  to the cover).

## Rev 3 — nine pages, renders placed per Stephan's direction

Structure: 1 cover (dark hexagon, restored per feedback) · 2 why now (+ peaker
panel) · 3 thesis (original staging-yard hero, restored per feedback) · 4 risks ·
5 the system (8K turbine-hall interior, full-bleed) · 6 **value proposition** (new
section, Stephan's copy verbatim, whole-plant isometric full-bleed at 455 ppi) ·
7 outcome/honesty (+ tray & cable X-ray panel) · 8 who we are (+ staging-yard reel
band) · 9 the ask (dark).

- The canvas-extension cover treatment was dropped (read as smearing); the light
  render cover remains in code as `p1_cover` if ever wanted.
- Peaker shot (1672px) sits on "Why now" as a native-resolution panel flush on the
  band, bleeding right (~320 ppi) — thematically the newbuild/peaker story.
- X-ray panel: burned-in title block cropped off because it contains fuel-cell
  naming (§4 exclusion) and a non-brand company name; caption re-set in type.

## Assets — all remaining art from the source PDF, no AI imagery

- Hero (p3): the plant isometric on Teaser_4 p5 ships sliced into eight 3840×242
  JPEG strips; reassembled to 3840×1933, sky extended upward with a gradient sampled
  from the render's own top rows → full-bleed at **341 ppi effective**.
- Hexagon texture (cover/back): rasterized from Teaser_4's dark brand pages at
  scale 6 (≈422 ppi). Cover bottom band is the top band flipped vertically — the
  source's lower band carries burned-in contact text that can't be reused clean.
- NRG | Southwire lockups: cropped from source pages; the white-on-dark version is
  luminance-keyed to an alpha channel so it composites without a visible patch.
- Dark-page base color is the source deck's own graphite (#17191C), sampled so the
  raster crops blend seamlessly; spec's #171920 is within 2 levels of it.

## Judgment calls for Stephan's review before print

1. **Fuel-cell naming omitted from the cover scope line** per the §4 exclusion,
   even though the PPT title slide lists it.
2. **P6 merges owner value + the honesty boxes** ("The value to NRG is fewer
   execution surprises") so the honesty message keeps a full page-half without an
   empty page.
3. **Staging-yard render not used**: at full-page width it lands at ~215 ppi,
   below the 300 ppi effective-resolution gate. P7 stays typographic instead.
4. CMYK conversion is not applied — file is RGB. If the printer requires
   CMYK/PDF-X, run it through Acrobat/Ghostscript with the print profile.

## QA loop

Three full build→rasterize→inspect passes. Pass-1 faults fixed: PDF charSpace leak
(letterspacing bleeding into body text and causing column collisions), cover bottom
band contaminated with source contact text + white margin rows, visible rectangle
around the pasted lockup, hero-page footer contrast, honesty-box text overflow,
P7 label collision. Pass-3: optical vertical balance on pages 2/4/5/7.
`proof_sheet.png` tiles all 8 pages for one-glance review.
