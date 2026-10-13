# RM-OT-05S handoff verification setup: re-establish correspondence for an externally edited / sculpted mesh so that
# s_verify.py can score it. Protected source faces are found by EXACT vertex coordinates (any face / vertex order on
# export is fine, but protected vertices must not be moved). Writes the reordered OBJ (P05S faces first, in order),
# maps (src_vertex) and labels (0 = exact source face, 5 = edited / new INFERRED).
# Usage: python3 s_rematch.py --edited EDITED.obj --src F1_working.obj --plan <05S plan dir> --out PREFIX
import argparse, json, numpy as np, trimesh, os
ap = argparse.ArgumentParser(); ap.add_argument('--edited'); ap.add_argument('--src'); ap.add_argument('--plan'); ap.add_argument('--out'); a = ap.parse_args()
e = trimesh.load(a.edited, process=False); Ve = np.asarray(e.vertices); Fe = np.asarray(e.faces)
s = trimesh.load(a.src, process=False); Vs = np.asarray(s.vertices); Fs = np.asarray(s.faces)
P = np.load(os.path.join(a.plan, 'interface_sets.npz'))['P05S_src_ordered']
key = {tuple(v): i for i, v in enumerate(Vs.tolist())}; smap = np.array([key.get(tuple(v), -1) for v in Ve.tolist()])
fkey = {}
for i, f in enumerate(Fe):
    if (smap[f] >= 0).all():
        m = smap[f]; r = int(np.argmin(m)); fkey[tuple(np.roll(m, -r))] = i
order = []; missing = 0
for f in Fs[P]:
    r = int(np.argmin(f)); i = fkey.get(tuple(np.roll(f, -r)))
    if i is None: missing += 1
    else: order.append(i)
rest = np.setdiff1d(np.arange(len(Fe)), order); Fo = np.vstack([Fe[order], Fe[rest]]); lab = np.r_[np.zeros(len(order), np.int8), np.full(len(rest), 5, np.int8)]
with open(a.out + '.obj', 'w') as fh:
    np.savetxt(fh, Ve, fmt='v %.17g %.17g %.17g'); np.savetxt(fh, Fo + 1, fmt='f %d %d %d')
np.savez(a.out + '_maps.npz', src_vertex=smap); np.save(a.out + '_face_labels.npy', lab)
rep = dict(protected_faces_expected=int(len(P)), protected_faces_found_exact=int(len(order)), protected_faces_missing_or_moved=int(missing), edited_faces=int(len(rest)))
print(json.dumps(rep, indent=1)); json.dump(rep, open(a.out + '_rematch.json', 'w'), indent=1)
