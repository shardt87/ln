"""Build the X-ray capture page (capture.html) from the built viewer: CDN three.js scripts rewritten to a local
node_modules (no network in the render container), and window.__vw exposed for covcam_w.js (X-ray colours, ghost
material, item meshes, the model).

    cd plant/tools/xray_capture && npm install            # playwright 1.56, three 0.147
    python3 make_capture_page.py ../../viewer/index_southwire.html
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "viewer", "index_southwire.html")
s = open(src, encoding="utf-8").read()
nm = "file://" + os.path.join(HERE, "node_modules", "three")
s = s.replace("https://cdn.jsdelivr.net/npm/three@0.147.0", nm)
hook = "window.tourAPI = {"
assert hook in s, "viewer changed: tourAPI hook not found"
s = s.replace(hook, "window.__vw={XCOL,XR,ghostMat,itemMeshes, get MODEL(){return MODEL}};\n" + hook, 1)
open(os.path.join(HERE, "capture.html"), "w", encoding="utf-8").write(s)
print("wrote", os.path.join(HERE, "capture.html"))
