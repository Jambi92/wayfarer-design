# hv_cuff_repair.py BRANCH.npz HEAD : Halvren HE2 closure order -- HR1 cuff SLIVER REPAIR (part of the Halvren ear realization path; geometry only, topology
# unchanged, deterministic). The HR1 skin-hugging cuff can leave isolated cuff quads with a corner < 12 deg at the lower postauricular corner (seen on c2 /
# other heads, e.g. right-side face 58925). For every cuff (or cuff-adjacent transition) quad with a corner < 12 deg, the CUFF vertices of that quad and
# their cuff 1-ring are relaxed TANGENTIALLY (umbrella step projected onto the local tangent plane, so the skin surface is kept) for up to 40 steps,
# accepted only while the worst corner of the affected quads improves. Root-loop (v005) vertices and the ear sheet never move. Rewrites the npz in place
# and records the repair in the branch json ('hv_cuff_repair'). Root visual integration order: a stage-2 per-vertex tangential pattern search (below) handles
# slivers at the cuff / rim seam that the umbrella step cannot improve, and over-stretched (aspect > 10) cuff quads.
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
def aspect(X, F):
    L = np.stack([np.linalg.norm(X[F[:, (k + 1) % 4]] - X[F[:, k]], axis=1) for k in range(4)], 1); return L.max(1) / (L.min(1) + 1e-30)
score = lambda X, F: min(corners(X, F).min(), 12.0 * 10.0 / max(aspect(X, F).max(), 10.0))   # worst corner, penalised once any quad aspect exceeds 10
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
# stage 2 (only if quads < 12 deg or with aspect > 10 remain, e.g. at the cuff/rim seam where the rim never moves): deterministic per-vertex tangential pattern search on the
# cuff vertices of the remaining bad quads; a move is kept only if the worst corner of all quads around that vertex improves (no other quad may drop below it) and no quad aspect exceeds 10
mn = corners(V, Q[cufff]); bad = cufff[(mn < 12.0) | (aspect(V, Q[cufff]) > 10.0)]; s2 = []   # remaining slivers or over-stretched (aspect > 10) cuff quads
if len(bad):
    mv = sorted({int(v) for f in bad for v in Q[f] if part[v] == 'cuff'})
    for sweep in range(30):
        moved = False
        for v in mv:
            A = np.array(vf[v]); cur = score(V, Q[A]); n = vnormal(V, v); e1 = np.cross(n, [1.0, 0, 0]); e1 = e1 if np.linalg.norm(e1) > 0.1 else np.cross(n, [0, 1.0, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
            L = np.mean([np.linalg.norm(V[w] - V[v]) for w in nb[v]]); best = (cur, None)
            for st in (0.15, 0.07, 0.03):
                for a in range(8):
                    d = st * L * (np.cos(a * np.pi / 4) * e1 + np.sin(a * np.pi / 4) * e2); X = V.copy(); X[v] += d; m2 = score(X, Q[A])
                    if m2 > best[0] + 1e-4: best = (m2, d)
            if best[1] is not None: V[v] += best[1]; moved = True
        if not moved: break
    s2 = dict(vertices=mv, sweeps=sweep + 1, worst_after_deg=round(float(corners(V, Q[cufff]).min()), 2), worst_aspect_after=round(float(aspect(V, Q[cufff]).max()), 2))
    log.append(dict(stage2=s2))
z['V'] = V.astype(z['V'].dtype); np.savez_compressed(P, **z) if False else np.savez(P, **z)
rec['hv_cuff_repair'] = dict(rule='tangential umbrella relaxation of cuff vertices of quads with a corner < 12 deg (+ cuff 1-ring), accepted while the worst corner improves; stage 2 per-vertex tangential pattern search if any remain', log=log)
json.dump(rec, open(P.replace('.npz', '.json'), 'w'), indent=1)
print(json.dumps(log))
