"""RAC W1e: attach the accepted ear-family reference geometry (ear_families_v2) to a candidate body (author decisions E-D1...E-D6).
The generator's human auricle is collapsed onto the side of the head (each ear vertex pulled 85 % toward the skull plane at the
root and 60 % toward the root), and the family ear is placed at the root: ear-local x (lateral) -> +/-x, y (back) -> -f, z (up) -> u.
BUILDER-CHOSEN attachment rule: family geometry (authored at MF-M-R head scale) is scaled uniformly by HH(body) / HH(MF-M-R);
PK-compact and CG-finefolded were authored in absolute cm for the PK-NAT / CG-NAT heads (ear
height / HH 0.30-0.31, MF 0.28; PK canon: no mandatory tiny ears) and are attached unscaled;
the anterior attachment line sits 0.2 cm behind the front of the generator auricle, 0.15 cm inside the medial root, and the
auricle's vertical midpoint sits at the generator auricle's vertical midpoint.
Writes a composite npz (body + ears) for evidence renders, plus the ear landmark readings in the body frame.
The composite is EVIDENCE GEOMETRY; body measurements stay on the body npz (ears excluded from head metrics as before).
Usage: python3 attach_ears.py body_r6.npz FAMILY out_npz   (reads body_meas.json beside the npz for HH)"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ear_families_v2 as E

OWN_SCALE = {"PK-compact", "CG-finefolded"}           # authored at their own head scale
HH_MF = 22.51                                           # MF-M-R HH (W1c accepted reference, cm)

def attach(npz, family, out, HH):
    D = dict(np.load(npz, allow_pickle=True)); V = D["V"].astype(float).copy(); F = D["F"]; keep = D["keep"]; we = D["w_ears"]
    Ve, Fe, p, q = E.build(family); sc = 1.0 if family in OWN_SCALE else HH / HH_MF; Ve = Ve * sc
    newV, newF, rec = [V], [F], {"family": family}
    off = len(V)
    for side, sgn in (("l", 1), ("r", -1)):
        idx = np.where(keep & (we > 0.5) & (V[:, 0] * sgn > 0))[0]
        P = V[idx]
        # root: the most medial ear vertices (attachment), centroid of the 25 % closest to the midline
        k = np.argsort(np.abs(P[:, 0]))[: max(4, len(P) // 4)]
        root = P[k].mean(0).copy()
        rx = root[0] - 0.15 * sgn; rf = P[:, 1].max() - 0.2; ru = 0.5 * (P[:, 2].min() + P[:, 2].max()) - 0.5 * (Ve[:, 2].min() + Ve[:, 2].max())
        # collapse the generator auricle onto the head side
        P2 = P.copy()
        P2[:, 0] = root[0] + (P[:, 0] - root[0]) * 0.15
        P2[:, 1:] = root[1:] + (P[:, 1:] - root[1:]) * 0.4
        V[idx] = P2
        # place the family ear: local (x lat, y back, z up) -> body (x = sgn*x, f = -y, u = z)
        Ve_b = np.c_[sgn * Ve[:, 0], -Ve[:, 1], Ve[:, 2]] + np.array([rx, rf, ru])
        Fe_b = Fe[:, ::-1] if sgn < 0 else Fe
        newV.append(Ve_b); newF.append(Fe_b + off); off += len(Ve_b)
        sa, sb = Ve_b[:, 2].max(), Ve_b[:, 2].min()
        rec[side] = {"root": [rx, rf, ru], "scale": sc, "superaurale_u": float(sa), "subaurale_u": float(sb), "auricle_height_cm": float(sa - sb),
                     "lateral_extent_from_skull_root_cm": float((Ve_b[:, 0] * sgn).max() - rx * sgn)}
    V2 = np.vstack(newV); F2 = np.vstack(newF); n_add = len(V2) - len(V)
    D2 = dict(D); D2["V"] = V2.astype(np.float32); D2["F"] = F2
    D2["keep"] = np.r_[keep, np.ones(n_add, bool)]
    for k_ in list(D2):
        if k_.startswith("w_"):
            D2[k_] = np.r_[D[k_], np.full(n_add, 1.0 if k_ in ("w_head", "w_ears") else 0.0, np.float32)]
    meta = json.loads(str(D["meta"])); meta["ears"] = {"n_body_verts": int(len(V)), "family": family, "source": "tools/rac/w1/ear_families_v2.py"}; D2["meta"] = json.dumps(meta)
    np.savez_compressed(out, **D2)
    return rec

if __name__ == "__main__":
    meas = sys.argv[1].replace("_r6.npz", "_meas.json")
    r = attach(sys.argv[1], sys.argv[2], sys.argv[3], json.load(open(meas))["combined"]["cranio"]["HH"]); print(json.dumps(r, indent=1))
