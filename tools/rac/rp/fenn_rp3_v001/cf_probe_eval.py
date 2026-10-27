# cf_probe_eval.py PROBEDIR OUT.json : response of each MPFB head / face target (value 0.5 on FNL4) -- descriptor deltas (% of FNL4), region RMS (head size
# removed) and the largest non-head displacement (body architecture must not change).
import sys, os, json, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fn_face_metrics as F
PD, OUT = sys.argv[1:3]; base = F.load(F.TEMPLATE_R6); b0 = F.descriptors(base['V']); res = {}
nonhead = (base['wh'] < 0.05) & ~F.EAR
for d in sorted(glob.glob(PD + '/*/P_r6.npz')):
    tag = d.split('/')[-2]; V = F.load(d)['V']; ds = F.descriptors(V); rr, _ = F.region_rms(V, base['V'])
    res[tag] = dict(delta_pct={k: round(100 * (ds[k] / b0[k] - 1), 3) for k in ds}, region_rms_mm=rr, nonhead_max_mm=round(float(np.linalg.norm(V[nonhead] - base['V'][nonhead], axis=1).max() * 10), 3),
                    stature_change_mm=round(float((V[:, 2].max() - V[:, 2].min()) - (base['V'][:, 2].max() - base['V'][:, 2].min())) * 10, 3))
    print('%-28s' % tag, ' '.join('%s %+.2f' % (k.split('_over')[0][:10], v) for k, v in res[tag]['delta_pct'].items() if k != 'head_height_cm'), '| HH %+.2f nonhead %.2fmm' % (res[tag]['delta_pct']['head_height_cm'], res[tag]['nonhead_max_mm']))
json.dump(dict(baseline=b0, probes=res), open(OUT, 'w'), indent=1, default=float)
