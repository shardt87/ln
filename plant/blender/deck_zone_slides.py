"""Zone close-up slides for the Anixter/Wesco deck: one SK-3X1 render per zone of the slide-19 map, full bleed, with the
zone's orange number disc (same as the map marker), the zone name and a one-line caption, in the deck's type.

  python3 blender/deck_zone_slides.py      ->  renders/deck/zones/zone_XX.png + zones_contact.jpg
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "deck")
EPIC = os.path.join(HERE, "..", "renders", "epic")
OUT = os.path.join(HERE, "..", "renders", "deck", "zones")
ORANGE = (224, 122, 46)

# zone: (render, caption)
ZONES = {
    1: ("Switchyard, GSU & grid tie", "E19", "Generator step-up transformers facing the 230 kV switchyard"),
    2: ("BESS yard", "E65", "Crew pulling 1,500 V DC conductor into the precast trench between the containers"),
    3: ("Reel staging & prefab", "E89", "SIMpull Reels on Cradles, Reel Rollers and stacked reels on JAX stands"),
    4: ("Admin & control room", "E86", "Main control room: six-position console and the 16-cube video wall"),
    5: ("E-house", "E32", "Unit e-houses with stairs and cable entries, unit transformers and manholes"),
    6: ("HRSG trains & stacks", "E101", "GT exhaust diffuser, HRSG casing with the drums on top, stack at the outlet"),
    7: ("Turbine hall", "P21_photo", "GT1 on the operating deck: combustor section and the fuel-gas manifold"),
    8: ("GT air inlets", "E30", "Inlet filter houses and transformer bays along the turbine-hall road"),
    9: ("MCC, VFD & UPS room", "E83", "MCCs and protection panels, conduit drops from the overhead tray"),
    10: ("Modular power yard", "E14", "Engine hall exhaust trains, SCRs and stacks"),
    11: ("Air-cooled condenser", "E34", "Steam risers, wind wall, stair tower and fan bells under the deck"),
    12: ("Chillers & cooling towers", "E43", "GT inlet chilling: chiller building, pumps and e-house, tower behind"),
    13: ("Water treatment", "E35", "Raw, fire / service and demineralised water tanks, fire pump house"),
    14: ("Carbon capture (CCS)", "E68", "ARMOR-X and Type TC-ER on the CCS rack below the absorbers"),
    15: ("Gas metering", "P110_photo", "Gas yard: rigid conduit and exposed ARMOR-X MC-HL on strut"),
    16: ("Cable corridor & MV", "E67", "ARMOR-X and MV-105 in the tray, the legend on every jacket"),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


def load(key):
    f = os.path.join(EPIC, key + ".jpg") if "photo" in key else os.path.join(EPIC, key + "_pro_clean.jpg")
    im = Image.open(f).convert("RGB")
    W, H = im.size
    if abs(W / H - 16 / 9) > .01:                                       # crop to 16:9 around the centre
        if W / H < 16 / 9:
            h = int(W * 9 / 16)
            im = im.crop((0, H - h - int(H * .04), W, H - int(H * .04)))       # portrait: keep the lower part
        else:
            w = int(H * 16 / 9)
            im = im.crop(((W - w) // 2, 0, (W - w) // 2 + w, H))
    return im.resize((1920, 1080), Image.LANCZOS)


def slide(z, name, key, cap):
    im = load(key)
    a = np.asarray(im).astype(np.float32)
    y = np.linspace(0, 1, 1080)[:, None, None]
    x = np.linspace(0, 1, 1920)[None, :, None]
    shade = np.clip((y - .58) / .42, 0, 1) ** 1.3 * np.clip(1.25 - x * .7, 0, 1) * .88   # bottom-left gradient
    top = np.clip((.16 - y) / .16, 0, 1) * .5                                            # light top band
    a = a * (1 - shade) * (1 - top) + np.array((13, 15, 18), np.float32) * (shade + top * (1 - shade))
    S = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(S)
    R = 46
    cx, cy = 128 + R, 812
    d.ellipse([cx - R - 4, cy - R - 4, cx + R + 4, cy + R + 4], fill=(245, 245, 242))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=ORANGE)
    d.text((cx, cy + 2), str(z), font=font("BarlowCondensed-ExtraBold.ttf", 54), fill=(255, 255, 255), anchor="mm")
    d.text((cx + R + 30, cy - 50), f"ZONE {z:02d}", font=font("BarlowCondensed-Bold.ttf", 30), fill=ORANGE)
    d.text((cx + R + 28, cy - 18), name.upper(), font=font("BarlowCondensed-ExtraBold.ttf", 66), fill=(245, 245, 242))
    d.text((128, 900), cap, font=font("Barlow-Regular.ttf", 30), fill=(228, 228, 224))
    d.text((128, 1020), "SK-3X1 PLANT MODEL · RENDERED ILLUSTRATION", font=font("BarlowCondensed-Bold.ttf", 24),
           fill=(200, 200, 196))
    d.text((60, 44), "THE PLANT IS THE MODEL", font=font("BarlowCondensed-Bold.ttf", 26), fill=ORANGE)
    return S


def main():
    os.makedirs(OUT, exist_ok=True)
    thumbs = []
    for z, (name, key, cap) in ZONES.items():
        S = slide(z, name, key, cap)
        S.save(os.path.join(OUT, f"zone_{z:02d}.png"))
        thumbs.append(S.resize((480, 270), Image.LANCZOS))
    C = Image.new("RGB", (1920, 1080))
    for i, t in enumerate(thumbs):
        C.paste(t, ((i % 4) * 480, (i // 4) * 270))
    C.save(os.path.join(OUT, "zones_contact.jpg"), quality=90)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
