# elbow_girth.py OUT.json SIDE ANGLE NAME=POSED.npz ... : limb girth balloon / collapse check (order 69f2660 §10 visual). Rings of the arm part at fixed REST
# axial distances (4..14 cm) from the elbow pivot along the upper-arm and forearm axes; for each ring the mean distance of its vertices from the POSED bone line
# (upper arm: posed shoulder -> posed elbow; forearm: posed elbow -> posed wrist, from the rig pose matrices of the D2 pose) is compared with the same ring in the
# straight-elbow base pose. Reported per ring: all-around mean radius change (cm) and the change on the outer half (away from the contact side).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
from diag_lib import Rig, build_poses, bl_to_src
os.environ.setdefault('ELBOW_SET', '1'); os.environ.setdefault('ELBOW_SET_R', '1'); os.environ.setdefault('ELBOW_ARC', '1')
O, S, A = sys.argv[1:4]; items = [a.split('=', 1) for a in sys.argv[4:]]
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']
RD = '/tmp/claude-0/rt/rd'; rig = Rig(RD + '/rig/rig_v001.json', RD + '/rig/weights_v001c.npz'); P = build_poses(rig)
def joints(pn):
    M, _ = rig.pose_mats(P[pn]); g = lambda b: bl_to_src(M[b][:3, 3][None])[0]
    return g('upperarm_' + S), g('forearm_' + S), g('hand_' + S)
sh0, el0, wr0 = joints('D2_%s_base_abd45' % S); sh1, el1, wr1 = joints('D2_%s_flex%s' % (S, A))
ua = (el0 - sh0) / np.linalg.norm(el0 - sh0); fa = (wr0 - el0) / np.linalg.norm(wr0 - el0)
arm = np.zeros(len(V0), bool); arm[Q[FP == PARTS.index('arm_' + S)].ravel()] = True
Vb = np.load(items[0][1])['V'].astype(float)                           # base posed (straight elbow): rings defined on it
ring = {}
for seg, axv in (('upper', -ua), ('fore', fa)):
    t = (Vb - el0) @ axv
    for k in (4, 6, 8, 10, 12, 14): ring['%s_%d' % (seg, k)] = np.nonzero(arm & (np.abs(t - k) < 0.3) & (np.linalg.norm((Vb - el0) - np.outer(t, axv), axis=1) < 10))[0]
def radius(V, ids, a, b):
    d = (b - a) / np.linalg.norm(b - a); q = V[ids] - a; r = q - np.outer(q @ d, d); return np.linalg.norm(r, axis=1), r
out = json.load(open(O)) if os.path.exists(O) else {}; base = {}
for nm, pth in items:
    V = np.load(pth)['V'].astype(float); row = {}
    for key, ids in ring.items():
        a, b = ((sh0, el0) if nm == items[0][0] else (sh1, el1)) if key.startswith('upper') else ((el0, wr0) if nm == items[0][0] else (el1, wr1))
        r, rv = radius(V, ids, a, b)
        if nm == items[0][0]: base[key] = r
        r0 = base[key]; dr = r - r0
        # outer half = vertices whose base radial direction points away from the other segment (dot with the base flexion-side direction < 0)
        row[key] = dict(mean_dr_cm=round(float(dr.mean()), 3), p90_dr_cm=round(float(np.percentile(dr, 90)), 3), min_dr_cm=round(float(dr.min()), 3))
    out['%s_%s_%s' % (nm, S, A)] = row
    print(nm, S, A, ' '.join('%s %+.2f' % (k, v['mean_dr_cm']) for k, v in row.items()))
json.dump(out, open(O, 'w'), indent=1)
