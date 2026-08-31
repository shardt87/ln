// Southwire PowerGen Value Proposition deck — SWR-PG-VP Rev 01
// 9 main slides + 4 appendix, 16:9 LAYOUT_WIDE, native shapes/text only.
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.author = "Stephan Hardt";
pres.company = "Southwire";
pres.title = "Southwire PowerGen Value Proposition — SWR-PG-VP Rev 01";

const W = 13.333;
const WHITE = "FFFFFF";
const INK = "1A1D21";
const COPPER = "C67A43";
const MUTE = "6B7075"; // muted on light
const DMUTE = "A6ACB3"; // muted on dark
const CARD = "F5F4F2";
const DCARD = "23272C";
const DFRAME = "22262B";
const FONT = "Arial";

const TOTAL = 13;

function footer(slide, n, dark) {
  const c = dark ? "8C9299" : "9A9FA4";
  slide.addText("Stephan Hardt · Power Generation Solutions", {
    x: 0.6, y: 7.12, w: 5.5, h: 0.26, fontFace: FONT, fontSize: 8, color: c,
    isTextBox: true, margin: 0, align: "left", valign: "middle",
  });
  slide.addText(`SWR-PG-VP Rev 01 · Internal — Southwire · slide ${n} of ${TOTAL}`, {
    x: 7.2, y: 7.12, w: 5.53, h: 0.26, fontFace: FONT, fontSize: 8, color: c,
    isTextBox: true, margin: 0, align: "right", valign: "middle",
  });
}

function kicker(slide, text, dark) {
  slide.addText(text, {
    x: 0.6, y: 0.48, w: 12.13, h: 0.3, fontFace: FONT, fontSize: 10.5, bold: true,
    color: COPPER, charSpacing: 2, isTextBox: true, margin: 0, align: "left", valign: "middle",
  });
}

function takeaway(slide, text, dark, opts) {
  const o = opts || {};
  slide.addText(text, {
    x: 0.6, y: o.y || 0.84, w: o.w || 12.13, h: o.h || 0.85,
    fontFace: FONT, fontSize: o.size || 32, bold: true,
    color: dark ? WHITE : INK, isTextBox: true, margin: 0, align: "left", valign: "top",
  });
}

function chip(slide, x, y, label, wOverride) {
  const w = wOverride || 0.22 + label.length * 0.072;
  slide.addText(label, {
    shape: pres.ShapeType.roundRect, rectRadius: 0.04,
    x, y, w, h: 0.26, fill: { color: COPPER }, color: WHITE,
    fontFace: FONT, fontSize: 8, bold: true, charSpacing: 1,
    align: "center", valign: "middle", isTextBox: true, margin: 0,
  });
  return w;
}

function placeholderFrame(slide, x, y, w, h, label, dark) {
  slide.addShape(pres.ShapeType.rect, {
    x, y, w, h,
    fill: { color: dark ? DFRAME : "F1EEEA" },
    line: { color: COPPER, width: 0.75, dashType: "dash" },
  });
  slide.addText(label, {
    x: x + 0.15, y, w: w - 0.3, h, fontFace: FONT, fontSize: 9.5,
    color: dark ? DMUTE : MUTE, align: "center", valign: "middle",
    isTextBox: true, margin: 0,
  });
}

function dot(slide, x, y, dark) {
  slide.addShape(pres.ShapeType.ellipse, {
    x, y, w: 0.09, h: 0.09, fill: { color: COPPER }, line: { type: "none" },
  });
}

// ---------------------------------------------------------------- SLIDE 1 (dark)
{
  const s = pres.addSlide();
  s.background = { color: INK };
  kicker(s, "POWER GENERATION SOLUTIONS · SEPT 3, 2026", true);
  takeaway(s, "We built the technical assets of an engineering partner — in-house.", true, { size: 30, h: 0.75 });

  const fw = 3.79, fy = 1.85, fh = 2.35;
  const xs = [0.6, 4.77, 8.94];
  const labels = [
    "PLACEHOLDER\nfirst-generation collateral (A1)",
    "PLACEHOLDER\nCCGT plant render + SK-120\napplication zones (A2)",
    "PLACEHOLDER\nNRG teaser cover, Rev 11 (A3)",
  ];
  const caps = ["2024 — generic collateral", "2026 — CAD-grade site model", "Aug 2026 — account-specific teaser"];
  for (let i = 0; i < 3; i++) {
    placeholderFrame(s, xs[i], fy, fw, fh, labels[i], true);
    s.addText(caps[i], {
      x: xs[i], y: fy + fh + 0.06, w: fw, h: 0.28, fontFace: FONT, fontSize: 9.5,
      color: DMUTE, align: "left", valign: "middle", isTextBox: true, margin: 0,
    });
  }
  s.addText("→", { x: 4.39, y: 2.78, w: 0.38, h: 0.5, fontFace: FONT, fontSize: 18, bold: true, color: COPPER, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  s.addText("→", { x: 8.56, y: 2.78, w: 0.38, h: 0.5, fontFace: FONT, fontSize: 18, bold: true, color: COPPER, align: "center", valign: "middle", isTextBox: true, margin: 0 });

  const beats = [
    "Working assets, not marketing art — the plant model drives the zone mapping and the One-Line Read.",
    "They turned a generic capabilities request into an account-specific teaser.",
    "Built in-house. Outsourced to a technical-visualization firm, the same asset set is estimated at $X.",
  ];
  const by = [4.95, 5.5, 6.05];
  for (let i = 0; i < 3; i++) {
    s.addText(String(i + 1), {
      x: 0.6, y: by[i], w: 0.35, h: 0.42, fontFace: FONT, fontSize: 15, bold: true,
      color: COPPER, align: "left", valign: "top", isTextBox: true, margin: 0,
    });
    s.addText(beats[i], {
      x: 1.05, y: by[i], w: 9.6, h: 0.42, fontFace: FONT, fontSize: 12,
      color: WHITE, align: "left", valign: "top", isTextBox: true, margin: 0,
    });
  }
  const cw = chip(s, 10.85, 6.05, "TO VERIFY");
  s.addText("basis: comparable visualization-firm quote, dated ___", {
    x: 1.05, y: 6.5, w: 9.6, h: 0.28, fontFace: FONT, fontSize: 8.5, italic: true,
    color: DMUTE, align: "left", valign: "top", isTextBox: true, margin: 0,
  });
  footer(s, 1, true);
  s.addNotes(
    "Why this matters to Donna: this capability is what lets a cable manufacturer hold spec-level conversations — no agency retainer, no per-project art budget. The plant model drives the application-zone mapping and the One-Line Read conversation; the NRG teaser came out of a generic capabilities request. The outsourced-cost figure is a placeholder until a comparable visualization-firm quote is in hand.\n[Sources] Internal asset archive (A1–A3, Rev 89 set; NRG teaser Rev 11). Outsourced estimate: to verify against a visualization-firm rate card or dated quote."
  );
}

// ---------------------------------------------------------------- SLIDE 2 (light)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "WHERE THE VERTICAL STANDS", false);
  takeaway(s, "Educated, adapting, executing.", false);

  // Column headers
  s.addText("PAST", { x: 0.6, y: 1.72, w: 3.3, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });
  s.addText("PRESENT", { x: 4.15, y: 1.72, w: 5.2, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });
  s.addText("FUTURE", { x: 9.6, y: 1.72, w: 3.13, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });

  // PAST card
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 2.1, w: 3.3, h: 3.45, fill: { color: CARD }, line: { type: "none" } });
  s.addText([
    { text: "No vertical", options: { breakLine: true } },
    { text: "No definition", options: { breakLine: true } },
    { text: "No market view", options: { breakLine: true } },
    { text: "Generic collateral", options: {} },
  ], { x: 0.85, y: 2.35, w: 2.85, h: 2.9, fontFace: FONT, fontSize: 12.5, color: INK, lineSpacing: 26, isTextBox: true, margin: 0, valign: "top" });

  // PRESENT — Built
  s.addShape(pres.ShapeType.rect, { x: 4.15, y: 2.1, w: 5.2, h: 1.66, fill: { color: CARD }, line: { type: "none" } });
  s.addText("BUILT", { x: 4.38, y: 2.24, w: 2.0, h: 0.25, fontFace: FONT, fontSize: 9, bold: true, color: MUTE, charSpacing: 1.5, isTextBox: true, margin: 0 });
  chip(s, 8.15, 2.22, "PROVISIONAL");
  s.addText(
    "Market mapped and sized · customer set locked — IPP / EPC / OEM / utility generation · 3D plant model + application zones · ~$9.7M July OEM quoting · Patrick and Mike onboard",
    { x: 4.38, y: 2.52, w: 4.74, h: 1.1, fontFace: FONT, fontSize: 10.5, color: INK, isTextBox: true, margin: 0, valign: "top" }
  );

  // PRESENT — Engaged & learned
  s.addShape(pres.ShapeType.rect, { x: 4.15, y: 3.9, w: 5.2, h: 1.65, fill: { color: CARD }, line: { type: "none" } });
  s.addText("ENGAGED & LEARNED", { x: 4.38, y: 4.04, w: 3.4, h: 0.25, fontFace: FONT, fontSize: 9, bold: true, color: MUTE, charSpacing: 1.5, isTextBox: true, margin: 0 });
  s.addText([
    { text: "NRG — teaser in motion, site visit on the table", options: { breakLine: true } },
    { text: "CPV — active development, offtaker / PPA financing insight", options: { breakLine: true } },
    { text: "Southern Power — warm inbound, SVP level", options: {} },
  ], { x: 4.38, y: 4.32, w: 4.74, h: 1.1, fontFace: FONT, fontSize: 10.5, color: INK, lineSpacing: 16, isTextBox: true, margin: 0, valign: "top" });

  // FUTURE card
  s.addShape(pres.ShapeType.rect, { x: 9.6, y: 2.1, w: 3.13, h: 3.45, fill: { color: CARD }, line: { type: "none" } });
  s.addText([
    { text: "Lanes activated, with owners", options: { breakLine: true } },
    { text: "Utility funnel running with the incumbent team", options: { breakLine: true } },
    { text: "OEM engine scaled", options: { breakLine: true } },
    { text: "Strategy document with BD", options: {} },
  ], { x: 9.83, y: 2.35, w: 2.68, h: 2.9, fontFace: FONT, fontSize: 11.5, color: INK, lineSpacing: 20, isTextBox: true, margin: 0, valign: "top" });

  // Copper learnings band
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 5.8, w: 12.13, h: 1.1, fill: { color: COPPER }, line: { type: "none" } });
  s.addText("WHAT THE OUTREACH TAUGHT US", { x: 0.9, y: 5.92, w: 5.0, h: 0.24, fontFace: FONT, fontSize: 8.5, bold: true, color: "F6E3D3", charSpacing: 1.5, isTextBox: true, margin: 0 });
  s.addText(
    "IPPs push execution risk to their EPCs — so we go OEM- and EPC-first near-term and play the IPP game long. Discovery beats pitching. Success stories open doors.",
    { x: 0.9, y: 6.18, w: 11.5, h: 0.62, fontFace: FONT, fontSize: 12, color: WHITE, isTextBox: true, margin: 0, valign: "top" }
  );
  footer(s, 2, false);
  s.addNotes(
    "One paragraph per engagement. NRG: teaser delivered against their public program; site visit on the table; taught us to read an account's own numbers back to them. CPV: active development conversations; taught us how offtaker/PPA financing shapes what a developer will pay for. Southern Power: warm inbound at SVP level; taught us success stories open doors. The strategy pivot (OEM- and EPC-first) traces to real IPP feedback — they push execution risk to their EPCs — not a whiteboard.\n[Sources] July OEM quoting report (~$9.7M, quoting not bookings); engagement notes per account; market model is PROVISIONAL pending internal PO history and BOMs — US_Gas_Power_Wire_Cable_Market_Model_v1.xlsx (17 sheets, live formulas) with the executive readout, research cutoff Aug 27, 2026."
  );
}

// ---------------------------------------------------------------- SLIDE 3 (light)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "SCOPE DEFINITION", false);
  takeaway(s, "Everything inside the fence. Boundary at the point of interconnection.", false, { size: 28, h: 0.7 });

  // Fence
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 1.95, w: 7.5, h: 3.05, fill: { color: "FDF8F3" }, line: { color: COPPER, width: 2 } });
  s.addText("PLANT FENCE — POWERGEN SCOPE", { x: 0.95, y: 2.12, w: 6.8, h: 0.3, fontFace: FONT, fontSize: 10, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });

  const blocks1 = ["Generation packages", "BOP cable", "Switchgear"];
  const bx1 = [0.95, 3.21, 5.47], bw1 = 2.06;
  for (let i = 0; i < 3; i++) {
    s.addShape(pres.ShapeType.rect, { x: bx1[i], y: 2.6, w: bw1, h: 0.72, fill: { color: WHITE }, line: { color: COPPER, width: 1 } });
    s.addText(blocks1[i], { x: bx1[i] + 0.08, y: 2.6, w: bw1 - 0.16, h: 0.72, fontFace: FONT, fontSize: 10.5, color: INK, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  }
  const blocks2 = ["Step-up and generation-side e-houses", "BESS · fuel cells"];
  const bx2 = [0.95, 4.34], bw2 = 3.19;
  for (let i = 0; i < 2; i++) {
    s.addShape(pres.ShapeType.rect, { x: bx2[i], y: 3.52, w: bw2, h: 0.72, fill: { color: WHITE }, line: { color: COPPER, width: 1 } });
    s.addText(blocks2[i], { x: bx2[i] + 0.08, y: 3.52, w: bw2 - 0.16, h: 0.72, fontFace: FONT, fontSize: 10.5, color: INK, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  }
  s.addText("Gas primary · nuclear secondary — scope holds regardless of end user", {
    x: 0.95, y: 4.5, w: 6.8, h: 0.3, fontFace: FONT, fontSize: 9.5, italic: true, color: MUTE, isTextBox: true, margin: 0,
  });

  // POI marker on the fence boundary
  s.addShape(pres.ShapeType.line, { x: 8.1, y: 3.6, w: 1.2, h: 0, line: { color: MUTE, width: 1.25 } });
  s.addShape(pres.ShapeType.ellipse, { x: 7.72, y: 3.24, w: 0.76, h: 0.76, fill: { color: WHITE }, line: { color: COPPER, width: 2 } });
  s.addText("POI", { x: 7.72, y: 3.24, w: 0.76, h: 0.76, fontFace: FONT, fontSize: 10.5, bold: true, color: COPPER, align: "center", valign: "middle", isTextBox: true, margin: 0 });

  // Outside: utility T&D
  s.addShape(pres.ShapeType.rect, { x: 9.3, y: 2.6, w: 3.43, h: 2.0, fill: { color: "F1F1F1" }, line: { color: "CFCFCF", width: 1 } });
  s.addText([
    { text: "UTILITY-OWNED T&D AND GRID", options: { bold: true, fontSize: 11, color: "55595E", breakLine: true } },
    { text: "", options: { fontSize: 5, breakLine: true } },
    { text: "Out of scope for this vertical. The incumbent team's market.", options: { fontSize: 10, color: MUTE } },
  ], { x: 9.55, y: 2.85, w: 2.93, h: 1.9, fontFace: FONT, align: "left", valign: "top", isTextBox: true, margin: 0 });

  s.addText("Excluding T&D is why the utility ask is a funnel, not a sales push.", {
    x: 0.6, y: 5.5, w: 12.13, h: 0.35, fontFace: FONT, fontSize: 11, color: MUTE, isTextBox: true, margin: 0,
  });
  footer(s, 3, false);
  s.addNotes(
    "Definition decisions behind the diagram: fiber is out; hydro is deferred (longer clock, no near-term staffing) — detail in Appendix 3. End-user-agnostic scope (BESS and fuel cells regardless of who owns them) matters for the OEM lane: the same package electrical scope shows up behind the meter and in front of it. Boundary at the POI is what makes the utility relationship a funnel rather than a turf question.\n[Sources] Scope definition workbook; Appendix 3 in/out table."
  );
}

// ---------------------------------------------------------------- SLIDE 4 (dark)
{
  const s = pres.addSlide();
  s.background = { color: INK };
  kicker(s, "MARKET TRENDS", true);
  takeaway(s, "Every trend adds electrical scope inside the fence.", true);

  const rows = [
    "Interconnection queues push data centers and industrials to on-site and behind-the-meter generation — Microsoft–Chevron BTM deal as the marker.",
    "Offtaker-anchored PPAs are financing new plants.",
    "Combined cycle favored on efficiency and the sustainability story.",
    "Hydrogen-capable turbines being specified.",
    "Carbon-capture-ready designs specified; capture systems still cost-prohibitive.",
    "Hyperscalers are building internal power-generation teams.",
  ];
  const ys = [1.95, 2.72, 3.32, 3.92, 4.52, 5.28];
  const hs = [0.68, 0.5, 0.5, 0.5, 0.5, 0.5];
  for (let i = 0; i < rows.length; i++) {
    dot(s, 0.62, ys[i] + 0.1, true);
    s.addText(rows[i], {
      x: 0.95, y: ys[i], w: 9.7, h: hs[i], fontFace: FONT, fontSize: 12.5, color: WHITE,
      isTextBox: true, margin: 0, valign: "top",
    });
  }
  chip(s, 10.15, 4.5, "TIMING — WORKING ASSUMPTION", 2.55);
  s.addText("More generation, built faster, closer to load — all of it wired.", {
    x: 0.6, y: 6.15, w: 12.13, h: 0.5, fontFace: FONT, fontSize: 16, bold: true, color: COPPER, isTextBox: true, margin: 0,
  });
  footer(s, 4, true);
  s.addNotes(
    "Where each trend showed up in our own account conversations: interconnection-queue pressure and BTM moves came up with the data-center-adjacent IPP conversations; offtaker-anchored PPA financing came directly from CPV; combined-cycle preference and hydrogen-capable turbine specs recur in OEM conversations; carbon-capture-ready is specified in new designs while capture systems remain cost-prohibitive (that split is Known; deployment timing is a Working Assumption); hyperscaler internal power teams are visible in hiring and in who shows up at generation events.\n[Sources] Public record: Microsoft–Chevron behind-the-meter deal announcement; NRG 2Q26 earnings (Aug 4, 2026) for program context; account conversation notes per lane."
  );
}

// ---------------------------------------------------------------- SLIDE 5 (light)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "VALUE PROPOSITION BY LANE", false);
  chip(s, 11.9, 0.48, "DRAFT");
  takeaway(s, "Time to power is an electrical execution problem before it is a cable-buying problem. We take hours out of the electrical scope.", false, { size: 22, h: 0.95, w: 11.1 });

  const lanes = [
    ["OEM", "One supplier across the package's electrical scope — fewer POs, fewer gaps, faster integration."],
    ["EPC", "Engineered cable systems and spec support that take field hours off the critical path."],
    ["UTILITY GEN", "HV underground and grounding for the plant side of the POI, backed by the incumbent team's relationships."],
  ];
  const ly = [2.15, 3.5, 4.85];
  for (let i = 0; i < 3; i++) {
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: ly[i], w: 7.9, h: 1.2, fill: { color: CARD }, line: { type: "none" } });
    s.addText(lanes[i][0], { x: 0.85, y: ly[i] + 0.14, w: 3.0, h: 0.26, fontFace: FONT, fontSize: 10.5, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });
    s.addText(lanes[i][1], { x: 0.85, y: ly[i] + 0.44, w: 7.4, h: 0.68, fontFace: FONT, fontSize: 12, color: INK, isTextBox: true, margin: 0, valign: "top" });
  }
  s.addText("Lane wording: working draft for Stephan's edit.", {
    x: 0.6, y: 6.2, w: 7.9, h: 0.28, fontFace: FONT, fontSize: 9, italic: true, color: MUTE, isTextBox: true, margin: 0,
  });

  // Right third — NRG deployment
  s.addText("DEPLOYED — NRG", { x: 8.8, y: 2.15, w: 3.93, h: 0.26, fontFace: FONT, fontSize: 10, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });
  placeholderFrame(s, 8.8, 2.48, 3.93, 1.7, "PLACEHOLDER\nNRG teaser cover (A3)", false);
  const nrg = [
    "Read their public program back — 1.5 GW TEF · 5.4 GW newbuild runway · 25.8 GW fleet (2Q26)",
    "Owner's Equation levers",
    "Prefab case, honesty framing intact",
  ];
  const ny = [4.32, 5.02, 5.34];
  const nh = [0.66, 0.28, 0.28];
  for (let i = 0; i < 3; i++) {
    dot(s, 8.82, ny[i] + 0.07, false);
    s.addText(nrg[i], { x: 9.08, y: ny[i], w: 3.65, h: nh[i], fontFace: FONT, fontSize: 10, color: INK, isTextBox: true, margin: 0, valign: "top" });
  }
  s.addText("The value prop deployed against a named account — in motion, not closed.", {
    x: 8.8, y: 5.78, w: 3.93, h: 0.55, fontFace: FONT, fontSize: 9, italic: true, color: MUTE, isTextBox: true, margin: 0, valign: "top",
  });
  footer(s, 5, false);
  s.addNotes(
    "How the same architecture translates lane to lane: the umbrella is execution hours, not cable price. For OEMs that reads as consolidation (fewer POs, fewer integration gaps); for EPCs as engineered systems and spec support off the critical path; for utility generation as HV underground and grounding on the plant side of the POI. The NRG figures are their own public program read back to them — 1.5 GW TEF portfolio, 5.4 GW newbuild runway, 25.8 GW operating fleet, per 2Q26 earnings; never summed. Benchmark arithmetic lives in Appendix 4 only — gross is not net.\n[Sources] NRG 2Q26 earnings (Aug 4, 2026), public record. Prefab benchmark: Appendix 4 (adjacent-market, a fuel cell manufacturer's program)."
  );
}

// ---------------------------------------------------------------- SLIDE 6 (light)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "UTILITY LANE", false);
  takeaway(s, "The utility team is the funnel. Here's the ask.", false);

  const asks = [
    ["Visibility on which IOUs and co-ops are building generation.", "Market intel — part of it comes from published reports. Low lift."],
    ["Agent support on generation-side opportunities.", null],
    ["HV underground and grounding as the utility side's product contribution to plants.", null],
  ];
  const ay = [1.95, 2.95, 3.7];
  for (let i = 0; i < 3; i++) {
    s.addText(String(i + 1), { x: 0.6, y: ay[i], w: 0.5, h: 0.5, fontFace: FONT, fontSize: 22, bold: true, color: COPPER, isTextBox: true, margin: 0, valign: "top" });
    s.addText(asks[i][0], { x: 1.3, y: ay[i] + 0.03, w: 11.4, h: 0.45, fontFace: FONT, fontSize: 14.5, color: INK, isTextBox: true, margin: 0, valign: "top" });
    if (asks[i][1]) {
      s.addText(asks[i][1], { x: 1.3, y: ay[i] + 0.48, w: 11.4, h: 0.3, fontFace: FONT, fontSize: 10.5, color: MUTE, isTextBox: true, margin: 0, valign: "top" });
    }
  }

  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 4.6, w: 12.13, h: 0.95, fill: { color: CARD }, line: { type: "none" } });
  s.addText(
    "Georgia Power hosted a generation event in Birmingham. Our agent attended; we weren't in the room. We need to know before, not after.",
    { x: 0.9, y: 4.78, w: 11.5, h: 0.6, fontFace: FONT, fontSize: 12, color: INK, isTextBox: true, margin: 0, valign: "top" }
  );

  chip(s, 0.6, 5.95, "DECISION REQUIRED");
  s.addText(
    "Agent credit for non-portfolio products — how do agents get paid or recognized when they open generation doors?",
    { x: 2.15, y: 5.93, w: 10.55, h: 0.55, fontFace: FONT, fontSize: 12, color: INK, isTextBox: true, margin: 0, valign: "top" }
  );
  footer(s, 6, false);
  s.addNotes(
    "The funnel logic: T&D is excluded from this vertical's scope, so the utility team's value here is access, not quota. Ask one is largely published-report work — low lift. The Birmingham note is an account fact, not blame: Jay Carver owns the Georgia Power account. On agent credit, the Whitehead dual-credit arrangement exists as word-of-mouth only today — that is why this is tagged Decision Required rather than proposed as policy.\n[Sources] Agent report from the Birmingham generation event; account ownership per the utility team's coverage map."
  );
}

// ---------------------------------------------------------------- SLIDE 7 (light)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "EPC LANE · RENAMED FROM INDUSTRIAL", false);
  takeaway(s, "Influence the spec where the cable decisions actually get made.", false, { size: 28, h: 0.7 });

  const rows = [
    ["EXECUTION", "Patrick is the execution resource — upstream spec work with EPCs, ahead of the RFQ.", null],
    ["DISTRIBUTION", "Runs through Brian Sides and CIE Wire. Visit Sept 2, Alabaster. Full project BOM outstanding — being chased there; update live in this meeting.", "TO VERIFY"],
    ["NO STANDALONE CHANNEL STRATEGY", "Brian signals where distribution needs activating. Medium-voltage interconnect — switchgear-class OEMs — routes through his world.", null],
  ];
  const ry = [2.05, 3.25, 4.6];
  for (let i = 0; i < 3; i++) {
    s.addText(rows[i][0], { x: 0.6, y: ry[i], w: 6.0, h: 0.26, fontFace: FONT, fontSize: 10.5, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });
    if (rows[i][2]) chip(s, 2.15, ry[i] - 0.03, rows[i][2]);
    s.addText(rows[i][1], { x: 0.6, y: ry[i] + 0.32, w: 11.6, h: 0.62, fontFace: FONT, fontSize: 13, color: INK, isTextBox: true, margin: 0, valign: "top" });
  }
  s.addText("The long game, alongside IPP project work.", {
    x: 0.6, y: 6.1, w: 12.13, h: 0.35, fontFace: FONT, fontSize: 12, italic: true, color: MUTE, isTextBox: true, margin: 0,
  });
  footer(s, 7, false);
  s.addNotes(
    "The CIE play: lead with the full-plant application overview, then ask where the BOM stands — don't open with the ask. If the Sept 2 Alabaster visit lands before this meeting, update the BOM status live and drop the To Verify tag. The $11/kW MV field benchmark is what recalibrated the portfolio estimates — it puts a number on medium-voltage scope per plant and keeps the distribution conversation grounded.\n[Sources] CIE Wire visit plan (Sept 2, Alabaster); $11/kW MV field benchmark from project reference data; distribution routing per Brian Sides."
  );
}

// ---------------------------------------------------------------- SLIDE 8 (light)
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  kicker(s, "OEM LANE", false);
  s.addText("$9.7M", {
    x: 0.6, y: 1.15, w: 8.5, h: 1.85, fontFace: FONT, fontSize: 92, bold: true, color: COPPER, isTextBox: true, margin: 0, valign: "top",
  });
  s.addText("quoted to generation OEMs in July.", {
    x: 0.6, y: 3.15, w: 11.0, h: 0.45, fontFace: FONT, fontSize: 17, color: INK, isTextBox: true, margin: 0,
  });

  const lines = [
    "Lead flow: Jeff's direct team first — Tim Tucker is the point — then OEM distribution.",
    "Generation OEMs are a new segment for the direct team. Clean lane, no channel conflict.",
    "Mike's OEM map on hand — appendix; pull up if asked.",
  ];
  const ly = [4.15, 4.7, 5.25];
  for (let i = 0; i < 3; i++) {
    dot(s, 0.62, ly[i] + 0.09, false);
    s.addText(lines[i], { x: 0.95, y: ly[i], w: 11.6, h: 0.42, fontFace: FONT, fontSize: 12.5, color: INK, isTextBox: true, margin: 0, valign: "top" });
  }
  s.addText("Where PowerGen makes money now — while the project lanes mature.", {
    x: 0.6, y: 6.1, w: 12.13, h: 0.35, fontFace: FONT, fontSize: 12, italic: true, color: MUTE, isTextBox: true, margin: 0,
  });
  footer(s, 8, false);
  s.addNotes(
    "Why OEM is the near-term engine while project lanes mature: shorter cycles, a clean new segment for the direct team, no channel conflict. Say the caveat out loud: $9.7M is July quoting activity, not booked revenue. Day-one guidance to the team: stay off utility accounts.\n[Sources] July OEM quoting report (~$9.7M, quoting). Lead-flow routing: Jeff's direct team, Tim Tucker as point. OEM map: Appendix 2."
  );
}

// ---------------------------------------------------------------- SLIDE 9 (dark)
{
  const s = pres.addSlide();
  s.background = { color: INK };
  kicker(s, "EXECUTION — PEOPLE AND COORDINATION", true);
  takeaway(s, "Names on the page. Ask per lane.", true);

  // Left: coordination map
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 1.95, w: 5.9, h: 0.55, fill: { color: COPPER }, line: { type: "none" } });
  s.addText("Stephan Hardt · Marc — vertical leads", {
    x: 0.6, y: 1.95, w: 5.9, h: 0.55, fontFace: FONT, fontSize: 11.5, bold: true, color: WHITE, align: "center", valign: "middle", isTextBox: true, margin: 0,
  });
  s.addShape(pres.ShapeType.line, { x: 3.55, y: 2.5, w: 0, h: 0.25, line: { color: DMUTE, width: 1 } });

  const team = [
    ["Patrick", "EPC"],
    ["Mike Patello", "OEM · Tucker / Murray mentoring"],
    ["Jeff's team", "direct + lead flow"],
    ["Brian Sides", "distribution signals · MV / industrial"],
    ["John's utility team", "funnel · market intel · agents"],
    ["BD", "lead-gen and data arm"],
  ];
  const tx = [0.6, 3.65], tw = 2.85, th = 0.92;
  for (let i = 0; i < 6; i++) {
    const x = tx[i % 2], y = 2.75 + Math.floor(i / 2) * 1.07;
    s.addShape(pres.ShapeType.rect, { x, y, w: tw, h: th, fill: { color: DCARD }, line: { type: "none" } });
    s.addText([
      { text: team[i][0], options: { bold: true, fontSize: 10.5, color: WHITE, breakLine: true } },
      { text: team[i][1], options: { fontSize: 9, color: DMUTE } },
    ], { x: x + 0.18, y: y + 0.12, w: tw - 0.36, h: th - 0.24, fontFace: FONT, align: "left", valign: "top", isTextBox: true, margin: 0 });
  }

  // Right: asks per lane
  s.addText("THE ASKS", { x: 7.0, y: 1.98, w: 5.73, h: 0.26, fontFace: FONT, fontSize: 10, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0 });
  const asks = [
    ["UTILITY", "the three asks — visibility, agent support, HV underground"],
    ["EPC", "BOM closure + spec access upstream"],
    ["OEM", "protect the lane, scale lead flow"],
    ["EXECUTIVE", "Donna as sponsor — strategy document, cross-team decisions, agent credit first"],
  ];
  const ry = [2.4, 3.28, 4.0, 4.72];
  for (let i = 0; i < 4; i++) {
    s.addText(asks[i][0], { x: 7.0, y: ry[i], w: 1.55, h: 0.3, fontFace: FONT, fontSize: 10, bold: true, color: COPPER, charSpacing: 1, isTextBox: true, margin: 0, valign: "top" });
    s.addText(asks[i][1], { x: 8.65, y: ry[i], w: 4.08, h: 0.68, fontFace: FONT, fontSize: 11, color: WHITE, isTextBox: true, margin: 0, valign: "top" });
  }
  chip(s, 7.0, 5.62, "PROVISIONAL");
  s.addText("Market behind the lanes: $170–240M a year in U.S. gas-generation cable POs through 2030 — model v1, awaiting internal PO history and BOMs.", {
    x: 7.0, y: 5.95, w: 5.73, h: 0.62, fontFace: FONT, fontSize: 9.5, color: DMUTE, isTextBox: true, margin: 0, valign: "top",
  });

  s.addText("The homework is done. This is the operating model.", {
    x: 0.6, y: 6.35, w: 12.13, h: 0.45, fontFace: FONT, fontSize: 15, bold: true, color: COPPER, isTextBox: true, margin: 0,
  });
  footer(s, 9, true);
  s.addNotes(
    "Cadence proposal: this group reconvenes monthly for the first quarter, then quarterly; lane owners report against the asks on this slide. The 30-day strategy document (with BD) lands: validated market model (replacing the PROVISIONAL tag), lane plans with owners and dates, the agent-credit decision, and the utility funnel mechanics agreed with John's team. The market line stays PROVISIONAL out loud: base case $170–240M per year in U.S. gas-generation cable POs through 2030 (constant 2026 dollars, manufacturer net sales, generation-side cable only), 2026 SAM ~$172M, cumulative 2026–35 SAM ~$1.0B — only 46% of named MW is evidence-backed and no internal quote/BOM/PO data is loaded, so no figure is presented as validated.\n[Sources] Internal — roles per current org; asks trace to slides 5–8. Market: US_Gas_Power_Wire_Cable_Market_Model_v1.xlsx (Executive_Summary, base scenario, PO-year view) and the gas-power executive readout (research cutoff Aug 27, 2026) — PROVISIONAL, model passes 27 QA tests with 3 disclosed exceptions."
  );
}

// ---------------------------------------------------------------- APPENDIX 1
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("APPENDIX 1 — ILLUSTRATION EVOLUTION, FULL SET", {
    x: 0.6, y: 0.5, w: 12.13, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: INK, isTextBox: true, margin: 0,
  });
  const fw = 3.79, fh = 2.45;
  const xs = [0.6, 4.77, 8.94], ys = [1.25, 4.05];
  let n = 1;
  for (const y of ys) {
    for (const x of xs) {
      placeholderFrame(s, x, y, fw, fh, `PLACEHOLDER — frame ${n} (A1/A2 set)`, false);
      s.addText("date ___", { x, y: y + fh + 0.04, w: fw, h: 0.24, fontFace: FONT, fontSize: 8.5, color: MUTE, isTextBox: true, margin: 0 });
      n++;
    }
  }
  footer(s, 10, false);
  s.addNotes(
    "Full illustration set, dated, oldest to newest. If any composite is exported as an image, the credit line gets burned into the pixels — not a separate overlay.\n[Sources] Internal asset archive (A1 early collateral; A2 Rev 89 render set)."
  );
}

// ---------------------------------------------------------------- APPENDIX 2
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("APPENDIX 2 — OEM MAP", {
    x: 0.6, y: 0.5, w: 12.13, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: INK, isTextBox: true, margin: 0,
  });
  placeholderFrame(s, 0.6, 1.25, 12.13, 5.55, "PLACEHOLDER — Mike's OEM map (A4): target OEMs by application zone", false);
  footer(s, 11, false);
  s.addNotes("Mike Patello's OEM map — target OEMs by application zone. Pull up from slide 8 if asked.\n[Sources] Mike Patello's OEM mapping.");
}

// ---------------------------------------------------------------- APPENDIX 3
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("APPENDIX 3 — DEFINITION DETAIL", {
    x: 0.6, y: 0.5, w: 12.13, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: INK, isTextBox: true, margin: 0,
  });
  const rows = [
    ["IN", "Gas generation (primary)", "Core market; where the buildout is"],
    ["IN", "Nuclear (secondary)", "Longer clock; track, don't staff"],
    ["IN", "Generation packages, BOP cable, switchgear", "Inside the fence"],
    ["IN", "Step-up and generation-side e-houses", "Plant side of the POI"],
    ["IN", "BESS and fuel cells — any end user", "Scope holds behind the meter"],
    ["OUT", "Utility-owned T&D and grid", "Boundary at the POI; the incumbent team's market"],
    ["OUT", "Fiber", "Adjacent scope, different buyer; revisit only with a project pull"],
    ["DEFERRED", "Hydro", "Revisit later; no near-term staffing"],
  ];
  const tableRows = rows.map((r) => [
    { text: r[0], options: { bold: true, color: r[0] === "IN" ? COPPER : MUTE, align: "left" } },
    { text: r[1], options: { color: INK } },
    { text: r[2], options: { color: MUTE } },
  ]);
  s.addTable(tableRows, {
    x: 0.6, y: 1.25, w: 12.13, colW: [1.4, 4.6, 6.13], rowH: 0.62,
    fontFace: FONT, fontSize: 11, border: { type: "solid", pt: 0.5, color: "E2E2E2" },
    valign: "middle", margin: [0.06, 0.1, 0.06, 0.1],
  });
  footer(s, 12, false);
  s.addNotes(
    "The in/out table behind slide 3, with one-line rationale each — including the fiber-out and hydro-deferred decisions.\n[Sources] Scope definition workbook."
  );
}

// ---------------------------------------------------------------- APPENDIX 4
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("APPENDIX 4 — BENCHMARK ARITHMETIC", {
    x: 0.6, y: 0.5, w: 12.13, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: INK, isTextBox: true, margin: 0,
  });
  chip(s, 0.6, 1.15, "ADJACENT-MARKET BENCHMARK", 2.45);
  s.addText("Prefab spine case — a fuel cell manufacturer's program.", {
    x: 0.6, y: 1.6, w: 12.13, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: INK, isTextBox: true, margin: 0,
  });
  s.addText("4,400 → ~880 field hours per installation", {
    x: 0.6, y: 2.2, w: 12.13, h: 0.65, fontFace: FONT, fontSize: 26, bold: true, color: COPPER, isTextBox: true, margin: 0,
  });
  const math = [
    "$418K field labor at stick-build → $83.6K prefab → $334K saved per unit (gross).",
    "Extrapolated across a 100-unit program: $33.4M — an extrapolation, not a forecast.",
  ];
  const my = [3.1, 3.62];
  for (let i = 0; i < 2; i++) {
    dot(s, 0.62, my[i] + 0.08, false);
    s.addText(math[i], { x: 0.95, y: my[i], w: 11.6, h: 0.42, fontFace: FONT, fontSize: 13, color: INK, isTextBox: true, margin: 0, valign: "top" });
  }
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 4.5, w: 12.13, h: 1.55, fill: { color: "F7EEE6" }, line: { type: "none" } });
  s.addText("CAVEATS — READ BEFORE USING THESE NUMBERS", {
    x: 0.9, y: 4.66, w: 8.0, h: 0.24, fontFace: FONT, fontSize: 8.5, bold: true, color: COPPER, charSpacing: 1.5, isTextBox: true, margin: 0,
  });
  s.addText(
    "Adjacent-market benchmark from a fuel cell manufacturer's program — not an NRG or Southwire-project result. Gross is not net. Installed cost is higher — the argument is TCO over asset life. This slide exists so the main deck never carries dollar math.",
    { x: 0.9, y: 4.94, w: 11.5, h: 1.0, fontFace: FONT, fontSize: 11.5, color: INK, isTextBox: true, margin: 0, valign: "top" }
  );
  footer(s, 13, false);
  s.addNotes(
    "The full caveat band matters more than the arithmetic: this is an adjacent-market benchmark from a fuel cell manufacturer's public prefab program, not an NRG or Southwire-project result; savings are gross, not net; installed cost goes up — the argument is TCO over asset life. Slides 5 and 8 deliberately carry none of this dollar math.\n[Sources] Fuel cell manufacturer's public prefab program (field-hour benchmark); internal extrapolation."
  );
}

pres.writeFile({ fileName: "Southwire_PowerGen_ValueProp_Rev01.pptx" }).then(() => {
  console.log("written: Southwire_PowerGen_ValueProp_Rev01.pptx");
});
