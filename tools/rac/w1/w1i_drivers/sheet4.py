# RAC W1i render sheets (order §7): side | front | front 3/4 | back 3/4 orthographic panels, one consistent scale per sheet.
# Usage: python3 sheet4.py out.jpg [--crop trunk|axilla] [--noarms] [--pp 2.2] [--cols 2] "label=path_r6.npz" ...
#  --crop trunk : u from 30 cm below the hip joints to 12 cm above the suprasternal proxy (same cm scale for every body)
#  --crop axilla: 16 cm above to 30 cm below the shoulder joints, front and back 3/4 plus horizontal sections (arm vs trunk outline)
#  --crop hips  : knee joints - 10 cm to spine_02 + 10 cm (W1j femur trade)
#  --noarms     : faces with arm weight > 0.5 removed (trunk outline without arm occlusion)
import sys, os, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import evidence as EV
from arm_measure import load

def views(V):
    x, f, u = V.T; a = np.radians(45)
    return [("side", f, x), ("front", x, f), ("front 3/4", x * np.cos(a) + f * np.sin(a), f * np.cos(a) - x * np.sin(a)),
            ("back 3/4", x * np.cos(a) - f * np.sin(a), -f * np.cos(a) - x * np.sin(a))]

def armw_of(d):
    return np.maximum.reduce([d["w_" + k] for k in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])

def panel(lab, p, pp, ur, noarms):
    d = load(p); V = d["V"].astype(float); F = d["F"]; u = V[:, 2]; J = d["joints"]; hd = lambda n: np.asarray(J[n][0], float)
    if noarms:
        aw = armw_of(d); F = F[(aw[F] < 0.5).all(1)]
    u0, u1 = ur(hd); H = int((u1 - u0) * pp); ims = []
    for name, hx, dp in views(V):
        im = EV.render(V, F, hx, u, dp, pp, (-55, u0), (int(110 * pp), H), 10); ImageDraw.Draw(im).text((4, 4), name, fill=(0, 0, 0)); ims.append(im)
    T = Image.new("RGB", (sum(i.width for i in ims) + 10 * (len(ims) - 1), H + 24), "white"); ImageDraw.Draw(T).text((4, 4), lab, fill=(0, 0, 0))
    x0 = 0
    for im in ims: T.paste(im, (x0, 24)); x0 += im.width + 10
    return T

def sections_panel(lab, p, pp=6.0, offs=(2, 4, 6, 8, 10, 12, 14)):
    """horizontal sections at cm below the shoulder-joint height: trunk (arm weight < 0.2) outline grey, arm (upper-arm weight > 0.5)
    outline red; left side only, view from above, same scale for every level"""
    d = load(p); V = d["V"].astype(float); F = d["F"]; J = d["joints"]; hd = lambda n: np.asarray(J[n][0], float)
    aw = armw_of(d); up = np.maximum(d["w_upperarm_l"], d["w_upperarm_r"])
    TF = F[((aw < 0.2) & d["keep"])[F].all(1)]; AF = F[(up > 0.5)[F].all(1)]
    shu = (hd("upperarm_l")[2] + hd("upperarm_r")[2]) / 2; cx = hd("upperarm_l")[0]
    W = int(40 * pp); Hh = int(40 * pp); tiles = []
    def segs(TT, z):
        out = []
        for t in TT:
            P = V[t]; s = P[:, 2] - z; pts = []
            for i, j in ((0, 1), (1, 2), (2, 0)):
                if s[i] * s[j] < 0: k = s[i] / (s[i] - s[j]); pts.append(P[i, :2] + (P[j, :2] - P[i, :2]) * k)
            if len(pts) == 2: out.append(pts)
        return out
    for o in offs:
        z = shu - o; im = Image.new("RGB", (W, Hh), "white"); dr = ImageDraw.Draw(im)
        tr = lambda q: ((q[0] - cx) * pp + W / 2, Hh / 2 - (q[1] - hd("upperarm_l")[1]) * pp)
        for c, TT in (((90, 90, 90), TF[np.abs(V[TF][:, :, 2].mean(1) - z) < 6]), ((200, 30, 30), AF[np.abs(V[AF][:, :, 2].mean(1) - z) < 6])):
            for a, b in segs(TT, z): dr.line([tr(a), tr(b)], fill=c, width=2)
        dr.text((4, 4), "%d cm below shoulder joint" % o, fill=(0, 0, 0)); dr.rectangle([0, 0, W - 1, Hh - 1], outline=(200, 200, 200)); tiles.append(im)
    T = Image.new("RGB", (len(tiles) * (W + 6), Hh + 24), "white"); ImageDraw.Draw(T).text((4, 4), lab + "   left arm (red) vs trunk (grey), view from above, 40 cm tiles", fill=(0, 0, 0))
    for k, im in enumerate(tiles): T.paste(im, (k * (W + 6), 24))
    return T

if __name__ == "__main__":
    a = sys.argv[1:]; out = a.pop(0); crop = None; noarms = False; pp = 2.2; cols = 2
    while a and a[0].startswith("--"):
        k = a.pop(0)
        if k == "--crop": crop = a.pop(0)
        elif k == "--noarms": noarms = True
        elif k == "--pp": pp = float(a.pop(0))
        elif k == "--cols": cols = int(a.pop(0))
    bodies = [x.split("=", 1) for x in a]
    if crop == "trunk":
        ur = lambda hd: ((hd("thigh_l")[2] + hd("thigh_r")[2]) / 2 - 30, (hd("clavicle_l")[2] + hd("clavicle_r")[2]) / 2 + 12)
        spans = []
        for _, p in bodies:
            d = load(p); J = d["joints"]; hd = lambda n: np.asarray(J[n][0], float); spans.append(ur(hd))
        L = max(b - a_ for a_, b in spans); ur2 = lambda hd: (ur(hd)[0], ur(hd)[0] + L)   # same window height for every body
        ims = [panel(l, p, pp, ur2, noarms) for l, p in bodies]
    elif crop == "hips":   # W1j femur trade: knee joints - 10 cm to spine_02 + 10 cm, same window for every body
        ur = lambda hd: ((hd("calf_l")[2] + hd("calf_r")[2]) / 2 - 10, hd("spine_02")[2] + 10)
        spans = []
        for _, p in bodies:
            d = load(p); J = d["joints"]; hd = lambda n: np.asarray(J[n][0], float); spans.append(ur(hd))
        L = max(b - a_ for a_, b in spans); ur2 = lambda hd: (ur(hd)[0], ur(hd)[0] + L)
        ims = [panel(l, p, pp, ur2, noarms) for l, p in bodies]
    elif crop == "axilla":
        ur = lambda hd: ((hd("upperarm_l")[2] + hd("upperarm_r")[2]) / 2 - 30, (hd("upperarm_l")[2] + hd("upperarm_r")[2]) / 2 + 16)
        ims = []
        for l, p in bodies: ims += [panel(l, p, pp, ur, noarms), sections_panel(l, p)]
        cols = 1
    else:
        top = 262 if any(float(np.load(p)["V"][:, 2].max()) > 240 for _, p in bodies) else 245
        ims = [panel(l, p, pp, lambda hd: (-2, top), noarms) for l, p in bodies]
    rows = (len(ims) + cols - 1) // cols; W = max(i.width for i in ims); Hh = max(i.height for i in ims)
    S = Image.new("RGB", (W * cols + 20 * (cols - 1), Hh * rows), "white")
    for k, im in enumerate(ims): S.paste(im, ((k % cols) * (W + 20), (k // cols) * Hh))
    S.save(out, quality=85); print("saved", out, S.size)
