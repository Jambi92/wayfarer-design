# RM-OT-05V measurement audit of the neutral ARM candidate: R-13 stature (skull vertex vs raw extent), R-6 stance, R-5 bilateral
# residual, foot digits / plantigrade contact, crotch relation, garment / hair residue screen. Read-only.
# Usage: python3 v_measure.py STATE.npz OUT.json
import sys, json, numpy as np, trimesh
from scipy.spatial import cKDTree
X0 = -0.5
d = np.load(sys.argv[1]); V = d['V'].astype(np.float64); F = d['F']; fg = d['fgrp']; vid = d['vid']
m = trimesh.Trimesh(V, F, process=False); X = V[:, 0] - X0; Y = V[:, 1]; Z = V[:, 2]; out = {}
def sec(z, sel=None):
    s = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    return [] if s is None else [e for e in s.discrete if (sel is None or sel(e.mean(0)))]
# ---- R-13 stature
ground = float(Z.min()); top = int(np.argmax(Z))
ear_zone = (np.abs(X) > 9.0) & (Z > 222)
cv = np.where(~ear_zone & (np.abs(X) < 8.0) & (Z > 200))[0]; vx = cv[np.argmax(Z[cv])]
out['R13_stature'] = dict(ground_z_cm=round(ground, 3), raw_full_extent_cm=round(float(Z[top] - ground), 2), raw_top_vertex_xyz=np.round(V[top], 2).tolist(),
    raw_top_is=('ear' if ear_zone[top] else 'cranium'), skull_vertex_xyz=np.round(V[vx], 2).tolist(), skull_vertex_label=int(np.bincount(fg[(F == vx).any(1)]).argmax()),
    anatomical_stature_cm=round(float(Z[vx] - ground), 2), GOREF_cm=230.9, nominal_cm=229.0, delta_vs_GOREF_cm=round(float(Z[vx] - ground - 230.9), 2),
    note='skull vertex = highest point of the cranial vault with ears (lateral pinnae) excluded; no hair, mane or keratin display remains. '
         'The vault is INFERRED (builder-chosen ellipsoid, plan step E), so this stature is a construction value, not a discovered measurement.')
# ---- trunk / limb axes
def centroid_at(z, xsign=None, xmin=None):
    L = sec(z, (lambda c: (xsign is None or np.sign(c[0] - X0) == xsign) and (xmin is None or abs(c[0] - X0) > xmin)))
    if not L: return None
    L = max(L, key=lambda e: np.linalg.norm(np.diff(e, axis=0), axis=1).sum()); return L.mean(0)
def ang(a, b):   # angle of a->b from vertical (deg), plus frontal (x) and sagittal (y) components
    v = np.asarray(b) - np.asarray(a); return dict(from_vertical_deg=round(float(np.degrees(np.arccos(abs(v[2]) / np.linalg.norm(v)))), 2),
        frontal_deg=round(float(np.degrees(np.arctan2(v[0], abs(v[2])))), 2), sagittal_deg=round(float(np.degrees(np.arctan2(v[1], abs(v[2])))), 2))
legs = {}
for s, nm in ((1, '+X'), (-1, '-X')):
    hip = centroid_at(90, s); knee = centroid_at(57, s); ankle = centroid_at(14, s)
    if hip is None or knee is None or ankle is None: continue
    t = np.asarray(knee) - hip; sh = np.asarray(ankle) - knee
    flex = float(np.degrees(np.arccos(np.dot(t, sh) / np.linalg.norm(t) / np.linalg.norm(sh))))
    legs[nm] = dict(thigh_axis=ang(hip, knee), shank_axis=ang(knee, ankle), knee_angle_between_segments_deg=round(flex, 2),
                    thigh_centroid_z90=np.round(hip, 2).tolist(), knee_centroid_z57=np.round(knee, 2).tolist(), ankle_centroid_z14=np.round(ankle, 2).tolist())
arms = {}
for s, nm in ((1, '+X'), (-1, '-X')):
    up = centroid_at(152, s, xmin=22); wr = centroid_at(108, s, xmin=30)
    if up is None or wr is None: continue
    arms[nm] = dict(upper_arm_centroid_z152=np.round(up, 2).tolist(), wrist_centroid_z108=np.round(wr, 2).tolist(), arm_axis=ang(up, wr),
                    abduction_deg=round(float(np.degrees(np.arctan2(abs(wr[0] - X0) - abs(up[0] - X0), up[2] - wr[2]))), 2))
trunk = [centroid_at(z, None) for z in (115, 135, 160)]
feet = {}
for s, nm in ((1, '+X'), (-1, '-X')):
    P = V[(np.sign(X) == s) & (Z < 12) & (np.abs(X) > 5)]
    heel = P[P[:, 1] < P[:, 1].min() + 6].mean(0); toe = P[P[:, 1] > P[:, 1].max() - 6].mean(0)
    soleP = P[P[:, 2] < ground + 0.35]
    heel_contact = int((soleP[:, 1] < P[:, 1].min() + 15).sum()); fore_contact = int((soleP[:, 1] > P[:, 1].max() - 25).sum())
    # five-digit check: forward-extent profile across the forefoot, local maxima separated by clefts
    Q = P[(P[:, 2] < 9) & (P[:, 1] > P[:, 1].max() - 14)]; xs = np.arange(Q[:, 0].min(), Q[:, 0].max(), 0.4)
    prof = np.array([Q[(Q[:, 0] >= x) & (Q[:, 0] < x + 0.4)][:, 1].max() if ((Q[:, 0] >= x) & (Q[:, 0] < x + 0.4)).any() else np.nan for x in xs])
    peaks = []
    for i in range(2, len(prof) - 2):
        w = prof[max(0, i - 4):i + 5]
        if np.isfinite(prof[i]) and prof[i] >= np.nanmax(w) - 1e-9:
            if not peaks or xs[i] - peaks[-1][0] > 2.5: peaks.append((float(xs[i]), float(prof[i])))
    clefts = [round(float(np.nanmin(prof[(xs > a[0]) & (xs < b[0])])), 2) for a, b in zip(peaks, peaks[1:])]
    feet[nm] = dict(heel_xy=np.round(heel[:2], 2).tolist(), toe_xy=np.round(toe[:2], 2).tolist(), foot_length_cm=round(float(P[:, 1].max() - P[:, 1].min()), 2),
                    foot_axis_yaw_deg=round(float(np.degrees(np.arctan2(toe[0] - heel[0], toe[1] - heel[1]))), 2),
                    sole_contact_vertices=int(len(soleP)), heel_contact_vertices=heel_contact, forefoot_contact_vertices=fore_contact,
                    heel_lowest_z_cm=round(float(P[P[:, 1] < P[:, 1].min() + 10][:, 2].min() - ground), 3),
                    digit_tips=len(peaks), digit_tip_x=[round(p[0], 1) for p in peaks], cleft_depth_y=clefts)
out['R6_stance'] = dict(legs=legs, arms=arms, feet=feet, trunk_centroids_z115_135_160=[np.round(t, 2).tolist() if t is not None else None for t in trunk],
                        trunk_axis=ang(trunk[0], trunk[2]) if trunk[0] is not None and trunk[2] is not None else None,
                        heel_separation_cm=round(abs(feet['+X']['heel_xy'][0] - feet['-X']['heel_xy'][0]), 2) if len(feet) == 2 else None,
                        hip_separation_cm=round(abs(legs['+X']['thigh_centroid_z90'][0] - legs['-X']['thigh_centroid_z90'][0]), 2) if len(legs) == 2 else None)
# ---- muzzle / head carriage: brow (forehead front at z 221) to muzzle tip
mz = V[(Z > 190) & (Z < 215) & (np.abs(X) < 4)]; tip = mz[np.argmax(mz[:, 1])]
out['head_carriage'] = dict(muzzle_tip=np.round(tip, 2).tolist(), note='qualitative; read with the profile render')
# ---- crotch relation (05O o_crotch method: lowest midline point between 30 % and 60 % of the anatomical stature)
st = out['R13_stature']['anatomical_stature_cm']; b = V[np.abs(X) < 1.0]; b = b[(b[:, 2] - ground > 0.3 * st) & (b[:, 2] - ground < 0.6 * st)]
cr = float(b[:, 2].min() - ground) if len(b) else None
out['crotch'] = dict(crotch_height_cm=round(cr, 2) if cr else None, crotch_over_stature=round(cr / st, 4) if cr else None, W2D_series=[0.452, 0.475], source_05N='0.46 H')
# ---- R-5 bilateral residual (body only, z 20-200)
P = V[(Z > 20) & (Z < 200)]; M = P.copy(); M[:, 0] = 2 * X0 - M[:, 0]; r = cKDTree(P).query(M)[0]
out['R5_bilateral'] = dict(median_mirror_residual_cm=round(float(np.median(r)), 3), p90_cm=round(float(np.percentile(r, 90)), 3), max_cm=round(float(r.max()), 3))
# ---- labels
out['labels'] = {str(k): int(v) for k, v in zip(*np.unique(fg, return_counts=True))}
out['inferred_area_fraction'] = round(float(m.area_faces[fg != 0].sum() / m.area), 4)
json.dump(out, open(sys.argv[2], 'w'), indent=1); print(json.dumps(out, indent=1)[:4000])
