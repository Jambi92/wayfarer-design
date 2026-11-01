# sa_identity2.py CAGE.npz DESIGN.pkl OUT.json : FINAL identity metrics measured DIRECTLY ON THE CAGE (order 236dddc §14), SA-M188 and SA-F188.
#   A. section / extent metrics on the cage mesh itself vs the source (v001 definitions): stature, thorax breadth / depth, pelvic band, tail 25/50/75 areas.
#   B. joint centres in the planes of the cage's own AUTHORED rings (shoulder A0, elbow El2, wrist Wr, hip L1, knee Kn2, ankle S11): section centroid of the
#      CAGE mesh vs of the source in the same plane -> forearm / arm, femur / leg on the cage.
#   C. head: rostral projection (cage rostrum tip - orbit-ring centres), orbit spacing (orbit-ring centre distance) vs the same rings' source sections.
#   D. tail: root area (module ring 0 section), RSI = V * d_com / A_root^1.5 over the free tail (creator-biology definition, 2 cm stations on the chain),
#      coupling = A25 / A_root, carriage elevation from the cage tail-section centres.
#   E. plantigrade: sole contact area (downward-facing area below u 0.6 cm) cage vs source; heel min u.  F. claws: cap quads per digit (20 digits).
#   G. structural ridges: W3B RM-UF-04 strength metric on the canonical head vertices PROJECTED ONTO THE CAGE vs the source.
#   H. display root: cage fit (median / p95 / max) over the display-root quads' source patch.
import sys, os, json, pickle, numpy as np, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
CG, DS, OUT = sys.argv[1:4]; W = '/tmp/claude-0/rt/sa'
src = open('/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v001/sa_identity.py').read().split("LMm = {k: v['p_cm']")[0].replace("OUT = sys.argv[1]; ", "")
src = src.replace("VM = b['v'].astype(float); F = b['f'].astype(np.int64); VF = np.load(W + '/src/saurin_w2_SA-F188_realization.npz')['v'].astype(float)",
                  "F = b['f'].astype(np.int64); _w = np.load(W + '/work/SA_RP5_WORK_v001.npz'); VM = _w['v_M'].astype(float); VF = _w['v_F'].astype(float)")
ns = {}; exec(src, ns)
z = np.load(CG); Q = z['Q']; fi, bc = z['tri'], z['bc']; Tc = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; ql = z['qlab'].astype(str)
dsg = pickle.load(open(DS, 'rb')); nm = list(dsg['name']); IX = {n: i for i, n in enumerate(nm)}
def ring(prefix): return [IX[n] for n in nm if n.startswith(prefix + '_') and n[len(prefix) + 1:].isdigit()]
def plane(P): c = P.mean(0); n = np.linalg.svd(P - c)[2][2]; return c, n
def sec_centroid(VV, FF, c, n, rad):
    s = (VV - c) @ n; m = (np.linalg.norm(VV - c, axis=1) < rad); f = FF[m[FF].all(1)]; sf = s[f]; cr = (sf.min(1) < 0) & (sf.max(1) > 0); f = f[cr]; pts = []; w = []
    for t in f:
        p = []
        for a, b in ((0, 1), (1, 2), (2, 0)):
            sa, sb = s[t[a]], s[t[b]]
            if sa * sb < 0: p.append(VV[t[a]] + sa / (sa - sb) * (VV[t[b]] - VV[t[a]]))
        if len(p) == 2: pts.append(0.5 * (p[0] + p[1])); w.append(np.linalg.norm(p[1] - p[0]))
    pts = np.array(pts); w = np.array(w); return (pts * w[:, None]).sum(0) / w.sum()
def head_ridge(Vfull, Vcage):
    sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w3b_drivers'); import w3b_common as C3, w3b_ridge as RG
    P = Vfull.copy(); hv = RG.HV; _, _, cp = igl.point_mesh_squared_distance(Vfull[hv], Vcage, Tc); nrm = igl.per_vertex_normals(Vfull, G.F)[hv]; P[hv] = Vfull[hv] + ((cp - Vfull[hv]) * nrm).sum(1)[:, None] * nrm   # normal offset to the cage (tangential layout kept)
    ms, _ = RG.metric(Vfull); mc, _ = RG.metric(P)
    return {k: dict(source_strength_cm=round(ms[k]['strength_cm'], 4), cage_strength_cm=round(mc[k]['strength_cm'], 4), ratio=round(mc[k]['strength_cm'] / ms[k]['strength_cm'], 3),
                    source_transition_p90_deg=round(ms[k]['transition_deg_p90'], 2), cage_transition_p90_deg=round(mc[k]['transition_deg_p90'], 2)) for k in ms}
res = {}
LMm = {k: v['p_cm'] for k, v in ns['LM'].items()}; LMf = {k: ns['carry'](v).tolist() for k, v in LMm.items()}
for bid, VS, L in (('SA-M188', ns['VM'], LMm), ('SA-F188', ns['VF'], LMf)):
    Vc = (bc[:, :, None] * VS[ns['F'][fi]]).sum(1); FF = ns['F']; r = {}
    s_ = ns['metrics'](VS, L); ns['F'] = Tc; c_ = ns['metrics'](Vc, L); ns['F'] = FF
    r['A_sections'] = {k: dict(source=s_[k], cage=c_[k], diff=round(c_[k] - s_[k], 4)) for k in s_ if any(t in k for t in ('stature', 'thorax', 'pelvic', 'tail_area', 'heel'))}
    J = {}
    for s in ('xpos', 'xneg'):
        for jn, pre in (('shoulder', 'A0_'), ('elbow', 'El2_'), ('wrist', 'Wr_'), ('hip', 'L1_'), ('knee', 'Kn2_'), ('ankle', 'S11_')):
            idx = ring(pre + s); c, n = plane(Vc[idx]); rad = 1.6 * np.linalg.norm(Vc[idx] - c, axis=1).max()
            J[jn + '_' + s] = dict(cage=sec_centroid(Vc, Tc, c, n, rad), source=sec_centroid(VS, FF, c, n, rad))
    B = {}
    for s in ('xpos', 'xneg'):
        for which in ('cage', 'source'):
            g = lambda k: J[k + '_' + s][which]
            B.setdefault('forearm_over_arm_' + s, {})[which] = round(float(np.linalg.norm(g('wrist') - g('elbow')) / (np.linalg.norm(g('elbow') - g('shoulder')) + np.linalg.norm(g('wrist') - g('elbow')))), 4)
            B.setdefault('femur_over_leg_' + s, {})[which] = round(float(np.linalg.norm(g('knee') - g('hip')) / (np.linalg.norm(g('knee') - g('hip')) + np.linalg.norm(g('ankle') - g('knee')))), 4)
    for k in B: B[k]['diff'] = round(B[k]['cage'] - B[k]['source'], 4)
    r['B_joint_ratios_from_cage_rings'] = B
    # C head
    hc = Vc[np.isin(np.arange(len(Vc)), Q[np.isin(ql, ['head', 'rostrum_cap'])].ravel())]; hs = VS[G.LAB == 'head']
    oc = {}; 
    for s in ('xpos', 'xneg'):
        idx = ring(s + '_orb0'); c, n = plane(Vc[idx]); rad = 1.6 * np.linalg.norm(Vc[idx] - c, axis=1).max(); oc[s] = dict(cage=sec_centroid(Vc, Tc, c, n, rad), source=sec_centroid(VS, FF, c, n, rad))
    r['C_head'] = dict(rostral_projection_cm=dict(cage=round(float(hc[:, 1].max() - 0.5 * (oc['xpos']['cage'][1] + oc['xneg']['cage'][1])), 3),
                                                  source=round(float(hs[:, 1].max() - 0.5 * (oc['xpos']['source'][1] + oc['xneg']['source'][1])), 3)),
                       orbit_spacing_ring_centres_cm=dict(cage=round(float(np.linalg.norm(oc['xpos']['cage'] - oc['xneg']['cage'])), 3), source=round(float(np.linalg.norm(oc['xpos']['source'] - oc['xneg']['source'])), 3)))
    for k in r['C_head']: r['C_head'][k]['diff'] = round(r['C_head'][k]['cage'] - r['C_head'][k]['source'], 3)
    # D tail (2 cm stations on the landmark chain, sections on the cage mesh vs the source)
    ch = np.array([L['tail_root_centre']] + [L['tail_chain_%02d' % k] for k in range(1, 17)] + [L['tail_tip']]); arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(ch, axis=0), axis=1))]
    st = np.arange(0, arc[-1] - 4, 2.0); TD = {}
    for which, (PP, TT) in (('cage', (Vc, Tc)), ('source', (VS, FF))):
        A = []; Cc = []
        for s0 in st:
            k = min(int(np.searchsorted(arc, s0, 'right')) - 1, len(ch) - 2); t = (s0 - arc[k]) / (arc[k + 1] - arc[k]); c = ch[k] + t * (ch[k + 1] - ch[k]); n = ch[k + 1] - ch[k]
            A.append(ns['sec_area'](PP, TT, c, n)); Cc.append(c)
        A = np.array(A); vol = np.trapezoid(A, st); com = np.trapezoid(A * st, st) / vol; Ar = A[0]
        mid = ch[8]; TD[which] = dict(root_area_cm2=round(float(Ar), 3), RSI_raw=round(float(vol * (st[-1] - com) / Ar ** 1.5), 4), coupling_A25_over_root=round(float(np.interp(0.25 * st[-1], st, A) / Ar), 4),
                                      A50_over_root=round(float(np.interp(0.5 * st[-1], st, A) / Ar), 4), tail_volume_L=round(float(vol / 1000), 4))
    TD['RSI_ratio_cage_over_source'] = round(TD['cage']['RSI_raw'] / TD['source']['RSI_raw'], 4)
    TD['carriage_elevation_deg'] = round(float(np.degrees(np.arctan2(ch[8][2] - ch[0][2], np.hypot(ch[8][0] - ch[0][0], ch[8][1] - ch[0][1])))), 3)
    TD['carriage_note'] = 'chain = accepted tail module centreline (module unchanged); section stations measured on the cage mesh'
    r['D_tail'] = TD
    # E plantigrade
    def sole(PP, TT):
        nn = np.cross(PP[TT[:, 1]] - PP[TT[:, 0]], PP[TT[:, 2]] - PP[TT[:, 0]]); a = 0.5 * np.linalg.norm(nn, axis=1); m = (PP[TT].max(1)[:, 2] < 0.6) & (nn[:, 2] < -0.7 * 2 * a); return float(a[m].sum())
    r['E_plantigrade'] = dict(sole_contact_area_cm2=dict(cage=round(sole(Vc, Tc), 2), source=round(sole(VS, FF), 2)), heel_min_u_cm=dict(cage=round(float(Vc[:, 2].min()), 3), source=round(float(VS[:, 2].min()), 3)))
    # F claws
    caps = {}
    for s in ('xpos', 'xneg'):
        for dg in ['f1', 'f2', 'f3', 'f4', 'th'] + ['t%d' % k for k in range(1, 6)]:
            idx = set(ring('%s_%s_r2' % (s, dg))); caps['%s_%s' % (s, dg)] = int(sum(1 for q, l in zip(Q, ql) if l in ('finger_cap', 'thumb_cap', 'toe_cap') and set(q.tolist()) & idx) > 0 or
                                                                                     any(l in ('finger_cap', 'thumb_cap', 'toe_cap') for l in ql[np.isin(Q, list(idx)).any(1)]))
    r['F_claws'] = dict(digits_with_claw_cap=int(sum(caps.values())), of=len(caps), cap_quads=int(np.isin(ql, ['finger_cap', 'thumb_cap', 'toe_cap']).sum()))
    # H display root fit
    dm = np.isin(ql, ['display_root']); dv = np.unique(Q[dm])
    sv = np.nonzero(np.linalg.norm(VS - Vc[dv].mean(0), axis=1) < 1.2 * np.linalg.norm(Vc[dv] - Vc[dv].mean(0), axis=1).max())[0]
    dd = np.sqrt(igl.point_mesh_squared_distance(VS[sv], Vc, Tc)[0]) * 10
    r['H_display_root'] = dict(quads=int(dm.sum()), source_patch_vertices=int(len(sv)), fit_mm=dict(median=round(float(np.median(dd)), 3), p95=round(float(np.percentile(dd, 95)), 3), max=round(float(dd.max()), 3)))
    if bid == 'SA-M188': r['G_structural_ridges'] = head_ridge(VS, Vc)
    res[bid] = r; print(bid, json.dumps(r)[:1500], flush=True)
res['note'] = ('every metric here is measured on the cage mesh (sections, its own authored rings, projections onto it) and on the source with the same definition; '
               'lower axial trunk is height-defined by its landmarks (spine_lower_axial_91 / _123) and is reported in A only as defined.')
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: np.asarray(o).round(4).tolist())
