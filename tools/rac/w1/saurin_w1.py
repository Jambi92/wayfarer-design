"""RAC W1: Saurin ARM candidate checks + RM-CF-01 + stature accounting (diagnostic only; frozen reference never modified).
Re-uses the Part 7 / §263 tool chain (tools/rodin/creator-biology, tools/rodin/female/closure) from its working copies.
Usage: python saurin_w1.py <pc_staged_saurin_final_base.npz> <out.json>"""
import sys, json, hashlib, pickle, numpy as np
sys.path.insert(0, '/tmp/claude-0/rodin/v1'); sys.path.insert(0, '/tmp/claude-0/rodin/v5'); sys.path.insert(0, '/tmp/claude-0/rb')
import vary, metrics, tissue, fsets3
import wf_saurin_head63 as H
from scipy.spatial import cKDTree
pc_path, out_path = sys.argv[1], sys.argv[2]
R = {}
R['pc_file_sha256'] = hashlib.sha256(open(pc_path, 'rb').read()).hexdigest()
pc = np.load(pc_path); z = np.load(vary.REF_BASE)
V = z['V'].astype(float); F = z['F'].astype(np.int64)
R['pc_vs_working_copy_max_abs_dV_cm'] = float(np.abs(pc['v'].astype(float) - V).max())
R['pc_vs_working_copy_faces_equal'] = bool(np.array_equal(pc['f'], z['F']))
L = pickle.load(open('/tmp/claude-0/rodin/v1/Lbase.pkl', 'rb')); L._u0 = V[:, 2]; L._f0 = V[:, 1]
lm = pickle.load(open('/tmp/claude-0/rodin/v1/lm.pkl', 'rb')); ref = json.load(open('/tmp/claude-0/rodin/v1/ref_metrics.json'))
eye = (H.eye_centers()[0], H.eye_centers()[1])
x, f, u = V.T
# --- ARM state checks (male centre) ---
R['stature_cm'] = float(u.max() - u.min()); R['feet_min_u'] = float(u.min())
mir = V.copy(); mir[:, 0] *= -1; d, _ = cKDTree(V).query(mir)
R['symmetry_mirror_dist_cm'] = dict(median=float(np.median(d)), p99=float(np.percentile(d, 99)), max=float(d.max()))
R['tail_present_min_u_cm'] = float(u[L.tail > 0.9].min())
R['n_verts'] = int(len(V)); R['n_tris'] = int(len(F))
# --- reproduce Part 7 reference metrics on the base (reproducibility check) ---
p = {}; P = vary.warp(V, L, p, eye=eye); M = metrics.measure(P, F, L, p, lm, ref); M.pop('_A', None)
R['male_metrics'] = {k: float(v) for k, v in M.items() if np.isscalar(v)}
R['male_vs_ref_metrics_json'] = {k: [float(M[k]), float(ref[k])] for k in ref if k in M}
# --- female centre (§263) ---
def extras(P, q):
    x_, f_, u_ = P.T; s = q['_s']; x0, f0, u0 = V.T; tor = L.torso > 0.6
    vb = tor & (u0 > 112) & (u0 < 150)
    i91 = np.argmin(np.abs(u0 - 91) + 100 * (~tor)); i123 = np.argmin(np.abs(u0 - 123) + 100 * (~tor))
    return dict(ventral_f=float(f_[vb].max() - np.interp(130, np.arange(200), L.torso_cf) * s), lower_trunk=float(u_[i123] - u_[i91]))
outc = {}
for jid, q0 in (('male_ref', {}), ('female_centre', fsets3.CEN), ('female_reference_plus10', fsets3.REF)):
    q = dict(q0); Pq = tissue.fwarp(V, L, q, eye=eye); Mq = metrics.measure(Pq, F, L, q, lm, ref); Mq.pop('_A', None)
    e = extras(Pq, q)
    outc[jid] = dict(params={k: float(v) for k, v in q0.items()}, height=float(Mq['height']), lower_trunk=e['lower_trunk'],
                     pelvis_w=float(Mq['pelvis_w']), thorax_d_over_w=float(Mq['thorax_d_over_w']), ventral_f=e['ventral_f'],
                     head_len_ratio=float(Mq['head_len_ratio']), tail_len_pct=float(Mq['tail_len_pct']), rostral_index_part7=float(Mq['rostral_index']))
    if jid == 'female_centre': Pfem = Pq
R['stature_accounting'] = outc
# --- RM-CF-01: r3-conformant FPI = (f(FAL) - f(OC_mid)) / HL, HL = f(FAL) - f(Op) ---
E_world = np.array([vary.head_world(np.array(c)) for c in eye[0]])
def fpi(P, Pref=V, pitch_deg=0.0):
    hd = L.head > 0.95; x_, f_, u_ = P.T
    # eye centres follow the mean displacement of the 200 nearest reference vertices
    tr = cKDTree(Pref); OC = []
    for c in E_world:
        _, k = tr.query(c, k=200); OC.append(c + (P[k] - Pref[k]).mean(0))
    OC = np.array(OC); oc = OC.mean(0)
    # optional pitch about the eye midpoint (sensitivity of the FH*-equivalent frame)
    a = np.radians(pitch_deg); ca, sa = np.cos(a), np.sin(a)
    rel = P - oc; f2 = oc[1] + ca * rel[:, 1] - sa * rel[:, 2]; u2 = oc[2] + sa * rel[:, 1] + ca * rel[:, 2]
    mid = hd & (np.abs(x_) < 1.0)
    i_fal = np.where(mid)[0][np.argmax(f2[mid])]
    post = hd & (u_ > 176); i_op = np.where(post)[0][np.argmin(f2[post])]
    top = np.sort(f2[mid])[-20:]
    HL = f2[i_fal] - f2[i_op]; proj = f2[i_fal] - oc[1]
    return dict(FAL=P[i_fal].tolist(), Op=P[i_op].tolist(), OC_mid=oc.tolist(), HL_cm=float(HL), proj_cm=float(proj), FPI=float(proj / HL),
                FAL_top20_spread_cm=float(top.max() - top.min()), FAL_abs_x_cm=float(abs(x_[i_fal])))
cf = {}
cf['male_centre_base'] = fpi(V)
cf['male_centre_base_pitch_-3'] = fpi(V, pitch_deg=-3.0); cf['male_centre_base_pitch_+3'] = fpi(V, pitch_deg=3.0)
cf['female_centre_base'] = fpi(Pfem)
for jid, q in (('rostrum_min_-15', {'ros_len': 0.85}), ('cranium_long_+8', {'cran_len': 1.08}), ('corner_rostrum_min_x_cranium_long', {'ros_len': 0.85, 'cran_len': 1.08}),
               ('rostrum_max_+20', {'ros_len': 1.20})):
    qq = dict(q); Pw = vary.warp(V, L, qq, eye=eye); cf[jid] = fpi(Pw); cf[jid]['params'] = q
try:
    S = np.load(vary.REF_SURF)['V'].astype(float)
    Ls = pickle.load(open('/tmp/claude-0/rodin/v1/Lsurf.pkl', 'rb'))
    hd = Ls.head > 0.95; x_, f_, u_ = S.T; mid = hd & (np.abs(x_) < 1.0)
    i_fal = np.where(mid)[0][np.argmax(f_[mid])]; post = hd & (u_ > 176); i_op = np.where(post)[0][np.argmin(f_[post])]
    oc = E_world.mean(0); cf['male_centre_scaled_surface'] = dict(HL_cm=float(f_[i_fal] - f_[i_op]), proj_cm=float(f_[i_fal] - oc[1]),
        FPI=float((f_[i_fal] - oc[1]) / (f_[i_fal] - f_[i_op])), note='scaled-surface mesh (not the ARM state); for comparison with the Part 7 value')
except Exception as ex:
    cf['male_centre_scaled_surface'] = dict(error=str(ex))
R['RM_CF_01'] = cf
R['canon'] = dict(rostral_index_reference=0.288, band=[0.255, 0.335], head_len_over_H=[0.156, 0.184],
                  female_accounting=dict(lower_trunk_male=32.0, lower_trunk_female_centre=33.6, lower_trunk_ref_female=34.3,
                                         pelvic_w_male=41.7, pelvic_w_female_centre=43.1, d_w_male=0.880, d_w_female=0.922))
json.dump(R, open(out_path, 'w'), indent=1)
print(json.dumps({k: R[k] for k in ('stature_cm', 'symmetry_mirror_dist_cm', 'pc_vs_working_copy_max_abs_dV_cm')}, indent=1))
for k, v in cf.items(): print(k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items() if kk in ('FPI', 'HL_cm', 'proj_cm', 'FAL_top20_spread_cm', 'FAL_abs_x_cm')})
for k, v in outc.items(): print(k, {kk: round(vv, 3) for kk, vv in v.items() if isinstance(vv, float)})
