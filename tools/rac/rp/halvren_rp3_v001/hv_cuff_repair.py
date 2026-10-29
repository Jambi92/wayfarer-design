# hv_cuff_repair.py BRANCH.npz HEAD : Halvren HE2 closure order -- HR1 cuff SLIVER REPAIR (part of the Halvren ear realization path; geometry only, topology
# unchanged, deterministic). The HR1 skin-hugging cuff can leave isolated cuff quads with a corner < 12 deg at the lower postauricular corner (seen on c2 /
# other heads, e.g. right-side face 58925). For every cuff (or cuff-adjacent transition) quad with a corner < 12 deg, the CUFF vertices of that quad and
# their cuff 1-ring are relaxed TANGENTIALLY (umbrella step projected onto the local tangent plane, so the skin surface is kept) for up to 40 steps,
# accepted only while the worst corner of the affected quads improves. Root-loop (v005) vertices and the ear sheet never move. Rewrites the npz in place
# and records the repair in the branch json ('hv_cuff_repair').
import sys, json, numpy as np
P, H = sys.argv[1:3]; z = dict(np.load(P)); V = z['V'].astype(float); Q = np.asarray(z['Q']); part = z['part']; rec = json.load(open(P.replace('.npz', '.json')))
br = (part[Q] != 'v005').any(1); cufff = np.nonzero((part[Q] == 'cuff').any(1) & br)[0]
def corners(X, F):
    a = []
    for k in range(4):
        u = X[F[:, (k - 1) % 4]] - X[F[:, k]]; w = X[F[:, (k + 1) % 4]] - X[F[:, k]]
        a.append(np.degrees(np.arccos(np.clip((u * w).sum(1) / (np.linalg.norm(u, axis=1) * np.linalg.norm(w, axis=1) + 1e-30), -1, 1))))
    return np.min(a, 0)
nb = {}
for q in Q[cufff]:
    for k in range(4): nb.setdefault(q[k], set()).update((q[(k + 1) % 4], q[(k - 1) % 4]))
vf = {}
for fi, q in enumerate(Q):
    for v in q: vf.setdefault(int(v), []).append(fi)
def vnormal(X, v):
    n = np.zeros(3)
    for f in vf[v]:
        q = Q[f]; n += np.cross(X[q[2]] - X[q[0]], X[q[3]] - X[q[1]])
    return n / (np.linalg.norm(n) + 1e-30)
log = []
for it in range(3):
    mn = corners(V, Q[cufff]); bad = cufff[mn < 12.0]
    if not len(bad): break
    mv = {int(v) for f in bad for v in Q[f] if part[v] == 'cuff'}; mv |= {int(w) for v in list(mv) for w in nb.get(v, ()) if part[w] == 'cuff'}; mv = sorted(mv)
    aff = sorted({f for v in mv for f in vf[v]}); A = np.array(aff); best = corners(V, Q[A]).min(); X = V.copy(); steps = 0
    for s in range(40):
        Y = X.copy()
        for v in mv:
            c = np.mean([X[w] for w in nb[v]], 0) - X[v]; n = vnormal(X, v); Y[v] = X[v] + 0.5 * (c - (c @ n) * n)
        m2 = corners(Y, Q[A]).min()
        if m2 <= best + 1e-6: break
        X = Y; best = m2; steps += 1
    log.append(dict(iteration=it, bad_faces=[int(f) for f in bad], moved_vertices=len(mv), steps=steps, worst_after_deg=round(float(best), 2), max_move_cm=round(float(np.abs(X - V).max()), 4)))
    if steps == 0: break
    V = X
z['V'] = V.astype(z['V'].dtype); np.savez_compressed(P, **z) if False else np.savez(P, **z)
rec['hv_cuff_repair'] = dict(rule='tangential umbrella relaxation of cuff vertices of quads with a corner < 12 deg (+ cuff 1-ring), accepted while the worst corner improves', log=log)
json.dump(rec, open(P.replace('.npz', '.json'), 'w'), indent=1)
print(json.dumps(log))
