# v003_build.py OUT.npz : RP3 Marchfolk v003 shared family-core correction (order 103c832 §4 / §5 / §6). Deterministic; both configurations share
# every operation (no configuration-specific topology); left / right operations are mirrored.
#  R  root-loop insertions (topology): one closed ring split into each listed closed quad strip (pinky MCP / hypothenar root, toe-1 and toe-4/5 MTP
#     roots, mirrored) -- the only topology change; linear rows (edge midpoints) appended to the map.
#  P  junction-pole relocation: poles on / within 2 loops of a §7 crease line slid along the joint axis to 2.3 local loops off the crease (cosine
#     falloff over the neighbouring rings, short tangential relax, pole pinned). Every candidate move is accepted only if, in BOTH configurations, no
#     station within reach gets worse (firm verdict, loop count, crease / 2-loop poles) and the target improves; otherwise smaller / opposite variants
#     are tried, else the move is dropped.
#  T  T-4 relaxation of violating quads (face / hands / feet / all) with the same acceptance test plus face-ring preservation.
# Moved vertices are barycentric points on one hm08 source triangle of the configuration-average surface (same UV chart): exact on each
# configuration's own accepted source surface.
import sys, os, json, time, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core3lib import *
OUT = sys.argv[1]; t0 = time.time(); RESUME = sys.argv[sys.argv.index('--resume') + 1] if '--resume' in sys.argv else None
PHASES = sys.argv[sys.argv.index('--phases') + 1].split(',') if '--phases' in sys.argv else ['P', 'T']; T4R = int(sys.argv[sys.argv.index('--t4rounds') + 1]) if '--t4rounds' in sys.argv else 5
B = load(); bs = np.load(W + '/v3_base.npz'); chart = bs['chart']
Qh = B['Qh']; Ah = B['A']; surf = Surface(Ah, Qh, chart)
Q = B['Q2'].copy(); UV = B['UV2'].copy(); M = B['M2'].copy(); vc = bs['vc'].copy(); seam = bs['seam'].copy()
LOG = dict(rings=[], poles=[], t4=[])
# ------------------------------------------------------------------ R: root-loop insertions (loop ids of the v002 topology, left side; mirrored)
loops0 = closed_loops(Q, M.shape[0]); X0 = M @ Ah; mir0 = mirror_map(X0, 0.3)
RINGS = [('pinky_mcp_hypothenar_root', 412, 1006), ('toe1_mtp_root', 491, 1113), ('toe2_mtp_root', 497, 1120), ('toe3_mtp_root', 508, 1132), ('toe4_toe5_mtp_root', 520, 1147)]
for nm, la, lb in RINGS:
    for side, (A_, B_) in (('l', (loops0[la], loops0[lb])), ('r', (mir0[loops0[la]], mir0[loops0[lb]]))):
        if (A_ < 0).any() or (B_ < 0).any(): print('mirror fail', nm); continue
        out = insert_ring(Q, UV, M, A_.tolist(), B_.tolist())
        if out is None: print('strip fail', nm, side); continue
        Q, UV, M, ext = out; vc = np.r_[vc, [vc[p] if vc[p] == vc[q] else vc[p] for p, q in ext]]; seam = np.r_[seam, [bool(seam[p] or seam[q] or vc[p] != vc[q]) for p, q in ext]]
        LOG['rings'].append(dict(name=nm + '_' + side, strip_quads=len(A_), verts_added=len(ext)))
nV = M.shape[0]; print('after rings', nV, len(Q), flush=True)
# ------------------------------------------------------------------ state
moved = {}
if RESUME:
    rz = np.load(RESUME); assert np.array_equal(rz['Q'], Q), 'resume topology mismatch'
    M = sp.csr_matrix((rz['M_data'], rz['M_indices'], rz['M_indptr']), shape=tuple(rz['M_shape'])); UV = rz['UV'].astype(float)
    moved = {int(v): (int(t), b) for v, t, b in zip(rz['moved'], rz['tri'], rz['bary'])}; LOG = json.loads(str(rz['log'])); LOG.setdefault('resumed', []).append(RESUME); print('resumed', RESUME, len(moved), flush=True)
X = M @ Ah; Adj = adjacency(Q, nV); deg = np.asarray(Adj.sum(1)).ravel(); _, val = topo(Q, nV); isp = val != 4
loops = closed_loops(Q, nV); S = {C: stations(B[C]['meta']) for C in 'MF'}; JR = {C: ring_stations(B[C]['meta']) for C in 'MF'}; mir = mirror_map(X, 0.3)
pin = seam.copy()
for C in 'MF':
    LM = json.load(open('%s/lm/MF-%s-R_landmarks.json' % (W, C)))['landmarks']; kd = cKDTree(M @ B[C]['Vh'])
    for k, v in LM.items():
        if v['source'] == 'surface-fit': pin[kd.query(v['p_cm'])[1]] = True
fnA = np.cross(X[Q[:, 2]] - X[Q[:, 0]], X[Q[:, 3]] - X[Q[:, 1]]); fnA /= np.linalg.norm(fnA, axis=1, keepdims=True); VN = vnormals(X, Q); sharp = np.zeros(nV, bool)
for k in range(4): sharp[Q[:, k]] |= (fnA * VN[Q[:, k]]).sum(1) < np.cos(np.radians(35))
pin |= sharp; pin |= pin[np.maximum(mir, 0)] & (mir >= 0)
def rows_matrix(mv):
    Ml = M.tolil(copy=True)
    for v, (t, bc) in mv.items():
        row = {}
        for j, w in zip(surf.T[t], bc):
            if w > 1e-12: row[int(j)] = row.get(int(j), 0.0) + float(w)
        Ml.rows[v] = sorted(row); Ml.data[v] = [row[j] for j in sorted(row)]
    return Ml.tocsr()
def positions(Xa, mv):
    """configuration positions: unmoved rows from M, moved rows barycentric"""
    out = {}
    for C in 'MF':
        Vc = M @ B[C]['Vh']
        if mv:
            ids = np.array(sorted(mv), int); T = surf.T[[mv[v][0] for v in ids]]; bc = np.array([mv[v][1] for v in ids])
            Vc[ids] = (B[C]['Vh'][T] * bc[:, :, None]).sum(1)
        out[C] = Vc
    return out
def project(Xa, mv, ids):
    ids = np.asarray(sorted(set(int(i) for i in ids)), int)
    if not len(ids): return
    P, tri, bc = surf.project(Xa[ids], vc[ids])
    for i, v in enumerate(ids): mv[int(v)] = (int(tri[i]), bc[i]); Xa[v] = P[i]
def hops(src, K):
    d = {src: 0}; fr = [src]
    for h in range(1, K + 1):
        nf = []
        for u in fr:
            for w in Adj.indices[Adj.indptr[u]:Adj.indptr[u + 1]]:
                if int(w) not in d: d[int(w)] = h; nf.append(int(w))
        fr = nf
    return d
def relax(Xa, mv, region, fixed, it=4, lam=0.35, para=0.0):
    region = np.array(sorted(set(region) - set(fixed) - set(np.nonzero(pin)[0].tolist())), int)
    if not len(region): return
    rq = np.unique(np.nonzero(np.isin(Q, region))[0])
    for _ in range(it):
        N = vnormals(Xa, Q); L = (Adj[region] @ Xa) / deg[region, None]; tgt = L
        if para > 0:
            acc = np.zeros((nV, 3)); cnt = np.zeros(nV); q = Q[rq]
            for k in range(4): pr = Xa[q[:, (k - 1) % 4]] + Xa[q[:, (k + 1) % 4]] - Xa[q[:, (k + 2) % 4]]; np.add.at(acc, q[:, k], pr); np.add.at(cnt, q[:, k], 1)
            tgt = (1 - para) * L + para * acc[region] / np.maximum(cnt[region], 1)[:, None]
        dX = lam * (tgt - Xa[region]); dX -= (dX * N[region]).sum(1, keepdims=True) * N[region]; Xa[region] += dX; project(Xa, mv, region)
cen = {C: {s[0]: (np.asarray(s[1], float), max(s[4], 2 * s[3]) + 1.0) for s in S[C]} for C in 'MF'}
def audit(Vc, names=None):
    R = {}
    for C in 'MF':
        Ss = [s for s in S[C] if names is None or s[0] in names]; Js = [j for j in JR[C] if names is None or j[0] in {ring_name(n) for n in names}]
        R[C] = full_s7(Vc[C], Q, B[C]['meta'], loops, Ss, Js)
    return R
def key(r): return (max(0, r['required'] - r['loops_s7']), r['crease'], r['within2'])
def near_stations(ids, rad=None):
    """every station whose band reach (max(R, 2W) + 1 cm) touches a changed vertex"""
    P = X[np.asarray(list(ids), int)]; kd = cKDTree(P); out = set()
    for C in 'MF':
        for nm, (c, reach) in cen[C].items():
            if kd.query(c)[0] < reach: out.add(nm)
    return out
CUR = audit(positions(X, moved))
def score_all(R): return {C: (sum(not r['firm'] for r in R[C].values()), sum(not r['strict'] for r in R[C].values())) for C in 'MF'}
print('start', score_all(CUR), '%.0fs' % (time.time() - t0), flush=True)
def try_move(target, plan):
    """plan: list of (pole, displacement vector, h). Returns True if accepted (state updated)."""
    global X, moved, CUR
    for variant in ((1.0, 4), (1.0, 0), (0.6, 2), (1.5, 2), (0.4, 0)):
        sc, rit = variant; Xt = X.copy(); mvt = dict(moved); disp = np.zeros((nV, 3)); fixed = set()
        for p, dv, h in plan:
            dvv = dv * sc
            K = int(np.ceil(np.linalg.norm(dvv) / h)) + 3
            for v, hh in hops(p, K).items():
                if pin[v]: continue
                disp[v] += 0.5 * (1 + np.cos(np.pi * hh / (K + 1))) * dvv
            fixed.add(p)
        ch = np.nonzero(np.linalg.norm(disp, axis=1) > 0)[0]
        if not len(ch): return False
        Xt[ch] += disp[ch]; project(Xt, mvt, ch)
        if rit:
            reg = set(ch.tolist())
            for v in list(reg): reg.update(Adj.indices[Adj.indptr[v]:Adj.indptr[v + 1]].tolist())
            relax(Xt, mvt, reg, fixed, it=rit)
        names = near_stations(ch) | set(target); Rt = audit(positions(Xt, mvt), names)
        ok = True; gain = 0
        for C in 'MF':
            for nm in names:
                a, b = key(CUR[C][nm]), key(Rt[C][nm])
                if b[0] > a[0] or (CUR[C][nm]['firm'] and not Rt[C][nm]['firm']) or b[1] > a[1] or (b[2] > a[2] and nm not in target): ok = False
                if nm in target: gain += (a[1] - b[1]) * 10 + (a[2] - b[2])
        if VERB:
            worse = [(C, nm, key(CUR[C][nm]), key(Rt[C][nm])) for C in 'MF' for nm in names if key(Rt[C][nm]) != key(CUR[C][nm])]
            print('      variant', variant, 'ok', ok, 'gain', gain, worse[:12], flush=True)
        if ok and gain > 0:
            X = Xt; moved = mvt
            for C in 'MF': CUR[C].update(Rt[C])
            return variant
    return False
# ------------------------------------------------------------------ P: pole relocation
TGT = 2.3; done_keys = set(); VERB = '--verbose' in sys.argv
for phase in (('firm', 'strict') if 'P' in PHASES else ()):
    for it in range(6):
        bad = sorted({nm for C in 'MF' for nm, r in CUR[C].items() if (not r['firm'] if phase == 'firm' else not r['strict']) and (r['crease'] or r['within2'])})
        print(phase, it, score_all(CUR), 'targets', len(bad), '%.0fs' % (time.time() - t0), flush=True)
        if not bad: break
        prog = False
        for nm in bad:
            if nm.endswith('_r') and nm[:-1] + 'l' in bad: continue           # handled with its mirror
            if nm.startswith('toe') and '_j1_' in nm: continue                 # MTP fan: handled by the grouped forefoot move below
            names = [nm] + ([nm[:-1] + 'r'] if nm.endswith('_l') else [])
            plan = {}
            for C in 'MF':
                for n_ in names:
                    r = CUR[C][n_]
                    for p, t in zip(r['pole_ids'], r['pole_t']):
                        if pin[p] or abs(t) > (2.0 if phase == 'strict' else 0.5): continue
                        sg = np.sign(t) if abs(t) > 0.05 else -1.0; dv = (sg * TGT - t) * r['h'] * r['d']
                        if p not in plan or np.linalg.norm(dv) > np.linalg.norm(plan[p][0]): plan[p] = (dv, r['h'])
            # mirror completion
            for p in list(plan):
                m_ = mir[p]
                if m_ >= 0 and m_ not in plan and not pin[m_]: plan[m_] = (plan[p][0] * [-1, 1, 1], plan[p][1])
            kk = (nm, phase, tuple(sorted(plan)))
            if not plan or kk in done_keys: continue
            done_keys.add(kk); res = try_move(names, [(p, dv, h) for p, (dv, h) in plan.items()])
            LOG['poles'].append(dict(phase=phase, station=names, poles=sorted(int(p) for p in plan), accepted=bool(res), variant=list(res) if res else None)); prog |= bool(res)
            print('   ', names, len(plan), 'accepted' if res else 'rejected', res, flush=True)
        # grouped forefoot (MTP fan) move: junction poles shared by adjacent toe roots slid PROXIMALLY past every toe-root crease they touch
        toe_bad = [nm for nm in bad if nm.startswith('toe') and '_j1_' in nm]
        if toe_bad:
            plan = {}
            for C in 'MF':
                for nm in [n for n in CUR[C] if n.startswith('toe') and '_j1_' in n]:
                    r = CUR[C][nm]
                    for p, t in zip(r['pole_ids'], r['pole_t']):
                        if pin[p]: continue
                        need = (t + TGT) * r['h']
                        if need > 0 and (p not in plan or need > plan[p][2]): plan[p] = (-r['d'] * need, r['h'], need)
            kk = ('forefoot', phase, tuple(sorted(plan)))
            if plan and kk not in done_keys:
                done_keys.add(kk); tg = sorted({n for C in 'MF' for n in CUR[C] if n.startswith('toe') and '_j1_' in n})
                res = try_move(tg, [(p, dv, h) for p, (dv, h, _) in plan.items()])
                LOG['poles'].append(dict(phase=phase, station='forefoot_mtp_group', poles=sorted(int(p) for p in plan), accepted=bool(res), variant=list(res) if res else None)); prog |= bool(res)
                print('    forefoot group', len(plan), 'accepted' if res else 'rejected', res, flush=True)
        if not prog: break
# ------------------------------------------------------------------ T: T-4 relaxation (chunked by region, accepted only without station / face-ring regression)
FACE0 = None
def face_rings(Vc):
    out = {}
    for C in 'MF':
        LM = json.load(open('%s/lm/MF-%s-R_landmarks.json' % (W, C)))['landmarks']; ml, mr = np.array(LM['mouth_corner_l']['p_cm']), np.array(LM['mouth_corner_r']['p_cm']); mc = 0.5 * (ml + mr); mc[0] = 0
        out[C] = (len(encircling(Vc[C], loops, mc, np.array([0, 1.0, 0]), 5.5, 3.5)), len(encircling(Vc[C], loops, np.array(LM['eye_l']['p_cm']), np.array([0, 1.0, 0]), 3.2, 3.0)),
                  len(encircling(Vc[C], loops, np.array(LM['eye_r']['p_cm']), np.array([0, 1.0, 0]), 3.2, 3.0)))
    return out
Vc = positions(X, moved); FACE0 = face_rings(Vc)
def t4count(Vc): return {C: int((lambda a: (a[2] | a[3]).sum())(quality(Vc[C], Q))) for C in 'MF'}
print('T-4 before', t4count(Vc), 'face', FACE0, flush=True)
from scipy.sparse.csgraph import connected_components as cc_
for rnd in range(T4R if 'T' in PHASES else 0):
    Vc = positions(X, moved); bad = np.zeros(len(Q), bool)
    for C in 'MF': a = quality(Vc[C], Q); bad |= a[2] | a[3]
    bv = np.unique(Q[bad].ravel()); bv = bv[~pin[bv]]
    if not len(bv): break
    # chunk bad vertices into connected clusters (graph on vertices of bad faces)
    sub = Adj[bv][:, bv]; ncl, lab = cc_(sub, directed=False); acc = 0; rej = 0
    order_ = np.argsort(-np.bincount(lab))
    for cl in order_:
        ids = bv[lab == cl]; reg = set(ids.tolist())
        for v in list(reg): reg.update(Adj.indices[Adj.indptr[v]:Adj.indptr[v + 1]].tolist())
        if rnd < 2: reg -= set(np.nonzero(isp)[0].tolist())                # keep poles fixed in the first rounds
        Xt = X.copy(); mvt = dict(moved); relax(Xt, mvt, reg, set(), it=6, lam=0.4, para=0.5)
        Vt = positions(Xt, mvt); ri = np.unique(np.nonzero(np.isin(Q, list(reg)))[0])
        q0 = sum(int((quality(Vc[C], Q[ri])[2] | quality(Vc[C], Q[ri])[3]).sum()) for C in 'MF'); q1 = sum(int((quality(Vt[C], Q[ri])[2] | quality(Vt[C], Q[ri])[3]).sum()) for C in 'MF')
        if q1 >= q0: rej += 1; continue
        names = near_stations(np.array(list(reg)))
        ok = True
        if names:
            Rt = audit(Vt, names)
            for C in 'MF':
                for nm in names:
                    a, b = key(CUR[C][nm]), key(Rt[C][nm])
                    if b[0] > a[0] or b[1] > a[1] or b[2] > a[2]: ok = False
        if ok and len(reg) and Vt['M'][list(reg)][:, 2].max() > 140:              # face region: rings must be preserved
            if face_rings(Vt) != FACE0: ok = False
        if ok:
            X = Xt; moved = mvt; Vc = Vt; acc += 1
            if names:
                for C in 'MF': CUR[C].update(Rt[C])
        else: rej += 1
    print('T-4 round', rnd, 'clusters', ncl, 'accepted', acc, 'rejected', rej, t4count(Vc), '%.0fs' % (time.time() - t0), flush=True); LOG['t4'].append(dict(round=rnd, clusters=int(ncl), accepted=acc, rejected=rej, t4=t4count(Vc)))
# ------------------------------------------------------------------ save
M3 = rows_matrix(moved); Vc = positions(X, moved); RF = audit(Vc)
UV3 = UV.copy(); Tq = surf.tq; Tk = surf.tk
for f, q in enumerate(Q):
    for k, v in enumerate(q):
        if int(v) in moved:
            t, bc = moved[int(v)]; corners = [0, 1, 2] if Tk[t] == 0 else [0, 2, 3]; UV3[f, k] = (B['UVh'][Tq[t]][corners] * bc[:, None]).sum(0)
res = {C: dict(firm_fail=sorted(k for k, r in RF[C].items() if not r['firm']), strict_fail=sorted(k for k, r in RF[C].items() if not r['strict'])) for C in 'MF'}
print(json.dumps(res)); print('T-4 after', t4count(Vc), 'face', face_rings(Vc), '%.0fs' % (time.time() - t0))
mv = np.array(sorted(moved), int)
np.savez_compressed(OUT, Q=Q, UV=UV3, M_data=M3.data, M_indices=M3.indices, M_indptr=M3.indptr, M_shape=np.array(M3.shape), moved=mv, tri=np.array([moved[v][0] for v in mv], int),
                    bary=np.array([moved[v][1] for v in mv]).reshape(-1, 3), pin=pin, n_v002=B['M2'].shape[0], log=json.dumps(dict(LOG, result=res)))
