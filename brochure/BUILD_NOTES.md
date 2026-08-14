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
- Word count: **386** (gate ≤400), via pdfplumber word extraction.

## Assets — all from the source PDF, no AI imagery

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

1. **Cover tagline cut.** "PRESERVE SCHEDULE CERTAINTY THROUGH ENERGIZATION" was
   removed from the cover to honor the ≤400-word budget and the "nothing else on the
   cover" instruction. Easy to restore (commented location in `p1_cover`).
2. **P5 diagram labels only.** The six step names are kept; the 4-word descriptors
   under each step were cut for the word budget. The flow still reads.
3. **P6 honesty page** has no headline — just the two bordered statements, per
   "give it room".
4. **P7 stat row**: first label shortened to "FOUNDED" (Carrollton no longer fits at
   tracked caps without colliding with the next column).
5. **Staging-yard render not used**: at full-page width it lands at ~215 ppi,
   below the 300 ppi gate. P7 stays typographic instead.
6. CMYK conversion is not applied — file is RGB. If the printer requires
   CMYK/PDF-X, run it through Acrobat/Ghostscript with the print profile.

## QA loop

Three full build→rasterize→inspect passes. Pass-1 faults fixed: PDF charSpace leak
(letterspacing bleeding into body text and causing column collisions), cover bottom
band contaminated with source contact text + white margin rows, visible rectangle
around the pasted lockup, hero-page footer contrast, honesty-box text overflow,
P7 label collision. Pass-3: optical vertical balance on pages 2/4/5/7.
`proof_sheet.png` tiles all 8 pages for one-glance review.
