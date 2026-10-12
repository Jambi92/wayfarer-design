# RAC RM-OT-05E minimal technical guards (order §8), derived from d_guard (RM-OT-05D). Baseline = Gorrund 05D E1 (same skeleton).
# Added: plantigrade foot (heel and ball on the ground plane), hand / foot topology and digit count (faces identical; hands and feet
# unchanged vs the unorganized route beyond the 0.4 cm subcutaneous hold), proxy-floor dependency report.
# (05D header follows)
# For every candidate body (reference / low / Narrow / Broad):
#   stature, ground, no uniform scaling + joints / -LEAN / bone scales unchanged (vs the 05C developmental baseline on the same skeleton),
#   outward-normal test (true_envelope.test_outward), true-floor respected, gross self-intersection vs the same route without the
#   organization, arm / trunk clearance, posture (R-6 joints unchanged), surface-volume change vs the route (reported separately),
#   composition ordering (low vs reference) and frame ordering (Narrow < reference < Broad) preserved on skin stations,
#   skeleton-anchored station readings (skeletal_stations.read_body: protected / organized / true floor / legacy).
# Usage: python3 d_guard.py OUT.json NAME...
import os, sys, json, numpy as np, subprocess
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D)
for p in (W1, W1 + '/rmot05c_drivers'): sys.path.insert(0, p)
sys.path.insert(0, W1 + '/rmot05d_drivers')
import c_guard as CG, true_envelope as TE, skeletal_stations as SS, bony_envelope as BE
S = CG.S; DD = [S + '/w2c/donor', S + '/w2d/h', S + '/w1g/donor', S + '/w2d/donor']
def base05c(n):                                  # 05E: the baseline is Gorrund 05D E1 (+ the same state suffix)
    return 'GO5DE1' + n[6:]
def rec_of(n):
    p = CG.path(n); d = os.path.dirname(p)
    for suf in ('_w2c.json', '_w2d.json'):
        if os.path.exists(d + '/' + n + suf): return json.load(open(d + '/' + n + suf))
    return {}
def skin_st(prefix):
    from arm_measure import load
    return BE.fast_stations(load(prefix + '_rest.npz'))
if __name__ == '__main__':
    out = sys.argv[1]; res = {}
    for n in sys.argv[2:]:
        p = CG.path(n); b0 = base05c(n); p0 = CG.path(b0)
        B = np.load(p + '_r6.npz', allow_pickle=True); B0 = np.load(p0 + '_r6.npz', allow_pickle=True)
        V = B['V'].astype(float); F = B['F']; keep = B['keep'].astype(bool); J = json.loads(str(B['joints'])); J0 = json.loads(str(B0['joints']))
        meta = json.loads(str(B['meta'])); rec = {'baseline_05C': b0, 'race_base_floor': (meta.get('race_base') or {}).get('floor')}
        rec['stature_cm'] = float(V[keep, 2].max()); rec['stature_05C_cm'] = float(B0['V'][keep, 2].max()); rec['stature_pass'] = bool(abs(rec['stature_cm'] - rec['stature_05C_cm']) < 0.01)
        fz = {sd: float(V[keep & (np.maximum(B['w_foot_' + sd], B['w_ball_' + sd]) > 0.5), 2].min()) for sd in ('l', 'r')}
        rec['ground'] = {'min_u_cm': float(V[keep, 2].min()), 'foot_min_u_cm': fz, 'pass': bool(abs(V[keep, 2].min()) < 1e-3 and max(fz.values()) < 0.3)}
        jd = max(np.abs(np.array(J[k]) - np.array(J0[k])).max() for k in J)
        skel_src = meta.get('skeleton', n + '-LEAN').replace('-LEAN', '')
        Lp = CG.path(skel_src) + '-LEAN'; L = dict(np.load(Lp + '_r6.npz', allow_pickle=True))
        L0p = CG.path(b0 if not n.endswith('-LOW') else b0.replace('-LOW', '')) + '-LEAN'; L0 = np.load(L0p + '_r6.npz', allow_pickle=True)
        ld = float(np.abs(L['V'].astype(float) - L0['V'].astype(float)).max())
        r1, r0 = rec_of(skel_src), rec_of(b0.replace('-LOW', ''))
        bs = (r1.get('bone_scales') == r0.get('bone_scales'))
        rec['skeleton_unchanged'] = {'max_joint_delta_cm': float(jd), 'max_LEAN_vertex_delta_cm': ld, 'bone_scales_equal': bool(bs), 'pass': bool(jd < 0.05 and ld < 0.05 and bs)}
        ok, det = TE.test_outward(V, F, B); okL, detL = TE.test_outward(L['V'].astype(float), L['F'], L)
        rec['outward_normal_test'] = {'body': det, 'lean': detL, 'pass': bool(ok and okL)}
        # true floor respected (floor of this body's skeleton, moved to the body frame by the body's own grounding: same skeleton, so compare in LEAN
        # frame through the similarity used by make: re-derive from the unorganized state of this body)
        Vr = CG.route_baseline(B)
        Fv = TE.floor(L['V'].astype(float), L)[0]
        # the body frame = f(LEAN) re-grounded; f is ~identity scale; recover it from the route state (same skeleton, same f): offset = Vr - (Lean + tissue) is
        # not available, so estimate the rigid shift by matching the joint heads (joints in the body file = f(J_lean) - z0)
        JL = json.loads(str(L['joints'])); a = np.array([JL[k][0] for k in JL]); b = np.array([J[k][0] for k in JL])
        sc = np.sqrt(((b - b.mean(0)) ** 2).sum() / ((a - a.mean(0)) ** 2).sum()); Fb = (Fv - a.mean(0)) * sc + b.mean(0)
        nF = TE.outward_normals(Fb, F, keep); sd_ = np.einsum('ij,ij->i', V - Fb, nF)
        ext = np.clip(B['w_head'] + B['w_neck_01'] + B['w_hand_l'] + B['w_hand_r'] + B['w_fingers_l'] + B['w_fingers_r'], 0, 1) >= 0.3
        org = keep & ~ext
        rec['true_floor'] = {'organized_region': {'min_signed_cm': float(sd_[org].min()), 'n_inside_0p2cm': int((sd_[org] < -0.2).sum())},
                             'head_neck_hands_not_organized': {'n_floor_test_inside_0p2cm': int((sd_[keep & ext] < -0.2).sum()), 'max_change_vs_route_cm': float(np.abs(V - Vr)[keep & ext].max()),
                                                                'note': 'not organized (left as the route); the 0.4 cm inward offset folds on thin parts (ear, fingers), so the floor test is not meaningful there'},
                             'pass': bool((sd_[org] < -0.2).sum() == 0)}
        # plantigrade: heel (posterior foot) and ball / toes both at the ground plane, as on the baseline
        def plant(Vx):
            o = {}
            for sd in ('l', 'r'):
                fm = keep & (B['w_foot_' + sd] > 0.5); bm = keep & (B['w_ball_' + sd] > 0.5)
                o[sd] = {'heel_min_u_cm': float(Vx[fm, 2].min()), 'ball_min_u_cm': float(Vx[bm, 2].min())}
            return o
        pl = plant(V); pl0 = plant(B0['V'].astype(float))
        rec['plantigrade'] = {'body': pl, 'baseline_E1': pl0, 'pass': bool(all(max(v.values()) < 0.6 for v in pl.values()))}
        hf = np.clip(sum(B['w_' + k] for k in ('hand_l', 'hand_r', 'fingers_l', 'fingers_r', 'ball_l', 'ball_r', 'toes_l', 'toes_r') if 'w_' + k in B.files), 0, 1) > 0.5
        rec['hand_foot_topology'] = {'faces_identical_to_baseline': bool(np.array_equal(F, B0['F'])), 'n_vertices_equal': bool(len(V) == len(B0['V'])),
                                     'max_hand_digit_change_vs_route_cm': float(np.abs(V - Vr)[keep & hf].max()),
                                     'pass': bool(np.array_equal(F, B0['F']) and np.abs(V - Vr)[keep & hf].max() < 1.0)}
        rec['proxy_floor_dependency'] = 'posterior hip-level depth (S6 depth; gluteal over ischium) and S2 lateral (latissimus / serratus cover) remain skeleton proxies (true_envelope.DEPENDENCIES); 05E cues there (posterior plane, pelvis-thigh transition, trunk corners) are bounded by the proxy floor, not by bone'
        sx, sxr = CG.self_x(V, F, keep), CG.self_x(Vr, F, keep)
        rec['self_intersection'] = {'piercing_edges': sx, 'route_without_05D': sxr, 'pass': bool(sx <= sxr + 10)}
        a_ = subprocess.run(['python3', W1 + '/arm_clearance.py', p + '_r6.npz'], capture_output=True, text=True, cwd=W1).stdout
        try:
            ac = eval(a_.split('_r6.npz ', 1)[1].strip()); rec['arm_clearance'] = {sd: {k: ac[sd][k] for k in ('min_arm_trunk_gap_cm', 'verts_inside_trunk_section')} for sd in ('l', 'r')}
            rec['arm_clearance']['pass'] = bool(all(ac[sd]['verts_inside_trunk_section'] == 0 for sd in ('l', 'r')))
        except Exception as ex: rec['arm_clearance'] = {'error': str(ex)}
        rec['posture'] = {'r6_joints_equal_05C': bool(jd < 0.05), 'pass': bool(jd < 0.05)}
        rec['volume_l'] = CG.volume(V, F) / 1000.0; rec['volume_route_l'] = CG.volume(Vr, F) / 1000.0; rec['volume_ratio_vs_route'] = rec['volume_l'] / rec['volume_route_l']
        rec['skin_pelvic_AP_cm'] = CG.skin_pelvic_depth(V, J, keep, np.maximum.reduce([B['w_' + k] for k in ('upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r')]))
        rec['skin_stations'] = skin_st(p)
        if not n.endswith('-LOW'):
            rec['skeletal_stations'] = SS.read_body(p, DD)
        res[n] = rec; print(n, json.dumps({k: (v.get('pass') if isinstance(v, dict) and 'pass' in v else v) for k, v in rec.items() if k not in ('skin_stations', 'skeletal_stations')}), flush=True)
    # composition and frame ordering on skin stations (organized vs the 05C baseline ordering, which is the route ordering)
    def st(n): return res[n]['skin_stations'] if n in res else skin_st(CG.path(n))
    for race in ('GO',):
        for c in ('P1', 'P2', 'P3'):
            r, lo, nn, bb = '%s5E%s' % (race, c), '%s5E%s-LOW' % (race, c), '%s5E%sN' % (race, c), '%s5E%sB' % (race, c)
            if not all(x in res for x in (r, lo, nn, bb)): continue
            b = base05c(r)
            comp = {S_: [np.sign(st(lo)[S_][i] - st(r)[S_][i]) == np.sign(st(b + '-LOW')[S_][i] - st(b)[S_][i]) for i in (0, 1)] for S_ in ('S2', 'S5', 'S6')}
            fr = {S_: bool(st(nn)[S_][0] < st(r)[S_][0] < st(bb)[S_][0]) == bool(st(b + 'N')[S_][0] < st(b)[S_][0] < st(b + 'B')[S_][0]) for S_ in ('S2', 'S5', 'S6')}
            res[r]['composition_ordering'] = {'per_station_same_sign_as_baseline': comp, 'pass': bool(all(all(v) for v in comp.values()))}
            res[r]['frame_ordering'] = {'per_station_same_as_baseline': fr, 'pass': bool(all(fr.values()))}
    json.dump(res, open(out, 'w'), indent=1, default=float)
