# RM-OT-05P stage A: CORONAL articulated stance correction (bow-legged presentation) from the declared baseline.
# Chain per leg (left leg X>0; right leg is the exact mirror): hip H, knee K, ankle A (from p_legaxes on the baseline).
#   T_thigh = rotation about the AP (Y-parallel) axis through H by t1 (adduction), chosen so K lands on the H-A line;
#   T_shank = T_thigh then rotation about the AP axis through the moved knee by t2, chosen so the ankle returns to its
#             original X (stance width kept - the broad pelvic stance is not collapsed);
#   T_foot  = T_shank then rotation about the AP axis through the moved ankle by -(t1+t2) so the sole stays flat.
# Rigid segment rotations (lengths exact); linear-blend weights: pelvis->thigh ramp z_top..z_bot, thigh->shank band
# knee_z +/- kb, shank->foot band ankle_z +/- fb; the two legs blend 50/50 across the midline (|X| < 2 cm). Forearms /
# hands are separate mesh components and keep weight 0. Grounding: one vertical translation back to z = 0.
# Usage: python3 p_coronal.py --in BASE.obj --axes AXES.json --out OUT.obj [--z_top 120 --z_bot 98 --kb 5 --fb 4]
import argparse, json, numpy as np, trimesh, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
ap = argparse.ArgumentParser(); ap.add_argument('--in', dest='inp'); ap.add_argument('--axes'); ap.add_argument('--out')
ap.add_argument('--z_top', type=float, default=120.0); ap.add_argument('--z_bot', type=float, default=98.0); ap.add_argument('--kb', type=float, default=5.0); ap.add_argument('--fb', type=float, default=4.0)
a = ap.parse_args(); m = trimesh.load(a.inp, process=False); V = np.asarray(m.vertices, float); F = np.asarray(m.faces)
L = json.load(open(a.axes)); H = np.array(L['hip']); K = np.array(L['knee']); A = np.array(L['ankle'])
def roty(P, c, t):
    q = np.atleast_2d(P) - c; ct, st = np.cos(t), np.sin(t); return np.c_[q[:, 0] * ct + q[:, 2] * st, q[:, 1], -q[:, 0] * st + q[:, 2] * ct] + c
# t1: knee onto the hip-ankle line (in XZ)
u = (K[2] - H[2]) / (A[2] - H[2]); lx = H[0] + u * (A[0] - H[0]); dk = K - H
t1 = np.arctan2(dk[0], -dk[2]) - np.arctan2(lx - H[0], -(K[2] - H[2]))
K1 = roty(K, H, t1)[0]; A1 = roty(A, H, t1)[0]
# t2: rotate the shank about the moved knee so the ankle returns to its original X
da = A1 - K1; rxz = np.hypot(da[0], da[2]); t2 = np.arctan2(da[0], -da[2]) - np.arcsin(np.clip((A[0] - K1[0]) / rxz, -1, 1))   # roty turns the from-vertical angle phi into phi - t
A2 = roty(A1, K1, t2)[0]
sub = V[:, 2] < a.z_top + 6; fm = sub[F].all(1); E = np.vstack([F[fm][:, [0, 1]], F[fm][:, [1, 2]], F[fm][:, [2, 0]]])
Am = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(len(V), len(V))); nc, lab = connected_components(Am, directed=False)
legs = (lab == np.bincount(lab[V[:, 2] < 3]).argmax()) & sub
ss = lambda t: (lambda q: q * q * (3 - 2 * q))(np.clip(t, 0, 1))
def chain(P):          # left-leg chain applied to points P (already in the left frame)
    Pt = roty(P, H, t1); Ps = roty(Pt, K1, t2); Pf = roty(Ps, A2, -(t1 + t2)); return Pt, Ps, Pf
def legmove(P):
    z = P[:, 2]; wl = ss((a.z_top - z) / (a.z_top - a.z_bot)); wsh = ss((K[2] + a.kb - z) / (2 * a.kb)); wf = ss((A[2] + a.fb - z) / (2 * a.fb))
    Pt, Ps, Pf = chain(P); leg = Pt * (1 - wsh)[:, None] + (Ps * (1 - wf)[:, None] + Pf * wf[:, None]) * wsh[:, None]
    return P * (1 - wl)[:, None] + leg * wl[:, None]
mir = np.array([-1, 1, 1.0])
out = V.copy(); idx = np.where(legs)[0]; P = V[idx]
ml = legmove(P); mr = legmove(P * mir) * mir              # left-leg chain and its mirror for the right leg
sl = ss((P[:, 0] + 2.0) / 4.0); out[idx] = ml * sl[:, None] + mr * (1 - sl)[:, None]
dz = -out[:, 2].min(); out[:, 2] += dz
trimesh.Trimesh(out, F, process=False).export(a.out)
m0 = trimesh.Trimesh(V, F, process=False); m1 = trimesh.Trimesh(out, F, process=False)
leg_vol = lambda M: None
rec = dict(input=a.inp, output=a.out, t1_hip_adduction_deg=round(float(np.degrees(t1)), 2), t2_knee_coronal_deg=round(float(np.degrees(t2)), 2), foot_counter_deg=round(float(-np.degrees(t1 + t2)), 2),
           landmarks_before=dict(hip=H.round(2).tolist(), knee=K.round(2).tolist(), ankle=A.round(2).tolist()),
           landmarks_after=dict(hip=(H + [0, 0, dz]).round(2).tolist(), knee=(K1 + [0, 0, dz]).round(2).tolist(), ankle=(A2 + [0, 0, dz]).round(2).tolist()),
           thigh_length=[round(float(np.linalg.norm(K - H)), 3), round(float(np.linalg.norm(K1 - H)), 3)], shank_length=[round(float(np.linalg.norm(A - K)), 3), round(float(np.linalg.norm(A2 - K1)), 3)],
           knee_lateral_of_hip_ankle_line_cm=[round(float(K[0] - lx), 2), round(float(K1[0] - (H[0] + (K1[2] - H[2]) / (A2[2] - H[2]) * (A2[0] - H[0]))), 2)],
           ankle_x=[round(float(A[0]), 2), round(float(A2[0]), 2)], grounding_dz_cm=round(float(dz), 2),
           stature_maxz=[round(float(V[:, 2].max()), 2), round(float(out[:, 2].max()), 2)], volume_L=[round(m0.volume / 1000, 2), round(m1.volume / 1000, 2)],
           max_vertex_displacement_cm=round(float(np.linalg.norm(out - V, axis=1).max()), 2), leg_vertices=int(legs.sum()),
           weights=dict(z_top=a.z_top, z_bot=a.z_bot, knee_band=a.kb, foot_band=a.fb, midline_blend='|X|<2 cm 50/50'))
json.dump(rec, open(a.out.replace('.obj', '_record.json'), 'w'), indent=1); print(json.dumps(rec, indent=1))
