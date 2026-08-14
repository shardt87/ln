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

## Rev 7 — outcome page recomposed

Page 7 rebuilt as a two-column architecture after Stephan flagged it as unclear:
left column tells one story top-to-bottom (headline → four levers with their
outcomes → the two outcome-hypothesis boxes), and the tray-and-cable x-ray now
sits in a full-height dark "blueprint sidebar" on the right — background matched
to the render, edges feathered — captioned "The routed model: one electrical
system — trays, routes and cable planned plant-wide before material is
released." The image now has a stated purpose instead of floating in a corner.

## Rev 6 — back of book strengthened from Teaser_3

Three new pages added after the outcome page, extracted from the original
Teaser_3 deck (corrected wording applied per §4):

- **08 Owner economics** — "Cable is a small cost category with outsized
  execution consequences" + the four owner lenses (COD/revenue start, installed
  cost, capital certainty, availability/lifecycle).
- **09 Plant-wide coverage** — "Six clusters map a routed 3×1 electrical
  reference model" (corrected from 3×1x1) with the six cluster scopes, cable
  classes band and the illustrative disclaimer. "GENERATION ISLAND + BOP"
  spelled correctly.
- **10 Governance / decision rights** — the five-party accountability table with
  Southwire's row highlighted, closing with the corrected line "Southwire
  connects selected decisions — it does not replace owner, EPC, OEM, Contractor
  or Channel accountability or preference."

Now 12 pages (saddle-stitch friendly). QA gates updated; the ISLAN gate now
matches the source typo only ("ISLAN ") so the corrected ISLAND spelling passes.

## Rev 5 — Rev 4 reverted at Stephan's direction

Stephan reviewed the anti-pitch pass against the prior version and preferred the
prior version outright. The brochure is restored to Rev 3 exactly (verified
text-identical to the reference PDF he attached): hexagon cover, NRG | Southwire
lockups, full "Who We Are" page, value proposition on the whole-plant isometric.
The Rev 4 changes (iso cover, Southwire-only headers, framed gate-render plate,
demoted corporate page) remain in git history at commit be794de if any single
element is ever wanted back.

## Rev 4 (reverted) — "anti-pitch" pass (responding to executive review feedback)

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
