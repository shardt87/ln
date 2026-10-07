"""Scale figure in PPE, shared by every scene (realism.people, maintenance, cable stories).

About 5 ft 10 in, built from tapered rods: work boots, jointed legs in work trousers, pelvis, tapered torso in a
hi-vis vest with two reflective bands, shoulders, jointed arms in long sleeves with gloves, neck, head, hard hat
with brim. a = facing direction (radians, from +x). pose: 'stand' (arms relaxed, slightly forward) or 'work'
(forearms raised in front, handling something)."""
import math


def build(rod, x, y, z, a=0.0, vest="hivis", hat="hardhat", pose=None):
    f = (math.cos(a), math.sin(a))                 # forward
    s = (-math.sin(a), math.cos(a))                # left
    if pose is None:
        pose = "work" if (int(abs(x) * 7 + abs(y) * 3) % 3 == 0) else "stand"

    def P(fw, sd, h):
        return (x + f[0] * fw + s[0] * sd, y + f[1] * fw + s[1] * sd, z + h)
    for k in (-1, 1):                              # boots, legs
        sd = .27 * k
        rod(P(-.12, sd, .18), P(.42, sd, .18), .17, "boot", r2=.15, seg=10)
        rod(P(0, sd, .3), P(.02, sd, 1.55), .2, "workwear", r2=.24, seg=12)              # shin
        rod(P(.02, sd, 1.55), P(0, sd * 1.05, 3.05), .25, "workwear", r2=.3, seg=12)     # thigh
    rod(P(0, -.42, 2.95), P(0, .42, 2.95), .3, "workwear", seg=12)                     # pelvis
    rod(P(0, 0, 2.95), P(.03, 0, 3.6), .44, "workwear", r2=.46, seg=14)                # belly / belt line
    rod(P(.03, 0, 3.55), P(.02, 0, 4.6), .5, vest, r2=.55, seg=16)                     # torso in the vest
    for h in (3.78, 4.18):                                                             # reflective bands
        rod(P(.03, 0, h), P(.03, 0, h + .1), .53, "reflect", seg=16)
    rod(P(0, -.6, 4.58), P(0, .6, 4.58), .25, vest, seg=12)                            # shoulders
    for k in (-1, 1):
        sd = .66 * k
        if pose == "work":
            el, wr = P(.25, sd * .95, 3.75), P(.95, sd * .55, 4.0)
        else:
            el, wr = P(.12, sd * 1.02, 3.62), P(.3, sd * .98, 2.85)
        rod(P(0, sd, 4.55), el, .17, "workwear", r2=.15, seg=10)                       # upper arm
        rod(el, wr, .15, "workwear", r2=.12, seg=10)                                    # forearm
        hd = (wr[0] + (wr[0] - el[0]) * .35, wr[1] + (wr[1] - el[1]) * .35, wr[2] + (wr[2] - el[2]) * .35)
        rod(wr, hd, .12, "glove", r2=.1, seg=8)                                         # glove
    rod(P(0, 0, 4.7), P(0, 0, 5.0), .16, "skin", seg=10)                               # neck
    rod(P(.02, 0, 4.98), P(.03, 0, 5.32), .3, "skin", r2=.33, seg=14)                  # head
    rod(P(.03, 0, 5.32), P(.03, 0, 5.55), .33, "skin", r2=.27, seg=14)
    rod(P(.06, 0, 5.5), P(.06, 0, 5.55), .5, hat, seg=18)                              # hard-hat brim
    rod(P(.04, 0, 5.55), P(.03, 0, 5.92), .4, hat, r2=.2, seg=18)                      # shell
