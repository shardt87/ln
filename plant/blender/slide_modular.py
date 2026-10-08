"""'Modular power' slide (16:9, PNG + PDF) on the E80 plate, in the layout of the user's slide: title and
subtitle, photo with numbered markers, three numbered items on the right, footer.

    python blender/slide_modular.py [renders/epic/E80_pro.png]
Markers are projected from the model by the Blender build (E80 callouts in E80_pro.labels.json)."""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
DJ = "/usr/share/fonts/truetype/dejavu/"
S = 2                                       # px per design px (output 4000 x 2250)
W, H = 2000 * S, 1125 * S
NAVY, GREY, COPPER, BG, RULE = (31, 45, 61), (98, 104, 110), (166, 84, 40), (247, 247, 245), (214, 214, 210)
ITEMS = [
    ("01", "Generation packages", ["Eight 18-cylinder gas engines (RICE)", "in one hall with SCR stacks, plus two",
                                   "LM6000-class simple-cycle units."]),
    ("02", "Generator sets", ["Two black-start gensets with their", "switchgear; eight containerized and",
                              "trailer gensets on the portable pad."]),
    ("03", "Fuel-cell power", ["Twelve solid-oxide fuel-cell modules", "and six 1 MW microturbines, inverters",
                               "and the 480 V : 13.8 kV step-up."]),
]


def f(name, px):
    return ImageFont.truetype(DJ + name, int(px * S))


def main(src):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((73 * S, 42 * S), "MODULAR POWER", font=f("DejaVuSans-Bold.ttf", 40), fill=NAVY)
    d.text((74 * S, 102 * S), "Generation packages, generator sets, and fuel-cell power.",
           font=f("DejaVuSans.ttf", 20), fill=GREY)
    # photo
    px0, py0, pw, ph = 37 * S, 177 * S, 1411 * S, 794 * S
    ph_img = Image.open(src).convert("RGB")
    sw, sh = ph_img.size
    sc = max(pw / sw, ph / sh)
    ph_img = ph_img.resize((round(sw * sc), round(sh * sc)), Image.LANCZOS)
    ox, oy = (ph_img.size[0] - pw) // 2, (ph_img.size[1] - ph) // 2
    img.paste(ph_img.crop((ox, oy, ox + pw, oy + ph)), (px0, py0))
    # markers
    lab = json.load(open(os.path.splitext(src)[0] + ".labels.json"))
    k = sc
    for c in lab.get("callouts", []):
        x = px0 + c["x"] * (ph_img.size[0] / lab["rw"]) - ox
        y = py0 + c["y"] * (ph_img.size[1] / lab["rh"]) - oy
        r = 29 * S
        y -= r * 1.25                                   # marker floats above the unit, with a short leader
        d.line([(x, y + r), (x, y + r * 1.25)], fill="white", width=3 * S)
        sh_ = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh_).ellipse([x - r, y - r + 3 * S, x + r, y + r + 3 * S], fill=90)
        img.paste((0, 0, 0), mask=sh_.filter(ImageFilter.GaussianBlur(4 * S)))
        d.ellipse([x - r, y - r, x + r, y + r], fill="white")
        d.ellipse([x - r + 4 * S, y - r + 4 * S, x + r - 4 * S, y + r - 4 * S], fill=COPPER)
        t = c["num"]
        ft = f("DejaVuSans-Bold.ttf", 30)
        tw = d.textlength(t, font=ft)
        d.text((x - tw / 2, y - 19 * S), t, font=ft, fill="white")
    # right column
    y = 318
    for num, head, body in ITEMS:
        d.text((1521 * S, y * S), num, font=f("DejaVuSans-Bold.ttf", 21), fill=COPPER)
        d.text((1521 * S, (y + 40) * S), head, font=f("DejaVuSans-Bold.ttf", 27), fill=NAVY)
        for i, line in enumerate(body):
            d.text((1521 * S, (y + 86 + i * 31) * S), line, font=f("DejaVuSans.ttf", 19.5), fill=GREY)
        y += 245
    d.line([(73 * S, 1015 * S), (1921 * S, 1015 * S)], fill=RULE, width=S)
    d.text((73 * S, 1036 * S), "Rendered from the SK-3X1 3D model (modular yard, north block). Surrounding plant omitted "
           "for clarity. Conceptual illustration: not engineered.", font=f("DejaVuSans.ttf", 17), fill=GREY)
    d.text((73 * S, 1069 * S), "© 2026 Southwire Company, LLC. All rights reserved.", font=f("DejaVuSans.ttf", 15),
           fill=GREY)
    out = os.path.join(PLANT, "renders", "deck", "SK-3X1_modular_power")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out + ".png")
    img.save(out + ".pdf", resolution=144 * S / 2)
    print("wrote", out + ".png")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(PLANT, "renders", "epic", "E80_pro.png"))
