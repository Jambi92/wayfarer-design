# sa6_gate_reset.py LAYERDIR OUTDIR [STATES] : start sets for the rig v002 pass-7 state-layer refit (order 07a3f24c §4; sa6_pd2_fit.gate_set).
#   The pass 1-6 state layers were fitted on the 34 anatomical poses only.  Their family samples BEYOND the anatomical driver range (angles only the special
#   gates reach: foot +-25, jaw -24 / -32, ...) were never refitted: they still held the rig v001 state values, which fold the ankle / foot / jaw gates on
#   heavy states.  This resets exactly those samples to the base v003 sample (the layer adds nothing there, as in layer v004), leaving every sample inside the
#   anatomical range, every pose key and every other family untouched -> anatomical results are unchanged (the hat at an anatomical angle never reaches a
#   sample beyond the range).  The pass-7 fit (PD2_GATES=1) then fits the gates from this start.  Writes OUTDIR/CF_state_<S>.json/.npz + OUTDIR/reset.json.
import sys, os, json, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
assert os.environ.get('RP6_RIG') == 'v002'
import sa6_correctives as CC, sa6_pd2_fit as PF
LD, OD = sys.argv[1:3]; os.makedirs(OD, exist_ok=True)
ST = sys.argv[3].split(',') if len(sys.argv) > 3 else sorted(os.path.basename(p)[9:-5] for p in glob.glob(LD + '/CF_state_*.json'))
rec = json.load(open(OD + '/reset.json')) if os.path.exists(OD + '/reset.json') else {}
for nm in ST:
    R, cfg = PF.state_rig(nm); B = CC.Correctives.load(R, PF.WD + '/CF_%s.json' % cfg); K = CC.Correctives.load(R, LD + '/CF_state_%s.json' % nm)
    rng = {k: 0.0 for k in K.F}
    for sp in R.suite('anat').values():
        T = R.pose(sp)
        for k, f in K.F.items(): rng[k] = max(rng[k], abs(K.driver(T, f)))
    out = []
    for k, f in K.F.items():
        if k not in B.F or f.get('layer'): continue
        fb = B.F[k]
        for i, s in enumerate(f['samples']):
            if abs(s) <= rng[k] + 1e-6 or s not in fb['samples']: continue
            idx, dd = fb['D'][fb['samples'].index(s)]
            old = np.zeros((R.nv, 3)); old[f['D'][i][0]] = f['D'][i][1]; new = np.zeros((R.nv, 3)); new[idx] = dd
            out.append(dict(family=k, sample_deg=s, anatomical_range_deg=round(rng[k], 3), max_change_cm=round(float(np.linalg.norm(new - old, axis=1).max()), 4)))
            f['D'][i] = (idx.copy(), dd.copy())
    js = json.load(open(LD + '/CF_state_%s.json' % nm)); meta = {k: v for k, v in js.items() if k not in ('families', 'pose_keys', 'name', 'arrays')}
    K.save(OD + '/CF_state_%s.json' % nm, dict(meta, gate_reset=dict(tool='sa6_gate_reset.py', source=LD, samples_reset=len(out))))
    rec[nm] = out; json.dump(rec, open(OD + '/reset.json', 'w'), indent=1)
    print(nm, 'reset', len(out), 'samples, max change %.3f cm' % max([o['max_change_cm'] for o in out] or [0]), flush=True)
