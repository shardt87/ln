# Gamma build — Southwire PowerGen Value Proposition (SWR-PG-VP Rev 01)

Rebuilds the 13-slide PowerGen value-proposition deck (9 main + 4 appendix) as a
Gamma presentation from `gamma_input.md`.

Status: generation is blocked on Gamma credits (the API returned
`403 Insufficient credits remaining`). Refill at https://gamma.app/settings/billing,
then re-run the generation with the parameters below.

## Generation parameters (Gamma generate API / MCP tool)

- `inputText`: full contents of `gamma_input.md` (13 cards separated by `---`)
- `title`: `Southwire PowerGen Value Proposition — SWR-PG-VP Rev 01`
- `format`: `presentation`
- `numCards`: `13`
- `cardSplit`: `inputTextBreaks`
- `textMode`: `preserve`
- `themeId`: `cigar` (copper accent on neutral base — closest stock match to the
  white / graphite 1A1D21 / copper C67A43 design system)
- `cardOptions.dimensions`: `16x9`
- `cardOptions.headerFooter`:
  - bottomLeft, text: `Stephan Hardt · Power Generation Solutions`
  - bottomCenter, text: `SWR-PG-VP Rev 01 · Internal — Southwire`
  - bottomRight: card number
- `imageOptions.source`: `placeholder` (Stephan supplies assets A1–A5; never stock art)
- `textOptions`: amount `medium`, audience `Southwire executives`, tone
  `plain internal business language, short declarative sentences, no marketing jargon`
- `exportAs`: `pptx` (optional — adds a PowerPoint export alongside the Gamma)
- `additionalInstructions`:
  > Minimal executive design. White base with dark graphite (1A1D21) treatment for
  > cards 1, 4, and 9 (the opener, the trends card, and the execution close); light
  > backgrounds for all other cards. Copper (C67A43) is the only accent color — use
  > it for the status tag chips (TO VERIFY, DECISION REQUIRED, PROVISIONAL, DRAFT,
  > Working Assumption) and the closing lines. No gradients, no decorative bars. On
  > card 8, render $9.7M as one oversized numeral dominating the card. Keep every
  > [PLACEHOLDER — ...] as a visibly labeled empty frame — do not substitute stock
  > or generated imagery for them. One takeaway headline per card; keep body text
  > under ~60 words per card.

## Content QA gates (from the build prompt)

Before shipping, grep `gamma_input.md` and any export — the build fails on any hit:

```
grep -iE "13 ?B|13 billion|leverage|robust|seamless|synerg|holistic|unlock|empower|delve|land grab|hoarding|friendly contact|claim the rest|told not asked|Bloom|best-in-class|world-class"
```

Also verify: credit line on all 13 slides; "quoting" (never "sales"/"bookings") near
$9.7M; dollar math confined to Appendix 4; NRG figures never summed; the fuel cell
manufacturer never named.
