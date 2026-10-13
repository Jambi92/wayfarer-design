# RAC RM-OT-05P (from 05O o_brush.py; --stance optional = identity frame): bounded local surface refinement (transition repair) on the stance variant, with the 05L brush engine
# (tools/rac/w1/rmot05l_drivers/l_brush.py: draw / crease / flatten / smooth, mirrored bilaterally). Every stroke is named and
# placed by hand. Stroke points may be written in the RD2 frame and are carried into the stance frame with the same
# hip / ankle rotations + grounding as o_stance.py ("frame": "trunk" = rigid +dz only, "leg" = hip rotation, "foot" =
# hip + ankle counter-rotation). Points are snapped to the nearest surface vertex. Writes OUT.obj and OUT_strokes.json.
# Usage: python3 o_brush.py --in IN.obj --strokes STROKES.json --stance STANCE_record.json --out OUT.obj
import argparse, json, os, sys, numpy as np, trimesh
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rmot05l_drivers')); from l_brush import Mesh, stroke
ap = argparse.ArgumentParser(); ap.add_argument('--in', dest='inp'); ap.add_argument('--strokes'); ap.add_argument('--stance'); ap.add_argument('--out'); a = ap.parse_args()
m = trimesh.load(a.inp, process=False); V = np.asarray(m.vertices, float); F = np.asarray(m.faces)
R = json.load(open(a.stance)) if a.stance else dict(phi_deg=0, hip_axis=dict(point=[0, 0, 0]), ankle_axis=dict(point=[0, 0, 0]), grounding_dz_cm=0.0); phi = np.radians(R['phi_deg']); hc = np.array(R['hip_axis']['point']); ac = np.array(R['ankle_axis']['point']); dz = R['grounding_dz_cm']
def rotx(p, c, t):
    q = np.asarray(p, float) - c; cy, sy = np.cos(t), np.sin(t); return np.array([q[0], q[1] * cy - q[2] * sy, q[1] * sy + q[2] * cy]) + c
def carry(p, frame):
    if frame == 'leg': p = rotx(p, hc, phi)
    elif frame == 'foot': p = rotx(rotx(p, ac, -phi), hc, phi)
    return np.asarray(p, float) + [0, 0, dz]
M = Mesh(V, F); T = cKDTree(V); log = []
for s in json.load(open(a.strokes)):
    pts = np.array([V[T.query(carry(p, s.get('frame', 'trunk')))[1]] for p in s['pts']])
    stroke(M, s['kind'], pts, s['r'], s['s']); log.append(dict(s, snapped=pts.round(2).tolist()))
trimesh.Trimesh(M.V, F, process=False).export(a.out)
d = np.linalg.norm(M.V - V, axis=1)
json.dump(dict(input=a.inp, strokes=log, moved_vertices=int((d > 0.01).sum()), max_displacement_cm=round(float(d.max()), 2)), open(a.out.replace('.obj', '_strokes.json'), 'w'), indent=1)
print(len(log), 'strokes; moved', int((d > 0.01).sum()), 'max', round(float(d.max()), 2))
