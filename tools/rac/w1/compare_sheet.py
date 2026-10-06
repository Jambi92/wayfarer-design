"""RAC W1f evidence: side | front | 3/4-back orthographic panels for a list of bodies on one 10 cm grid (before/after sheets).
Usage: python3 compare_sheet.py out.jpg "label=path_r6.npz" ..."""
import sys, os, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence as EV
def panel(lab, p, pp=2.2):
    D = np.load(p, allow_pickle=True); V = D["V"].astype(float); F = D["F"]; x, f, u = V.T; H = int(245 * pp)
    s = EV.render(V, F, f, u, x, pp, (-40, -2), (int(80 * pp), H), 10); fr = EV.render(V, F, x, u, f, pp, (-45, -2), (int(90 * pp), H), 10)
    a = np.radians(45); hx = x * np.cos(a) - f * np.sin(a); dp = -f * np.cos(a) - x * np.sin(a)
    bk = EV.render(V, F, hx, u, dp, pp, (-50, -2), (int(100 * pp), H), 10)
    T = Image.new("RGB", (s.width + fr.width + bk.width + 20, H + 24), "white"); ImageDraw.Draw(T).text((4, 4), lab + "   side | front | 3/4 back", fill=(0, 0, 0))
    T.paste(s, (0, 24)); T.paste(fr, (s.width + 10, 24)); T.paste(bk, (s.width + fr.width + 20, 24)); return T
if __name__ == "__main__":
    ims = [panel(*a.split("=", 1)) for a in sys.argv[2:]]
    cols = 2 if len(ims) > 2 else 1; rows = (len(ims) + cols - 1) // cols; W = max(i.width for i in ims); Hh = max(i.height for i in ims)
    S = Image.new("RGB", (W * cols + 20 * (cols - 1), Hh * rows), "white")
    for k, im in enumerate(ims): S.paste(im, ((k % cols) * (W + 20), (k // cols) * Hh))
    S.save(sys.argv[1], quality=82)
