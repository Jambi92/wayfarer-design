# RAC W3B canonical field metrics (reference for every scale guard): core = smooth field weight >= 0.9 (same core as every test), canonical
# seeds / fields / relief, functional bend radius on the base mesh. Writes scratch w3b/scale_canon_metrics.json
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale as SC, w3b_regions as RG
out = {}
for k, m in RG.masks().items():
    w = SC.weight(m); core = w >= 0.9
    rel, seeds, R, H, aff, pure = SC.variant(w, 1.0, 1.0, reseed=False)
    fm = SC.field_metrics(core, pure, seeds); fm['bend_radius_cm'] = SC.bend_radius(core); fm['span_deg'] = float(np.degrees(fm['size_cm'] / fm['bend_radius_cm']))
    fm['n_core_vertices'] = int(core.sum()); fm['n_mask_vertices'] = int(m.sum()); out[k] = fm
    print(k, {a: (round(b, 4) if isinstance(b, float) else b) for a, b in fm.items()}, flush=True)
json.dump(out, open(C.W + '/scale_canon_metrics.json', 'w'), indent=1)
