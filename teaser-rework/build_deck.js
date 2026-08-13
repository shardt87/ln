const pptxgen = require("pptxgenjs");
const path = require("path");

const A = p => path.join(__dirname, "assets", p);

// ---- palette ----
const INK = "201D1A";        // near-black headings
const BODY = "3D3833";       // body text
const MUTED = "797065";      // captions
const COPPER = "B4713D";     // brand accent
const COPPER_D = "8F5527";   // darker copper
const CARD = "F5F1EC";       // light card
const CARD_BD = "E3DACE";    // card border
const DK_BG = "191B1E";      // dark slide bg
const DK_TXT = "F4F2EF";
const DK_MUT = "9AA0A6";
const DK_LINE = "3A3D40";

const FONT = "Arial";
const W = 13.333, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Stephan Hardt";
pres.title = "Southwire Power Generation Solutions — IPP Teaser";

// ---- helpers ----
let pageNo = 0;
function footer(slide, dark = false, xOff = 0.55) {
  pageNo += 1;
  const n = String(pageNo).padStart(2, "0");
  slide.addText("SOUTHWIRE POWER GENERATION SOLUTIONS  ·  DISCUSSION TEASER  ·  REV 08", {
    x: xOff, y: H - 0.38, w: 8.5, h: 0.25, fontFace: FONT, fontSize: 7.5,
    color: dark ? DK_MUT : MUTED, charSpacing: 1.2, margin: 0, valign: "middle",
  });
  slide.addText(n, {
    x: W - 1.05, y: H - 0.38, w: 0.5, h: 0.25, fontFace: FONT, fontSize: 8,
    bold: true, color: COPPER, align: "right", margin: 0, valign: "middle",
  });
}
function kicker(slide, text, opts = {}) {
  slide.addText(text, Object.assign({
    x: 0.55, y: 0.42, w: 9.5, h: 0.3, fontFace: FONT, fontSize: 10.5, bold: true,
    color: COPPER, charSpacing: 2.4, margin: 0, valign: "middle",
  }, opts));
}
function title(slide, text, opts = {}) {
  slide.addText(text, Object.assign({
    x: 0.55, y: 0.74, w: 10.5, h: 0.95, fontFace: FONT, fontSize: 26, bold: true,
    color: INK, margin: 0, valign: "top", lineSpacingMultiple: 1.04,
  }, opts));
}
function hexNum(slide, num, x, y, size, opts = {}) {
  const o = Object.assign({ fill: COPPER, txt: "FFFFFF", fs: 12 }, opts);
  slide.addShape("hexagon", { x, y, w: size, h: size * 0.9, fill: { color: o.fill }, line: { type: "none" } });
  slide.addText(String(num), {
    x, y, w: size, h: size * 0.9, fontFace: FONT, fontSize: o.fs, bold: true,
    color: o.txt, align: "center", valign: "middle", margin: 0,
  });
}

// =====================================================================
// SLIDE 1 — COVER (original art, full bleed)
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: "0E0F10" };
  s.addImage({ path: A("cover_art.png"), x: 0, y: 0, w: W, h: 7.505 });
  s.addNotes("Cover kept from Rev 07 — strongest page in the original file. Full-bleed brand art with tagline and direct contact.");
  pageNo += 1; // count cover, no visible footer
}

// =====================================================================
// SLIDE 2 — WHY NOW: THE PROGRAM NRG IS RUNNING
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "WHY NOW   ·   THE PROGRAM NRG IS RUNNING");
  s.addText("Public record, Feb 2025 – Jan 2026. Nothing here is confidential.", {
    x: 8.6, y: 0.42, w: 4.2, h: 0.3, fontFace: FONT, fontSize: 8.5, italic: true,
    color: MUTED, align: "right", margin: 0, valign: "middle",
  });
  title(s, "Doubling down on generation means buying a lot of electrical scope, soon.", { w: 11.6 });

  s.addText("THE MOVE", { x: 1.28, y: 1.62, w: 5.6, h: 0.24, fontFace: FONT, fontSize: 8.5, bold: true, color: MUTED, charSpacing: 2, margin: 0 });
  s.addText("WHERE CABLE DECIDES", { x: 7.35, y: 1.62, w: 5.4, h: 0.24, fontFace: FONT, fontSize: 8.5, bold: true, color: COPPER_D, charSpacing: 2, margin: 0 });

  const rows = [
    {
      h: "NEWBUILD  ·  5.4 GW WITH GE VERNOVA AND KIEWIT-TIC",
      d: "Four combined-cycle projects for ERCOT and PJM; first unit ~1.2 GW with a 2029 COD, the balance through 2032. Turbine and EPC capacity already secured.",
      c: "A 2029 COD freezes its cable specification in the next 12–24 months. Insulation system, jacket latitude, raceway segregation and flame rating are still decisions today — by award, they are history.",
    },
    {
      h: "ACQUIRED FLEET  ·  13 GW FROM LS POWER, CLOSED JAN 30, 2026",
      d: "Eighteen gas plants across nine states, doubling the fleet to ~25 GW — eighteen sets of as-builts and aging cable systems inherited on one balance sheet.",
      c: "Fleet-wide cable condition is measurable: field assessment, rejuvenation (150M+ ft on record) and one governed cable standard across eighteen sites instead of eighteen inherited ones.",
    },
    {
      h: "BROWNFIELD ADDS  ·  TEXAS ENERGY FUND AND PJM UPRATES",
      d: "TEF-backed units at existing sites — Greens Bayou 443 MW, Cedar Bayou — plus ~2 GW of CT-to-combined-cycle conversion potential identified in PJM.",
      c: "Constrained brownfield without spare corridors is exactly where HV underground and factory-built modular power earn their place — capacity added inside a fence line you already own.",
    },
    {
      h: "DATA CENTER COLOCATION  ·  LOIs SIGNED, ~7.5 GW IN NEGOTIATION",
      d: "Letters of intent with data-center developers, an agreement expected to be announced in 2026, and behind-the-meter configurations on the table.",
      c: "The same circuit schedule serves both sides of the meter: modular gas power on one side, UL-listed data center cable assemblies on the other. Both are existing Southwire lines.",
    },
  ];
  let y = 1.95;
  rows.forEach((r, i) => {
    hexNum(s, i + 1, 0.55, y + 0.02, 0.42, { fs: 12 });
    s.addText(r.h, { x: 1.28, y: y, w: 5.75, h: 0.3, fontFace: FONT, fontSize: 10.5, bold: true, color: INK, margin: 0, valign: "top" });
    s.addText(r.d, { x: 1.28, y: y + 0.28, w: 5.75, h: 0.82, fontFace: FONT, fontSize: 9.5, color: BODY, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
    s.addText(r.c, { x: 7.35, y: y, w: 5.4, h: 1.1, fontFace: FONT, fontSize: 9.5, color: BODY, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
    if (i < rows.length - 1) {
      s.addShape("line", { x: 1.28, y: y + 1.16, w: 11.47, h: 0, line: { color: CARD_BD, width: 0.75 } });
    }
    y += 1.28;
  });
  s.addNotes("Was page 3 of Rev 07 — promoted to slide 2. All four program moves are public record; the right column translates each into a cable decision with a deadline.");
  footer(s);
}

// =====================================================================
// SLIDE 3 — THE PROBLEM
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "THE PROBLEM");
  title(s, "On paper, electrical scope rarely sets the schedule.\nIn the field, it routinely does.", { w: 11.8, h: 1.15 });

  const cards = [
    { n: 1, h: "Field labor", d: "Terminations and pulls land in the same weeks as commissioning — absorbed as overtime and re-pulls, not as a line item anyone approved." },
    { n: 2, h: "Supply window", d: "The cable specification is written 12–24 months before anyone buys or reserves capacity. The market moves; the spec does not." },
    { n: 3, h: "System risk", d: "Cable sized for the drawing, not the installed geometry, fails in year eight — on an asset you still own and still owe." },
  ];
  const cw = 3.94, gap = 0.32;
  cards.forEach((c, i) => {
    const x = 0.55 + i * (cw + gap);
    s.addShape("roundRect", { x, y: 2.25, w: cw, h: 2.5, rectRadius: 0.06, fill: { color: CARD }, line: { color: CARD_BD, width: 1 } });
    hexNum(s, c.n, x + 0.28, 2.55, 0.44);
    s.addText(c.h, { x: x + 0.28, y: 3.12, w: cw - 0.56, h: 0.35, fontFace: FONT, fontSize: 15, bold: true, color: INK, margin: 0 });
    s.addText(c.d, { x: x + 0.28, y: 3.5, w: cw - 0.56, h: 1.1, fontFace: FONT, fontSize: 10.5, color: BODY, margin: 0, valign: "top", lineSpacingMultiple: 1.12 });
  });

  s.addText([
    { text: "Each of the three lands directly in the owner's math. ", options: { bold: true, color: INK } },
    { text: "A late electrical scope does not show up as a cable problem — it shows up as COD slip, contingency burn and lost IRR.", options: { color: BODY } },
  ], { x: 0.55, y: 5.15, w: 12.2, h: 0.6, fontFace: FONT, fontSize: 13, margin: 0, valign: "top", lineSpacingMultiple: 1.1 });

  s.addText("Next page: where cable actually moves LCOE and IRR — and where it does not.", {
    x: 0.55, y: 5.95, w: 12.2, h: 0.3, fontFace: FONT, fontSize: 10, italic: true, color: MUTED, margin: 0,
  });
  s.addNotes("Was page 4 of Rev 07. Fixed: grammar in the headline ('push the date and influences IRR/LCOE'), and removed the cropped LCOE screenshot — that content is rebuilt natively on the next slide.");
  footer(s);
}

// =====================================================================
// SLIDE 4 — THE OWNER'S EQUATION
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "THE OWNER’S EQUATION");
  title(s, "Cable is a small line item with large coefficients.", { w: 11.5 });
  s.addText("LCOE and IRR decide every project. Five variables actually move — none of them is the purchase price.", {
    x: 0.55, y: 1.42, w: 11.5, h: 0.3, fontFace: FONT, fontSize: 11, color: BODY, margin: 0,
  });

  // left: two formula panels
  s.addShape("roundRect", { x: 0.55, y: 1.95, w: 3.7, h: 2.2, rectRadius: 0.06, fill: { color: CARD }, line: { color: CARD_BD, width: 1 } });
  s.addText("LCOE  —  COST PER MWh", { x: 0.85, y: 2.15, w: 3.2, h: 0.25, fontFace: FONT, fontSize: 9.5, bold: true, color: COPPER_D, charSpacing: 1.5, margin: 0 });
  s.addText("CAPEX + O&M + Fuel\n(lifetime, discounted)", { x: 0.85, y: 2.48, w: 3.1, h: 0.6, fontFace: FONT, fontSize: 11.5, bold: true, color: INK, align: "center", margin: 0 });
  s.addShape("line", { x: 1.15, y: 3.14, w: 2.5, h: 0, line: { color: INK, width: 1.25 } });
  s.addText("Lifetime MWh delivered (discounted)", { x: 0.85, y: 3.2, w: 3.1, h: 0.3, fontFace: FONT, fontSize: 10.5, bold: true, color: INK, align: "center", margin: 0 });
  s.addText("Lower the top. Grow the bottom. De-risk the rate that discounts both.", { x: 0.85, y: 3.6, w: 3.1, h: 0.45, fontFace: FONT, fontSize: 9, italic: true, color: MUTED, margin: 0 });

  s.addShape("roundRect", { x: 0.55, y: 4.35, w: 3.7, h: 1.95, rectRadius: 0.06, fill: { color: CARD }, line: { color: CARD_BD, width: 1 } });
  s.addText("IRR  —  RETURN ON THE PROJECT", { x: 0.85, y: 4.55, w: 3.2, h: 0.25, fontFace: FONT, fontSize: 9.5, bold: true, color: COPPER_D, charSpacing: 1.5, margin: 0 });
  s.addText("NPV = Σ CFₜ ÷ (1 + IRR)ᵗ = 0", { x: 0.85, y: 4.9, w: 3.1, h: 0.35, fontFace: FONT, fontSize: 12, bold: true, color: INK, align: "center", margin: 0 });
  s.addText("Most sensitive to COD date, capex certainty and availability — revenue that starts late is IRR you never get back.", { x: 0.85, y: 5.35, w: 3.1, h: 0.8, fontFace: FONT, fontSize: 9, italic: true, color: MUTED, margin: 0, lineSpacingMultiple: 1.1 });

  // right: five levers
  const levers = [
    { n: 1, h: "SCHEDULE → COD", d: "Cable sits on the energization critical path. Supply certainty and delivery sequencing protect the revenue start date — the largest single IRR lever." },
    { n: 2, h: "RISK → DISCOUNT RATE", d: "Evidence-based scope lowers contingency and financing risk: an estimate within 4% on footage was 26% off on copper — right in total, wrong where the money is." },
    { n: 3, h: "CAPEX — THE NUMERATOR", d: "Cable is under 2% of plant capex — purchase price barely moves the top line. Installed cost does: routing, reels, pulls, rework." },
    { n: 4, h: "MWh — THE DENOMINATOR", d: "Availability and asset life grow the bottom of the equation: cable health, rejuvenation and life extension keep MWh flowing." },
    { n: 5, h: "COMMODITY VOLATILITY", d: "Copper and aluminum exposure managed through supply strategy and hedging — capex certainty that lenders can underwrite." },
  ];
  let ly = 1.95;
  levers.forEach((l) => {
    hexNum(s, l.n, 4.62, ly + 0.06, 0.36, { fs: 10.5 });
    s.addText(l.h, { x: 5.18, y: ly, w: 7.6, h: 0.24, fontFace: FONT, fontSize: 10.5, bold: true, color: COPPER_D, charSpacing: 0.8, margin: 0 });
    s.addText(l.d, { x: 5.18, y: ly + 0.24, w: 7.6, h: 0.56, fontFace: FONT, fontSize: 9.5, color: BODY, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
    ly += 0.88;
  });

  s.addShape("roundRect", { x: 0.55, y: 6.5, w: 12.23, h: 0.5, rectRadius: 0.05, fill: { color: INK }, line: { type: "none" } });
  s.addText("Cable barely moves the numerator — it moves COD, risk and availability, where LCOE and IRR are decided.", {
    x: 0.75, y: 6.5, w: 11.9, h: 0.5, fontFace: FONT, fontSize: 11.5, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0,
  });
  s.addNotes("Imported from the VP deck (page 2) — the best IPP-language slide in either file, rebuilt natively. Lever order corrected to a clean 1–5 (Rev 03 numbered them 3,1,2,4,1).");
  footer(s);
}

// =====================================================================
// SLIDE 5 — THE ANSWER: GOVERNED DELIVERY SYSTEM
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "THE ANSWER   ·   SOUTHWIRE WORKING MODEL, FOR NRG VALIDATION");
  title(s, "Move cable from late procurement to a governed delivery system.", { w: 11.8 });
  s.addText("One owner basis travels from specification through turnover — while repeatable package interfaces become prefab / skid spines.", {
    x: 0.55, y: 1.42, w: 11.8, h: 0.3, fontFace: FONT, fontSize: 11, color: BODY, margin: 0,
  });

  // 7-step chain
  const steps = ["SPECIFY", "FORECAST", "RESERVE", "RELEASE", "DELIVER", "INSTALL", "TURN OVER"];
  const x0 = 0.85, xEnd = 12.5, hexW = 0.52;
  const dx = (xEnd - x0 - hexW) / (steps.length - 1);
  s.addShape("line", { x: x0 + hexW / 2, y: 2.36, w: (steps.length - 1) * dx, h: 0, line: { color: CARD_BD, width: 1.5 } });
  steps.forEach((st, i) => {
    const hx = x0 + i * dx;
    const isEnd = i === 0 || i === steps.length - 1;
    hexNum(s, i + 1, hx, 2.13, hexW, { fill: isEnd ? COPPER_D : COPPER, fs: 13 });
    s.addText(st, { x: hx - 0.55, y: 2.66, w: hexW + 1.1, h: 0.24, fontFace: FONT, fontSize: 9, bold: true, color: BODY, align: "center", charSpacing: 1, margin: 0 });
  });

  // three pillars
  const pillars = [
    { h: "OWNER APPLICATION BASIS", d: "Cable codes, duty, compliance and approved alternates — one basis, owned by NRG, honored by every EPC.", hl: false },
    { h: "RELEASE + REEL STRATEGY", d: "Material sequenced to energization, turnover and installation zones — not to a purchase-order date.", hl: false },
    { h: "PREFAB / SKID SPINES", d: "Pre-engineered power, control, instrumentation and fiber wherever package interfaces repeat.", hl: true },
  ];
  const pw = 3.94, pgap = 0.32;
  pillars.forEach((p, i) => {
    const x = 0.55 + i * (pw + pgap);
    s.addShape("roundRect", {
      x, y: 3.35, w: pw, h: 1.95, rectRadius: 0.06,
      fill: { color: p.hl ? "F0DFCE" : CARD }, line: { color: p.hl ? COPPER : CARD_BD, width: 1 },
    });
    s.addText(p.h, { x: x + 0.28, y: 3.62, w: pw - 0.56, h: 0.3, fontFace: FONT, fontSize: 11.5, bold: true, color: p.hl ? COPPER_D : INK, charSpacing: 0.6, margin: 0 });
    s.addText(p.d, { x: x + 0.28, y: 3.98, w: pw - 0.56, h: 1.1, fontFace: FONT, fontSize: 10.5, color: BODY, margin: 0, valign: "top", lineSpacingMultiple: 1.12 });
  });

  s.addText("Field-engineer what is unique.  Prefabricate what repeats.", {
    x: 0.55, y: 5.75, w: 12.23, h: 0.55, fontFace: FONT, fontSize: 19, bold: true, color: COPPER_D, align: "center", margin: 0,
  });
  s.addNotes("Was page 6 of Rev 07. Typeface unified with the rest of the deck (Rev 07 used a different font family here).");
  footer(s);
}

// =====================================================================
// SLIDE 6 — PROOF: 4,400 -> 880
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "PROOF, FROM AN ADJACENT MARKET   ·   MODULAR POWER DEVELOPER");
  title(s, "We moved the field build into the factory.", { w: 11.5 });
  s.addText("One factory-built cable spine; the generation modules plug into it. Field man-hours per spine:", {
    x: 0.55, y: 1.48, w: 11.5, h: 0.3, fontFace: FONT, fontSize: 12, color: BODY, margin: 0,
  });

  s.addText("4,400", { x: 0.55, y: 2.15, w: 4.6, h: 1.55, fontFace: FONT, fontSize: 88, bold: true, color: INK, margin: 0, valign: "middle" });
  s.addText("observed, site-built", { x: 0.62, y: 3.72, w: 4.2, h: 0.28, fontFace: FONT, fontSize: 11, color: MUTED, margin: 0 });

  s.addShape("rightArrow", { x: 5.5, y: 2.62, w: 1.7, h: 0.62, fill: { color: COPPER }, line: { type: "none" } });

  s.addText("~880", { x: 7.65, y: 2.15, w: 4.4, h: 1.55, fontFace: FONT, fontSize: 88, bold: true, color: COPPER, margin: 0, valign: "middle" });
  s.addText("modeled, factory-built", { x: 7.72, y: 3.72, w: 4.2, h: 0.28, fontFace: FONT, fontSize: 11, color: MUTED, margin: 0 });

  s.addText("~80% of field labor hours and ~50% of schedule, modeled — roughly $334K gross per spine at $95/hr.", {
    x: 0.55, y: 4.3, w: 12.2, h: 0.35, fontFace: FONT, fontSize: 14, bold: true, color: INK, margin: 0,
  });

  s.addShape("roundRect", { x: 0.55, y: 4.85, w: 12.23, h: 1.45, rectRadius: 0.06, fill: { color: CARD }, line: { color: CARD_BD, width: 1 } });
  s.addText("READ THE FINE PRINT — WE MEAN IT", { x: 0.85, y: 5.02, w: 6, h: 0.24, fontFace: FONT, fontSize: 8.5, bold: true, color: COPPER_D, charSpacing: 2, margin: 0 });
  s.addText(
    "The prefabricated assembly costs more than site-built tray and strut. The argument is total cost of ownership over a forty-year asset life, not first cost. Gross labor avoided is not net savings — subtract the prefab premium, engineering, factory labor, freight, factory acceptance and commissioning. Prefabrication does not automatically remove an activity from the critical path. Every figure on this page comes from an adjacent market and stays illustrative until validated against your labor data.",
    { x: 0.85, y: 5.3, w: 11.6, h: 1.2, fontFace: FONT, fontSize: 9.5, italic: true, color: BODY, margin: 0, valign: "top", lineSpacingMultiple: 1.15 }
  );
  s.addNotes("Was page 7 of Rev 07. Fixed: the disclaimer paragraph ran off the right edge of the page mid-word; it is now fully visible — and framed as a feature, since the honesty is the differentiator.");
  footer(s);
}

// =====================================================================
// SLIDE 7 — PROOF: ROUTED SITE MODEL (STATS)
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "PROOF   ·   ROUTED 3×1 NGCC SITE MODEL, REV 89");
  title(s, "We routed the entire plant before anyone asked for a quote.", { w: 7.6, h: 1.3 });

  s.addImage({ path: A("vp-006.png"), x: 8.35, y: 0.5, w: 4.55, h: 3.66 });
  s.addText("Routed 3D site model: plant zones → equipment duty → cable systems → application pages", {
    x: 8.35, y: 4.2, w: 4.55, h: 0.45, fontFace: FONT, fontSize: 8.5, italic: true, color: MUTED, margin: 0, align: "center", lineSpacingMultiple: 1.1,
  });

  const stats = [
    { v: "96", l: "SCHEDULE RECORDS" },
    { v: "1,784", l: "CIRCUITS ROUTED" },
    { v: "2,478", l: "PHYSICAL RUNS" },
    { v: "1.14M", l: "PROCUREMENT FT" },
    { v: "563,091", l: "LB COPPER" },
    { v: "~0.50", l: "LB CU / FT AVG" },
  ];
  const sw = 2.42, sh = 1.18, sgx = 0.22, sgy = 0.24;
  stats.forEach((st, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.55 + col * (sw + sgx), y = 2.05 + row * (sh + sgy);
    s.addShape("roundRect", { x, y, w: sw, h: sh, rectRadius: 0.05, fill: { color: CARD }, line: { color: CARD_BD, width: 1 } });
    s.addText(st.v, { x: x + 0.15, y: y + 0.12, w: sw - 0.3, h: 0.62, fontFace: FONT, fontSize: 27, bold: true, color: COPPER_D, align: "center", valign: "middle", margin: 0 });
    s.addText(st.l, { x: x + 0.1, y: y + 0.78, w: sw - 0.2, h: 0.28, fontFace: FONT, fontSize: 8.5, bold: true, color: MUTED, align: "center", charSpacing: 1.2, margin: 0 });
  });

  s.addText([
    { text: "Basis: ", options: { bold: true, color: INK } },
    { text: "NGCC master cable schedule Rev M21, geometry-governed. Specification numbers are Southwire family references — a stock number requires conductor sizing and is deliberately not shown. Concept, not for construction.", options: { color: BODY } },
  ], { x: 0.55, y: 5.05, w: 7.6, h: 0.75, fontFace: FONT, fontSize: 9.5, margin: 0, valign: "top", lineSpacingMultiple: 1.12 });

  s.addText([
    { text: "HV underground 69–500 kV · MV EPR 133% 5 / 15 / 25 / 35 kV · duct bank, direct buried and tray.  ", options: { bold: true, color: INK } },
    { text: "Published Southwire record: 15M+ ft HV underground, zero in-service failures.", options: { color: COPPER_D, bold: true } },
  ], { x: 0.55, y: 5.85, w: 12.2, h: 0.5, fontFace: FONT, fontSize: 10.5, margin: 0, valign: "top", lineSpacingMultiple: 1.15 });

  s.addText("Full plant-zone map with per-zone cable applications: Appendix A (SK-120).", {
    x: 0.55, y: 6.45, w: 12.2, h: 0.28, fontFace: FONT, fontSize: 9.5, italic: true, color: MUTED, margin: 0,
  });
  s.addNotes("Replaces page 9 of Rev 07, which shrank the full 34-inch SK-120 poster onto one slide (illegible). The six headline stats are now native tiles; the poster itself is Appendix A at full bleed.");
  footer(s);
}

// =====================================================================
// SLIDE 8 — WHAT THIS LOOKS LIKE INSIDE NRG'S PROGRAM
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "ONE PROPOSITION   ·   FOUR PLACES IT LANDS IN YOUR PROGRAM");
  title(s, "The same platform, in the language of each part of the program.", { w: 11.8 });

  const cases = [
    {
      n: 1, tag: "NEWBUILD · 5.4 GW, FIRST COD 2029",
      h: "Protect COD and capital certainty.",
      d: "Clarify electrical scope, interfaces and supply exposure before EPC decisions harden — while insulation, jacket and raceway are still choices, not history.",
    },
    {
      n: 2, tag: "ACQUIRED FLEET · 18 PLANTS, 13 GW",
      h: "One governed standard, not eighteen inherited ones.",
      d: "Field assessment, rejuvenation and a fleet cable basis turn eighteen sets of as-builts into one measurable, fundable condition baseline.",
    },
    {
      n: 3, tag: "BROWNFIELD · TEF UNITS + PJM UPRATES",
      h: "Capacity inside the fence line.",
      d: "HV underground and factory-built modular spines add megawatts where corridors are full — designed for installed cost, not purchase price.",
    },
    {
      n: 4, tag: "COLOCATION · ~7.5 GW IN NEGOTIATION",
      h: "Both sides of the meter, one schedule.",
      d: "Modular gas power on one side, UL-listed data center assemblies on the other — existing Southwire lines, one circuit schedule, one delivery system.",
    },
  ];
  const qw = 6.0, qh = 2.18, qgx = 0.32, qgy = 0.26;
  cases.forEach((c, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.55 + col * (qw + qgx), y = 1.75 + row * (qh + qgy);
    s.addShape("roundRect", { x, y, w: qw, h: qh, rectRadius: 0.06, fill: { color: CARD }, line: { color: CARD_BD, width: 1 } });
    hexNum(s, c.n, x + 0.26, y + 0.26, 0.4);
    s.addText(c.tag, { x: x + 0.82, y: y + 0.28, w: qw - 1.05, h: 0.24, fontFace: FONT, fontSize: 8.5, bold: true, color: COPPER_D, charSpacing: 1.5, margin: 0 });
    s.addText(c.h, { x: x + 0.82, y: y + 0.54, w: qw - 1.05, h: 0.62, fontFace: FONT, fontSize: 14.5, bold: true, color: INK, margin: 0, valign: "top", lineSpacingMultiple: 1.02 });
    s.addText(c.d, { x: x + 0.82, y: y + 1.12, w: qw - 1.05, h: 0.92, fontFace: FONT, fontSize: 10, color: BODY, margin: 0, valign: "top", lineSpacingMultiple: 1.1 });
  });

  s.addText("Delivering value across the lifecycle:  Develop → Design → Specify → Procure → Build → Commission → Operate → Maintain → Extend", {
    x: 0.55, y: 6.62, w: 12.23, h: 0.3, fontFace: FONT, fontSize: 10, bold: true, color: MUTED, align: "center", margin: 0,
  });
  s.addNotes("Replaces the generic 'One Proposition. Four Use Cases.' page (Rev 07 p10, imported from the internal VP deck with a wrong kicker). Each use case is now mapped to a specific element of NRG's public program.");
  footer(s);
}

// =====================================================================
// SLIDE 9 — WHO WE ARE
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "SOUTHWIRE COMPANY");
  title(s, "A family-held American manufacturer, founded in 1950.", { w: 11.5 });

  s.addText("WHAT WE MAKE", { x: 0.55, y: 1.7, w: 4, h: 0.26, fontFace: FONT, fontSize: 9.5, bold: true, color: COPPER_D, charSpacing: 2, margin: 0 });
  const make = [
    ["High-voltage underground", " — 69–500 kV cable, accessories, installation engineering and field testing."],
    ["Medium & low voltage", " — 5–35 kV EPR and XLPE; 600 V power and control; tray-rated TC-ER."],
    ["Instrumentation & comms", " — shielded pairs and triads, thermocouple, industrial Ethernet and fiber."],
    ["Classified areas & circuit integrity", " — hazardous-location methods, MC-HL, two-hour rated cable, splice kits."],
    ["Modular & factory-built power", " — fine-strand flexible, VFD and tray cable; whips and job kits per module."],
    ["Data center assemblies", " — UL-listed, built, labeled, tested and drum-packed to your schedule."],
  ];
  let my = 2.02;
  make.forEach(([b, r]) => {
    s.addText([{ text: b, options: { bold: true, color: INK } }, { text: r, options: { color: BODY } }],
      { x: 0.55, y: my, w: 6.1, h: 0.52, fontFace: FONT, fontSize: 9.5, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
    my += 0.56;
  });

  s.addText("WHAT WE DO", { x: 7.05, y: 1.7, w: 4, h: 0.26, fontFace: FONT, fontSize: 9.5, bold: true, color: COPPER_D, charSpacing: 2, margin: 0 });
  const doItems = [
    "High-voltage underground transmission services",
    "Field assessment services",
    "Cable rejuvenation — 150M+ ft on record",
    "SPEED services & storm activation team",
    "Contractor solutions professionals",
    "CableTechSupport™ services",
    "Reel tracking system",
    "Solutions University & project services",
  ];
  s.addText(doItems.map((t, i) => ({
    text: t, options: { bullet: { code: "2022", indent: 12 }, color: BODY, breakLine: i < doItems.length - 1, paraSpaceAfter: 6 },
  })), { x: 7.05, y: 2.02, w: 4.0, h: 3.4, fontFace: FONT, fontSize: 9.5, margin: 0, valign: "top" });

  s.addImage({ path: A("teaser-026.png"), x: 10.05, y: 4.55, w: 2.85, h: 2.54 });
  s.addText("Domestic manufacturing and auditable documentation that survives lender diligence.", {
    x: 0.55, y: 5.85, w: 8.9, h: 0.55, fontFace: FONT, fontSize: 12, bold: true, italic: true, color: COPPER_D, margin: 0, valign: "top",
  });
  s.addNotes("Was page 13 of Rev 07 (which carried a wrong kicker and squeezed all content into the top-left). Condensed to what an IPP cares about; lender-diligence line promoted.");
  footer(s);
}

// =====================================================================
// SLIDE 10 — DISCOVERY (dark)
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: DK_BG };
  s.addImage({ path: A("teaser-027.png"), x: W - 2.03, y: 0, w: 2.03, h: 7.5 });
  kicker(s, "DISCOVERY", { y: 0.6 });
  s.addText("We would rather ask than tell.", {
    x: 0.55, y: 0.95, w: 9.5, h: 0.85, fontFace: FONT, fontSize: 30, bold: true, color: DK_TXT, margin: 0,
  });

  const qs = [
    "Which electrical activity slipped first on your last build — and what was it waiting on?",
    "What does a week of delayed COD cost, and who owns that number?",
    "Across the four JV newbuilds — is the cable spec per-project, per-EPC, or a fleet standard?",
    "Which of the eighteen acquired plants has an uprate study underway — and who runs the take-offs?",
  ];
  let qy = 2.15;
  qs.forEach((q, i) => {
    s.addText(String(i + 1).padStart(2, "0"), { x: 0.55, y: qy, w: 0.55, h: 0.4, fontFace: FONT, fontSize: 14, bold: true, color: COPPER, margin: 0, valign: "top" });
    s.addText(q, { x: 1.25, y: qy, w: 9.4, h: 0.62, fontFace: FONT, fontSize: 12.5, color: DK_TXT, margin: 0, valign: "top", lineSpacingMultiple: 1.1 });
    if (i < qs.length - 1) s.addShape("line", { x: 1.25, y: qy + 0.72, w: 9.4, h: 0, line: { color: DK_LINE, width: 0.75 } });
    qy += 0.94;
  });

  s.addText([
    { text: "Right room: ", options: { bold: true, color: DK_TXT } },
    { text: "construction management, the field electrical superintendent, your EPC’s electrical lead, procurement.", options: { color: DK_MUT } },
  ], { x: 0.55, y: 6.0, w: 10.1, h: 0.35, fontFace: FONT, fontSize: 10.5, margin: 0 });
  s.addText("If cable is not where your schedule is lost, that is a useful answer and we will say so.", {
    x: 0.55, y: 6.4, w: 10.1, h: 0.3, fontFace: FONT, fontSize: 10.5, italic: true, color: DK_MUT, margin: 0,
  });
  s.addNotes("Was page 11 of Rev 07 — kept nearly verbatim; it was one of the strongest pages. Now numbered correctly in the flow.");
  footer(s, true);
}

// =====================================================================
// SLIDE 11 — THE ASK (dark)
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: DK_BG };
  s.addImage({ path: A("teaser-028.png"), x: 0, y: 0, w: 2.03, h: 7.5 });
  kicker(s, "THE ASK", { x: 2.75, y: 0.85 });
  s.addText("One hour.\nOne site walk.", {
    x: 2.75, y: 1.25, w: 9.5, h: 1.7, fontFace: FONT, fontSize: 40, bold: true, color: DK_TXT, margin: 0, lineSpacingMultiple: 1.02,
  });
  s.addText("An active build, or an acquired plant with an uprate study. No pricing. No pitch.", {
    x: 2.75, y: 3.2, w: 9.6, h: 0.35, fontFace: FONT, fontSize: 13, color: DK_TXT, margin: 0,
  });
  s.addText("You get a written read-back of where schedule and field labor are being lost on your electrical scope — including where we cannot help.", {
    x: 2.75, y: 3.7, w: 9.6, h: 0.6, fontFace: FONT, fontSize: 13, color: DK_TXT, margin: 0, lineSpacingMultiple: 1.15,
  });
  s.addText("If the session shows nothing, it costs you an hour and we say thank you.", {
    x: 2.75, y: 4.45, w: 9.6, h: 0.3, fontFace: FONT, fontSize: 11, italic: true, color: DK_MUT, margin: 0,
  });

  s.addShape("line", { x: 2.75, y: 5.15, w: 9.5, h: 0, line: { color: DK_LINE, width: 1 } });
  s.addText("Stephan Hardt", { x: 2.75, y: 5.35, w: 5.5, h: 0.35, fontFace: FONT, fontSize: 16, bold: true, color: DK_TXT, margin: 0 });
  s.addText("Director, Power Generation Solutions  ·  Southwire Company", { x: 2.75, y: 5.72, w: 6.5, h: 0.28, fontFace: FONT, fontSize: 10.5, color: DK_MUT, margin: 0 });
  s.addText("stephan.hardt@southwire.com", { x: 8.3, y: 5.35, w: 3.95, h: 0.3, fontFace: FONT, fontSize: 12, bold: true, color: COPPER, align: "right", margin: 0 });
  s.addText("+1 470-439-8488", { x: 8.3, y: 5.7, w: 3.95, h: 0.28, fontFace: FONT, fontSize: 11, color: DK_MUT, align: "right", margin: 0 });

  s.addText("Figures are illustrative or from adjacent markets, and identified as such. Nothing here commits price, lead time or scope.", {
    x: 2.75, y: 6.45, w: 9.5, h: 0.3, fontFace: FONT, fontSize: 9, italic: true, color: DK_MUT, margin: 0,
  });
  s.addNotes("Was page 14 of Rev 07 — kept nearly verbatim. The de-risked, no-pitch ask is the right close for an IPP audience.");
  footer(s, true, 2.75);
}

// =====================================================================
// SLIDE 12 — APPENDIX A: SK-120 (full bleed)
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  // 2200x1205 -> at full width 13.333 => h = 7.303, centered vertically
  s.addImage({ path: A("sk120_art.png"), x: 0, y: 0.1, w: W, h: 7.303 });
  s.addNotes("The SK-120 poster at full page width — legible on screen when zoomed, and flagged for 34-inch print. In Rev 07 this was shrunk onto a content slide and unreadable.");
}

pres.writeFile({ fileName: "Southwire_PowerGen_Teaser_IPP_Rev08.pptx" })
  .then(f => console.log("WROTE", f))
  .catch(e => { console.error(e); process.exit(1); });
