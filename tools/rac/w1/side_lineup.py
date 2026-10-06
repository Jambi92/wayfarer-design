"""RAC W1e: left-side orthographic lineup of reference bodies on a common scale (visual check, PV-D17). 10 cm ticks.
Usage: python3 side_lineup.py cand_dir out.jpg ID..."""
import sys, os, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence as EV

def main(cd, out, ids):
    pp = 1.8; H = int(240 * pp); tiles = []
    for i in ids:
        D = np.load(os.path.join(cd, i + "_r6.npz"), allow_pickle=True); V = D["V"].astype(float); F = D["F"]; x, f, u = V.T
        im = EV.render(f, F, f, u, x, pp, (-40, -2), (int(80 * pp), H), 10)
        T = Image.new("RGB", (im.width, H + 20), "white"); ImageDraw.Draw(T).text((4, 4), i, fill=(0, 0, 0)); T.paste(im, (0, 20)); tiles.append(T)
    S = Image.new("RGB", (sum(t.width for t in tiles), H + 20), "white"); x0 = 0
    for t in tiles: S.paste(t, (x0, 0)); x0 += t.width
    S.save(out, quality=88)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
