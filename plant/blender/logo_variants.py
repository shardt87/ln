"""Southwire logo variants for printed decals on the model (screens/): all white (on the orange steel reel flanges and
the red trailer skirts), solid colour (deep copper mark, black wordmark: on the white tractor cab) and the round
mark alone, the "meatball", in solid copper, square (filling the black steel reel flanges)."""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "screens")


def main():
    src = Image.open(os.path.join(HERE, "deck", "southwire_pgs_logo.png")).convert("RGBA")
    for name, fn in (("sw_logo_white.png", lambda r, g, b: (255, 255, 255)),
                     ("sw_logo_solid.png", lambda r, g, b: (17, 18, 20) if min(r, g, b) > 150 else (166, 90, 44))):
        im = src.copy()
        px = im.load()
        for j in range(im.height):
            for i in range(im.width):
                r, g, b, a = px[i, j]
                px[i, j] = fn(r, g, b) + (255,) if a >= 110 else (0, 0, 0, 0)
        p = os.path.join(OUT, name)
        im.save(p)
        print(p, im.size)
    # the meatball: the mark left of the wordmark (x < 303), cropped square, solid copper, transparent elsewhere
    m = src.crop((0, 0, 303, src.height))
    bb = m.getbbox()
    m = m.crop(bb)
    S = max(m.size)
    sq = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sq.paste(m, ((S - m.width) // 2, (S - m.height) // 2))
    sq = sq.resize((1024, 1024), Image.LANCZOS)
    px = sq.load()
    for j in range(sq.height):
        for i in range(sq.width):
            px[i, j] = (184, 104, 52, 255) if px[i, j][3] >= 110 else (0, 0, 0, 0)
    p = os.path.join(OUT, "sw_meatball.png")
    sq.save(p)
    print(p, sq.size)


if __name__ == "__main__":
    main()
