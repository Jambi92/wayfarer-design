# RM-OT-05AB: read-only limb/trunk section profiles for joint-centre estimation (donor C or a W1/control r6 mesh).
# For every height step: all section loops with centre, extents, perimeter. Writes a compact JSON the joint estimator reads.
# Usage: python3 ab_profile.py OUT.json NAME=PATH[:gor6|npzrev] [STEP_CM=0.5]
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'rmot05aa_drivers')); import aa_macro
out, spec = sys.argv[1], sys.argv[2]; step = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
name, m = aa_macro.load(spec); H = float(m.bounds[1][2]); rows = []
for z in np.arange(step, H - step, step):
    s = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if s is None: continue
    L = []
    for e in s.discrete:
        c = e.mean(0); L.append([round(float(c[0]), 2), round(float(c[1]), 2), round(float(e[:, 0].min()), 2), round(float(e[:, 0].max()), 2),
                                 round(float(e[:, 1].min()), 2), round(float(e[:, 1].max()), 2), round(float(np.linalg.norm(np.diff(e, axis=0), axis=1).sum()), 2)])
    rows.append([round(float(z), 2), L])
json.dump(dict(name=name, H=H, step=step, fields='cx cy xmin xmax ymin ymax perimeter', rows=rows), open(out, 'w')); print(name, H, len(rows))
