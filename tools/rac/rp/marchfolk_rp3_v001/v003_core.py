# v003_core.py OUT.npz [--t4] : RP3 Marchfolk v003 shared family-core correction (order 103c832 §4 / §5).
# Topology = v002 (same vertex count, face list, vertex order; no configuration-specific branch). Corrections are SURFACE-CONSTRAINED VERTEX
# RELOCATIONS on the configuration-average hm08 surface A = (MF-M-R + MF-F-R) / 2:
#   P (§4) junction-pole relocation: every pole that sits on (|axial offset| <= 0.5 local loop) or within 2 loops of a contract §7 joint crease line
#          (palm MCP roots, thenar / hypothenar, ankle, MTP / toe IP, shoulder) is slid along the joint axis to >= 2.3 local loops off the crease,
#          with a cosine falloff over the neighbouring rings, then the region is relaxed tangentially (pole pinned) -- the loop that crosses the
#          crease becomes a regular ring and the convergence moves into the palm / foot body or the digit shaft;
#   T (§5) T-4 outlier relaxation (--t4): quads violating 45-135 deg / aspect <= 4 in face, hands, feet (plus their 1-ring) are relaxed by a
#          tangential Laplacian + parallelogram-completion step, sharp-fold vertices (eye / lip pocket rims) pinned.
# Every moved vertex is stored as barycentrics on ONE hm08 source triangle (R-6 triangulation, restricted to its own UV chart): its map row is
# 3 hm08 weights, identical for both configurations, and it lies exactly on each configuration's own accepted source surface (T-1 / T-2 vertex
# deviation 0). UV seam vertices and rig-facing surface-fit landmark vertices are pinned. Weights / UVs / MPFB targets transfer through M3.
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core3lib import *
OUT = sys.argv[1]; DO_T4 = '--t4' in sys.argv
B = load(); bs = np.load(W + '/v3_base.npz'); chart = bs['chart']; vc = bs['vc']; seam = bs['seam']
Qh = B['Qh']; Q = B['Q2']; M2 = B['M2']; nV = M2.shape[0]; Ah = B['A']; surf = Surface(Ah, Qh, chart)
Adj = adjacency(Q, nV); deg = np.asarray(Adj.sum(1)).ravel(); _, val = topo(Q, nV); poles = val != 4
loops = closed_loops(Q, nV); S = {C: stations(B[C]['meta']) for C in 'MF'}; JR = {C: ring_stations(B[C]['meta']) for C in 'MF'}
X = M2 @ Ah
# pins: seams, surface-fit landmark vertices, sharp folds
pin = seam.copy()
for C in 'MF':
    LM = json.load(open('%s/lm/MF-%s-R_landmarks.json' % (W, C)))['landmarks']; V2 = M2 @ B[C]['Vh']; kd = cKDTree(V2)
    for k, v in LM.items():
        if v['source'] == 'surface-fit': pin[kd.query(v['p_cm'])[1]] = True
fnA = np.cross(X[Q[:, 2]] - X[Q[:, 0]], X[Q[:, 3]] - X[Q[:, 1]]); fnA /= np.linalg.norm(fnA, axis=1, keepdims=True); VN = vnormals(X, Q)
sharp = np.zeros(nV, bool)
for k in range(4): sharp[Q[:, k]] |= (fnA * VN[Q[:, k]]).sum(1) < np.cos(np.radians(35))
pin |= sharp
moved = {}; log = []
def project(ids):
    ids = np.asarray(sorted(set(int(i) for i in ids)), int)
    if not len(ids): return
    P, tri, bc = surf.project(X[ids], vc[ids])
    for i, v in enumerate(ids): moved[int(v)] = (int(tri[i]), bc[i]); X[v] = P[i]
def hops(src, K):
    d = {src: 0}; fr = [src]
    for h in range(1, K + 1):
        nf = []
        for u in fr:
            for w in Adj.indices[Adj.indptr[u]:Adj.indptr[u + 1]]:
                if w not in d: d[int(w)] = h; nf.append(int(w))
        fr = nf
    return d
def relax(region, fixed, it=6, lam=0.35, para=0.0):
    region = np.array(sorted(set(region) - set(fixed)), int)
    if not len(region): return
    rq = np.unique(np.nonzero(np.isin(Q, region))[0])
    for _ in range(it):
        N = vnormals(X, Q); L = (Adj[region] @ X) / deg[region, None]; tgt = L
        if para > 0:
            acc = np.zeros((nV, 3)); cnt = np.zeros(nV)
            for k in range(4):   # parallelogram completion: v_k ~ v_{k-1} + v_{k+1} - v_{k+2}
                q = Q[rq]; pr = X[q[:, (k - 1) % 4]] + X[q[:, (k + 1) % 4]] - X[q[:, (k + 2) % 4]]; np.add.at(acc, q[:, k], pr); np.add.at(cnt, q[:, k], 1)
            pg = acc[region] / np.maximum(cnt[region], 1)[:, None]; tgt = (1 - para) * L + para * pg
        dX = lam * (tgt - X[region]); dX -= (dX * N[region]).sum(1, keepdims=True) * N[region]; X[region] += dX; project(region)
def maps(): return build_map(M2, moved, surf)
def audit_all():
    M3 = maps(); R = {}
    for C in 'MF': R[C] = full_s7(M3 @ B[C]['Vh'], Q, B[C]['meta'], loops, S[C], JR[C])
    return R
def problems(R, strict):
    out = {}
    for C in 'MF':
        for k, r in R[C].items():
            bad = (not r['strict']) if strict else (not r['firm'])
            if bad: out.setdefault(k, {})[C] = r
    return out
# ---------------------------------------------------------------- P: pole relocation
TGT = 2.3; tries = {}
for phase in ('firm', 'strict'):
    for it in range(14):
        R = audit_all(); pb = problems(R, phase == 'strict')
        nf = {C: sum(not r['firm'] for r in R[C].values()) for C in 'MF'}; ns = {C: sum(not r['strict'] for r in R[C].values()) for C in 'MF'}
        print(phase, it, 'firm fail', nf, 'strict fail', ns, flush=True); log.append(dict(phase=phase, it=it, firm_fail=nf, strict_fail=ns, problems=sorted(pb)))
        todo = {}
        for k, rr in pb.items():
            for C, r in rr.items():
                if r['loops_s7'] < r['required']: continue                    # loop-count shortfall: handled separately
                for p, t in zip(r['pole_ids'], r['pole_t']):
                    if abs(t) > (2.0 if phase == 'strict' else 0.5): continue
                    if pin[p]: continue
                    sg = np.sign(t) if abs(t) > 0.05 else -1.0                 # tiny offset: move proximal (into palm / foot body / trunk side)
                    need = (sg * TGT - t) * r['h']; dv = need * r['d']
                    key = (p, k)
                    if key not in todo or np.linalg.norm(dv) > np.linalg.norm(todo[key][0]): todo[key] = (dv, r['h'])
        if not todo: break
        disp = np.zeros((nV, 3)); wsum = np.zeros(nV); fixed = set()
        for (p, k), (dv, h) in todo.items():
            tries[(p, k)] = tries.get((p, k), 0) + 1
            if tries[(p, k)] > 6: continue
            K = int(np.ceil(np.linalg.norm(dv) / h)) + 3; hd = hops(p, K)
            for v, hh in hd.items():
                if pin[v]: continue
                wv = 0.5 * (1 + np.cos(np.pi * hh / (K + 1))); disp[v] += wv * dv; wsum[v] = max(wsum[v], wv)
            fixed.add(p)
        ch = np.nonzero(np.linalg.norm(disp, axis=1) > 0)[0]
        if not len(ch): break
        X[ch] += disp[ch]; project(ch)
        reg = set(ch.tolist())
        for v in list(reg): reg.update(Adj.indices[Adj.indptr[v]:Adj.indptr[v + 1]].tolist())
        relax(reg - set(np.nonzero(pin)[0].tolist()), fixed, it=4)
# ---------------------------------------------------------------- T: T-4 outlier relaxation
if DO_T4:
    zoneM = None
    for rnd in range(3):
        ang, asp, ba, bp = quality(X, Q); bad = np.nonzero(ba | bp)[0]; reg = set(Q[bad].ravel().tolist())
        for v in list(reg): reg.update(Adj.indices[Adj.indptr[v]:Adj.indptr[v + 1]].tolist())
        reg = reg - set(np.nonzero(pin | poles)[0].tolist()) if rnd == 0 else reg - set(np.nonzero(pin)[0].tolist())
        print('t4 round', rnd, 'bad A-faces', len(bad), 'region', len(reg), flush=True)
        relax(reg, set(), it=8, lam=0.4, para=0.5)
    # re-check stations after T-4 and re-run pole relocation passes if needed
R = audit_all()
M3 = maps(); Vc = {C: M3 @ B[C]['Vh'] for C in 'MF'}
res = {C: dict(firm_fail=sorted(k for k, r in R[C].items() if not r['firm']), strict_fail=sorted(k for k, r in R[C].items() if not r['strict'])) for C in 'MF'}
print(json.dumps(res))
mv = np.array(sorted(moved), int)
np.savez_compressed(OUT, M_data=M3.data, M_indices=M3.indices, M_indptr=M3.indptr, M_shape=np.array(M3.shape), moved=mv, tri=np.array([moved[v][0] for v in mv], int),
                    bary=np.array([moved[v][1] for v in mv]), pin=pin, log=json.dumps(dict(iterations=log, result=res)))
