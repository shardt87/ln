"""Stamp the author credit (blender/credit.py) on every page of a finished PDF: a small line centred on the bottom
edge, below the documents' own footers, on a dark backing so it reads over full-bleed photos too. Vector text.
A PDF is stamped once (marked in its keywords), so generators can call it after every rebuild.

    python tools/stamp_credit.py FILE.pdf [...]
"""
import os
import sys

import pymupdf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blender"))
import credit  # noqa: E402

MARK = "author-credit"


def stamp(path):
    doc = pymupdf.open(path)
    kw = doc.metadata.get("keywords") or ""
    if MARK in kw:
        print("already stamped", path)
        return False
    text = f"{credit.NAME}  ·  {credit.EMAIL}"
    for page in doc:
        r = page.rect
        fs = max(6.0, min(8.5, r.width / 110))                    # scale with the page, readable on letter and slides
        w = pymupdf.get_text_length(text, fontname="helv", fontsize=fs)
        x0, y1 = (r.width - w) / 2, r.height - fs * .55
        pad = fs * .45
        page.draw_rect(pymupdf.Rect(x0 - pad * 2, y1 - fs - pad * .6, x0 + w + pad * 2, y1 + pad), color=None,
                       fill=(.08, .09, .10), fill_opacity=.72, overlay=True)
        page.insert_text((x0, y1 - fs * .12), text, fontname="helv", fontsize=fs, color=(.86, .86, .84), overlay=True)
    meta = dict(doc.metadata)
    meta["keywords"] = (kw + " " + MARK).strip()
    meta["author"] = credit.NAME
    doc.set_metadata(meta)
    tmp = path + ".tmp"
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    os.replace(tmp, path)
    print("stamped", path)
    return True


if __name__ == "__main__":
    for p in sys.argv[1:]:
        stamp(p)
