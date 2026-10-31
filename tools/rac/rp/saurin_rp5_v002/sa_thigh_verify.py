# sa_thigh_verify.py : RP5 full-cage order §3 / §22 thigh-cleanup verification gate on SA_RP5_WORK_v001 vs v000 (canonical), both configurations.
#   geometry: changed set == authorized patch (leg-labelled, u 66-84 on SA-M188, medial / posterior sector), every other base vertex bit-identical;
#   relief: the sa_thigh.py diagnosis re-run on v001 (sector statistics, hotspots);  W2 canon: stature, bbox, closed volume, leg / thigh / pelvis / lower-trunk
#   section areas + perimeters, tail / head identity metrics (sa_identity definitions);  silhouette IoU (front / profile L+R / rear / 3-4) at 3 px / cm with the
#   tail, plus a 12 px / cm thigh crop;  c1 / c2 route coherence (same changed set, same rule).
import sys, os, json, hashlib, subprocess, numpy as np, igl
from PIL import Image, ImageDraw
W = '/tmp/claude-0/rt/sa'; R = '/home/claude/wayfarer-design/tools/rac/rp'
b = np.load(W + '/src/saurin_w2_final_base.npz'); F = b['f'].astype(np.int64)
V0 = {'SA-M188': b['v'].astype(float), 'SA-F188': np.load(W + '/src/saurin_w2_SA-F188_realization.npz')['v'].astype(float)}
z = np.load(W + '/work/SA_RP5_WORK_v001.npz'); V1 = {'SA-M188': z['v_M'].astype(float), 'SA-F188': z['v_F'].astype(float)}
lab = np.load(W + '/lm/SA-M188_regions.npz')['label']; LM = json.load(open(W + '/lm/SA-M188_landmarks.json'))['landmarks']
res = {}
# 1. geometry locality
for bid in V0:
    d = np.linalg.norm(V1[bid] - V0[bid], axis=1); auth = np.load(W + '/work/%s_changed_idx.npy' % bid); ch = auth; Vm = V0['SA-M188']
    moved = np.nonzero(d > 0)[0]; assert np.isin(moved, auth).all(), 'vertex moved outside the authorized set'
    res.setdefault('geometry', {})[bid] = dict(changed=int(len(ch)), all_leg=bool(np.isin(lab[ch], ['leg_xneg', 'leg_xpos']).all()),
        u_range_on_SA_M188_cm=[round(float(Vm[ch, 2].min()), 3), round(float(Vm[ch, 2].max()), 3)], inside_63_87_incl_3cm_ramps=bool((Vm[ch, 2] >= 63).all() and (Vm[ch, 2] <= 87).all()), full_strength_band_cm=[66, 84],
        unchanged_outside_bit_identical=bool((V1[bid][np.setdiff1d(np.arange(len(Vm)), ch)] == V0[bid][np.setdiff1d(np.arange(len(Vm)), ch)].astype(np.float32).astype(float)).all()),
        max_disp_mm=round(float(d.max() * 10), 3))
res['geometry']['same_changed_set_c1_c2'] = bool(np.array_equal(np.load(W + '/work/SA-M188_changed_idx.npy'), np.load(W + '/work/SA-F188_changed_idx.npy')))
# 2. relief diagnosis re-run (same code, v001 arrays)
os.makedirs(W + '/work/v001src', exist_ok=True)
np.savez(W + '/work/v001src/saurin_w2_final_base.npz', v=z['v_M'], f=z['f']); np.savez(W + '/work/v001src/saurin_w2_SA-F188_realization.npz', v=z['v_F'])
os.symlink(W + '/src/saurin_w2_final_surface_delta.npz', W + '/work/v001src/saurin_w2_final_surface_delta.npz') if not os.path.exists(W + '/work/v001src/saurin_w2_final_surface_delta.npz') else None
subprocess.run(['python3', R + '/saurin_rp5_v001/sa_thigh.py', W + '/work/v001src', W + '/lm', W + '/work/thigh_v001'], stdout=subprocess.DEVNULL, check=True)
d0 = json.load(open('/home/claude/wayfarer-design/reviews/rac-rp5-evidence/saurin/thigh/SAURIN_thigh_artdebt_diagnosis.json')); d1 = json.load(open(W + '/work/thigh_v001/SAURIN_thigh_artdebt_diagnosis.json'))
res['relief'] = {bid: {sec: dict(v000=d0[bid][sec], v001=d1[bid][sec]) for sec in ('anterolateral', 'transition', 'medial_posterior')} for bid in V0}
for bid in V0: res['relief'][bid]['hotspots'] = dict(v000=dict(threshold_mm=d0[bid]['hotspot_threshold_mm'], vertices=d0[bid]['hotspot_vertices']),
                                                    v001_at_v000_threshold=None, v001=dict(threshold_mm=d1[bid]['hotspot_threshold_mm'], vertices=d1[bid]['hotspot_vertices']))
# hotspot count of v001 at the ORIGINAL threshold (the tear / marks above the v000 p99.5 level)
# fine-scale defect measures (the marks / striations and the folded tear are sub-1.5-cm): fine relief energy (sigma 0.7 cm high-pass |rel|, sigma-0.7
# averaged, mm) p99 per sector and the count of folded / crumpled vertices (normal deviation > 12 deg from the 3-ring averaged normal) per sector
src_ = open(R + '/saurin_rp5_v002/sa_thigh_v001.py').read().split('out = {}; Vnew')[0].replace('SRC, LMD, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True)', "SRC, LMD, OUT = W + '/src', W + '/lm', W + '/work'")
ns = {'W': W}; exec(src_, ns); ns_sub = ns['relief'](V0['SA-M188'])['sub']          # the SA-M188 leg sub-mesh (shared vertices) for every body / version
for bid in V0:
    sub0 = None; fm = {}
    for tag, Vv in (('v000', V0[bid]), ('v001', V1[bid])):
        Rr = ns['relief'](Vv, ns_sub)
        Vs_, N_, al_ = Rr['Vs'], Rr['N'], Rr['al']; rf = np.einsum('ij,ij->i', Vs_ - Rr['Hf'](Vs_), N_); mag = Rr['Hf'](np.abs(rf)) * 10; nv = ns['normal_var'](N_, Rr['A'])
        band = (V0['SA-M188'][ns_sub, 2] > 66) & (V0['SA-M188'][ns_sub, 2] < 84)
        wfull = np.zeros(len(ns_sub), bool); wfull[np.isin(ns_sub, np.load(W + '/work/SA-M188_changed_idx.npy'))] = True
        wv = np.zeros(len(V0['SA-M188'])); zz_ = np.load(W + '/work/SA_RP5_WORK_v001_weights.npz'); wv[zz_['sub']] = zz_['w']; wsub = wv[ns_sub]
        fm[tag] = {sec: dict(fine_relief_energy_p99_mm=round(float(np.percentile(mag[mk], 99)), 3), folded_vertices_gt12deg=int((nv[mk] > 12).sum()),
                             folded_vertices_gt12deg_in_full_strength_patch=int((nv[mk & (wsub >= 0.5)] > 12).sum()))
                   for sec, mk in (('anterolateral', band & (al_ > 0.35)), ('transition', band & (np.abs(al_) <= 0.35)), ('medial_posterior', band & (al_ < -0.35)))}
    res['relief'][bid]['fine_scale'] = fm
    zz = np.load(W + '/work/thigh_v001/%s_thigh_relief.npz' % bid); sub, rel, al = zz['sub'], zz['rel'], zz['al']; Vb = V1[bid][sub]; band = (Vb[:, 2] > 66) & (Vb[:, 2] < 84)
    res['relief'][bid]['hotspots']['v001_at_v000_threshold'] = int((band & (al < 0.35) & (np.abs(rel) * 10 > d0[bid]['hotspot_threshold_mm'])).sum())
# 3. W2 canon measures
def vol(V): return float(igl.volume(V, F[:, :3]) if hasattr(igl, 'volume') else 0)
def signed_volume(V): a, bb, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]; return float(np.einsum('ij,ij->i', a, np.cross(bb, c)).sum() / 6)
def hsec(V, u, mask):
    """horizontal section at height u restricted to vertices of mask's faces: (area cm2, perimeter cm) of each closed component, sorted by x"""
    Fm = F[mask[F].all(1)]; s = V[:, 2] - u; E = np.unique(np.sort(np.r_[Fm[:, [0, 1]], Fm[:, [1, 2]], Fm[:, [2, 0]]], 1), axis=0)
    cr = E[(s[E[:, 0]] > 0) != (s[E[:, 1]] > 0)]; w = s[cr[:, 0]] / (s[cr[:, 0]] - s[cr[:, 1]]); P = V[cr[:, 0]] + w[:, None] * (V[cr[:, 1]] - V[cr[:, 0]])
    out = []
    for sg in (-1, 1):
        Q = P[np.sign(P[:, 0]) == sg][:, :2]
        if len(Q) < 8: continue
        c = Q.mean(0); o = np.argsort(np.arctan2(Q[:, 1] - c[1], Q[:, 0] - c[0])); Q = Q[o]
        A = 0.5 * abs(np.dot(Q[:, 0], np.roll(Q[:, 1], -1)) - np.dot(Q[:, 1], np.roll(Q[:, 0], -1)))
        from scipy.spatial import ConvexHull; Pm = float(ConvexHull(Q).area)          # tape-measure girth = convex-hull perimeter of the section
        out.append((round(A, 3), round(Pm, 3)))
    return out
leg = np.isin(lab, ['leg_xneg', 'leg_xpos'])
for bid in V0:
    m = {}
    for tag, V in (('v000', V0[bid]), ('v001', V1[bid])):
        mm = dict(stature_cm=round(float(np.ptp(V[:, 2])), 4), bbox_cm=np.round(np.r_[V.min(0), V.max(0)], 4).tolist(), volume_cm3=round(signed_volume(V), 2))
        for u in (60, 66, 70, 74, 78, 82, 86): mm['thigh_u%d_area_perim' % u] = hsec(V, u, leg)
        tor = ~np.isin(lab, ['arm_xneg', 'arm_xpos', 'hand_xneg', 'hand_xpos'])
        sl = V[(np.abs(V[:, 2] - 86) < 0.3) & np.isin(lab, ['torso', 'leg_xneg', 'leg_xpos'])]; mm['pelvis_u86_width_depth_cm'] = [round(float(np.ptp(sl[:, 0])), 3), round(float(np.ptp(sl[:, 1])), 3)]
        m[tag] = mm
    m['delta'] = dict(stature_mm=round((m['v001']['stature_cm'] - m['v000']['stature_cm']) * 10, 4), bbox_mm=np.round((np.array(m['v001']['bbox_cm']) - np.array(m['v000']['bbox_cm'])) * 10, 4).tolist(),
                      volume_cm3=round(m['v001']['volume_cm3'] - m['v000']['volume_cm3'], 3), volume_pct=round(100 * (m['v001']['volume_cm3'] / m['v000']['volume_cm3'] - 1), 5),
                      thigh_area_pct={k: [round(100 * (a1[0] / a0[0] - 1), 4) for a0, a1 in zip(m['v000'][k], m['v001'][k])] for k in m['v000'] if k.startswith('thigh')},
                      thigh_girth_mm={k: [round(10 * (a1[1] - a0[1]), 3) for a0, a1 in zip(m['v000'][k], m['v001'][k])] for k in m['v000'] if k.startswith('thigh')},
                      pelvis_u86_mm=np.round((np.array(m['v001']['pelvis_u86_width_depth_cm']) - np.array(m['v000']['pelvis_u86_width_depth_cm'])) * 10, 4).tolist())
    res.setdefault('w2_measures', {})[bid] = m
# landmark-driven identity metrics (femur / leg, lower trunk, tail, head): landmark vertices are outside the changed set -> identical; verified by recomputation
ch = np.nonzero(np.linalg.norm(V1['SA-M188'] - V0['SA-M188'], axis=1) > 0)[0]; Vm = V0['SA-M188']
lmk = {k: np.array(v['p_cm']) for k, v in LM.items()}; dmin = {k: round(float(np.linalg.norm(Vm[ch] - p, axis=1).min()), 2) for k, p in lmk.items()}
res['landmarks_min_distance_to_changed_set_cm'] = dict(sorted(dmin.items(), key=lambda kv: kv[1])[:8]); res['landmarks_inside_changed_set'] = [k for k, v in dmin.items() if v < 0.2]
# 4. silhouettes
def sil(V, yaw, px, box=None, ss=2):
    an = np.radians(yaw); Rm = np.array([[np.cos(an), -np.sin(an), 0], [np.sin(an), np.cos(an), 0], [0, 0, 1]]); P = V @ Rm.T
    if box is None: x0, x1, z0, z1 = -150, 150, -2, 192
    else: x0, x1, z0, z1 = box
    q = px * ss; u = (P[:, 0] - x0) * q; v = (z1 - P[:, 2]) * q; Wd, Hd = int((x1 - x0) * px), int((z1 - z0) * px)
    im = Image.new('L', (Wd * ss, Hd * ss), 0); dr = ImageDraw.Draw(im)
    keep = np.ones(len(F), bool) if box is None else ((P[F, 2].max(1) > z0) & (P[F, 2].min(1) < z1))
    for t in F[keep]: dr.polygon([(u[t[0]], v[t[0]]), (u[t[1]], v[t[1]]), (u[t[2]], v[t[2]])], fill=255)
    return np.array(im, float).reshape(Hd, ss, Wd, ss).mean((1, 3)) >= 127.5
for bid in V0:
    s = {}
    for nm, yaw in (('front', 0), ('rear', 180), ('profile_left', 90), ('profile_right', -90), ('q3_front_left', 45), ('q3_front_right', -45)):
        A = sil(V0[bid], yaw, 3.0); B = sil(V1[bid], yaw, 3.0); s[nm] = round(float((A & B).sum() / (A | B).sum()), 7)
    for nm, yaw in (('thigh_front_12px', 0), ('thigh_profile_12px', 90), ('thigh_rear_12px', 180)):
        A = sil(V0[bid], yaw, 12.0, (-40, 40, 60, 90)); B = sil(V1[bid], yaw, 12.0, (-40, 40, 60, 90)); s[nm] = round(float((A & B).sum() / (A | B).sum()), 7); s[nm + '_pixels_changed'] = int((A ^ B).sum())
    res.setdefault('silhouette_iou_v000_v001', {})[bid] = s
g = res['geometry']; ok = all(g[b]['all_leg'] and g[b]['inside_63_87_incl_3cm_ramps'] and g[b]['unchanged_outside_bit_identical'] for b in V0) and g['same_changed_set_c1_c2']
# relief criterion: medial / posterior + transition sectors brought to the accepted anterolateral (W2I4 re-modelled) sector's native fine-scale level
# (fine relief energy p99 reduced, and <= 1.10 x the anterolateral p99) and the folded / crumpled vertices (normal deviation > 12 deg) of the full-strength patch
# reduced from 102 to <= 2 isolated vertices (tear removed; the accepted anterolateral face itself carries 89 such vertices of native relief)
# (the sigma-1.5 relief statistics are reported; the gate is on the sub-1.5-cm defect measures: the marks / tear are fine-scale, the 1.5-cm form is anatomy and is kept)
rl = all(all(res['relief'][b]['fine_scale']['v001'][s_]['fine_relief_energy_p99_mm'] < res['relief'][b]['fine_scale']['v000'][s_]['fine_relief_energy_p99_mm'] for s_ in ('medial_posterior', 'transition'))
         and max(res['relief'][b]['fine_scale']['v001'][s_]['fine_relief_energy_p99_mm'] for s_ in ('medial_posterior', 'transition')) <= 1.10 * res['relief'][b]['fine_scale']['v001']['anterolateral']['fine_relief_energy_p99_mm']
         and sum(res['relief'][b]['fine_scale']['v001'][s_]['folded_vertices_gt12deg_in_full_strength_patch'] for s_ in ('medial_posterior', 'transition')) <= 2 for b in V0)
w2 = all(abs(res['w2_measures'][b]['delta']['stature_mm']) < 0.01 and max(abs(x) for x in res['w2_measures'][b]['delta']['bbox_mm']) < 0.01 and abs(res['w2_measures'][b]['delta']['volume_pct']) < 0.01 for b in V0)
si = all(min(v for k, v in res['silhouette_iou_v000_v001'][b].items() if not k.startswith('thigh') ) >= 0.999 for b in V0)
res['gate'] = dict(geometry_local=ok, relief_corrected=rl, w2_measures_unchanged=w2, silhouette_equivalent=si, landmarks_untouched=not res['landmarks_inside_changed_set'], PASS=bool(ok and rl and w2 and si and not res['landmarks_inside_changed_set']))
json.dump(res, open(W + '/work/SA_RP5_WORK_v001_verification.json', 'w'), indent=1); print(json.dumps(res['gate'])); print(json.dumps(res['relief']['SA-M188'])[:1500]); print(res['w2_measures']['SA-M188']['delta']); print(res['silhouette_iou_v000_v001'])
