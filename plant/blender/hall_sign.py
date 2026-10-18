"""The turbine-hall end-wall graphic (plant/screens/hall_wall_sign.png), printed on the east wall by hall_finish.py:
'3x1 CCGT' in Southwire black, a copper rule, and 'WIRE & CABLE PARTNER' with the Southwire Power Generation
Solutions logo as wide as the rule (white wordmark recoloured black for the light wall). Transparent background.

    python blender/hall_sign.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "screens", "hall_wall_sign.png")
INK, COPPER = (28, 29, 31, 255), (184, 115, 51, 255)
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
    small = ImageFont.truetype(os.path.join(HERE, "deck", "BarlowCondensed-Bold.ttf"), 120)
    tracked(d, W / 2, 680, "WIRE & CABLE PARTNER", small, INK, 22)
    logo = Image.open(os.path.join(HERE, "deck", "southwire_pgs_logo.png")).convert("RGBA")
    px = logo.load()
    for j in range(logo.height):                                                    # white wordmark -> Southwire black
        for i in range(logo.width):
            r, g, b, a = px[i, j]
            if a and min(r, g, b) > 200:
                px[i, j] = INK[:3] + (a,)
    lw = 2600                                                                       # the logo as wide as the rule
    lh = int(logo.height * lw / logo.width)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    img.alpha_composite(logo, (int(W / 2 - lw / 2), 790))
    img.save(OUT)
    print(OUT, img.size)


if __name__ == "__main__":
    main()
