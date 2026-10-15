# RM-OT-05V: source tail for the neutral ARM (GORRUND_V1 Part 1 tail row; R-11 mandatory race anatomy).
# Extracts the source tail study (base.glb connected component 4 per reviews/rac-rmot05n-evidence/source/island_manifest.json,
# 14,884 faces) from the IMMUTABLE base.glb, converts to cm Z-up exactly as the 05N part files (x, -z, y) * 100, and places it with
# the 05N organism review placement (organism_params.json: scale 1.6, root_raw, tilt 50 deg posterior, yaw -35 deg, attach at the
# sacral midline). Placement / scale are REVIEW / BUILDER values (05N: "not frozen tail numbers"), recorded as provenance (R-14).
# Usage: python3 v_tail.py --glb base.glb --params organism_params.json --x0 -0.5 --out tail_placed.obj
import argparse, json, hashlib, numpy as np, trimesh
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--glb', '--params', '--out')]; ap.add_argument('--x0', type=float, default=0.0); a = ap.parse_args()
sha = hashlib.sha256(open(a.glb, 'rb').read()).hexdigest(); assert sha == '78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b', 'base.glb differs'
sc = trimesh.load(a.glb, process=False); geo = list(sc.geometry.values()) if hasattr(sc, 'geometry') else [sc]
m = geo[0] if len(geo) == 1 else trimesh.util.concatenate(geo)
m = trimesh.Trimesh(m.vertices, m.faces, process=False); m.merge_vertices(digits_vertex=5)
cc = trimesh.graph.connected_components(m.face_adjacency, nodes=np.arange(len(m.faces)), min_len=1)
# component 4 of the manifest: the 14,884-face tail study with bbox x[-0.317,-0.147] y[0.021,0.289] z[-0.057,0.042] (GLB units)
cand = [c for c in cc if len(c) == 14884]
B = [m.vertices[np.unique(m.faces[c])] for c in cand]
sel = [c for c, b in zip(cand, B) if abs(b[:, 0].min() + 0.317) < 0.002 and abs(b[:, 1].max() - 0.289) < 0.002]
assert len(sel) == 1, 'tail component not uniquely identified'
f = m.faces[sel[0]]; u = np.unique(f); mp = -np.ones(len(m.vertices), int); mp[u] = np.arange(len(u)); Vg = m.vertices[u]; Fp = mp[f]
V = np.c_[Vg[:, 0], -Vg[:, 2], Vg[:, 1]] * 100.0           # 05N part-file convention (cm, Z up)
P = json.load(open(a.params))['tail']; s = P['scale']; r = np.array(P['root_raw'])
W = np.c_[-(V[:, 1] - r[1]) * s, (V[:, 0] - r[0]) * s, (V[:, 2] - r[2]) * s]
th = np.radians(-P['tilt_deg']); c_, s_ = np.cos(th), np.sin(th); W = np.c_[W[:, 0], W[:, 1] * c_ - W[:, 2] * s_, W[:, 1] * s_ + W[:, 2] * c_]
ps = np.radians(P['yaw_deg']); W = np.c_[W[:, 0] * np.cos(ps) - W[:, 1] * np.sin(ps), W[:, 0] * np.sin(ps) + W[:, 1] * np.cos(ps), W[:, 2]] + np.array(P['attach'])
W[:, 0] += a.x0                                             # sacral midline = the body's bilateral plane
trimesh.Trimesh(W, Fp, process=False).export(a.out)
print(json.dumps(dict(base_glb=sha, faces=int(len(Fp)), bounds=[W.min(0).round(2).tolist(), W.max(0).round(2).tolist()], placement=P, x0=a.x0)))
