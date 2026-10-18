"""The turbine-hall end-wall graphic (plant/screens/hall_wall_sign.png), printed on the east wall by hall_finish.py:
'3x1 CCGT' in Southwire black, a copper rule, and 'WIRE & CABLE PARTNER' with the Southwire Power Generation
Solutions logo (white wordmark recoloured black for the light wall). Transparent background.

    python blender/hall_sign.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "screens", "hall_wall_sign.png")
INK, COPPER = (28, 29, 31, 255), (184, 115, 51, 255)
W, H = 2900, 1200                                        # 58 x 24 ft at 50 px / ft


def main():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(os.path.join(HERE, "deck", "BarlowCondensed-ExtraBold.ttf"), 560)
    d.text((W / 2, 300), "3x1 CCGT", font=big, fill=INK, anchor="mm")
    d.rectangle([W / 2 - 1150, 640, W / 2 + 1150, 668], fill=COPPER)              # copper rule
    small = ImageFont.truetype(os.path.join(HERE, "deck", "BarlowCondensed-Bold.ttf"), 120)
    label = "WIRE & CABLE PARTNER"
    x = W / 2 - 1150
    for ch in label:                                                                 # tracked caps
        d.text((x, 860), ch, font=small, fill=INK, anchor="lm")
        x += d.textlength(ch, font=small) + 14
    logo = Image.open(os.path.join(HERE, "deck", "southwire_pgs_logo.png")).convert("RGBA")
    px = logo.load()
    for j in range(logo.height):                                                    # white wordmark -> Southwire black
        for i in range(logo.width):
            r, g, b, a = px[i, j]
            if a and min(r, g, b) > 200:
                px[i, j] = INK[:3] + (a,)
    lw = int(W / 2 + 1150 - (x + 80))
    lh = int(logo.height * lw / logo.width)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    img.alpha_composite(logo, (int(x + 80), int(860 - lh / 2)))
    img.save(OUT)
    print(OUT, img.size)


if __name__ == "__main__":
    main()
