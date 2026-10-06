"""RAC W1f: GO L775 matched-display silhouette test / ALPC-8 (Durrim vs Gorrund), on the same stations.
Both bodies at the SAME neutralized composition (the skeletal-envelope bodies: generator minimum muscle and fat; no clothing,
hair or face presentation in the reference meshes), R-6 stance, each scaled to the same displayed height (display normalization
only - no anatomy is rescaled). Outputs:
- silhouette IoU of the height-normalized front and side masks (1.0 = identical; identical silhouettes FAIL);
- the canon contrasts read on the normalized bodies: torso (axial) vertical contribution, ribcage vertical length, leg (limb)
  contribution, and the normalized breadth / depth profile at stations S2-S6;
- a side-by-side sheet.
Usage: python3 silhouette_test.py du_r6.npz go_r6.npz out_prefix"""
import sys, os, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence as EV
from arm_measure import measure

def mask(V, F, hx, hy, dep, H, px=600):
    pp = px / H; w = int(1.0 * H * pp)
    im = EV.render(V, F, hx, hy, dep, pp, (-0.5 * H, 0), (w, px + 4), 1000, shade_col=(0, 0, 0), amb=1.0)
    a = np.asarray(im.convert("L"))[:-6] < 128; return a, im          # bottom rows hold the ground line

def main(du, go, out):
    R = {}; ims = []; masks = {}
    for tag, p in (("DU", du), ("GO", go)):
        D = np.load(p, allow_pickle=True); V = D["V"].astype(float); F = D["F"]; keep = D["keep"]
        H = V[keep, 2].max() - V[keep, 2].min(); x, f, u = V.T
        mf, imf = mask(V, F, x, u, f, H); ms, ims_ = mask(V, F, f - np.median(f[keep]), u, x, H)
        masks[tag] = (mf, ms); m = measure(p)
        R[tag] = {"stature": H, "torso_share": m["torso_len"] / H, "thoracic_vertical_share": m["thoracic_vertical"] / H,
                  "leg_share": m["mean"]["hip_height"] / H, "neck_share": m["neck_len"] / H,
                  "torso_vertical_over_thoracic_breadth": m["torso_len"] / m["thorax_breadth_max"],
                  "ribcage_vertical_over_thoracic_breadth": m["thoracic_vertical"] / m["thorax_breadth_max"],
                  "stations_over_H": {k: [v[0] / H, v[1] / H] for k, v in m["alpc_stations"].items()}}
        ims.append((tag, imf, ims_))
    iou = {v: float((masks["DU"][k] & masks["GO"][k]).sum() / (masks["DU"][k] | masks["GO"][k]).sum()) for k, v in ((0, "front"), (1, "side"))}
    C = {"silhouette_IoU": iou,
         "torso (axial) vertical contribution GO > DU": [R["GO"]["torso_share"], R["DU"]["torso_share"], R["GO"]["torso_share"] > R["DU"]["torso_share"]],
         "ribcage vertical / stature GO > DU": [R["GO"]["thoracic_vertical_share"], R["DU"]["thoracic_vertical_share"], R["GO"]["thoracic_vertical_share"] > R["DU"]["thoracic_vertical_share"]],
         "torso shape: torso vertical / thoracic breadth GO > DU (DU vertically compact torso)": [R["GO"]["torso_vertical_over_thoracic_breadth"], R["DU"]["torso_vertical_over_thoracic_breadth"], R["GO"]["torso_vertical_over_thoracic_breadth"] > R["DU"]["torso_vertical_over_thoracic_breadth"]],
         "ribcage shape: ribcage vertical / thoracic breadth GO > DU": [R["GO"]["ribcage_vertical_over_thoracic_breadth"], R["DU"]["ribcage_vertical_over_thoracic_breadth"], R["GO"]["ribcage_vertical_over_thoracic_breadth"] > R["DU"]["ribcage_vertical_over_thoracic_breadth"]],
         "leg (limb) contribution GO > DU": [R["GO"]["leg_share"], R["DU"]["leg_share"], R["GO"]["leg_share"] > R["DU"]["leg_share"]]}
    C["identical_silhouettes"] = bool(min(iou.values()) > 0.995)
    res = {"readings": R, "checks": C}
    json.dump(res, open(out + ".json", "w"), indent=1, default=float)
    Wd = sum(i[1].width + i[2].width + 20 for i in ims) + 20; S = Image.new("RGB", (Wd, ims[0][1].height + 40), "white"); d = ImageDraw.Draw(S); xo = 0
    d.text((4, 4), "ALPC-8 / GO L775 matched-display silhouettes (same displayed height; minimum composition)  IoU front %.3f side %.3f" % (iou["front"], iou["side"]), fill=(0, 0, 0))
    for tag, a, b in ims:
        S.paste(a, (xo, 30)); S.paste(b, (xo + a.width + 5, 30)); d.text((xo + 4, 18), tag + " front | side", fill=(0, 0, 0)); xo += a.width + b.width + 25
    S.save(out + ".jpg", quality=88)
    print(json.dumps(C, indent=1, default=float))

if __name__ == "__main__":
    main(*sys.argv[1:4])
