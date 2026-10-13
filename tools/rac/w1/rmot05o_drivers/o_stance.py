# RAC RM-OT-05O §3: STANCE-ONLY articulated correction of GO-RD2-REF (or its LOW companion with the same landmarks).
#
# Measured on RD2 (o_legaxes.py): the knee is nearly straight (sagittal thigh/shank inclinations -16.9 / -14.5 deg),
# but the WHOLE leg slopes backward from the hip: ankle 26.8 cm posterior of the hip centre, foot held flat by ~16 deg of
# ankle dorsiflexion, trunk vertical. The correction is therefore a hip rotation, not a knee straightening:
#   T_leg  = rotation about the hip axis (the X-parallel line through both hip centres, which share y and z) by phi, chosen
#            so the hip-ankle line becomes vertical in the sagittal plane;
#   T_foot = T_leg followed by the opposite rotation about the ankle centre, so the sole returns to flat plantigrade contact;
#   pelvis / trunk / arms / head untouched. Knee angle unchanged (no straightening, no hyperextension).
# Skin weights (linear blend): leg weight ramps from 0 at z_top to 1 at z_bot (smoothstep) inside the pelvis-and-legs mesh
# component only (forearms / hands, which hang beside the thighs as separate components, keep weight 0); foot weight ramps
# from 0 at ankle_z + foot_band to 1 at ankle_z - foot_band/2. Rigid rotations keep thigh and shank lengths exact.
# Grounding: one vertical translation that returns the lowest sole point to z = 0 (reported; no limb or global scaling).
# Usage: python3 o_stance.py --in MESH.obj --axes LEGAXES.json --out OUT.obj [--z_top 116 --z_bot 94 --foot_band 4]
import argparse, json, numpy as np, trimesh
from scipy.sparse.csgraph import connected_components
ap = argparse.ArgumentParser(); ap.add_argument('--in', dest='inp', required=True); ap.add_argument('--axes', required=True); ap.add_argument('--out', required=True)
ap.add_argument('--z_top', type=float, default=116.0); ap.add_argument('--z_bot', type=float, default=94.0); ap.add_argument('--foot_band', type=float, default=4.0)
ap.add_argument('--phi_deg', type=float, default=None, help='override; default = make the hip-ankle line vertical'); a = ap.parse_args()
m = trimesh.load(a.inp, process=False); V = np.asarray(m.vertices, float); F = np.asarray(m.faces)
L = json.load(open(a.axes)); hip = np.array(L['hip']); knee = np.array(L['knee']); ankle = np.array(L['ankle'])
phi = np.radians(a.phi_deg) if a.phi_deg is not None else np.arctan2(hip[1] - ankle[1], hip[2] - ankle[2])
def rotx(P, c, t):
    q = P - c; cy, sy = np.cos(t), np.sin(t)
    return np.c_[q[:, 0], q[:, 1] * cy - q[:, 2] * sy, q[:, 1] * sy + q[:, 2] * cy] + c
hipc = np.array([0.0, hip[1], hip[2]]); ank_new = rotx(ankle[None], hipc, phi)[0]
# --- weights: leg region = pelvis-and-legs component of the sub-mesh below z_top + 6 (arms excluded)
sub = np.where(V[:, 2] < a.z_top + 6)[0]; inside = np.zeros(len(V), bool); inside[sub] = True
fm = inside[F].all(1); E = np.vstack([F[fm][:, [0, 1]], F[fm][:, [1, 2]], F[fm][:, [2, 0]]])
import scipy.sparse as sp
A = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(len(V), len(V)))
nc, lab = connected_components(A, directed=False)
low_feet = np.where(V[:, 2] < 3)[0]; legs_lab = np.bincount(lab[low_feet]).argmax(); legmask = (lab == legs_lab) & inside
ss = lambda t: (lambda u: u * u * (3 - 2 * u))(np.clip(t, 0, 1))
w_leg = ss((a.z_top - V[:, 2]) / (a.z_top - a.z_bot)) * legmask
fz0, fz1 = ankle[2] + a.foot_band, ankle[2] - a.foot_band / 2
w_foot = ss((fz0 - V[:, 2]) / (fz0 - fz1)) * legmask
P_leg = rotx(V, hipc, phi)
anc = np.array([0.0, ankle[1], ankle[2]])
P_foot = rotx(rotx(V, anc, -phi), hipc, phi)          # foot keeps its orientation, carried by the leg rotation
out = V * (1 - w_leg)[:, None] + (w_leg * (1 - w_foot))[:, None] * P_leg + (w_leg * w_foot)[:, None] * P_foot
dz = -out[:, 2].min(); out[:, 2] += dz
tr = lambda p, foot=False: (rotx(rotx(p[None], anc, -phi), hipc, phi)[0] if foot else rotx(p[None], hipc, phi)[0]) + [0, 0, dz]
hip_n = hip + [0, 0, dz]; knee_n = tr(knee); ankle_n = tr(ankle)
trimesh.Trimesh(out, F, process=False).export(a.out)
disp = np.linalg.norm(out - V, axis=1)
rec = dict(input=a.inp, output=a.out, phi_deg=round(float(np.degrees(phi)), 2), hip_axis=dict(point=hipc.tolist(), direction=[1, 0, 0]),
           ankle_axis=dict(point=anc.tolist(), direction=[1, 0, 0]), weights=dict(z_top=a.z_top, z_bot=a.z_bot, foot_band=a.foot_band, leg_vertices=int((w_leg > 0).sum()), excluded='forearms / hands (separate components)'),
           grounding_dz_cm=round(float(dz), 2),
           landmarks_before=dict(hip=hip.round(2).tolist(), knee=knee.round(2).tolist(), ankle=ankle.round(2).tolist()),
           landmarks_after=dict(hip=np.round(hip_n, 2).tolist(), knee=np.round(knee_n, 2).tolist(), ankle=np.round(ankle_n, 2).tolist()),
           thigh_length=[round(float(np.linalg.norm(knee - hip)), 3), round(float(np.linalg.norm(knee_n - hip_n)), 3)],
           shank_length=[round(float(np.linalg.norm(ankle - knee)), 3), round(float(np.linalg.norm(ankle_n - knee_n)), 3)],
           hip_ankle_sagittal_offset_cm=[round(float(hip[1] - ankle[1]), 2), round(float(hip_n[1] - ankle_n[1]), 2)],
           stature=[round(float(V[:, 2].max()), 2), round(float(out[:, 2].max()), 2)],
           max_vertex_displacement_cm=round(float(disp.max()), 2), knee_angle='unchanged (rigid leg rotation)')
json.dump(rec, open(a.out.replace('.obj', '_record.json'), 'w'), indent=1); print(json.dumps(rec, indent=1))
