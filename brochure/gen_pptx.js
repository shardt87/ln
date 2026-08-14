// Editable 16:9 PPTX of Southwire_PowerGen_Brochure_NRG_Rev01
// Canvas: LAYOUT_WIDE 13.333 x 7.5 in = 960 x 540 pt. Coordinates in pt, y measured
// from the BOTTOM (print convention) to mirror build_brochure.py's layout logic.
const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in — true widescreen

const WARM = "F6F3EE", GRAPHITE = "17191C", INK = "1A1C22", GRAY = "6E6C66",
  GRAY_LT = "96938C", COPPER = "C67A43", COPPER_LT = "E3A06D", COPPER_DP = "9D4E24",
  TEAL = "1A272F", OFFWHITE = "ECEAE6", HAIR = "D8D2C8", HAIR_DK = "3C3F44",
  WHITE = "FFFFFF", MUTED = "969490", STEEL = "32353A";
const A = "assets/";
const PW = 960, PH = 540, M = 56;
const X = (x) => x / 72;
const Y = (yTop) => (PH - yTop) / 72;
const W = (w) => w / 72;

// text: yb = baseline of first line, measured from bottom
function T(s, xpt, yb, wpt, lines, o = {}) {
  const size = o.size || 10, leading = o.leading || size * 1.35;
  const arr = Array.isArray(lines) ? lines : [lines];
  const topPdf = yb + size * 1.02;
  const h = (leading * (arr.length - 1) + size * 1.9) / 72;
  const opts = {
    x: o.align === "center" ? X(xpt) - W(wpt) / 2 : o.align === "right" ? X(xpt) - W(wpt) : X(xpt),
    y: Y(topPdf), w: W(wpt), h,
    fontFace: "Arial", fontSize: size, color: o.color || INK,
    bold: !!o.bold, italic: !!o.italic, align: o.align || "left",
    valign: "top", margin: 0, lineSpacing: leading,
  };
  if (o.track) opts.charSpacing = o.track;
  if (o.shadow) opts.shadow = { type: "outer", color: "000000", blur: 5, offset: 1.5, angle: 90, opacity: 0.55 };
  s.addText(arr.join("\n"), opts);
}
const rect = (s, x, yTop, w, h, color) =>
  s.addShape("rect", { x: X(x), y: Y(yTop), w: W(w), h: W(h), fill: { color }, line: { type: "none" } });
const hline = (s, x1, x2, y, color, width) =>
  s.addShape("line", { x: X(x1), y: Y(y), w: W(x2 - x1), h: 0, line: { color, width } });
const img = (s, file, x, yTop, w, h) =>
  s.addImage({ path: A + file, x: X(x), y: Y(yTop), w: W(w), h: W(h) });
const full = (s, file) => s.addImage({ path: A + file, x: 0, y: 0, w: 13.333, h: 7.5 });
const dot = (s, cx, cy, r, color) =>
  s.addShape("ellipse", { x: X(cx - r), y: Y(cy + r), w: W(2 * r), h: W(2 * r), fill: { color }, line: { type: "none" } });

const FOOT = "Stephan Hardt   |   Power Generation Solutions";

function lightFrame(s, kicker, folio, band) {
  s.background = { color: WARM };
  rect(s, 0, PH, PW, 3.5, COPPER);
  const lh = 21;
  img(s, "lockup_light.png", M, PH - 26, lh * 640 / 135, lh);
  T(s, PW - M, PH - 40, 240, kicker, { size: 7.5, bold: true, color: COPPER, track: 1.6, align: "right" });
  if (!band) {
    T(s, M, 26, 320, FOOT, { size: 6.5, color: GRAY_LT });
    T(s, PW - M, 26, 60, folio, { size: 6.5, bold: true, color: COPPER, track: 1.2, align: "right" });
  }
}
function bandFooter(s, folio, dark) {
  T(s, M, 13, 320, FOOT, { size: 6.5, color: dark || "8C8A86" });
  T(s, PW - M, 13, 60, folio, { size: 6.5, bold: true, color: COPPER_LT, track: 1.2, align: "right" });
}

// ---------------- 1 · cover
{
  const s = p.addSlide();
  s.background = { color: GRAPHITE };
  const bh = PW * 580 / 4752;
  img(s, "wide_hex_top.png", 0, PH, PW, bh);
  img(s, "wide_hex_bottom.png", 0, bh, PW, bh);
  const lw = 186, lh = lw * 202 / 943;
  img(s, "lockup_dark_keyed.png", PW / 2 - lw / 2, 402, lw, lh);
  T(s, PW / 2, 300, 820, "ACCELERATING", { size: 38, bold: true, color: WHITE, track: 5.5, align: "center" });
  T(s, PW / 2, 252, 820, "TIME TO POWER", { size: 38, bold: true, italic: true, color: COPPER_LT, track: 5.5, align: "center" });
  hline(s, PW / 2 - 58, PW / 2 + 58, 230, COPPER, 1.2);
  T(s, PW / 2, 202, 860, "Accelerating & protecting power readiness across NRG's gas power generation buildout.",
    { size: 10.5, color: OFFWHITE, align: "center" });
  T(s, PW / 2, 178, 900, "COMBINED CYCLE  ·  SIMPLE CYCLE & PEAKERS  ·  MODULAR POWER  ·  BLACK START  ·  COAL/GAS REPOWER  ·  GREENFIELD & BROWNFIELD",
    { size: 6.5, color: MUTED, track: 1.1, align: "center" });
  T(s, PW / 2, 136, 860, "PRESERVE SCHEDULE CERTAINTY THROUGH ENERGIZATION.",
    { size: 8.5, bold: true, color: COPPER_LT, track: 2.2, align: "center" });
  T(s, PW / 2, 58, 860, "Stephan Hardt   |   Director, Power Generation Solutions   |   www.southwire.com",
    { size: 7.5, color: "9E9C98", align: "center" });
}

// ---------------- 2 · why now
{
  const s = p.addSlide();
  lightFrame(s, "WHY NOW", "02", true);
  T(s, M, 448, 800, ["NRG's growth agenda creates three distinct", "electrical-delivery environments & power demand."],
    { size: 26, bold: true, leading: 31 });
  const cols = [
    ["1.5 GW", "TEF PORTFOLIO", "One project operating; two targeting mid-2028. Not the entire portfolio under construction."],
    ["5.4 GW", "NEWBUILD DEVELOPMENT", "Turbine and EPC access supports a development runway through 2032."],
    ["25.8 GW", "OPERATING FLEET", "Reported after the LS Power acquisition; ~1–2 GW of upgrades under evaluation."],
  ];
  const colw = (PW - 2 * M - 80) / 3;
  cols.forEach((c, i) => {
    const x = M + i * (colw + 40);
    T(s, x, 336, colw, c[0], { size: 32, bold: true });
    hline(s, x + 1, x + 27, 318, COPPER, 1.4);
    T(s, x, 298, colw, c[1], { size: 8, bold: true, color: COPPER_DP, track: 1.5 });
    T(s, x, 278, colw - 14, c[2], { size: 9.5, color: GRAY, leading: 13.5 });
  });
  const iw = 248, ih = iw * 9 / 16;          // complete gate view, uncropped
  img(s, "gate_complete.jpg", PW - M - iw, 236, iw, ih);
  T(s, M, 196, 500, ["Specifications, capacity, metals hedging, releases, reels, package interfaces and", "field readiness still have to converge on COD.  Do not sum the figures — asset states overlap."],
    { size: 9.5, color: GRAY, leading: 14 });
  T(s, M, 104, 300, "Source: NRG 2Q26, Aug. 4, 2026", { size: 6, color: GRAY_LT });
  rect(s, 0, 76, PW, 76, GRAPHITE);
  T(s, M, 52, 600, "DIFFERENT ASSET STATES. ONE REQUIREMENT.", { size: 8, bold: true, color: COPPER_LT, track: 1.8 });
  T(s, M, 30, 600, "Preserve schedule certainty through energization.", { size: 13, bold: true, color: WHITE });
  bandFooter(s, "02");
}

// ---------------- 3 · thesis (plant right, argument left)
{
  const s = p.addSlide();
  full(s, "wide_thesis.jpg");
  T(s, M, 500, 300, "THE THESIS", { size: 7.5, bold: true, color: COPPER_DP, track: 1.6 });
  T(s, M, 470, 840, ["Time to power is an electrical execution problem", "before it is a cable-buying problem."],
    { size: 22, bold: true, leading: 28 });
  const bullets = [
    "Interfaces cross packages, zones, POI, contractors and turnover paths.",
    "Late material decisions return as handling, rework and commissioning exposure.",
    "Managing the workstream as a system protects schedule better than isolated purchase-order optimization.",
  ];
  let by = 390;
  bullets.forEach((b) => {
    hline(s, M + 1, M + 13, by + 3, COPPER_DP, 1.4);
    T(s, M + 22, by, 190, b, { size: 8.5, leading: 11.5, color: INK });
    by -= 48;
  });
  rect(s, 0, 40, PW, 40, GRAPHITE);
  T(s, M, 16, 880, "The plant-wide electrical-delivery partner — cable scope ready for the workface, not merely available at the warehouse.",
    { size: 9, bold: true, italic: true, color: WHITE });
  T(s, PW - M, 500, 300, FOOT + "   ·   03", { size: 6.5, color: GRAY, align: "right" });
}

// ---------------- 4 · risks
{
  const s = p.addSlide();
  lightFrame(s, "THE THREE RISKS", "04", true);
  T(s, M, 448, 800, ["Three execution risks can erode certainty", "between design and energization."],
    { size: 26, bold: true, leading: 31 });
  const cols = [
    ["01", "LABOR & DEMAND PRESSURE", "Long pulls, dense terminations and compressed turnover windows concentrate labor when flexibility is lowest."],
    ["02", "MATERIAL + INSTALLATION FIT", "Ratings, routes, reel lengths, accessories and releases must match the workface, not only the BOM — or material arrives right and installs wrong."],
    ["03", "FRAGMENTED COORDINATION", "Civil, electrical, OEM and contractor decisions can converge after routing and procurement choices are already locked, turning gaps into rework."],
  ];
  const colw = (PW - 2 * M - 80) / 3;
  cols.forEach((c, i) => {
    const x = M + i * (colw + 40);
    T(s, x, 344, colw, c[0], { size: 20, bold: true, color: COPPER, track: 2 });
    hline(s, x + 1, x + 27, 328, COPPER, 1.4);
    T(s, x, 308, colw, c[1], { size: 8.5, bold: true, track: 1.2 });
    T(s, x, 288, colw - 14, c[2], { size: 9.5, color: GRAY, leading: 13.5 });
  });
  rect(s, 0, 76, PW, 76, GRAPHITE);
  T(s, M, 48, 700, "Late handoffs become schedule and commissioning exposure.", { size: 12.5, bold: true, color: WHITE });
  T(s, M, 28, 700, "LABOR AVAILABILITY   |   MATERIAL READINESS   |   DECISION TIMING", { size: 7, color: MUTED, track: 1.6 });
  bandFooter(s, "04");
}

// ---------------- 5 · the system
{
  const s = p.addSlide();
  full(s, "wide_interior.jpg");
  T(s, M, 498, 300, "THE SYSTEM", { size: 7.5, bold: true, color: COPPER_LT, track: 1.6 });
  T(s, M, 468, 840, ["One coordinated flow aligns decisions", "from planning through turnover."],
    { size: 22, bold: true, color: WHITE, leading: 28, shadow: true });
  T(s, M, 416, 700, ["Southwire connects application support, material planning, sequenced logistics", "and field readiness — without changing project accountability."],
    { size: 9.5, bold: true, color: OFFWHITE, leading: 14, shadow: true });
  rect(s, 0, 126, PW, 126, GRAPHITE);
  const steps = [
    ["PLAN +", "FORECAST"], ["APPLICATION", "ALIGNMENT"], ["MATERIAL + REEL", "STRATEGY"],
    ["RELEASE +", "LOGISTICS"], ["INSTALLATION", "READINESS"], ["FIELD SUPPORT +", "TURNOVER"],
  ];
  const x0 = M + 40, x1 = PW - M - 40, ny = 92;
  hline(s, x0, x1, ny, COPPER, 1);
  steps.forEach((name, i) => {
    const x = x0 + i * (x1 - x0) / 5;
    dot(s, x, ny, 11, i < 5 ? STEEL : COPPER_DP);
    T(s, x, ny - 3.4, 40, String(i + 1), { size: 9.5, bold: true, color: WHITE, align: "center" });
    T(s, x, ny - 26, 150, name, { size: 7, bold: true, color: OFFWHITE, track: 0.8, align: "center", leading: 10 });
  });
  T(s, PW / 2, 30, 880, "FIELD-ENGINEER WHAT IS UNIQUE. PREFABRICATE WHAT REPEATS.",
    { size: 8.5, bold: true, color: COPPER_LT, track: 1.6, align: "center" });
  bandFooter(s, "05");
}

// ---------------- 6 · value proposition (plant diagram restored)
{
  const s = p.addSlide();
  full(s, "wide_iso.jpg");
  T(s, M, 500, 400, "THE VALUE PROPOSITION", { size: 7.5, bold: true, color: COPPER_DP, track: 1.6 });
  T(s, M, 462, 600, "Southwire helps IPPs", { size: 27, bold: true });
  T(s, M, 428, 600, "accelerate time to power.", { size: 27, bold: true, color: COPPER_DP });
  hline(s, M + 1, M + 120, 404, COPPER, 1.2);
  T(s, M, 372, 268, ["By transforming fragmented plant-wide cable procurement into a coordinated, workface-ready electrical delivery system — reducing schedule risk, installed effort, and commissioning exposure from planning through energization."],
    { size: 10, color: "3A3C42", leading: 15 });
  T(s, M, 26, 320, FOOT, { size: 6.5, color: GRAY_LT });
  T(s, PW - M, 26, 60, "06", { size: 6.5, bold: true, color: COPPER, track: 1.2, align: "right" });
}

// ---------------- 7 · adjacent evidence
{
  const s = p.addSlide();
  s.background = { color: TEAL };
  T(s, M, 500, 300, "ADJACENT EVIDENCE", { size: 7.5, bold: true, color: COPPER_LT, track: 1.6 });
  T(s, M, 470, 520, ["Adjacent experience indicates where", "to test — not what NRG will save."],
    { size: 22, bold: true, color: WHITE, leading: 28 });
  T(s, M, 372, 200, "4,400", { size: 38, bold: true, color: WHITE });
  s.addShape("line", { x: X(M + 168), y: Y(386), w: W(40), h: 0, line: { color: COPPER, width: 1.6, endArrowType: "arrow" } });
  T(s, M + 228, 372, 200, "~880", { size: 38, bold: true, color: COPPER_LT });
  T(s, M, 350, 200, ["OBSERVED FIELD HOURS", "SITE-BUILT BASELINE"], { size: 6.8, bold: true, color: "B2B6B8", track: 1, leading: 10.5 });
  T(s, M + 228, 350, 220, ["MODELED FIELD HOURS", "FACTORY-BUILT ASSEMBLY"], { size: 6.8, bold: true, color: COPPER_LT, track: 1, leading: 10.5 });
  T(s, M, 312, 420, ["Field hours per electrical spine in one repetitive modular-generation scope.", "Illustrative adjacent-market benchmark — not an NRG result."],
    { size: 8.5, color: "969EA2", leading: 13 });
  T(s, M, 262, 300, "WHAT IT SUGGESTS", { size: 7.5, bold: true, color: COPPER_LT, track: 1.4 });
  T(s, M, 242, 400, ["Stable, repeatable interfaces may be candidates for offsite work."], { size: 9.5, color: OFFWHITE, leading: 14 });
  T(s, M, 202, 300, "WHAT IT DOES NOT PROVE", { size: 7.5, bold: true, color: COPPER_LT, track: 1.4 });
  T(s, M, 182, 400, ["Net NRG savings, schedule reduction or critical-path removal."], { size: 9.5, color: OFFWHITE, leading: 14 });
  const iw = 400, ih = iw * 730 / 1600;
  const ix = PW - iw - 40;
  img(s, "xray_feather.png", ix, 400, iw, ih);
  T(s, ix + 10, 200, 400, "THE ROUTED MODEL — WHAT MAKES THE FACTORY-BUILT NUMBER POSSIBLE",
    { size: 6.8, bold: true, color: COPPER_LT, track: 1 });
  T(s, ix + 10, 180, 390, ["One electrical system — trays, routes and cable planned", "plant-wide, so repeatable runs can be built offsite."],
    { size: 8.5, color: OFFWHITE, leading: 13 });
  T(s, ix + 10, 148, 390, "CCGT tray & cable x-ray · conceptual — not for construction", { size: 6, color: "8C989E" });
  T(s, M, 96, 880, "REBUILD THE CASE WITH NRG SCOPE, LABOR RATES, SCHEDULE LOGIC AND ACCEPTANCE CRITERIA.",
    { size: 7.5, bold: true, color: COPPER_LT, track: 1.2 });
  T(s, M, 80, 880, "NO PRESUMPTION THAT THE ANSWER IS PREFAB — OR THAT SOUTHWIRE BELONGS IN THE SOLUTION.",
    { size: 7.5, bold: true, color: "969EA2", track: 1.2 });
  T(s, M, 24, 320, FOOT, { size: 6.5, color: "969B9E" });
  T(s, PW - M, 24, 60, "07", { size: 6.5, bold: true, color: COPPER_LT, track: 1.2, align: "right" });
}

// ---------------- 8 · owner economics
{
  const s = p.addSlide();
  lightFrame(s, "OWNER ECONOMICS", "08", true);
  T(s, M, 450, 800, ["Cable is a small cost category with", "outsized execution consequences."], { size: 25, bold: true, leading: 30 });
  T(s, M, 398, 820, ["The owner lens is how electrical decisions influence COD readiness, installed effort, capital certainty", "and lifecycle continuity — not unit price alone."],
    { size: 10, color: GRAY, leading: 14 });
  const quads = [
    ["01", "COD / REVENUE START & ENERGY DELIVERED", "Capacity visibility, delivered power, release timing and installation readiness can influence energization milestones."],
    ["02", "INSTALLED COST", "Routes, reels, cuts, pulls, congestion and rework often matter more than purchase price alone."],
    ["03", "CAPITAL CERTAINTY", "Earlier scope visibility supports commodity planning, material allocation and contingency discipline."],
    ["04", "AVAILABILITY / LIFECYCLE", "Turnover records, spares, condition screens and replacement planning support long-term continuity."],
  ];
  const colw = (PW - 2 * M - 60) / 2;
  quads.forEach((q, i) => {
    const x = M + (i % 2) * (colw + 60);
    const y = 340 - Math.floor(i / 2) * 122;
    T(s, x, y, 120, q[0], { size: 16, bold: true, color: COPPER, track: 1.5 });
    hline(s, x + 1, x + 27, y - 12, COPPER, 1.4);
    T(s, x, y - 30, colw, q[1], { size: 8.5, bold: true, track: 1 });
    T(s, x, y - 48, colw - 20, q[2], { size: 9.5, color: GRAY, leading: 13.5 });
  });
  rect(s, 0, 68, PW, 68, GRAPHITE);
  T(s, M, 40, 800, "LOW CAPEX SHARE. HIGH SCHEDULE AND COMMISSIONING LEVERAGE.", { size: 10, bold: true, color: COPPER_LT, track: 1.8 });
  bandFooter(s, "08");
}

// ---------------- 9 · plant-wide coverage
{
  const s = p.addSlide();
  lightFrame(s, "PLANT-WIDE COVERAGE", "09", true);
  T(s, M, 452, 800, ["Six clusters map a routed 3×1 electrical reference model."], { size: 25, bold: true });
  const clusters = [
    ["GRID + SITE BACKBONE", "Switchyard, GSU/grid tie and MV corridors", "HV/EHV · MV · protection/control · fiber · grounding"],
    ["GENERATION ISLAND + BOP", "HRSG, turbine hall and GT inlet", "MV/LV/VFD · I&C · F&G/ESD · CEMS · heat trace"],
    ["MODULAR + PACKAGED SYSTEMS", "BESS, reel staging, prefab/skids and modular power", "DC/MV/LV · controls · fiber · engineered sets"],
    ["HEAT REJECTION + WATER + BOP", "ACC, cooling and water/wastewater", "Repeated fan/pump power · VFD · controls · wet runs"],
    ["BUILDINGS + DISTRIBUTION + BOP", "Control building, e-house and MCC/VFD/UPS", "MV/LV/VFD · essential AC/DC · life safety · BAS/data"],
    ["OPTIONAL + AUXILIARY + BOP", "Carbon capture and gas metering", "Classified power/control · instrumentation · F&G · fiber"],
  ];
  const colw = (PW - 2 * M - 76) / 3;
  clusters.forEach((c, i) => {
    const x = M + (i % 3) * (colw + 38);
    const y = 372 - Math.floor(i / 3) * 128;
    hline(s, x + 1, x + 27, y + 14, COPPER, 1.4);
    T(s, x, y, colw - 8, c[0], { size: 8.5, bold: true, leading: 12 });
    T(s, x, y - 24, colw - 12, c[1], { size: 9, color: GRAY, leading: 12.5 });
    T(s, x, y - 58, colw - 12, c[2], { size: 7.5, color: COPPER_DP, leading: 10.5 });
  });
  rect(s, 0, 76, PW, 76, GRAPHITE);
  T(s, M, 52, 880, "CABLE CLASSES — HV/EHV · MV 5–35 kV · LV 600 V · VFD · ESSENTIAL AC/DC · I&C · FIBER/NETWORK · LIFE SAFETY · GROUNDING",
    { size: 7.5, bold: true, color: COPPER_LT, track: 1.4 });
  T(s, M, 34, 880, "Illustrative — not NRG/IFC. Excludes generator-output bus, OEM wiring and contractor methods.", { size: 7, color: MUTED });
  bandFooter(s, "09");
}

// ---------------- 10 · governance
{
  const s = p.addSlide();
  lightFrame(s, "GOVERNANCE", "10", true);
  T(s, M, 452, 800, ["Clear decision rights preserve existing project accountability."], { size: 25, bold: true });
  const rows = [
    ["NRG + UTILITY INTERFACE", "Owner priorities, portfolio standards, risk tolerances, acceptance criteria and investment decisions.", false],
    ["EPC & OE/EOR", "Design authority, calculations, specifications, routing basis and approved technical design.", false],
    ["OEM & INTEGRATORS / PACKAGERS", "Equipment-package interfaces, internal wiring, approved terminations and warranty boundaries.", false],
    ["ELECTRICAL CONTRACTOR · CHANNEL", "Installation means and methods, pull planning, workface execution, testing support and field feedback.", false],
    ["SOUTHWIRE", "Application support, material and capacity visibility, engineered cable and reel strategy, sequenced delivery and selected field support.", true],
  ];
  let y = 372;
  rows.forEach(([label, desc, hl]) => {
    if (hl) rect(s, M - 12, y + 15, PW - 2 * M + 24, 42, "F0E4D6");
    T(s, M, y, 230, label, { size: 8, bold: true, color: hl ? COPPER_DP : INK, track: 1 });
    T(s, M + 250, y, PW - M - (M + 250), desc, { size: 9.5, color: hl ? "3A3C42" : GRAY, leading: 13 });
    hline(s, M, PW - M, y - 27, HAIR, 0.6);
    y -= 48;
  });
  rect(s, 0, 76, PW, 76, GRAPHITE);
  T(s, M, 48, 880, ["Southwire connects selected decisions — it does not replace owner, EPC, OEM,", "Contractor or Channel accountability or preference."],
    { size: 11, bold: true, color: WHITE, leading: 15 });
  bandFooter(s, "10");
}

// ---------------- 11 · who we are
{
  const s = p.addSlide();
  lightFrame(s, "WHO WE ARE", "11", true);
  T(s, M, 456, 840, ["A family-held American manufacturer —", "from copper rod to finished cable since 1950."],
    { size: 23, bold: true, leading: 28 });
  T(s, M, 394, 840, ["Roy Richards founded Southwire after the poles his crews built stood wireless for months after World War II. From 12 employees",
    "and three secondhand machines in Carrollton, Georgia, Southwire remains family-held and vertically integrated."],
    { size: 9.5, color: GRAY, leading: 14 });
  hline(s, M, PW - M, 354, HAIR, 0.75);
  const stats = [["1950", "FOUNDED", INK], ["9,000+", "EMPLOYEES WORLDWIDE", INK], ["$9.7B", "2025 REVENUE · FORBES", COPPER_DP], ["12", "INDUSTRIES SERVED", INK], ["7", "COPPER MARK SITES", INK]];
  const cw = (PW - 2 * M) / 5;
  stats.forEach((st, i) => {
    const x = M + i * cw;
    T(s, x, 320, cw, st[0], { size: 24, bold: true, color: st[2] });
    T(s, x, 302, cw, st[1], { size: 6.5, bold: true, color: GRAY, track: 1.1 });
  });
  const proofs = [
    ["COPPER TECHNOLOGY", "Half of the world’s copper rod passes through a Southwire SCR® system."],
    ["U.S. POWER GRID", "We produce half of the wire and cable that moves U.S. electricity."],
    ["AMERICAN HOMES", "Half of American homes contain wiring produced by Southwire."],
  ];
  const pw3 = (PW - 2 * M - 76) / 3;
  proofs.forEach((pr, i) => {
    const x = M + i * (pw3 + 38);
    hline(s, x + 1, x + 27, 258, COPPER, 1.4);
    T(s, x, 240, pw3, pr[0], { size: 8, bold: true, color: COPPER_DP, track: 1.5 });
    T(s, x, 220, pw3 - 12, pr[1], { size: 9.5, color: GRAY, leading: 13.5 });
  });
  const sh = PW * 441 / 3840;
  img(s, "wide_yard.png", 0, 34 + sh, PW, sh);
  T(s, M, 14, 320, FOOT, { size: 6.5, color: GRAY_LT });
  T(s, PW - M, 14, 60, "11", { size: 6.5, bold: true, color: COPPER, track: 1.2, align: "right" });
}

// ---------------- 12 · the ask
{
  const s = p.addSlide();
  s.background = { color: GRAPHITE };
  const sw = PH * 548 / 2640;
  img(s, "hex_side_fade.png", 0, PH, sw, PH);
  s.addShape("line", { x: X(sw + 4), y: 0, w: 0, h: 7.5, line: { color: COPPER, width: 1.4 } });
  const lw = 150, lh = lw * 202 / 943;
  img(s, "lockup_dark_keyed.png", PW - M - lw, 502, lw, lh);
  const x0 = sw + 52;
  T(s, x0, 452, 300, "THE ASK", { size: 7.5, bold: true, color: COPPER_LT, track: 1.6 });
  T(s, x0, 416, 700, "ONE SITE WALK.  ONE HOUR.", { size: 27, bold: true, color: WHITE });
  T(s, x0, 382, 700, "NO SALES PRESENTATION.", { size: 27, bold: true, color: WHITE });
  hline(s, x0, x0 + 64, 360, COPPER, 1.2);
  T(s, x0, 336, 700, ["NRG selects the starting scope — one live package, conversion/uprate screen or planned-outage", "replacement — and brings the people closest to execution."],
    { size: 10, color: OFFWHITE, leading: 14 });
  const walk = ["SELECT SCOPE", "WALK THE WORK", "MAP THE RISK", "DECIDE"];
  const wx0 = x0 + 20, wx1 = PW - M - 30, wy = 274;
  hline(s, wx0, wx1, wy, COPPER, 0.9);
  walk.forEach((w, i) => {
    const x = wx0 + i * (wx1 - wx0) / 3;
    dot(s, x, wy, 10, i === 3 ? COPPER_DP : STEEL);
    T(s, x, wy - 3, 40, String(i + 1), { size: 8.5, bold: true, color: WHITE, align: "center" });
    T(s, x, wy - 24, 150, w, { size: 6.8, bold: true, color: OFFWHITE, track: 1, align: "center" });
  });
  const rows = [
    ["INPUT", "One live scope"],
    ["OUTPUT", "Written execution-risk read-back — milestone exposure, route, reel + release constraints"],
    ["DECISION", "Stop, standardize or define a bounded pilot"],
  ];
  let ry = 212;
  rows.forEach(([label, val]) => {
    T(s, x0, ry, 100, label, { size: 8, bold: true, color: COPPER_LT, track: 1.6 });
    T(s, x0 + 104, ry - 1, PW - M - (x0 + 104), val, { size: 10.5, bold: true, color: WHITE });
    hline(s, x0, PW - M, ry - 13, HAIR_DK, 0.6);
    ry -= 42;
  });
  T(s, x0, 74, 700, "NO PRICING EXERCISE. NO BROAD COMMERCIAL COMMITMENT.", { size: 9, bold: true, color: COPPER_LT, track: 1.6 });
  T(s, x0, 46, 700, "Stephan Hardt   |   Director, Power Generation Solutions", { size: 8.5, bold: true, color: WHITE });
  T(s, x0, 30, 700, "stephan.hardt@southwire.com   |   +1 470-439-8488", { size: 8.5, color: "A8A6A2" });
  T(s, PW - M, 30, 60, "12", { size: 6.5, bold: true, color: COPPER_LT, track: 1.2, align: "right" });
}

p.author = "Stephan Hardt";
p.title = "Accelerating Time to Power — NRG | Southwire Power Generation Solutions";
p.subject = "SWR-PG-BROCHURE-NRG Rev 01";
p.writeFile({ fileName: "Southwire_PowerGen_Brochure_NRG_Rev01.pptx" }).then(() => console.log("written 16:9"));
