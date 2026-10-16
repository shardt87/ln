import re, html
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

DJ = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", DJ + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", DJ + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", DJ + "DejaVuSans.ttf"))       # (no oblique face installed)
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")
NAVY = colors.HexColor("#1f2d3d"); GREY = colors.HexColor("#62686e"); COP = colors.HexColor("#a65428")
S = dict(
    title=ParagraphStyle("t", fontName="DVB", fontSize=20, leading=25, textColor=NAVY, spaceAfter=6),
    sub=ParagraphStyle("s", fontName="DV", fontSize=11, leading=15, textColor=GREY, spaceAfter=14),
    h1=ParagraphStyle("h1", fontName="DVB", fontSize=14, leading=18, textColor=NAVY, spaceBefore=10, spaceAfter=6),
    h2=ParagraphStyle("h2", fontName="DVB", fontSize=10.5, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=3),
    h3=ParagraphStyle("h3", fontName="DVB", fontSize=9.5, leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=2),
    body=ParagraphStyle("b", fontName="DV", fontSize=9.5, leading=13.5, spaceAfter=5),
    small=ParagraphStyle("sm", fontName="DV", fontSize=8, leading=11, textColor=GREY, spaceAfter=4),
    quote=ParagraphStyle("q", fontName="DVI", fontSize=9.5, leading=13.5, leftIndent=14, textColor=colors.HexColor("#2d343b"), spaceAfter=5),
    tb=ParagraphStyle("tb", fontName="DV", fontSize=8, leading=10.5),
    tbb=ParagraphStyle("tbb", fontName="DVB", fontSize=8, leading=10.5, textColor=colors.white),
)
E = lambda s: html.escape(s, quote=False)
DOCS = [("A", "Consumer Terms of Service", "consumer-terms"), ("B", "Commercial Terms of Service", "commercial-terms"),
        ("C", "Usage Policy (Acceptable Use Policy)", "aup"), ("D", "Privacy Policy", "privacy")]
RETRIEVED = "October 16, 2026"


def bullets(items, style="body"):
    return ListFlowable([ListItem(Paragraph(i, S[style]), leftIndent=12, bulletColor=NAVY) for i in items],
                        bulletType="bullet", start="•", leftIndent=12, bulletFontName="DV")


def memo():
    f = []
    f += [Paragraph("Claude (Anthropic) terms: ownership of the SK-3X1 3D model and materials", S["title"]),
          Paragraph(f"Prepared for Southwire Legal · Stephan Hardt, Power Generation Solutions · {RETRIEVED}", S["sub"])]
    f += [Paragraph("Purpose", S["h1"]), Paragraph(
        "I used Anthropic's AI tool Claude (with Claude Code) to build the SK-3X1 3D gas power campus model, the web "
        "viewer, renders, the guided tour and slides for the November 11, 2026 internal training. This packet gives the "
        "terms that apply, the ownership clauses, what was created and what it contains, and the questions for your "
        "review. The full current text of each Anthropic document follows as Appendices A to D.", S["body"])]
    f += [Paragraph("Which terms apply", S["h1"]), Paragraph(
        "The work was done on a <b>personal Claude account</b> (not a company plan), so Anthropic's <b>Consumer Terms</b> "
        "apply. Company plans (Team, Enterprise, API) fall under the <b>Commercial Terms</b>, included for comparison.", S["body"])]
    rows = [[Paragraph(x, S["tbb"]) for x in ("Document", "Applies to", "Effective", "Source")],
            [Paragraph("Consumer Terms (App. A)", S["tb"]), Paragraph("Personal Free / Pro / Max accounts (Claude.ai, apps, Claude Code with that login)", S["tb"]),
             Paragraph("Oct 8, 2025", S["tb"]), Paragraph("anthropic.com/legal/consumer-terms", S["tb"])],
            [Paragraph("Commercial Terms (App. B)", S["tb"]), Paragraph("Company Team / Enterprise plans and the API", S["tb"]),
             Paragraph("Jun 17, 2025", S["tb"]), Paragraph("anthropic.com/legal/commercial-terms", S["tb"])],
            [Paragraph("Usage Policy (App. C)", S["tb"]), Paragraph("All users", S["tb"]), Paragraph("see text", S["tb"]),
             Paragraph("anthropic.com/legal/aup", S["tb"])],
            [Paragraph("Privacy Policy (App. D)", S["tb"]), Paragraph("All users", S["tb"]), Paragraph("see text", S["tb"]),
             Paragraph("anthropic.com/legal/privacy", S["tb"])]]
    t = Table(rows, colWidths=[1.45 * inch, 2.6 * inch, 0.85 * inch, 2.1 * inch])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#c9cdd1")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f5")])]))
    f += [t, Spacer(1, 8)]
    f += [Paragraph("Ownership: Consumer Terms, Section 4 (“Inputs, Outputs, Actions, and Materials”)", S["h1"]),
          Paragraph("Inputs:", S["h3"]), Paragraph("“you retain any right, title, and interest that you have in the Inputs you submit.”", S["quote"]),
          Paragraph("Outputs:", S["h3"]), Paragraph("“Subject to your compliance with our Terms, we assign to you all of our right, title, and interest—if any—in Outputs.”", S["quote"])]
    f += [Paragraph("Points to note in the Consumer Terms", S["h2"]), bullets([
        "Rights are assigned to the account holder (me personally), “if any”, subject to compliance. Whether they pass to "
        "Southwire is a question for my employment terms and Southwire policy.",
        "Section 3 bars using the services to develop competing products or services, or to resell the services.",
        "Section 4: outputs should not be relied on without independent checking. The model is labelled "
        "“conceptual illustration, not engineered, not for construction”.",
        "Preamble: the Commercial Terms do not cover Claude.ai or Claude Pro use for individuals."])]
    f += [Paragraph("For comparison: Commercial Terms (company plans)", S["h1"]),
          Paragraph("Section B, “Customer Content”:", S["h3"]),
          Paragraph("“Customer (a) retains all rights to its Inputs, and (b) owns its Outputs.”", S["quote"]),
          Paragraph("“Anthropic may not train models on Customer Content from Services.”", S["quote"]),
          Paragraph("Section K, “Indemnification”:", S["h3"]),
          Paragraph("K.1: Anthropic will defend the customer against claims that authorised paid use, or “Outputs generated "
                    "through such authorized use”, infringe a third-party intellectual property right. K.3 lists exclusions "
                    "(for example customer modifications, combinations with non-Anthropic technology, customer-provided Inputs, "
                    "and uses the customer knows or should know infringe).", S["body"])]
    f += [Paragraph("What was created and what it contains", S["h1"]), bullets([
        "<b>Generated with Claude:</b> Python build scripts, the 3D model data, the web viewer, the cable schedule and BOM "
        "workbook, render and slide scripts, and documentation, kept in a private GitHub repository.",
        "<b>Rendered by me</b> from those scripts with open-source tools: images, the tour video, slides.",
        "<b>Open-source components:</b> three.js (MIT licence) in the viewer; Blender (GPL; rendered images are the user's "
        "own) for renders; Barlow and DejaVu fonts (open font licences); Playwright and ffmpeg for recording.",
        "<b>Company and third-party content I supplied as input:</b> Southwire product names and logo (Southwire "
        "trademarks); extracts from the Wesco channel-partner deck; the SK-3X1 concept drawing set the model is based on."])]
    f += [Paragraph("Questions for Legal", S["h1"]), ListFlowable([ListItem(Paragraph(q, S["body"]), leftIndent=14) for q in [
        "Are the Consumer Terms acceptable for internal training use and for customer-facing marketing of this material?",
        "Should future work move to a Southwire Claude Team or Enterprise plan under the Commercial Terms (company "
        "ownership of outputs, no training on our content, IP indemnity)?",
        "Is anything needed regarding the Wesco deck content and the origin of the drawing set before any external use?"]],
        bulletType="1", leftIndent=14, bulletFontName="DV")]
    f += [Spacer(1, 8), Paragraph(
        f"The clauses above are quoted from the pages as published on {RETRIEVED}. Appendices A to D reproduce the page "
        "text as retrieved that day (layout simplified); the versions on anthropic.com govern. This summary is not legal "
        "advice.", S["small"])]
    return f


def appendix(letter_, title, slug):
    s = BeautifulSoup(open(slug + ".html", encoding="utf-8").read(), "html.parser")
    main = s.find("main") or s.body
    for t in main(["script", "style", "nav", "footer", "svg", "button", "form"]):
        t.decompose()
    f = [Paragraph(f"Appendix {letter_}: Anthropic {title}", S["title"]),
         Paragraph(f"Source: https://www.anthropic.com/legal/{slug} · retrieved {RETRIEVED} · layout simplified; the "
                   "published version governs.", S["sub"])]
    seen = set()
    for el in main.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
        if el.find_parent("li") is not None and el.name == "p":
            continue                                         # list items carry their paragraphs
        if el.name in ("p", "li") and el.find(["p", "li"]) is not None and el.name == "p":
            continue
        txt = re.sub(r"\s+", " ", el.get_text(" ")).strip()
        txt = re.sub(r"\s+([,.;:)”’])", r"\1", txt).replace("“ ", "“").replace("( ", "(")
        if not txt or txt in ("Download PDF version",) or (txt in seen and len(txt) < 40):
            continue
        seen.add(txt)
        if el.name in ("h1", "h2"):
            f.append(Paragraph(E(txt), S["h2"]))
        elif el.name in ("h3", "h4"):
            f.append(Paragraph(E(txt), S["h3"]))
        elif el.name == "li":
            f.append(Paragraph("• " + E(txt), ParagraphStyle("li", parent=S["body"], leftIndent=12, firstLineIndent=-8)))
        else:
            f.append(Paragraph(E(txt), S["body"]))
    return f


def footer(c, d):
    c.saveState()
    c.setFont("DV", 7.5)
    c.setFillColor(GREY)
    c.drawString(0.75 * inch, 0.5 * inch, "Claude (Anthropic) terms – SK-3X1 materials · for Southwire Legal review")
    c.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f"Page {d.page}")
    c.restoreState()


story = memo()
for L, T, slug in DOCS:
    story += [PageBreak()] + appendix(L, T, slug)
doc = SimpleDocTemplate(OUT := "/home/user/ln/plant/legal/Claude_Terms_SK-3X1_for_Legal_Review.pdf", pagesize=letter,
                        leftMargin=.75 * inch, rightMargin=.75 * inch, topMargin=.7 * inch, bottomMargin=.75 * inch,
                        title="Claude (Anthropic) terms – SK-3X1 materials", author="Stephan Hardt")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
