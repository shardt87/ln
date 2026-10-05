# NICA contractor booklet

8-page saddle-stitched booklet, US Letter, built from the Anixter/Wesco deck's brand system and the
application renders in `../renders/clean/`.

    python3 brochure.py          # rebuilds everything in out/

| File | Use |
|---|---|
| `out/NICA_booklet_print.pdf` | Printer file: single pages on 9.25 x 11.75 in with 0.125 in bleed and crop marks. Impose as a 2-sheet saddle stitch (1-8, 2-7 / 3-6, 4-5). |
| `out/NICA_booklet_reader.pdf` | Trimmed pages, no marks, for email and screen. |
| `out/NICA_booklet_spreads.pdf` | Reader spreads for review (cover, 2-3, 4-5, 6-7, back). |
| `out/NICA_booklet.pptx` | Editable; every text, rule, marker and box is a native shape. Needs the Barlow fonts installed (see `fonts/`). |
| `out/png/` | 150-dpi page previews. |
| `assets/` | Logo (with transparency) and renders extracted from the deck PDF. |
| `fonts/` | Barlow and Barlow Condensed (Google Fonts, SIL Open Font License) - install before opening the PPTX. |

Before print: replace the deck renders in `assets/` (cover, plant, cable systems, yard, cable details) with
clean originals - the extracted versions carry the deck's faint "Stephan Hardt" mark. Add the approved
QR destination (back page placeholder). The "Why now" figures on page 2 repeat the deck's public sources
and should be verified against them before external use.
