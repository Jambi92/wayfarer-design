"""RAC W1e: attach the ear families to the W1e reference bodies and render a head evidence sheet (side | front | back, 1 cm ticks).
Usage: python3 ear_attach_sheet.py cand_dir out_dir"""
import sys, os, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import attach_ears as A, evidence as EV

MAP = [("MF-M-R", "MF-human"), ("FN", "FN-elven"), ("AE", "AE-elven"), ("VA", "VA-elven"), ("HV", "HV-mixed"),
       ("GR", "GR-folded"), ("GO", "GO-bowl"), ("PK-NAT", "PK-compact"), ("CG-NAT", "CG-finefolded")]

def head_views(npz, title):
    D = np.load(npz, allow_pickle=True); V = D["V"].astype(float); F = D["F"]; keep = D["keep"]; hw = D["w_head"]
    Vs, Fs, off = [V], [F], len(V)
    for s in ("eye_l", "eye_r"):
        sv, sf = EV.sphere(D[s], float(D["eye_diam"]) / 2); Vs.append(sv); Fs.append(sf + off); off += len(sv)
    V2 = np.vstack(Vs); F2 = np.vstack(Fs); x, f, u = V2.T
    nb = int(json.loads(str(D["meta"])).get("ears", {}).get("n_body_verts", len(V)))
    fc = np.where((F2.min(1) >= nb)[:, None] & (F2.max(1) < len(V))[:, None], np.array([214, 178, 150.0]), np.array([205, 205, 200.0]))
    hv = keep & (hw > 0.5); top = V[hv, 2].max(); bot = V[hv, 2].min(); win = 1.15 * (top - bot) + 2; z0 = top - win + 1
    pp = 300.0 / win; H = 300
    cx = 0.5 * (V[hv, 1].min() + V[hv, 1].max())
    side = EV.render(f, F2, f, u, x, pp, (cx - 0.5 * win, z0), (H, H), 1, fcol=fc)
    front = EV.render(x, F2, x, u, f, pp, (-0.5 * win, z0), (H, H), 1, fcol=fc)
    back = EV.render(-x, F2, -x, u, -f, pp, (-0.5 * win, z0), (H, H), 1, fcol=fc)
    T = Image.new("RGB", (3 * H + 20, H + 24), "white"); d = ImageDraw.Draw(T); d.text((4, 4), title, fill=(0, 0, 0))
    for k, im in enumerate((side, front, back)): T.paste(im, (k * (H + 10), 24))
    return T

def main(cd, out):
    os.makedirs(out, exist_ok=True); res = {}; tiles = []
    for b, fam in MAP:
        src = os.path.join(cd, b + "_r6.npz"); dst = os.path.join(out, b + "_ears_r6.npz")
        HH = json.load(open(os.path.join(cd, b + "_meas.json")))["combined"]["cranio"]["HH"]
        res[b] = A.attach(src, fam, dst, HH)
        tiles.append(head_views(dst, "%s + %s  (scale %.3f; left side | front | back; 1 cm ticks; family ear tinted)" % (b, fam, res[b]["l"]["scale"])))
    W = tiles[0].width; S = Image.new("RGB", (2 * W + 10, ((len(tiles) + 1) // 2) * (tiles[0].height + 8)), "white")
    for k, t in enumerate(tiles): S.paste(t, ((k % 2) * (W + 10), (k // 2) * (t.height + 8)))
    S.save(os.path.join(out, "ears_attached_sheet.jpg"), quality=88)
    json.dump(res, open(os.path.join(out, "ears_attached.json"), "w"), indent=1)
    for b, r in res.items(): print(b, r["family"], "H %.2f ext %.2f scale %.3f" % (r["l"]["auricle_height_cm"], r["l"]["lateral_extent_from_skull_root_cm"], r["l"]["scale"]))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
