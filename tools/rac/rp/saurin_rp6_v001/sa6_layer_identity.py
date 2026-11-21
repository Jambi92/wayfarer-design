# sa6_layer_identity.py BODYDIR OUT.json [FITDIR] : package + blend identities (corrective-layer validation order 3e76b509 §1-2).
#   1. package inputs: SHA-256 + bytes of every package file the harness reads, against SA_RP6_rig_manifest_v001.json (v001 arrays) and the array hashes
#      recorded in the v002 JSON;
#   2. base sets rebuilt from the package == the production base sets (CF_M / CF_F in FITDIR when given): every key array identical, delta(T) identical on
#      the anatomical suite at 25 / 50 / 75 / 100 %;
#   3. every state set rebuilt from the package == the fitted state set (FITDIR/CF_state_<STATE>) key by key and in delta(T) on its own body;
#   4. blend identities on every endpoint body: Blend(B, {}) == B and Blend(B, {S: 1}) == S exactly (max |difference| reported, expected 0.0), and
#      Blend(B, {S: 0}) == B; neutral (rest pose): B, S and every blend give exactly 0 displacement.
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_layer_harness as H, sa6_blend as BL
BD, OUT = sys.argv[1:3]; FD = sys.argv[3] if len(sys.argv) > 3 else None; FR = (0.25, 0.5, 0.75, 1.0)
man = json.load(open(os.path.join(H.PKG, 'SA_RP6_rig_manifest_v001.json')))['files']
res = dict(status='RP6 RIG PILOT / NOT FROZEN', name='SA_RP6_layer_identity_v001', package=H.PKG, inputs={}, base={}, states={})
for f in ('SA_RP6_correctives_M_v001.npz', 'SA_RP6_correctives_F_v001.npz', 'SA_RP6_weights_M_v001.npz', 'SA_RP6_weights_F_v001.npz', 'SA_RP6_creator_layers_v001.npz'):
    p = os.path.join(H.PKG, f); h = C.sha(p); res['inputs'][f] = dict(sha256=h, bytes=os.path.getsize(p), manifest_match=bool(man.get(f, {}).get('sha256') == h and man[f]['bytes'] == os.path.getsize(p)))
c2 = json.load(open(os.path.join(H.PKG, C.BASE_CORR))); l2 = json.load(open(os.path.join(H.PKG, 'SA_RP6_creator_layers_v002.json')))
res['inputs']['v002_array_hashes_match'] = bool(all(c2['array_sha256'][c] == res['inputs']['SA_RP6_correctives_%s_v001.npz' % c]['sha256'] for c in 'MF') and l2['array_sha256'] == res['inputs']['SA_RP6_creator_layers_v001.npz']['sha256'])
def keys_equal(a, b):
    bad = []; ka = {(f['bone'], tuple(np.round(f['axis'], 6))): f for f in a.F.values()}; kb = {(f['bone'], tuple(np.round(f['axis'], 6))): f for f in b.F.values()}
    if set(ka) != set(kb): bad.append('family set')
    for k in set(ka) & set(kb):
        fa, fb = ka[k], kb[k]
        if fa['samples'] != fb['samples']: bad.append(('samples', k)); continue
        for (ia, da), (ib, db) in zip(fa['D'], fb['D']):
            if not (np.array_equal(ia, ib) and np.array_equal(da, db)): bad.append(('array', k))
    if set(a.PK) != set(b.PK): bad.append('pose-key set')
    for k in set(a.PK) & set(b.PK):
        if not (np.array_equal(a.PK[k]['idx'], b.PK[k]['idx']) and np.array_equal(a.PK[k]['d'], b.PK[k]['d']) and
                [(x[0], list(np.round(x[1], 6)), x[2]) for x in a.PK[k]['drivers']] == [(x[0], list(np.round(x[1], 6)), x[2]) for x in b.PK[k]['drivers']]): bad.append(('pk', k))
    return bad
def poses(R):
    for pn, spec in R.suite('anat').items():
        for fr in FR: yield pn, fr, R.pose([(b, p, a, dg * fr) for b, p, a, dg in spec])
bm = json.load(open(os.path.join(BD, 'bodies.json')))['bodies']
for cfg in 'MF':
    R = SP.Rig(cfg, C.w_path(cfg, H.PKG)); B = H.load_base(R, cfg); r = dict(n_families=len(B.F), n_keys=sum(len(f['D']) for f in B.F.values()), n_pose_keys=len(B.PK))
    if FD:
        Bf = CC.Correctives.load(R, os.path.join(FD, 'CF_%s.json' % cfg)); r['keys_equal_production'] = keys_equal(B, Bf) == []
        r['max_delta_diff_cm'] = max(float(np.abs(B.delta(T) - Bf.delta(T)).max()) for _, _, T in poses(R))
    r['neutral_max_cm'] = float(np.abs(B.delta(R.pose([]))).max()); res['base'][cfg] = r; print('base', cfg, r, flush=True)
for nm in H._js('SA_RP6_creator_layers_v002.json')['states']:
    b = bm['END_' + nm]; R, _ = BL.rig_of('END_' + nm, b, BD); cfg = b['cfg']; B = H.load_base(R, cfg); S, _ = H.load_state(R, nm); r = dict(base_config=cfg)
    if FD:
        sp = os.path.join(FD, 'CF_state_%s.json' % nm); sp = sp if os.path.exists(sp) else os.path.join(FD, 'pd2fit', 'CF_state_%s.json' % nm)
        Sf = CC.Correctives.load(R, sp); bad = keys_equal(S, Sf); r['keys_equal_fitted'] = bad == []; r['key_mismatches'] = [str(x) for x in bad[:5]]
    d_fit = d_b0 = d_s1 = d_w0 = 0.0
    for _, _, T in poses(R):
        s = S.delta(T); bb = B.delta(T)
        if FD: d_fit = max(d_fit, float(np.abs(s - Sf.delta(T)).max()))
        d_b0 = max(d_b0, float(np.abs(H.Blend(B, []).delta(T) - bb).max())); d_s1 = max(d_s1, float(np.abs(H.Blend(B, [(1.0, S)]).delta(T) - s).max()))
        d_w0 = max(d_w0, float(np.abs(H.Blend(B, [(0.0, S)]).delta(T) - bb).max()))
    T0 = R.pose([]); r.update(max_diff_vs_fitted_cm=d_fit, zero_influence_minus_base_cm=d_b0, unit_influence_minus_state_cm=d_s1, weight0_minus_base_cm=d_w0,
                              neutral_max_cm=dict(base=float(np.abs(B.delta(T0)).max()), state=float(np.abs(S.delta(T0)).max()), blend_half=float(np.abs(H.Blend(B, [(0.5, S)]).delta(T0)).max())))
    res['states'][nm] = r; print(nm, r, flush=True)
res['all_identities_exact'] = bool(all(v['manifest_match'] for k, v in res['inputs'].items() if isinstance(v, dict)) and res['inputs']['v002_array_hashes_match'] and
                                   all(v['neutral_max_cm'] == 0 for v in res['base'].values()) and all(v.get('max_delta_diff_cm', 0) == 0 and v.get('keys_equal_production', True) for v in res['base'].values()) and
                                   all(s['zero_influence_minus_base_cm'] == 0 and s['unit_influence_minus_state_cm'] == 0 and s['weight0_minus_base_cm'] == 0 and s['max_diff_vs_fitted_cm'] == 0 and
                                       s.get('keys_equal_fitted', True) and max(s['neutral_max_cm'].values()) == 0 for s in res['states'].values()))
json.dump(res, open(OUT, 'w'), indent=1); print('ALL IDENTITIES EXACT', res['all_identities_exact'])
