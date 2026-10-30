# hv_cuff_repair.py BRANCH.npz HEAD : Halvren HE2 closure order -- HR1 cuff SLIVER REPAIR (part of the Halvren ear realization path; geometry only, topology
# unchanged, deterministic). The HR1 skin-hugging cuff can leave isolated cuff quads with a corner < 12 deg at the lower postauricular corner (seen on c2 /
# other heads, e.g. right-side face 58925). For every cuff (or cuff-adjacent transition) quad with a corner < 12 deg, the CUFF vertices of that quad and
# their cuff 1-ring are relaxed TANGENTIALLY (umbrella step projected onto the local tangent plane, so the skin surface is kept) for up to 40 steps,
# accepted only while the worst corner of the affected quads improves. Root-loop (v005) vertices and the ear sheet never move. Rewrites the npz in place
# and records the repair in the branch json ('hv_cuff_repair'). Root visual integration order: a stage-2 per-vertex tangential pattern search (below) handles
# slivers at the cuff / rim seam that the umbrella step cannot improve, and over-stretched (aspect > 10) cuff quads; stage 3 (family closure order) does the
# same for auricle-sheet quads with aspect > 10 (anterior cavum rows of a short HE1).
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
score = lambda X, F, am=10.0: min(corners(X, F).min(), 12.0 * am / max(aspect(X, F).max(), am))   # worst corner, penalised once any quad aspect exceeds am
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
# stage 3 (only if branch quads with aspect > 9.8 remain on the auricle sheet, e.g. the anterior cavum rows of a short human-forward HE1): the same per-vertex
# tangential pattern search on the front / back sheet vertices of those quads, applied symmetrically to each vertex and its mirror twin (junction vertices -- sheet vertices sharing a face with the cuff -- never move)
AM3 = 9.8; brf = np.nonzero((part[Q] != 'v005').any(1))[0]; bad3 = brf[aspect(V, Q[brf]) > AM3]   # target aspect 9.8 (margin under the < 10 gate)
if len(bad3):                         # SYMMETRIC: the auricle sheet has one layout order per side (left block l0.., right block r0..), so every move is applied to
    side = z['side']; shl = np.nonzero((side == 'l') & np.isin(part, ['front', 'back', 'rim']))[0]; shr = np.nonzero((side == 'r') & np.isin(part, ['front', 'back', 'rim']))[0]
    l2r = dict(zip(shl.tolist(), shr.tolist())); r2l = {b: a for a, b in l2r.items()}; MIR = np.array([-1.0, 1.0, 1.0])   # the vertex and its mirror twin (x -> -x)
    jv = {int(v) for f in np.nonzero((part[Q] == 'cuff').any(1))[0] for v in Q[f] if part[v] in ('front', 'back', 'rim')}
    mv3 = sorted({r2l.get(int(v), int(v)) for f in bad3 for v in Q[f] if part[v] in ('front', 'back') and int(v) not in jv and r2l.get(int(v), int(v)) in l2r and l2r[r2l.get(int(v), int(v))] not in jv}); V0s = V.copy()
    nbA = {}
    for f in {f for v in mv3 for f in vf[v]}:
        q = Q[f]
        for k in range(4): nbA.setdefault(int(q[k]), set()).update((int(q[(k + 1) % 4]), int(q[(k - 1) % 4])))
    for sweep3 in range(30):
        moved = False
        for v in mv3:
            w = l2r[v]; A = np.array(vf[v]); Bf = np.array(vf[w]); cur = min(score(V, Q[A], AM3), score(V, Q[Bf], AM3)); n = vnormal(V, v); e1 = np.cross(n, [1.0, 0, 0]); e1 = e1 if np.linalg.norm(e1) > 0.1 else np.cross(n, [0, 1.0, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
            L = np.mean([np.linalg.norm(V[x] - V[v]) for x in nbA[v]]); best = (cur, None)
            for st in (0.15, 0.07, 0.03):
                for a in range(8):
                    d = st * L * (np.cos(a * np.pi / 4) * e1 + np.sin(a * np.pi / 4) * e2); X = V.copy(); X[v] += d; X[w] += d * MIR; m2 = min(score(X, Q[A], AM3), score(X, Q[Bf], AM3))
                    if m2 > best[0] + 1e-4: best = (m2, d)
            if best[1] is not None: V[v] += best[1]; V[w] += best[1] * MIR; moved = True
        if not moved: break
    log.append(dict(stage3=dict(bad_faces=len(bad3), vertex_pairs=len(mv3), symmetric=True, sweeps=sweep3 + 1, worst_aspect_after=round(float(aspect(V, Q[brf]).max()), 2),
                                worst_corner_after=round(float(corners(V, Q[brf]).min()), 2), max_move_cm=round(float(np.linalg.norm(V - V0s, axis=1).max()), 4))))
# stage 4 (only when the candidate's geo sets 'sheet_fold_fix' -- HE1 / HE3 of the ear family closure; the frozen HE2 is untouched): FOLDED auricle-sheet quads
# (the two triangle splits of a quad disagree in orientation: a > 90 deg fold across a diagonal, not zero-area) read as crinkles in the scapha / crura. The
# non-junction sheet vertices of folded quads are smoothed with a full umbrella step (normal component included), symmetrically with their mirror twins, and a
# step is kept only if the side's folded-quad count drops and every branch quad keeps a corner >= 12 deg and aspect < 10.
def folded(X, F):
    q = Q[F]; n1 = np.cross(X[q[:, 1]] - X[q[:, 0]], X[q[:, 2]] - X[q[:, 0]]); n2 = np.cross(X[q[:, 2]] - X[q[:, 0]], X[q[:, 3]] - X[q[:, 0]])
    n3 = np.cross(X[q[:, 2]] - X[q[:, 1]], X[q[:, 3]] - X[q[:, 1]]); n4 = np.cross(X[q[:, 3]] - X[q[:, 1]], X[q[:, 0]] - X[q[:, 1]]); return F[((n1 * n2).sum(1) < 0) | ((n3 * n4).sum(1) < 0)]
if float(rec.get('geo', {}).get('sheet_fold_fix', 0)) > 0:
    side = z['side']; shF = np.nonzero(np.isin(part[Q], ['front', 'back', 'rim']).all(1))[0]
    shl = np.nonzero((side == 'l') & np.isin(part, ['front', 'back', 'rim']))[0]; shr = np.nonzero((side == 'r') & np.isin(part, ['front', 'back', 'rim']))[0]
    l2r = dict(zip(shl.tolist(), shr.tolist())); r2l = {b: a for a, b in l2r.items()}; MIR = np.array([-1.0, 1.0, 1.0])
    jv = {int(v) for f in np.nonzero((part[Q] == 'cuff').any(1))[0] for v in Q[f] if part[v] in ('front', 'back', 'rim')}
    nbS = {}
    for q in Q[shF]:
        for k in range(4): nbS.setdefault(int(q[k]), set()).update((int(q[(k + 1) % 4]), int(q[(k - 1) % 4])))
    f0 = len(folded(V, shF)); V0f = V.copy(); steps4 = 0
    for it4 in range(25):
        fl = folded(V, shF)
        if not len(fl): break
        mv = sorted({r2l.get(int(v), int(v)) for f in fl for v in Q[f] if int(v) not in jv and r2l.get(int(v), int(v)) in l2r and l2r[r2l.get(int(v), int(v))] not in jv})
        mv = sorted(set(mv) | {w for v in mv for w in nbS[v] if w in l2r and w not in jv and l2r[w] not in jv})
        X = V.copy()
        for v in mv:
            d = 0.5 * (np.mean([V[w] for w in nbS[v]], 0) - V[v]); X[v] = V[v] + d; X[l2r[v]] = V[l2r[v]] + d * MIR
        if not (len(folded(X, shF)) < len(fl) and corners(X, Q[brf]).min() >= 12.0 and aspect(X, Q[brf]).max() < 10.0): break
        V = X; steps4 += 1
    log.append(dict(stage4_sheet_folds=dict(folded_before=f0, folded_after=len(folded(V, shF)), steps=steps4, symmetric=True, max_move_cm=round(float(np.linalg.norm(V - V0f, axis=1).max()), 4))))
# stage 5 (same gate): CREASED cuff edges -- an edge between two cuff quads whose normals differ by > 120 deg reads as a dark speck / notch at the root (e.g. the
# pre-tragal cuff of the short HE1 on c2). Per-vertex axis pattern search (3D, steps 0.2 / 0.1 / 0.05 of the local edge length) on the cuff / transition / head
# vertices of those quads + their 1-ring, minimising the worst dihedral around the vertex; a move is admissible only if every quad around it keeps a corner >= 12 deg
# and aspect < 10 and no new triangle crossing appears within 1.5 cm and no quad around it becomes folded. The cuff transitions are canonical PER SIDE (Fenn / Vael cuff canon), so each side is treated on its own.
if float(rec.get('geo', {}).get('sheet_fold_fix', 0)) > 0:
    EF = {}
    for fi, q in enumerate(Q):
        for k in range(4): EF.setdefault(tuple(sorted((int(q[k]), int(q[(k + 1) % 4])))), []).append(fi)
    def fnrm(X, F): n = np.cross(X[Q[F, 2]] - X[Q[F, 0]], X[Q[F, 3]] - X[Q[F, 1]]); return n / (np.linalg.norm(n, axis=1)[:, None] + 1e-30)
    def dih(X, faces):
        es = sorted({tuple(sorted((int(Q[f][k]), int(Q[f][(k + 1) % 4])))) for f in faces for k in range(4)}); es = [e for e in es if len(EF[e]) == 2 and not (part[list(e)] == 'rim').any()]
        if not es: return np.zeros(0), []
        A2 = np.array([EF[e] for e in es]); n = fnrm(X, A2.ravel()).reshape(-1, 2, 3); return np.degrees(np.arccos(np.clip((n[:, 0] * n[:, 1]).sum(1), -1, 1))), es
    TH5 = 120.0; cfa = np.nonzero((part[Q] == 'cuff').any(1))[0]; d5, es5 = dih(V, cfa); bad5 = [es5[i] for i in np.nonzero(d5 > TH5)[0]]; V05 = V.copy(); sw5 = 0
    KP = ('cuff', 'v005', 'transition')
    # local self-intersection guard (no new crossing may appear): triangles of the quads around a moved vertex vs every non-adjacent triangle within 1.5 cm,
    # tested edge-vs-triangle (Moller-Trumbore) both ways
    from scipy.spatial import cKDTree
    TRI = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; TQ = np.r_[np.arange(len(Q)), np.arange(len(Q))]
    def seg_tri(P0, P1, A0, B0, C0):
        e1 = B0 - A0; e2 = C0 - A0; d = P1 - P0; h = np.cross(d, e2); a = (e1 * h).sum(1); ok = np.abs(a) > 1e-12; f = 1.0 / np.where(ok, a, 1.0); s = P0 - A0
        u = f * (s * h).sum(1); q = np.cross(s, e1); w = f * (d * q).sum(1); t = f * (e2 * q).sum(1)
        return ok & (u > 1e-9) & (w > 1e-9) & (u + w < 1 - 1e-9) & (t > 1e-9) & (t < 1 - 1e-9)
    def crossings(X, ti, tj):
        if not len(ti): return 0
        a, b = TRI[ti], TRI[tj]; hit = np.zeros(len(ti), bool)
        for k in range(3):
            hit |= seg_tri(X[a[:, k]], X[a[:, (k + 1) % 3]], X[b[:, 0]], X[b[:, 1]], X[b[:, 2]]); hit |= seg_tri(X[b[:, k]], X[b[:, (k + 1) % 3]], X[a[:, 0]], X[a[:, 1]], X[a[:, 2]])
        return int(hit.sum())
    TC = cKDTree(V[TRI].mean(1)); PAIRS = {}
    def pairs(v):
        if v not in PAIRS:
            own = np.nonzero(np.isin(TQ, vf[v]))[0]; near = np.array(sorted(set(TC.query_ball_point(V[v], 1.5)))); ti, tj = [], []
            for t in own:
                c = near[~(np.isin(TRI[near], TRI[t]).any(1))]; ti += [t] * len(c); tj += c.tolist()
            PAIRS[v] = (np.array(ti, int), np.array(tj, int))
        return PAIRS[v]
    mv5 = sorted({int(v) for e in bad5 for f in EF[e] for v in Q[f] if part[v] in KP}); mv5 = sorted(set(mv5) | {int(w) for v in mv5 for f in vf[v] for w in Q[f] if part[w] in KP})
    for sw5 in range(40):
        moved = False
        for v in mv5:
            A = np.array(sorted({f for w in Q[vf[v]].ravel() for f in vf[int(w)]}))
            ti, tj = pairs(v); x0 = crossings(V, ti, tj); fo0 = len(folded(V, A))
            def obj(X):
                dd, _ = dih(X, A); return dd.max() if (corners(X, Q[A]).min() >= 12.0 and aspect(X, Q[A]).max() < 10.0 and crossings(X, ti, tj) <= x0 and len(folded(X, A)) <= fo0) else 1e9
            cur = obj(V); L = np.mean([np.linalg.norm(V[int(w)] - V[v]) for w in Q[vf[v]].ravel() if int(w) != v]); best = (cur, None)
            for st in (0.2, 0.1, 0.05):
                for dv in np.vstack([np.eye(3), -np.eye(3)]):
                    X = V.copy(); X[v] += st * L * dv; o = obj(X)
                    if o < best[0] - 1e-3: best = (o, st * L * dv)
            if best[1] is not None: V[v] += best[1]; moved = True
        if not moved: break
    d5b, _ = dih(V, cfa)
    log.append(dict(stage5_cuff_creases=dict(threshold_deg=TH5, creased_edges_before=len(bad5), creased_edges_after=int((d5b > TH5).sum()), worst_dihedral_before=round(float(d5.max()), 1), worst_dihedral_after=round(float(d5b.max()), 1),
                                              vertices=len(mv5), sweeps=sw5 + 1, folded_cuff_band_before=len(folded(V05, cfa)), folded_cuff_band_after=len(folded(V, cfa)), max_move_cm=round(float(np.linalg.norm(V - V05, axis=1).max()), 4))))
z['V'] = V.astype(z['V'].dtype); np.savez_compressed(P, **z) if False else np.savez(P, **z)
rec['hv_cuff_repair'] = dict(rule='tangential umbrella relaxation of cuff vertices of quads with a corner < 12 deg (+ cuff 1-ring), accepted while the worst corner improves; stage 2 per-vertex tangential pattern search if any remain; stage 3 the same on auricle-sheet quads with aspect > 9.8 (junction fixed, symmetric); stage 4 (sheet_fold_fix) symmetric umbrella relaxation of folded sheet quads; stage 5 (sheet_fold_fix) per-vertex pattern search on cuff edges creased > 120 deg', log=log)
json.dump(rec, open(P.replace('.npz', '.json'), 'w'), indent=1)
print(json.dumps(log))
