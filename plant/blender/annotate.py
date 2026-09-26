#!/usr/bin/env python3
"""Burn equipment labels and the credit block into Blender renders.

SK-3X1-11 style: "labels beside equipment; credit burned into every image".
Reads <view>_<style>.png and <view>_<style>.labels.json written by
SK-3X1_Rev14_blender_build.py and writes <view>_<style>_annotated.png.

    python3 plant/blender/annotate.py plant/renders/blender

Needs Pillow. Uses DejaVu fonts (Ubuntu: fonts-dejavu-core).
"""
import glob
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIRS = ["/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu", "/Library/Fonts", "C:/Windows/Fonts"]


def font(name, size):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


INK, COPPER, TEAL, PAPER = (31, 43, 51), (176, 102, 43), (23, 127, 126), (255, 255, 255)


def overlaps(a, b, pad=3):
    return not (a[2] + pad < b[0] or b[2] + pad < a[0] or a[3] + pad < b[1] or b[3] + pad < a[1])


def annotate(png, meta):
    src = Image.open(png).convert("RGB")
    W, H0 = src.size
    k = W / 1920
    bar_h = int(58 * k)
    im = Image.new("RGB", (W, H0 + bar_h), PAPER)      # credit bar below, not over, the render
    im.paste(src, (0, 0))
    H = H0 + bar_h
    d = ImageDraw.Draw(im)
    f_tag = font("DejaVuSansMono-Bold.ttf", max(10, int(15 * k)))
    f_small = font("DejaVuSans.ttf", max(9, int(14 * k)))
    f_title = font("DejaVuSans-Bold.ttf", max(11, int(19 * k)))
    placed = [(0, H - bar_h, W, H)]
    # labels, greedy placement around the anchor, skipping collisions
    for lab in sorted(meta["labels"], key=lambda l: l["y"]):
        ax, ay = lab["x"], lab["y"]
        text = lab["tag"]
        tw, th = d.textbbox((0, 0), text, font=f_tag)[2:]
        bw, bh = tw + int(10 * k), th + int(8 * k)
        cands = [(14 * k, -34 * k), (-14 * k - bw, -34 * k), (16 * k, 10 * k), (-16 * k - bw, 10 * k),
                 (-bw / 2, -48 * k), (-bw / 2, 16 * k), (30 * k, -60 * k), (-30 * k - bw, -60 * k)]
        for (dx, dy) in cands:
            x0, y0 = ax + dx, ay + dy
            box = (x0, y0, x0 + bw, y0 + bh)
            if box[0] < 4 or box[2] > W - 4 or box[1] < 4 or box[3] > H - bar_h - 4:
                continue
            if any(overlaps(box, p) for p in placed):
                continue
            col = TEAL if lab.get("optional") else INK
            cx = min(max(ax, box[0]), box[2])
            cy = box[3] if ay > box[3] else (box[1] if ay < box[1] else (box[1] + box[3]) / 2)
            d.line([(ax, ay), (cx, cy)], fill=col, width=max(1, int(1.4 * k)))
            d.ellipse([ax - 2.5 * k, ay - 2.5 * k, ax + 2.5 * k, ay + 2.5 * k], fill=col)
            d.rectangle(box, fill=PAPER, outline=col, width=max(1, int(1.2 * k)))
            d.text((box[0] + 5 * k, box[1] + 3 * k), text, font=f_tag, fill=col)
            placed.append(box)
            break
    # credit block (burned in)
    v = meta["view"]
    d.rectangle((0, H - bar_h, W, H), fill=PAPER)
    d.line([(0, H - bar_h), (W, H - bar_h)], fill=INK, width=max(1, int(2 * k)))
    d.rectangle((0, H - bar_h, int(8 * k), H), fill=COPPER)
    d.text((int(22 * k), H - bar_h + int(8 * k)), f"3x1 combined-cycle plant  |  View {v['k']}: {v['name'].split(' ', 1)[1] if v['name'].split(' ', 1)[0] == v['k'] else v['name']}",
           font=f_title, fill=INK)
    d.text((int(22 * k), H - bar_h + int(33 * k)),
           f"SK-3X1-3D / REV 14  ·  orthographic, fit {v['ortho_ft']:,} ft, margins L/R {v['margin_lr']}% "
           f"T/B {v['margin_tb']}%  ·  Blender Cycles, {v['samples']} samples, {v['style']} style",
           font=f_small, fill=(85, 99, 108))
    right1 = "Stephan Hardt | Power Generation Solutions"
    right2 = "Conceptual illustration. Not engineered. Not for construction."
    for i, (t, f, c) in enumerate(((right1, f_title, INK), (right2, f_small, COPPER))):
        tw = d.textbbox((0, 0), t, font=f)[2]
        d.text((W - tw - int(22 * k), H - bar_h + int(8 * k) + i * int(25 * k)), t, font=f, fill=c)
    out = png.replace(".png", "_annotated.png")
    im.save(out, optimize=True)
    return out


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "renders", "blender")
    n = 0
    for lj in sorted(glob.glob(os.path.join(root, "*.labels.json"))):
        png = lj.replace(".labels.json", ".png")
        if os.path.exists(png):
            print("annotated", annotate(png, json.load(open(lj))))
            n += 1
    print(f"{n} images annotated")


if __name__ == "__main__":
    main()
