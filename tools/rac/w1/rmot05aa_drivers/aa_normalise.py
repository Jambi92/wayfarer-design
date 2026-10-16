# RM-OT-05AA AA0: DISPLAY copies for the macro-frame exhibit: each mesh is uniformly scaled to a common displayed height (1.90 m) and
# centred on its trunk midline, written as glTF-axis npz for x_render.py. Display only; no source is written. Uniform scaling here is
# an exhibit normalisation (proportions unchanged), not a modification of any working mesh.
# Usage: python3 aa_normalise.py OUTDIR NAME=PATH[:gor6|npzrev] ...
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import aa_macro
out = sys.argv[1]; info = {}
for spec in sys.argv[2:]:
    name, m = aa_macro.load(spec); V = np.asarray(m.vertices); H = V[:, 2].max(); s = 1.90 / (H / 100)
    W = V / 100 * s; G = np.stack([W[:, 0], W[:, 2], -W[:, 1]], 1)          # review frame (front -Y) -> glTF (front +Z)
    np.savez(os.path.join(out, name + '.npz'), V=G.astype(np.float32), F=np.asarray(m.faces, np.int32)); info[name] = dict(source_height_raw=round(H, 1), display_scale=round(s, 5))
json.dump(info, open(os.path.join(out, 'normalise.json'), 'w'), indent=1); print(info)
