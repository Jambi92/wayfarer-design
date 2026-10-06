"""RAC W1f evidence: head front views with the O-1 orbital-margin rings and landmark globes (ocular_w1f.json); 1 cm ticks.
Usage: python3 ocular_sheet.py meas_dir ocular.json out.jpg ID..."""
import sys, os, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence as EV, orbit_ring as O
from arm_measure import load
def tile(md, oc, i):
    d = load(os.path.join(md, i + "_rest.npz")); V = d["V"].astype(float); F = d["F"]; r = oc["bodies"][i]
    Vs, Fs, off = [V], [F], len(V)
    for s in ("l", "r"):
        sv, sf = EV.sphere(d["eye_" + s].astype(float), r["globe_cm"] / 2); Vs.append(sv); Fs.append(sf + off); off += len(sv)
    V2 = np.vstack(Vs); F2 = np.vstack(Fs); ec = (d["eye_l"] + d["eye_r"]) / 2; win = r["HH"] * 0.55; pp = 300 / win
    org = (-win / 2, ec[2] - win * 0.45)
    im = EV.render(V2, F2, V2[:, 0], V2[:, 2], V2[:, 1], pp, org, (300, 300), 1); dr = ImageDraw.Draw(im)
    O.FWD = r.get("ring_forward_cm", 0.8)
    for s in ("l", "r"):
        P, c, ub = O.ring(d["eye_" + s].astype(float), s, r["ring_breadth_cm"], r["ring_height_cm"])
        pts = [((p[0] - org[0]) * pp, 300 - (p[2] - org[1]) * pp) for p in P]; dr.line(pts + [pts[0]], fill=(220, 30, 30), width=2)
    T = Image.new("RGB", (300, 336), "white"); ImageDraw.Draw(T).text((4, 3), "%s  ring %.2fx%.2f cm  globe %.2f cm" % (i, r["ring_breadth_cm"], r["ring_height_cm"], r["globe_cm"]), fill=(0, 0, 0))
    ImageDraw.Draw(T).text((4, 16), "ORB/HL x%.3f  globe/HH x%.3f vs MF  fits %s" % (r["vs_MF"]["ORB_breadth"], r["vs_MF"]["globe_over_HH"], r["fits"]), fill=(0, 0, 0))
    T.paste(im, (0, 34)); return T
if __name__ == "__main__":
    md, ocp, out = sys.argv[1:4]; oc = json.load(open(ocp)); ts = [tile(md, oc, i) for i in sys.argv[4:]]
    cols = 4; rows = (len(ts) + cols - 1) // cols; S = Image.new("RGB", (cols * 310, rows * 340), "white")
    for k, t in enumerate(ts): S.paste(t, ((k % cols) * 310, (k // cols) * 340))
    S.save(out, quality=88)
