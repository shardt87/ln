"""One-page memo: links to Anthropic's terms and policies (clickable). From Stephan Hardt to Southwire Legal."""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

DJ = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", DJ + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", DJ + "DejaVuSans-Bold.ttf"))
NAVY, GREY, LINK = colors.HexColor("#1f2d3d"), colors.HexColor("#62686e"), "#1a5fb4"
T = ParagraphStyle("t", fontName="DVB", fontSize=17, leading=22, textColor=NAVY, spaceAfter=4)
M = ParagraphStyle("m", fontName="DV", fontSize=9.5, leading=14, textColor=GREY)
B = ParagraphStyle("b", fontName="DV", fontSize=10.5, leading=15, spaceAfter=8)
L = ParagraphStyle("l", fontName="DV", fontSize=10.5, leading=14)
LB = ParagraphStyle("lb", fontName="DVB", fontSize=10.5, leading=14, textColor=NAVY)
DOCS = [
    ("Consumer Terms of Service", "Personal Claude accounts (Free, Pro, Max)", "https://www.anthropic.com/legal/consumer-terms"),
    ("Commercial Terms of Service", "Company Team / Enterprise plans and the API", "https://www.anthropic.com/legal/commercial-terms"),
    ("Usage Policy", "All users", "https://www.anthropic.com/legal/aup"),
    ("Privacy Policy", "All users", "https://www.anthropic.com/legal/privacy"),
    ("All Anthropic legal documents", "Index", "https://www.anthropic.com/legal"),
]
link = lambda u: f'<link href="{u}" color="{LINK}"><u>{u}</u></link>'
story = [Paragraph("Memo: Claude (Anthropic) terms and policies", T),
         Paragraph("To: Southwire Legal &nbsp;&nbsp;·&nbsp;&nbsp; From: Stephan Hardt, Power Generation Solutions"
                   " &nbsp;&nbsp;·&nbsp;&nbsp; Date: October 16, 2026", M), Spacer(1, 14),
         Paragraph("As discussed, here are the links to Anthropic's terms and policies for Claude, the AI tool I used for "
                   "the 3D plant model and training materials. Each link opens the current official version on "
                   "anthropic.com.", B), Spacer(1, 4)]
rows = []
for name, scope, url in DOCS:
    rows.append([Paragraph(f'<link href="{url}">{name}</link>', LB), Paragraph(scope, L)])
    rows.append([Paragraph(link(url), L), ""])
t = Table(rows, colWidths=[3.6 * inch, 3.2 * inch])
st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 1), (-1, 1), .4, colors.HexColor("#d5d8db"))]
for i in range(len(DOCS)):
    st += [("SPAN", (0, 2 * i + 1), (1, 2 * i + 1)), ("BOTTOMPADDING", (0, 2 * i + 1), (-1, 2 * i + 1), 10),
           ("LINEBELOW", (0, 2 * i + 1), (-1, 2 * i + 1), .4, colors.HexColor("#d5d8db"))]
t.setStyle(TableStyle(st))
story += [t, Spacer(1, 14),
          Paragraph("I used a personal Claude account, so the Consumer Terms apply to what I created; ownership of "
                    "outputs is covered in Section 4 (“Inputs, Outputs, Actions, and Materials”).", B),
          Paragraph("Happy to walk through what I built whenever useful.", B)]
out = "/home/user/ln/plant/legal/Claude_Terms_Links_Memo.pdf"
SimpleDocTemplate(out, pagesize=letter, leftMargin=.85 * inch, rightMargin=.85 * inch, topMargin=.8 * inch,
                  bottomMargin=.8 * inch, title="Memo: Claude (Anthropic) terms and policies", author="Stephan Hardt").build(story)
print(out)
