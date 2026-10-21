"""QR codes printed on the SC-4 pad's cable tags and its digital-model sign (screens/qr_cable.png, qr_sign.png).
The content is a placeholder record ID, not a live link. Needs the qrcode package (system python).

    python3 blender/qr_tags.py
"""
import os

import qrcode

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screens")
for name, text in (("qr_cable.png", "SW-3X1 / SC-4 / CABLE RECORD / C-4-101"),
                   ("qr_sign.png", "SW-3X1 / SC-4 / DIGITAL CABLE MODEL")):
    q = qrcode.QRCode(border=2, box_size=12, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(text)
    q.make(fit=True)
    p = os.path.join(OUT, name)
    q.make_image(fill_color="black", back_color="white").save(p)
    print(p)
