"""RAC W1g AD-W1G-8: BONY joint robusticity for the accepted Skarn rows "heavier joints" (SKARN L24 "heavier joints", L78 "larger
joints"). The W1c measure (arm_measure jb) is the SKIN joint breadth / adjacent bone length, composition-inclusive. Bony reading
(BUILDER-CHOSEN, R-14; same principle as bony_envelope.py): joint breadth = INFIMUM over the generator composition grid
{muscle, weight} in {0, .25, .5}^2 of the same skeleton (each body aligned to the reference rig joints), divided by the reference
adjacent bone length (rig joint distance). Skarn anatomy is not changed. Usage: python3 bony_joints.py w1f_dir w1g_dir"""
import sys, glob, json, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skeletal_proxy as SP
from arm_measure import measure
F, G = sys.argv[1], sys.argv[2]
out = {}
for cid, extra in (("MF-M-R", [F + '/low/MF-M-R-LOW_rest.npz']), ("SK", [])):
    comps = [F + '/final_lean/%s-LEAN_rest.npz' % cid, F + '/final/%s_rest.npz' % cid] + sorted(glob.glob(G + '/comp/%s-C*_rest.npz' % cid)) + extra
    rows = {}
    for p in comps:
        a = os.path.join(tempfile.mkdtemp(), 'a.npz'); SP.align(p, F + '/final/%s_rest.npz' % cid, a); M = measure(a)["mean"]
        rows[os.path.basename(p)] = {k: M[k] for k in ("elbow_breadth", "knee_breadth", "wrist_breadth", "upperarm", "thigh", "forearm")}
    ref = rows[cid + '_rest.npz']
    o = {"per_body": rows}
    for j, bone in (("elbow_breadth", "upperarm"), ("knee_breadth", "thigh"), ("wrist_breadth", "forearm")):
        mn = min(rows, key=lambda k: rows[k][j]); o[j] = {"bony_cm": rows[mn][j], "argmin": mn, "bone_cm": ref[bone], "ratio": rows[mn][j] / ref[bone], "skin_ratio": ref[j] / ref[bone], "skin_cm": ref[j]}
    out[cid] = o
json.dump(out, open(G + '/bony_joints.json', 'w'), indent=1, default=float)
for cid in out:
    print(cid, {j: (round(out[cid][j]["bony_cm"], 2), round(out[cid][j]["ratio"], 4), out[cid][j]["argmin"], round(out[cid][j]["skin_cm"], 2)) for j in ("elbow_breadth", "knee_breadth", "wrist_breadth")})
