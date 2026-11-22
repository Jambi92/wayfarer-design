# sa6_zero_protect.py CFG IN.json OUT.json : zero every corrective key's displacement on the BASE configuration's protected set (sa6_correctives.
#   base_protect: head unit, rigid claw caps, rigid landmarks + 2 rings -- the set the rigidity gate measures) -- rig v002 state layers / knots fitted
#   before the state / body rigs protected that set by vertex id (they re-found landmarks on their own geometry).  The result starts a refit pass whose
#   solver now holds those vertices; the refit removes any fold / tear / volume defect the zeroing re-opens.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_correctives as CC
cfg, IN, OUT = sys.argv[1:4]; js = json.load(open(IN)); z = np.load(IN.replace('.json', '.npz')); prot = CC.base_protect(cfg); out = {}; n = 0; mx = 0.0
for k in z.files:
    out[k] = z[k]
    if k.endswith('_d'):
        idx = z[k[:-2] + '_idx'].astype(np.int64); d = z[k].copy(); m = prot[idx]
        if m.any(): mx = max(mx, float(np.linalg.norm(d[m], axis=1).max())); d[m] = 0; n += int(m.sum())
        out[k] = d.astype(z[k].dtype)
js['protect_zeroed'] = dict(tool='sa6_zero_protect.py', base_config=cfg, entries=n, max_removed_cm=round(mx, 5), source=os.path.basename(IN))
np.savez_compressed(OUT.replace('.json', '.npz'), **out); json.dump(js, open(OUT, 'w'), indent=1); print(os.path.basename(IN), 'zeroed', n, 'max %.4f' % mx)
