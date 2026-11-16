# sa6_bake_sweep.py NAME BODYDIR ARTDIR OUTDIR : driver-transition sweep of a per-body bake (per-body bake feasibility order a13cae71 §2).
#   For every anatomical pose driven by a bone that carries a bake family, or owning a bake pose key, the pose's angle fraction is swept 0 -> 1 in steps of
#   0.025 and sampled at +-0.25 deg on both sides of every bake transition: each bake family sample, and each bake pose-key centre and tent edge.
#   Gates: the closure gates of sa6_blend.evaluate (same ownership rules, rig-owned folds / contact / tears / volume, rigid set), on the baked production.
#   Continuity: max |d(corrective)| per degree between neighbouring samples vs the sweep median (a jump at a driver boundary shows as a spike).
#   The evaluator is stateless (corrective = f(T) only), so the return sweep equals the forward sweep by construction (recorded, not recomputed).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v004.json')
import sa6_blend as BL, sa6_layer_harness as H, sa6_correctives as CC
nm, BD, AD, OD = sys.argv[1:5]; os.makedirs(OD, exist_ok=True); art = os.path.join(AD, 'BK_%s.json' % nm)
b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; R, z = BL.rig_of(nm, b, BD); K = CC.Correctives.load(R, art)
P0 = H.Blend(H.load_base(R, b['cfg']), [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]); suite = R.suite('anat')
kb = {f['bone'] for f in K.F.values()}; pkp = {k.rsplit('@', 1)[0] for k in K.PK}
poses = [pn for pn, spec in suite.items() if pn in pkp or any(e[0] in kb for e in spec)]
out = dict(status='RP6 RIG PILOT / NOT FROZEN', name=nm, artifact=os.path.basename(art), poses={}, return_sweep='identical by construction (stateless evaluator)')
for pn in poses:
    spec = suite[pn]; T1 = R.pose(spec); fr = set(np.round(np.arange(0, 1.0001, 0.025), 4))
    for f in K.F.values():
        if not any(e[0] == f['bone'] for e in spec): continue
        x1 = K.driver(T1, f)
        if abs(x1) < 1e-6: continue
        for s_ in f['samples']:
            for e in (-0.25, 0.25): fr.add(round((s_ + e * np.sign(x1)) / x1, 5))
    for k, pk in K.PK.items():
        if k.rsplit('@', 1)[0] != pn: continue
        x1 = K.driver(T1, dict(bone=pk['drivers'][0][0], axis=pk['drivers'][0][1])); s_ = pk['drivers'][0][2]; w = (pk.get('width') or [abs(s_)])[0]
        if abs(x1) < 1e-6: continue
        for c in (s_ - w, s_, s_ + w):
            for e in (-0.25, 0.25): fr.add(round((c + e * np.sign(x1)) / x1, 5))
    fr = sorted(f for f in fr if 0 <= f <= 1)
    r = BL.evaluate(nm, b, BD, fr, [pn], bake=art)
    full = max(abs(dg) for _, _, _, dg in spec); prev = None; rates = []
    for f in fr:
        d = P0.delta(R.pose([(bb, p, a, dg * f) for bb, p, a, dg in spec])) + K.delta(R.pose([(bb, p, a, dg * f) for bb, p, a, dg in spec]))
        if prev is not None and f > prev[0]: rates.append((np.abs(d - prev[1]).max() / ((f - prev[0]) * full), prev[0], f))
        prev = (f, d)
    rv = [x[0] for x in rates]; med = float(np.median(rv)) if rv else 0.0; mx = max(rates) if rates else (0, 0, 0)
    bad = [(k_, v['bake']) for k_, v in r['poses'][pn].items() if v['bake']['rig_flips'] or v['bake']['rig_pen'] or v['bake']['rig_tears'] or not v['bake']['volume_ok']]
    out['poses'][pn] = dict(n_samples=len(fr), gate_failures=[dict(frac=k_, **{x: v[x] for x in ('rig_flips', 'rig_pen', 'rig_tears', 'volume_ok', 'dV_cm3', 'regions')}) for k_, v in bad],
                            rigid_max_cm=max(v['bake'].get('rigid_max_cm', 0) for v in r['poses'][pn].values()), rate_max_cm_per_deg=float(mx[0]), rate_median_cm_per_deg=med,
                            rate_ratio=float(mx[0] / med) if med > 0 else 0.0, rate_max_at=[float(mx[1]), float(mx[2])])
    print(nm, pn, len(fr), 'samples, gate failures', len(bad), 'rate max %.4f median %.4f cm/deg' % (mx[0], med), flush=True)
out['clean'] = all(not v['gate_failures'] and v['rigid_max_cm'] <= 0.05 for v in out['poses'].values())
json.dump(out, open(os.path.join(OD, 'SW_%s.json' % nm), 'w'), indent=1); print(nm, 'SWEEP clean', out['clean'], 'poses', len(poses), flush=True)
