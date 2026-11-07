"""The 15-slide share version of the Nov 11 training deck (owner, Oct 26): slides that read without a presenter,
numbered 1/15 to 15/15. Writes the PDF, slide JPGs, a lineup sheet and a PowerPoint with the run-of-show notes of each
slide's source slide. Rebuild after deck_training.py."""
import os
import subprocess

import brochure_zones as bz
import deck_boilers as db
import deck_training as dt
import deck_training_candidates as cand

OUT = os.path.join(dt.PLANT, "renders", "deck", "share15")
N = 15
# (slide in the 70-slide training deck, builder): the source number picks the speaker notes
PLAN = [(1, lambda n: dt.s_title()), (4, lambda n: dt.s_why_built(n, N)), (6, lambda n: dt.s_story2(n, N)),
        (20, lambda n: dt.s_glance(n, N)), (25, lambda n: dt.s_map(n, N)), (33, lambda n: cand.c_cc4(n, N)),
        (34, lambda n: cand.c_xray_copper(n, N)), (35, lambda n: cand.c_xray(n, N)), (36, lambda n: cand.c_xray_campus(n, N)),
        (12, lambda n: dt.s_oneline(n, N)), (38, lambda n: dt.reused(db.slide_system, n, N, "Fundamentals &nbsp;&middot;&nbsp; the voltage ladder")),
        (44, lambda n: dt.s_buckets(n, N)), (48, lambda n: dt.s_overview(n, N)), (58, lambda n: dt.s_offer(n, N)),
        (62, lambda n: dt.s_resources(n, N))]


def main():
    import pymupdf
    from PIL import Image, ImageDraw, ImageFont
    import deck_training_pptx as dp
    os.makedirs(os.path.join(OUT, "jpg"), exist_ok=True)
    cand.FOOT_LEFT = "SW-3X1 MODEL &middot; CONCEPTUAL ILLUSTRATION, NOT ENGINEERED &middot; INTERNAL TRAINING"
    head = f"<!doctype html><html><head><meta charset='utf-8'><style>{db.CSS}</style></head><body>"
    out = pymupdf.open()
    for i, (_, f) in enumerate(PLAN):
        sec = f(i + 1).replace('<section class="page slide">', '<section class="page slide"><div class="s">', 1).replace("</section>", "</div></section>")
        hp = os.path.join(OUT, f"_s{i}.html")
        open(hp, "w").write(head + sec + "</body></html>")
        pdf = hp.replace(".html", ".pdf")
        subprocess.run([bz.CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                        "--no-pdf-header-footer", f"--print-to-pdf={pdf}", bz.url(hp)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out.insert_pdf(pymupdf.open(pdf))
        os.remove(pdf)
        os.remove(hp)
    p = os.path.join(OUT, "SW-3X1_Inside_Power_Generation_15.pdf")
    out.save(p, garbage=4, deflate=True)
    ims = []
    for i, pg in enumerate(out):
        pix = pg.get_pixmap(matrix=pymupdf.Matrix(1920 / pg.rect.width, 1920 / pg.rect.width))
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        im.save(os.path.join(OUT, "jpg", f"slide_{i + 1:02d}.jpg"), quality=88)
        ims.append(im)
    w, h, g = 640, 360, 14
    sheet = Image.new("RGB", (3 * w + 4 * g, 5 * (h + g) + g), (30, 30, 30))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    except OSError:
        font = ImageFont.load_default()
    for k, im in enumerate(ims):
        x, y = g + (k % 3) * (w + g), g + (k // 3) * (h + g)
        sheet.paste(im.resize((w, h)), (x, y))
        d.rectangle([x, y, x + 56, y + 38], fill=(180, 89, 31))
        d.text((x + 8, y + 5), str(k + 1), font=font, fill="white")
    sheet.save(os.path.join(OUT, "jpg", "lineup_15.jpg"), quality=86)
    notes = dp.notes_by_slide()
    dp.build(p, os.path.join(OUT, "SW-3X1_Inside_Power_Generation_15.pptx"), {i + 1: notes.get(src, "") for i, (src, _) in enumerate(PLAN)})
    print("wrote", p, len(out), "slides")


if __name__ == "__main__":
    main()
