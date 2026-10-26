# elbow_overlap_volume.py OUT.json SIDE BASE.npz NAME=POSED.npz ... : physical (occupied) volume vs closed-mesh (divergence) volume at the elbow.
# The divergence-theorem closed volume counts a self-overlapping region once per covering layer (winding number 2 inside an interpenetration), so W0 LBS at
# deep flexion -- forearm passing through the biceps -- reports the overlap TWICE. Here the generalized winding number w (libigl fast winding number) is
# sampled on a 2 mm grid in a 32 cm box around the posed elbow: overlap = vol{w >= 1.5}; occupied = vol{w >= 0.5}. Physical change vs the elbow-straight
# base pose (D2 base, same shoulder) = (V_div - overlap) - V_div(base) (the box contains every vertex that moves with the elbow).
import sys, os, re, json, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diag_lib import bl_to_src
O, S, BASE = sys.argv[1:4]; items = [a.split('=', 1) for a in sys.argv[4:]]
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); Q = np.asarray(Z['Q']); TRI = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]].astype(np.int64)
def cvol(V): return float(np.einsum('ij,ij->i', V[TRI[:, 0]], np.cross(V[TRI[:, 1]], V[TRI[:, 2]])).sum() / 6)
rig = json.load(open('/tmp/claude-0/rt/rd/rig/rig_v001.json')); B = {b['name']: b for b in rig['bones']}
out = json.load(open(O)) if os.path.exists(O) else {}; vb = cvol(np.load(BASE)['V'].astype(float))
for nm, pth in items:
    V = np.load(pth)['V'].astype(np.float64)
    # posed elbow centre: mean of the vertices nearest the rest pivot (same ids for every candidate)
    if 'ids' not in globals():
        Z0 = Z['V'].astype(float); e = bl_to_src(np.array(B['forearm_' + S]['head'])[None])[0]; ids = np.argsort(np.linalg.norm(Z0 - e, axis=1))[:400]
    c = V[ids].mean(0); h = 0.2; ax = np.arange(-16, 16 + 1e-9, h)
    G = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3) + c
    w = igl.fast_winding_number(V, TRI, G) if hasattr(igl, 'fast_winding_number') else None
    ov = float((w >= 1.5).sum() * h ** 3); occ = float((w >= 0.5).sum() * h ** 3); vd = cvol(V)
    out['%s_%s' % (nm, re.search(r'flex(\d+)', pth).group(1))] = dict(side=S, closed_div_cm3=round(vd, 1), overlap_cm3=round(ov, 1), occupied_box_cm3=round(occ, 1), closed_minus_overlap_cm3=round(vd - ov, 1),
                                                          div_change_vs_base_cm3=round(vd - vb, 1), physical_change_vs_base_cm3=round(vd - ov - vb, 1))
    print(nm, S, out['%s_%s' % (nm, re.search(r'flex(\d+)', pth).group(1))], flush=True)
json.dump(out, open(O, 'w'), indent=1)
