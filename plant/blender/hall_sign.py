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
WHITE = (244, 244, 241, 255)
FIELD, CHEV = (24, 25, 27, 255), (166, 90, 48, 255)       # the van livery: Southwire black field, chevrons in the band's
                                                          # copper (#a65a30; owner, Oct 20), printed with its metallic finish
W, H = 3000, 1500                                        # 60 x 30 ft at 50 px / ft


def tracked(d, cx, y, text, font, fill, gap):
    w = sum(d.textlength(ch, font=font) + gap for ch in text) - gap
    x = cx - w / 2
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill, anchor="lm")
        x += d.textlength(ch, font=font) + gap


def draw_sign(ink, out):
    """The sign in ink (black on the light wall, or white on the Southwire-black livery field)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(os.path.join(HERE, "deck", "BarlowCondensed-ExtraBold.ttf"), 470)
    d.text((W / 2, 250), "3x1 CCGT", font=big, fill=ink, anchor="mm")
    d.rectangle([W / 2 - 1300, 540, W / 2 + 1300, 568], fill=COPPER)              # copper rule
    small = ImageFont.truetype(os.path.join(HERE, "deck", "BarlowCondensed-ExtraBold.ttf"), 165)
    tracked(d, W / 2, 690, "WIRE & CABLE PARTNER", small, ink, 26)
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
                px[i, j] = ink
            else:
                px[i, j] = COPPER
    logo = logo.filter(ImageFilter.ModeFilter(5))                                   # clear stray specks
    img.alpha_composite(logo, (int(W / 2 - lw / 2), 820))
    img.save(out)
    print(out, img.size)


def livery(out, W_ft, H_ft, chevrons, s, u_black, ppf=40, notch=True):
    """The field-service van livery fitted to a wall: copper chevrons pointing right on the light wall and a
    Southwire-black field from u_black to the right edge, its leading edge notched like the van's (in ft from the
    image's left edge; s = how far the points run at mid-height). Transparent elsewhere: the wall shows through."""
    Wp, Hp = int(W_ft * ppf), int(H_ft * ppf)
    im = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    P = lambda u, v: (u * ppf, v * ppf)
    if u_black >= W_ft:                                  # chevrons only
        pass
    elif notch:
        d.polygon([P(u_black, 0), P(W_ft, 0), P(W_ft, H_ft), P(u_black, H_ft), P(u_black + s, H_ft / 2)], fill=FIELD)
    else:                                                # a plain rectangle
        d.rectangle([P(u_black, 0), P(W_ft, H_ft)], fill=FIELD)
    for (u, w) in chevrons:
        d.polygon([P(u, 0), P(u + w, 0), P(u + w + s, H_ft / 2), P(u + w, H_ft), P(u, H_ft), P(u + s, H_ft / 2)],
                  fill=CHEV)
    im.save(out)
    print(out, im.size)


def main():
    draw_sign(INK, OUT)
    draw_sign(WHITE, OUT.replace(".png", "_dark.png"))        # inside east wall, on the black livery field
    S = os.path.dirname(OUT)
    # west gable outside (u = 556 - y, z 0-63.8): the chevrons at the north end, between the corner and the riser
    # (y 527.5-532), pointing at the door; a plain black rectangle from just past the riser (y 526) over the door to
    # the SW corner (y 404)
    # (Oct 20: the black field taken off, the owner found it read fake; the gable stays white cladding, chevrons only)
    livery(os.path.join(S, "livery_west.png"), 152.0, 63.8, [(3.0, 4.0), (10.0, 4.0)], 8.0, 152.0, notch=False)
    # and above the band (z 65.6-96.8): each chevron's upper leg carried on at the same angle (8 ft of u per 31.9 ft of
    # rise), across the band gap and up to the coping, running off the NE corner (owner, Oct 20: one continuous stripe)
    up = Image.new("RGBA", (22 * 40, int(31.2 * 40)), (0, 0, 0, 0))
    k = 8.0 / 31.9
    for (u, w) in [(3.0, 4.0), (10.0, 4.0)]:
        u0 = u - 1.8 * k                                  # at EL 65.6, past the band
        u1 = u0 - 31.2 * k                                # at the coping
        ImageDraw.Draw(up).polygon([(u0 * 40, up.size[1]), ((u0 + w) * 40, up.size[1]), ((u1 + w) * 40, 0), (u1 * 40, 0)],
                                   fill=CHEV)
    up.save(os.path.join(S, "livery_west_up.png"))
    # east end wall inside (u = 503 - y, z 65.7-98): chevrons between the flag and the sign, black field behind the
    # sign to the SE corner (y 404)
    livery(os.path.join(S, "livery_east_in.png"), 99.0, 32.3, [(1.0, 3.0), (6.2, 3.0)], 5.0, 11.4)
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

    # SC-1 / SC-2 turbine enclosures, south face (owner, Oct 21: the combined cycle's branding on the simple cycle):
    # two chevrons over the full wall height (EL 1.5-21.2, 11 ft wide), the band crossing them as on the gable;
    # SC-1's point east and SC-2's west, both at the paired stacks
    D = os.path.dirname(OUT)
    p = os.path.join(D, "sc_chevrons_e.png")
    livery(p, 11.0, 19.7, [(.5, 2.0), (4.0, 2.0)], 4.0, 11.0, notch=False)
    Image.open(p).transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(D, "sc_chevrons_w.png"))
    for t in ("SC1", "SC2"):
        im = Image.new("RGBA", (3000, 1200), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((1500, 600), t, font=f, fill=INK, anchor="mm")
        im = im.crop(im.getbbox())
        p = os.path.join(D, f"unit_{t}.png")
        im.save(p)
        print(p, im.size)


if __name__ == "__main__":
    main()
