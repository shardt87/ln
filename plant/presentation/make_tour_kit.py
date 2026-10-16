"""Build the portable tour kit (zip): the Southwire viewer with the tour, the tour stops, the recorder, the caption
compositor, fonts and the one-click run scripts.

    python3 presentation/make_tour_kit.py   -> presentation/dist/SK-3X1_tour_kit.zip"""
import os
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PLANT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "dist", "SK-3X1_tour_kit.zip")
FILES = [(os.path.join(PLANT, "viewer", "index_southwire.html"), "SK-3X1_viewer.html"),
         (os.path.join(HERE, "tour.json"), "tour.json"),
         (os.path.join(HERE, "record_tour.js"), "record_tour.js"),
         (os.path.join(HERE, "compose_tour.py"), "compose_tour.py")]
FILES += [(os.path.join(HERE, "tour_kit", n), n) for n in sorted(os.listdir(os.path.join(HERE, "tour_kit")))]
FILES += [(os.path.join(PLANT, "blender", "deck", n), "fonts/" + n)
          for n in ("BarlowCondensed-Bold.ttf", "BarlowCondensed-ExtraBold.ttf", "Barlow-Regular.ttf")]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for src, arc in FILES:
        info = zipfile.ZipInfo.from_file(src, "SK-3X1_tour_kit/" + arc)
        if arc.endswith(".sh"):
            info.external_attr = 0o755 << 16
        with open(src, "rb") as f:
            z.writestr(info, f.read(), zipfile.ZIP_DEFLATED)
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB,", len(FILES), "files")
