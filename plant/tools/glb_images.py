#!/usr/bin/env python3
"""Shrink the images embedded in a GLB without touching geometry, materials or node data.

    python3 plant/tools/glb_images.py IN.glb [OUT.glb]      # OUT defaults to IN (rewritten in place)

The decals are printed panels (text on flat colour, often with a transparent background) and screen captures.
Text panels go to a 256-colour palette PNG (alpha kept, visually identical at panel size); opaque photo-like
images over 150 KB (CCTV / SCADA screens) go to JPEG quality 88. An image is only replaced when the new one is
smaller; identical images are stored once. Needs Pillow.
"""
import io
import json
import struct
import sys

from PIL import Image


def slim(data, mime, jpeg=True):
    im = Image.open(io.BytesIO(data))
    rgba = im.convert("RGBA")
    alpha = rgba.getextrema()[3][0] < 255
    buf = io.BytesIO()
    if not alpha and len(data) > 150_000:
        if not jpeg:                                                 # photo, and the caller wants PNG kept
            return data, mime
        rgba.convert("RGB").save(buf, "JPEG", quality=88, optimize=True)
        out, m = buf.getvalue(), "image/jpeg"
    else:
        q = rgba.quantize(256, method=Image.Quantize.FASTOCTREE) if alpha else rgba.convert("RGB").quantize(256)
        q.save(buf, "PNG", optimize=True)
        out, m = buf.getvalue(), "image/png"
    return (out, m) if len(out) < len(data) else (data, mime)


def main(src, dst):
    raw = open(src, "rb").read()
    magic, ver, _ = struct.unpack_from("<III", raw, 0)
    assert magic == 0x46546C67 and ver == 2, "not a glTF 2.0 binary"
    jl, _ = struct.unpack_from("<II", raw, 12)
    gltf = json.loads(raw[20:20 + jl])
    bl, _ = struct.unpack_from("<II", raw, 20 + jl)
    binc = raw[28 + jl:28 + jl + bl]
    views = gltf["bufferViews"]
    new_img, seen = {}, {}
    for im in gltf.get("images", []):
        if "bufferView" in im:
            v = views[im["bufferView"]]
            data = binc[v.get("byteOffset", 0):v.get("byteOffset", 0) + v["byteLength"]]
            new_img[im["bufferView"]] = slim(data, im.get("mimeType", "image/png"))
            im["mimeType"] = new_img[im["bufferView"]][1]
            # the same picture used by two materials (a PNG and a JPEG of one screen) is stored once
            im["bufferView"] = seen.setdefault(new_img[im["bufferView"]][0], im["bufferView"])
    # rebuild the binary chunk (4-byte aligned), dropping views no longer referenced and renumbering the rest
    used = {a["bufferView"] for a in gltf.get("accessors", []) if "bufferView" in a}
    used |= {im["bufferView"] for im in gltf.get("images", []) if "bufferView" in im}
    renum, kept, out = {}, [], bytearray()
    for i, v in enumerate(views):
        if i not in used:
            continue
        data = new_img[i][0] if i in new_img else \
            binc[v.get("byteOffset", 0):v.get("byteOffset", 0) + v["byteLength"]]
        out += b"\0" * (-len(out) % 4)
        v["byteOffset"], v["byteLength"] = len(out), len(data)
        out += data
        renum[i] = len(kept)
        kept.append(v)
    out += b"\0" * (-len(out) % 4)
    gltf["bufferViews"] = kept
    for x in gltf.get("accessors", []) + gltf.get("images", []):
        if "bufferView" in x:
            x["bufferView"] = renum[x["bufferView"]]
    gltf["buffers"][0]["byteLength"] = len(out)
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    total = 12 + 8 + len(js) + 8 + len(out)
    with open(dst, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, total))
        f.write(struct.pack("<II", len(js), 0x4E4F534A) + js)
        f.write(struct.pack("<II", len(out), 0x004E4942) + bytes(out))
    print(f"{dst}: {len(raw) / 1e6:.1f} MB -> {total / 1e6:.1f} MB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else sys.argv[1])
