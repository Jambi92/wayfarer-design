# RAC RM-OT-05C minimal guards (order §8). This is not the exhaustive W2C / W2D chain. For each candidate body:
#   stature            R-6 stature vs the 05B body on the same skeleton route (target 218 / 229 Grask, 230.9 Gorrund)
#   ground             sole contact: lowest keep vertex at u = 0 and both feet within 0.3 cm of the ground
#   uniform scaling    none: joints / bone scales / -LEAN skeleton identical to the 05B skeleton (max vertex / joint delta, cm)
#   self-intersection  edge-through-triangle count over non-adjacent faces (body mesh, keep), vs the same route without 05C (and vs 05B)
#   arm clearance      arm_clearance.py (closed-band interpenetration, min arm-trunk gap)
#   skeleton relations composition-infimum skeletal proxy at t = 0 vs 05B:
#                      GR-P2b bitrochanteric / crest, GR-P6 pelvis / thorax breadth;
#                      Gorrund pelvic depth / thoracic depth, pelvic depth share, S6 / S2 depth (deep pelvis); MF reference value
#   composition        body volume vs 05B (organization must not add / remove amount); low < reference ordering kept
#   deep pelvis (skin) Gorrund skin pelvic AP depth at the hip level vs 05B (diagnostic; the skin row is composition-inclusive)
# Usage: python3 c_guard.py OUT.json NAME...
import os, sys, json, numpy as np, subprocess
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D); sys.path.insert(0, W1)
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
MFSKP = S + '/s7n/w1i_base/t0.0/MF-M-R_meas.json'
def path(n):
    for d in ('w2c', 'w2d'):
        p = '%s/%s/b/%s/%s' % (S, d, n, n)
        if os.path.exists(p + '_r6.npz'): return p
    raise FileNotFoundError(n)
def ref05b(n):
    race = n[:2]; rest = n[5:]
    if n.endswith('-LOW'): return 'B_GR-BODY-06' if race == 'GR' else 'B_GOR-BODY-06'
    if race == 'GR': return {'': 'GR5B218', '229': 'GR5B229', 'N': 'GR5BN', 'B': 'GR5BB'}[rest]
    return {'': 'GO5BREF', 'N': 'GO5BN', 'B': 'GO5BB'}[rest]
def volume(V, F):
    return float(np.einsum('ij,ij->i', V[F[:, 0]], np.cross(V[F[:, 1]], V[F[:, 2]])).sum() / 6.0)
def self_x(V, F, keep, cell=3.0):
    """edges of the keep mesh that pierce a non-adjacent keep triangle (uniform-grid broad phase, Moller-Trumbore narrow phase)"""
    Fk = F[keep[F].all(1)]; E = np.unique(np.sort(np.r_[Fk[:, [0, 1]], Fk[:, [1, 2]], Fk[:, [2, 0]]], 1), axis=0)
    lo = V.min(0); key = lambda P: np.floor((P - lo) / cell).astype(np.int64)
    tmin = key(V[Fk].min(1)); tmax = key(V[Fk].max(1)); grid = {}
    for i, (a, b) in enumerate(zip(tmin, tmax)):
        for x in range(a[0], b[0] + 1):
            for y in range(a[1], b[1] + 1):
                for z in range(a[2], b[2] + 1): grid.setdefault((x, y, z), []).append(i)
    emid = key(0.5 * (V[E[:, 0]] + V[E[:, 1]])); pairs = []
    for ei, c in enumerate(map(tuple, emid)):
        for fi in grid.get(c, ()): pairs.append((ei, fi))
    if not pairs: return 0
    P = np.array(pairs); e = E[P[:, 0]]; f = Fk[P[:, 1]]
    adj = (e[:, :1] == f).any(1) | (e[:, 1:] == f).any(1); P, e, f = P[~adj], e[~adj], f[~adj]
    o = V[e[:, 0]]; dvec = V[e[:, 1]] - o; v0, v1, v2 = V[f[:, 0]], V[f[:, 1]], V[f[:, 2]]
    e1 = v1 - v0; e2 = v2 - v0; h = np.cross(dvec, e2); a = np.einsum('ij,ij->i', e1, h); ok = np.abs(a) > 1e-9
    inv = np.where(ok, 1 / np.where(ok, a, 1), 0); s = o - v0; u = inv * np.einsum('ij,ij->i', s, h); q = np.cross(s, e1)
    v = inv * np.einsum('ij,ij->i', dvec, q); t = inv * np.einsum('ij,ij->i', e2, q)
    hit = ok & (u > 1e-6) & (v > 1e-6) & (u + v < 1 - 1e-6) & (t > 1e-6) & (t < 1 - 1e-6)
    return int(len(np.unique(P[hit, 0])))
def route_baseline(B):
    """the same composition state on the same skeleton route WITHOUT the 05C organization: f(-LEAN) + (donor - donor_lean)"""
    import skeleton_envelope as SE, c_preview as P
    m = json.loads(str(B['meta'])); sk = m['skeleton']; body = sk.replace('-LEAN', '')
    L = np.load(path(body) + '-LEAN_r6.npz', allow_pickle=True); dr, dl = m['tissue_donor']
    R = np.load(P.find(dr) + '_r6.npz', allow_pickle=True); Dn = np.load(P.find(dl) + '_r6.npz', allow_pickle=True)
    f, sc = SE.simil(Dn, R); V = f(L['V'].astype(float)) + R['V'].astype(float) - f(Dn['V'].astype(float)); k = L['keep'].astype(bool); V[:, 2] -= V[k, 2].min()
    return V
def cib_fixed(n, r0):
    """composition-infimum bony stations of the candidate's grid read at the 05B reference's station levels (same anatomical levels; the
    ALPC level search otherwise re-anchors on the candidate's own reference skin, e.g. the waist minimum the organization removed)"""
    import glob, bony_envelope as BE
    p = path(n); d = os.path.dirname(p)
    comps = [p + '-LEAN_rest.npz'] + sorted(glob.glob(d + '/grid_%s/*_rest.npz' % n)) + [p + '_rest.npz']
    C = BE.cib(path(r0) + '_rest.npz', comps); C0 = json.load(open(os.path.dirname(path(r0)) + '/%s_cib.json' % r0))
    rat = lambda b: {'bitroch_over_crest': b['S6'][0] / b['S5'][0], 'pelvis_over_thorax_breadth': b['S5'][0] / b['S2'][0], 'pelvic_depth_over_thorax_depth': b['S6'][1] / b['S2'][1],
                     'S4_over_S2_b': b['S4'][0] / b['S2'][0], 'S3_over_S2_d': b['S3'][1] / b['S2'][1]}
    return {'stations': C['bony'], 'stations_05B': C0['bony'], 'argmin': C['argmin'], 'ratios': rat(C['bony']), 'ratios_05B': rat(C0['bony']),
            'max_station_delta_cm': max(abs(C['bony'][k][i] - C0['bony'][k][i]) for k in C['bony'] for i in (0, 1))}
def skp(n):
    p = path(n); q = '%s/../%s/skp_%s/%s_skp.json' % (p, n, n, n)
    q = os.path.dirname(p) + '/skp_%s/%s_skp.json' % (n, n)
    if not os.path.exists(q): return None
    r = json.load(open(q))['by_t']['0.0']['ratio']
    return {k: r[k] for k in ('bitroch_over_crest', 'pelvis_over_thorax_breadth', 'pelvic_depth_over_thorax_depth', 'pelvic_depth_share', 'S6_over_S2_d')}
def skin_pelvic_depth(V, J, keep, armw):
    hip = 0.5 * (J['thigh_l'][0][2] + J['thigh_r'][0][2]); m = keep & (np.abs(V[:, 2] - (hip + 4)) < 1.0) & (armw < 0.05) & (np.abs(V[:, 0]) < 12)
    return float(V[m, 1].max() - V[m, 1].min())
if __name__ == '__main__':
    out = sys.argv[1]; res = {}
    try: mf = json.load(open(MFSKP))['combined']['ratio']; MF = {k: mf.get(k) for k in ('bitroch_over_crest', 'pelvis_over_thorax_breadth', 'pelvic_depth_over_thorax_depth', 'pelvic_depth_share', 'S6_over_S2_d')}
    except Exception as ex: MF = {'error': str(ex)}
    res['MF_reference_skeletal_t0'] = MF
    for n in sys.argv[2:]:
        p = path(n); r0 = ref05b(n); p0 = path(r0)
        B = np.load(p + '_r6.npz', allow_pickle=True); B0 = np.load(p0 + '_r6.npz', allow_pickle=True)
        V = B['V'].astype(float); V0 = B0['V'].astype(float); F = B['F']; keep = B['keep'].astype(bool); J = json.loads(str(B['joints'])); J0 = json.loads(str(B0['joints']))
        armw = np.maximum.reduce([B['w_' + k] for k in ('upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r')])
        rec = {'ref05B': r0, 'race_base': bool(json.loads(str(B['meta'])).get('race_base'))}
        rec['stature_cm'] = float(V[keep, 2].max()); rec['stature_05B_cm'] = float(V0[keep, 2].max())
        fz = {sd: float(V[keep & (np.maximum(B['w_foot_' + sd], B['w_ball_' + sd]) > 0.5), 2].min()) for sd in ('l', 'r')}
        rec['ground'] = {'min_u_cm': float(V[keep, 2].min()), 'foot_min_u_cm': fz, 'pass': bool(abs(V[keep, 2].min()) < 1e-3 and max(fz.values()) < 0.3)}
        jd = max(np.abs(np.array(J[k]) - np.array(J0[k])).max() for k in J)
        if not n.endswith('-LOW'):
            L = np.load(p + '-LEAN_r6.npz', allow_pickle=True); L0 = np.load(p0 + '-LEAN_r6.npz', allow_pickle=True)
            ld = float(np.abs(L['V'].astype(float) - L0['V'].astype(float)).max())
        else: ld = 0.0
        rec['skeleton_unchanged'] = {'max_joint_delta_cm': float(jd), 'max_LEAN_vertex_delta_cm': ld, 'pass': bool(jd < 0.05 and ld < 0.05)}
        sx, sx0, sxr = self_x(V, F, keep), self_x(V0, F, keep), self_x(route_baseline(B), F, keep)
        rec['self_intersection'] = {'piercing_edges': sx, 'piercing_edges_05B': sx0, 'piercing_edges_route_without_05C': sxr, 'pass': bool(sx <= sxr + 10),
                                    'note': 'MPFB axilla / crotch contacts are present on the route itself; pass = no more than the same route without the 05C organization (+10)'}
        a = subprocess.run(['python3', W1 + '/arm_clearance.py', p + '_r6.npz'], capture_output=True, text=True, cwd=W1).stdout
        try:
            ac = eval(a.split('_r6.npz ', 1)[1].strip()); rec['arm_clearance'] = {sd: {k: ac[sd][k] for k in ('min_arm_trunk_gap_cm', 'verts_inside_trunk_section', 'signed_section_clearance_cm')} for sd in ('l', 'r')}
            rec['arm_clearance']['pass'] = bool(all(ac[sd]['verts_inside_trunk_section'] == 0 for sd in ('l', 'r')))
        except Exception as ex: rec['arm_clearance'] = {'error': a[-300:] + str(ex)}
        rec['volume_l'] = volume(V, F) / 1000.0; rec['volume_05B_l'] = volume(V0, F) / 1000.0; rec['volume_ratio'] = rec['volume_l'] / rec['volume_05B_l']
        rec['skin_pelvic_AP_cm'] = skin_pelvic_depth(V, J, keep, armw); rec['skin_pelvic_AP_05B_cm'] = skin_pelvic_depth(V0, J0, keep, armw)
        k1, k0 = (skp(n), skp(r0)) if not n.endswith('-LOW') else (None, None)
        if k1 and k0:
            rec['skeletal_t0'] = {k: [round(k1[k], 4), round(k0[k], 4), MF.get(k)] for k in k1}
            rec['skeletal_t0_note'] = '[candidate, 05B, MF reference]'
            if n.startswith('GR'):
                rec['GR-P2b'] = {'value': k1['bitroch_over_crest'], 'MF': MF.get('bitroch_over_crest'), 'pass': bool(MF.get('bitroch_over_crest') is None or k1['bitroch_over_crest'] >= MF['bitroch_over_crest'] - 1e-4)}
                rec['GR-P6'] = {'value': k1['pelvis_over_thorax_breadth'], '05B': k0['pelvis_over_thorax_breadth'], 'MF': MF.get('pelvis_over_thorax_breadth'), 'pass': bool(abs(k1['pelvis_over_thorax_breadth'] - k0['pelvis_over_thorax_breadth']) < 0.005)}
            else:
                rec['deep_pelvis_skeletal'] = {'pelvic_depth_over_thorax_depth': [k1['pelvic_depth_over_thorax_depth'], k0['pelvic_depth_over_thorax_depth']], 'pass': bool(k1['pelvic_depth_over_thorax_depth'] >= k0['pelvic_depth_over_thorax_depth'] - 0.005)}
        if not n.endswith('-LOW'):
            cf = cib_fixed(n, r0); rec['cib_at_05B_levels'] = cf
            rf = cf['ratios']
            if n.startswith('GR'):
                rec['GR-P2b_fixed_levels'] = {'bitroch_over_crest': rf['bitroch_over_crest'], 'MF': MF.get('bitroch_over_crest'), '05B': cf['ratios_05B']['bitroch_over_crest'],
                                              'pass': bool(rf['bitroch_over_crest'] >= MF.get('bitroch_over_crest', 0) - 1e-4)}
                rec['GR-P6_fixed_levels'] = {'pelvis_over_thorax_breadth': rf['pelvis_over_thorax_breadth'], 'MF': MF.get('pelvis_over_thorax_breadth'), '05B': cf['ratios_05B']['pelvis_over_thorax_breadth'],
                                             'pass': bool(abs(rf['pelvis_over_thorax_breadth'] - cf['ratios_05B']['pelvis_over_thorax_breadth']) < 0.005)}
            else:
                rec['deep_pelvis_fixed_levels'] = {'pelvic_depth_over_thorax_depth': rf['pelvic_depth_over_thorax_depth'], '05B': cf['ratios_05B']['pelvic_depth_over_thorax_depth'],
                                                   'pass': bool(rf['pelvic_depth_over_thorax_depth'] >= cf['ratios_05B']['pelvic_depth_over_thorax_depth'] - 0.005)}
            rec['skeleton_relations_unchanged_fixed_levels'] = bool(cf['max_station_delta_cm'] < 0.3)
        res[n] = rec; print(n, json.dumps({k: (v.get('pass') if isinstance(v, dict) else v) for k, v in rec.items()}), flush=True)
    json.dump(res, open(out, 'w'), indent=1, default=float)
