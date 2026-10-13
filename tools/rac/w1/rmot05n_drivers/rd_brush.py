# RM-OT-05N surface brush pass on the finished RD mesh (l_brush engine). Stroke points are placed by hand near the body and
# snapped to the surface (nearest vertex in the given half-space direction). Usage: rd_brush.py IN.obj STROKES.json OUT.obj
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05l_drivers'); from l_brush import Mesh, stroke
from scipy.spatial import cKDTree
V = np.array([[float(t) for t in l.split()[1:4]] for l in open(sys.argv[1]) if l.startswith('v ')])
F = np.array([[int(t) - 1 for t in l.split()[1:4]] for l in open(sys.argv[1]) if l.startswith('f ')])
M = Mesh(V, F); T = cKDTree(V); log = []
for s in json.load(open(sys.argv[2])):
    pts = np.array([V[T.query(p)[1]] for p in s['pts']]); stroke(M, s['kind'], pts, s['r'], s['s'])
    log.append(dict(s, snapped=pts.round(2).tolist()))
with open(sys.argv[3], 'w') as o:
    o.write('# RAC RM-OT-05N GO-RD reference after brush pass; cm, Z up, +Y anterior\n')
    for v in M.V: o.write('v %.4f %.4f %.4f\n' % tuple(v))
    for t in F: o.write('f %d %d %d\n' % tuple(t + 1))
json.dump(log, open(sys.argv[3].replace('.obj', '_strokes.json'), 'w'), indent=1); print(len(log), 'strokes')
