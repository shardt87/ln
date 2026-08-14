#!/usr/bin/env python3
"""Rasterize brochure pages for visual QA + proof sheet + text gates."""
import re
import subprocess
import sys
import pypdfium2 as pdfium
from PIL import Image

PDF = 'Southwire_PowerGen_Brochure_NRG_Rev01.pdf'

# 150 dpi rasters
pdf = pdfium.PdfDocument(PDF)
files = []
for i, page in enumerate(pdf):
    img = page.render(scale=150/72).to_pil()
    f = f'qa/pg{i+1}.png'
    img.save(f)
    files.append(f)
print('rasterized', len(files), 'pages at 150dpi', img.size)

# proof sheet grid
imgs = [Image.open(f) for f in files]
w, h = imgs[0].size
sw, sh = w // 2, h // 2
cols = 3 if len(imgs) > 8 else 4
rows = (len(imgs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * sw + (cols + 1) * 12, rows * sh + (rows + 1) * 12), (220, 218, 214))
for i, im in enumerate(imgs):
    x = 12 + (i % cols) * (sw + 12)
    y = 12 + (i // cols) * (sh + 12)
    sheet.paste(im.resize((sw, sh), Image.LANCZOS), (x, y))
sheet.save('proof_sheet.png')
print('proof_sheet.png', sheet.size)

# text gates — pdfplumber groups words correctly across columns
import pdfplumber
pages_text = []
with pdfplumber.open(PDF) as plumb:
    for pg in plumb.pages:
        ws = [w['text'] for w in pg.extract_words()]
        pages_text.append(' '.join(ws))
txt = '\n'.join(pages_text)
words = sum(len(p.split()) for p in pages_text)
print('WORD COUNT:', words, '(informational)')
txt2 = subprocess.run(['pdftotext', PDF, '-'], capture_output=True, text=True).stdout
banned = ['13 B', '13B', '$13', '4,400', '880', '334', '418', '83.6', '33.4M',
          '3x1x1', '3×1x1', 'Cyle', 'ISLAN', 'Cedar Bayou', 'Bloom', 'Fuel Cell', 'Caller']
fails = [b for b in banned if b in txt or b in txt2.replace(' ', '')]
print('BANNED STRINGS FOUND:', fails if fails else 'none')
credit = sum(1 for pg in pages_text if 'Stephan Hardt' in pg)
print('PAGES WITH CREDIT:', credit, '/ 9')
sys.exit(1 if fails else 0)
