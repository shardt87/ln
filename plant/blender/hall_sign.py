"""The turbine-hall end-wall graphic (plant/screens/hall_wall_sign.png), printed on the east wall by hall_finish.py:
'3x1 CCGT' in Southwire black, a copper rule, and 'WIRE & CABLE PARTNER' with the Southwire Power Generation
Solutions logo as wide as the rule (white wordmark recoloured black for the light wall). Transparent background.

    python blender/hall_sign.py
"""
import os

from PIL import ImageFilter, Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "screens", "hall_wall_sign.png")
INK, COPPER = (17, 18, 20, 255), (166, 90, 44, 255)       # solid Southwire black, deep burnished copper
W, H = 3000, 1500                                        # 60 x 30 ft at 50 px / ft


def tracked(d, cx, y, text, font, fill, gap):
    w = sum(d.textlength(ch, font=font) + gap for ch in text) - gap
    x = cx - w / 2
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill, anchor="lm")
        x += d.textlength(ch, font=font) + gap


def main():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(os.path.join(HERE, "deck", "BarlowCondensed-ExtraBold.ttf"), 470)
    d.text((W / 2, 250), "3x1 CCGT", font=big, fill=INK, anchor="mm")
    d.rectangle([W / 2 - 1300, 540, W / 2 + 1300, 568], fill=COPPER)              # copper rule
    small = ImageFont.truetype(os.path.join(HERE, "deck", "BarlowCondensed-ExtraBold.ttf"), 165)
    tracked(d, W / 2, 690, "WIRE & CABLE PARTNER", small, INK, 26)
    logo = Image.open(os.path.join(HERE, "deck", "southwire_pgs_logo.png")).convert("RGBA")
    lw = 2600                                                                       # the logo as wide as the rule
    lh = int(logo.height * lw / logo.width)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    px = logo.load()
    for j in range(lh):                   # solid print: white wordmark -> black, copper mark -> one deep copper,
        for i in range(lw):               # edges fully opaque (no washed-out half-transparent pixels)
            r, g, b, a = px[i, j]
            if a < 110:
                px[i, j] = (0, 0, 0, 0)
            elif min(r, g, b) > 150:
                px[i, j] = INK
            else:
                px[i, j] = COPPER
    logo = logo.filter(ImageFilter.ModeFilter(5))                                   # clear stray specks
    img.alpha_composite(logo, (int(W / 2 - lw / 2), 820))
    img.save(OUT)
    print(OUT, img.size)
    # the west gable outside carries the lettering alone, in the same face (92 x 22 ft, 50 px / ft)
    w = Image.new("RGBA", (4600, 1100), (0, 0, 0, 0))
    ImageDraw.Draw(w).text((2300, 550), "3x1 CCGT", font=ImageFont.truetype(os.path.join(HERE, "deck", "BarlowCondensed-ExtraBold.ttf"), 1000),
                           fill=INK, anchor="mm")
    p = os.path.join(os.path.dirname(OUT), "hall_west_lettering.png")
    w.save(p)
    print(p, w.size)
    # painted unit letters over the gallery doors (GT1 / GT2 / GT3 / ST1), the WIRE & CABLE PARTNER face, cropped tight
    f = ImageFont.truetype(os.path.join(HERE, "deck", "BarlowCondensed-ExtraBold.ttf"), 800)
    for t in ("GT1", "GT2", "GT3", "ST1"):
        im = Image.new("RGBA", (3000, 1200), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((1500, 600), t, font=f, fill=INK, anchor="mm")
        im = im.crop(im.getbbox())
        p = os.path.join(os.path.dirname(OUT), f"door_{t}.png")
        im.save(p)
        print(p, im.size)


if __name__ == "__main__":
    main()
