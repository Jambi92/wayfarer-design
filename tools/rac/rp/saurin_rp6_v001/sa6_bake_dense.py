# sa6_bake_dense.py NAME BODYDIR ARTDIR OUTDIR : dense between-sample audit of a per-body bake (offline bake validation order 8e3b7b4d).
#   Added after a 0.0025-grid check of END_MUFAHI pass-2 it3 on trunk_twist_30 found rig-owned failures BETWEEN the 0.025 sweep samples
#   (0.585-0.5925 contact, 0.64-0.6475 a fold) that the full sweep (SW) does not sample: the bake clears the packaged blend's defect at the fitted fractions only.
#   Pose set = the sweep's dense set (every pose touched by a bake family / pose key + the heavy-joint RISK set); each is played 0 -> 1 on a DENSE_STEP grid
#   (default 0.0025 = 1/400 of the full angle) plus +-0.25 deg at every bake / packaged-blend transition.  Same closure gates and ownership as sa6_blend.evaluate.
#   Records, per pose, the failing fractions of the bake AND of the packaged blend (prod) on the same grid, so a between-sample leak (prod fails, bake fails)
#   is told apart from a defect the bake adds (prod clean, bake fails).  DENSE_SHARD='i/n' -> poses[i::n], per-pose resume; --merge NAME OUTDIR -> DS_<NAME>.json
import sys, os, json, time, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v004.json')
if sys.argv[1] == '--merge':
    nm, OD = sys.argv[2:4]; out = None
    for p in sorted(glob.glob(os.path.join(OD, 'DS_%s.s*of*.json' % nm))):
        j = json.load(open(p)); out = out or dict(j, poses={}); out['poses'].update(j['poses'])
    for k in ('shard', 'shard_poses'): out.pop(k, None)
    out['clean'] = all(not v['bake_failing'] for v in out['poses'].values())
    out['n_samples'] = sum(v['n_samples'] for v in out['poses'].values())
    out['bake_failing_samples'] = sum(len(v['bake_failing']) for v in out['poses'].values())
    out['prod_failing_samples'] = sum(len(v['prod_failing']) for v in out['poses'].values())
    out['bake_added'] = sum(len(v['bake_added']) for v in out['poses'].values())
    json.dump(out, open(os.path.join(OD, 'DS_%s.json' % nm), 'w'), indent=1)
    print(nm, 'DENSE clean', out['clean'], 'samples', out['n_samples'], 'bake failing', out['bake_failing_samples'], '(added', out['bake_added'], ') prod failing', out['prod_failing_samples'], flush=True); sys.exit(0)
import sa6_blend as BL, sa6_layer_harness as H, sa6_correctives as CC
from sa6_bake import peak_mb
t_all = time.time(); nm, BD, AD, OD = sys.argv[1:5]; os.makedirs(OD, exist_ok=True); art = os.path.join(AD, 'BK_%s.json' % nm)
STEP = float(os.environ.get('DENSE_STEP', '0.0025'))
b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; R, z = BL.rig_of(nm, b, BD); K = CC.Correctives.load(R, art)
P0 = H.Blend(H.load_base(R, b['cfg']), [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]); suite = R.suite('anat')
kb = {f['bone'] for f in K.F.values()}; pkp = {k.rsplit('@', 1)[0] for k in K.PK}
RISK = ['shoulder_abd45_xpos', 'shoulder_abd45_xneg', 'shoulder_abd90_xpos', 'shoulder_abd90_xneg', 'shoulder_flex60_xpos', 'shoulder_flex60_xneg',
        'hip_flex70_xpos', 'hip_flex70_xneg', 'trunk_twist_30', 'lower_axial_flex_25']
kp = [pn for pn, spec in suite.items() if pn in pkp or R.bones_of(spec) & kb]
poses = sorted(set(kp) | {pn for pn in RISK if pn in suite})
if os.environ.get('DENSE_ONLY'): poses = [p for p in poses if p in os.environ['DENSE_ONLY'].split(',')]     # diagnostics only (never set in a bake)
FAM = list(K.F.values()) + [f for st in [P0.B] + [s_ for _, s_ in P0.S] for f in getattr(st, 'F', {}).values()]
SH = os.environ.get('DENSE_SHARD'); si, sn = (int(x) for x in SH.split('/')) if SH else (0, 1); tag = '.s%dof%d' % (si, sn) if SH else ''
OUT = os.path.join(OD, 'DS_%s%s.json' % (nm, tag))
out = json.load(open(OUT)) if os.path.exists(OUT) else dict(status='RP6 RIG PILOT / NOT FROZEN', name=nm, artifact=os.path.basename(art), step=STEP,
    pose_set='sweep dense set: bake-touched poses + heavy-joint RISK set', rule='rig-owned folds / contact / tears / volume (sa6_blend.evaluate ownership)', poses={})
for pn in poses[si::sn]:
    if pn in out['poses']: continue
    t0 = time.time(); spec = suite[pn]; T1 = R.pose(spec); fr = set(np.round(np.arange(0, 1.0 + 1e-9, STEP), 5))
    for f in FAM:                    # transitions as pose fractions; R.fracs_at inverts the coupled (v002) driver exactly
        if f['bone'] not in R.bones_of(spec): continue
        fr.update(round(x, 5) for x in R.fracs_at(spec, lambda T_: K.driver(T_, f), [s_ + e for s_ in f['samples'] for e in (-0.25, 0.25)], key=(f['bone'], tuple(f['axis']))))
    for k, pk in K.PK.items():
        if k.rsplit('@', 1)[0] != pn: continue
        dd = dict(bone=pk['drivers'][0][0], axis=pk['drivers'][0][1]); s_ = pk['drivers'][0][2]; w = (pk.get('width') or [abs(s_)])[0]
        fr.update(round(x, 5) for x in R.fracs_at(spec, lambda T_: K.driver(T_, dd), [c + e for c in (s_ - w, s_, s_ + w) for e in (-0.25, 0.25)], key=(dd['bone'], tuple(dd['axis']))))
    fr = sorted(f for f in fr if 0 < f <= 1)
    r = BL.evaluate(nm, b, BD, fr, [pn], bake=art)['poses'][pn]
    def failing(c): return sorted(k_ for k_, v in r.items() if v[c]['rig_flips'] or v[c]['rig_pen'] or v[c]['rig_tears'] or not v[c]['volume_ok'])
    bf, pf = failing('bake'), failing('prod')
    out['poses'][pn] = dict(n_samples=len(fr), full_deg=float(max(abs(dg) for _, _, _, dg in spec)), bake_failing=bf, prod_failing=pf,
                            bake_added=[f for f in bf if f not in set(pf)],
                            bake_detail={k_: {x: r[k_]['bake'][x] for x in ('rig_flips', 'rig_pen', 'rig_tears', 'volume_ok', 'dV_cm3')} for k_ in bf},
                            seconds=round(time.time() - t0, 1))
    json.dump(out, open(OUT, 'w'), indent=1)
    print('%s %-24s %4d samples bake failing %3d (added %d) prod failing %3d | %.0fs %.0f MB' % (nm, pn, len(fr), len(bf), len(out['poses'][pn]['bake_added']), len(pf), time.time() - t0, peak_mb()), flush=True)
out['shard'] = SH; out['shard_poses'] = poses[si::sn]; out['all_poses'] = poses; out['seconds'] = round(time.time() - t_all, 1); out['peak_mb'] = round(peak_mb(), 1)
json.dump(out, open(OUT, 'w'), indent=1)
if not SH:
    out['clean'] = all(not v['bake_failing'] for v in out['poses'].values()); json.dump(out, open(OUT, 'w'), indent=1)
