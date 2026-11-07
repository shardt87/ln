"""Side graphics for the Southwire cable-rejuvenation van (maintenance.rejuvenation): after Southwire's field-service
van livery, a white front, two copper chevrons, a black rear with the Southwire logo (copper mark, white wordmark)
and CABLE REJUVENATION SERVICES. One image per side so the lettering reads on both: van_east.png has the front at the
left, van_west.png at the right. 20 x 6.6 ft at 100 px / ft (the body behind the cab doors)."""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "screens")
WHITE, BLACK, COPPER = (238, 239, 238, 255), (24, 25, 27, 255), (196, 116, 70, 255)
W, H = 2000, 660


def side(front_left):
    im = Image.new("RGBA", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    # geometry drawn with the front at the left, mirrored afterwards for the other side (text added after)
    d.polygon([(760, 0), (W, 0), (W, H), (980, H), (1120, H / 2)], fill=BLACK)              # black rear, chevron edge
    for o in (0, 150):                                                                      # two copper chevrons
        d.polygon([(420 + o, 0), (520 + o, 0), (660 + o, H / 2), (520 + o, H), (420 + o, H), (560 + o, H / 2)], fill=COPPER)
    if not front_left:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    logo = Image.open(os.path.join(HERE, "deck", "southwire_pgs_logo.png")).convert("RGBA")
    lw = 760
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    cx = 1520 if front_left else W - 1520
    im.alpha_composite(logo, (int(cx - lw / 2), 150))
    f = ImageFont.truetype(os.path.join(HERE, "deck", "BarlowCondensed-Bold.ttf"), 64)
    ImageDraw.Draw(im).text((cx, 420), "CABLE REJUVENATION SERVICES", font=f, fill=(242, 242, 240, 255), anchor="mm")
    return im


def main():
    for name, fl in (("van_east.png", True), ("van_west.png", False)):
        p = os.path.join(OUT, name)
        side(fl).save(p)
        print(p)


if __name__ == "__main__":
    main()
