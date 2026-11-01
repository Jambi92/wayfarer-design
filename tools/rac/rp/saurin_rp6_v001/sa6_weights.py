# sa6_weights.py CFG(M|F) OUT.npz : Saurin RP6 production LBS weights (order a407015 §7, §22).
#   1. PRIMARY SEGMENTATION: each cage vertex -> the nearest deform-bone capsule among the bones its own authored semantic region allows (region / side
#      masks from the frozen per-quad labels; webs allow both neighbouring proximal phalanges + metacarpals; the tail-root rings allow pelvis + tail_01-03).
#   2. JOINT BLENDS by mesh-graph diffusion of the one-hot field (never through space -> no leakage across web slots / opposite walls / mouth): iteration counts
#      per region class scale with the local limb radius (digits 12, hands / feet 30, tail 70, body 220), pass order distal -> proximal, each pass only updates
#      its own class (other vertices act as fixed boundary values).
#   3. PRUNE to <= MAXINF influences per vertex (drop the smallest, renormalise), weights < 1e-3 removed; sums = 1 exactly.
#   Output: dense float32 matrix as a sparse CSR (indices / indptr / data), bone names, config. Deterministic.
import sys, os, json, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C
CFG, OUT = sys.argv[1:3]; MAXINF = int(os.environ.get('MAXINF', 4))
d = C.load(); Q = d['Q']; V = d['V1'] if CFG == 'M' else d['V2']; nv = len(V); ql = d['qlab']
P = json.load(open(C.EV6 + '/SA_RP6_joint_placement_%s_v001.json' % CFG))['bones']
DB = [b for b, v in P.items() if v['deform']]; bi = {b: i for i, b in enumerate(DB)}
# per-vertex label sets
QLU = sorted(set(ql)); qli = {q: i for i, q in enumerate(QLU)}
VL = np.zeros((nv, len(QLU)), bool); VL[Q.ravel(), np.repeat([qli[q] for q in ql], 4)] = True
def allowed(b):
    t = b.split('_')[-1] if b.split('_')[-1] in ('l', 'r') else None
    if b.startswith('clavicle'): S = {'shoulder', 'trunk', 'neck'}
    elif b.startswith('upperarm'): S = {'shoulder', 'upper_arm', 'elbow'}
    elif b.startswith('forearm'): S = {'elbow', 'forearm', 'wrist'}
    elif b.startswith('hand'): S = {'wrist', 'palm', 'thumb'}
    elif b.startswith('meta'): S = {'palm', 'finger_web', 'finger'}
    elif b.startswith('finger'): S = {'palm', 'finger', 'finger_cap', 'finger_web'}
    elif b.startswith('thumb'): S = {'palm', 'thumb', 'thumb_cap', 'wrist'}
    elif b.startswith('thigh'): S = {'hip', 'thigh', 'knee', 'pelvis'}
    elif b.startswith('shin'): S = {'knee', 'shin', 'ankle'}
    elif b.startswith('foot'): S = {'ankle', 'foot', 'forefoot', 'toe_web', 'shin'}
    elif b.startswith('toe'): S = {'forefoot', 'toe', 'toe_cap', 'toe_web'}
    elif b == 'pelvis': S = {'pelvis', 'hip', 'trunk', 'tail'}
    elif b.startswith('spine'): S = {'trunk', 'pelvis', 'shoulder', 'neck'}
    elif b.startswith('neck'): S = {'neck', 'trunk', 'head'}
    elif b == 'head': S = {'head', 'rostrum_cap', 'orbit', 'eye', 'display_root', 'neck'}
    elif b == 'jaw': S = {'head', 'rostrum_cap', 'neck'}
    elif b.startswith('tail'): S = {'tail', 'pelvis'}
    return [qli[q] for q in S if q in qli], t
xs = V[:, 0]
OK = np.zeros((nv, len(DB)), bool)
for b in DB:
    li, t = allowed(b); m = VL[:, li].any(1)
    if t: m &= (xs > 0) if t == 'l' else (xs < 0)
    OK[:, bi[b]] = m
# tail: only the first tail rings (phi < 0.08 -> root rings) may take pelvis; tail bones beyond tail_03 never touch pelvis-labelled vertices
tail_v = np.zeros(nv, bool); tail_v[np.unique(Q[ql == 'tail'])] = True
for b in DB:
    if b.startswith('tail_') and int(b[5:]) > 3: OK[~tail_v, bi[b]] = False
# legs never weight tail-quad vertices (tail root belongs to pelvis + tail chain)
for b in DB:
    if b.startswith(('thigh', 'shin', 'foot', 'toe')): OK[tail_v, bi[b]] = False
# jaw: only below the mouth slit / lower head (vertices below the jaw bone line and in front of the hinge)
H = np.array(P['jaw']['head']); Tj = np.array(P['jaw']['tail']); n_ = np.cross(Tj - H, [1.0, 0, 0]); n_ /= np.linalg.norm(n_)
mouth = d['loops']['mouth_slit']; lip_z = np.interp(V[:, 1], np.sort(V[mouth, 1]), V[mouth, 2][np.argsort(V[mouth, 1])])
headv = VL[:, [qli[q] for q in ('head', 'rostrum_cap', 'neck') if q in qli]].any(1) & (V[:, 2] > np.array(P['neck_02']['head'])[2])
jawzone = headv & (V[:, 1] > H[1] - 1.5) & (V[:, 2] < lip_z + 0.05) & (V[:, 2] < H[2] + 0.5)
OK[:, bi['jaw']] &= jawzone
# per-digit isolation: each digit (its authored digit quads + its claw cap = one mesh component) may only take its OWN digit chain (+ its metacarpal /
# the foot / hand); phalanx bones 02-03 never leave their own digit; 01 may also take the web / forefoot / palm rows. Removes cross-digit capsule capture
# where adjacent digit tips converge.
digit_of = np.full(nv, -1); dkey = []
for (s_, pre, k), comp in sorted(C.digit_components().items()):
    digit_of[comp] = len(dkey); dkey.append(((('toe_%d_' % k) if pre == 't' else ('thumb_' if pre == 'th' else 'finger_%d_' % k)), ('l' if s_ == 'xpos' else 'r'), k, pre))
def bone_digit(b):
    for i, (stem, t, k, pre) in enumerate(dkey):
        if b.startswith(stem) and b.endswith('_' + t): return i
    return -1
bdig = np.array([bone_digit(b) for b in DB])
for i, b in enumerate(DB):
    if bdig[i] >= 0:
        own = digit_of == bdig[i]; other = (digit_of >= 0) & ~own; OK[other, i] = False
        if not b.split('_')[-2] == '01' and not b.startswith('thumb_01'): OK[~own, i] = False
    elif b.startswith('meta'):
        k = int(b.split('_')[1]); t = b.split('_')[-1]
        own = [j for j, kk in enumerate(dkey) if kk[3] == 'f' and kk[2] == k and kk[1] == t]; OK[(digit_of >= 0) & ~np.isin(digit_of, own), i] = False
OK[~OK.any(1)] = True
# capsule distances
D = np.full((nv, len(DB)), 1e6)
for b in DB:
    a = np.array(P[b]['head']); c = np.array(P[b]['tail']); m = OK[:, bi[b]]
    tt = np.clip(((V[m] - a) @ (c - a)) / max((c - a) @ (c - a), 1e-9), 0, 1); D[m, bi[b]] = np.linalg.norm(V[m] - (a + tt[:, None] * (c - a)), axis=1)
prim = D.argmin(1)
# wrist: forearm / hand split by the wrist plane (normal = forearm direction through the wrist joint) on every wrist / palm / thumb-base vertex the two
# bones compete for -> the carpal (hand) band is one closed ring (no forearm-to-metacarpal direct contact, no hand-weight islands)
for t in ('l', 'r'):
    fa, hb = bi['forearm_' + t], bi['hand_' + t]; wp = np.array(P['hand_' + t]['head']); nd = wp - np.array(P['forearm_' + t]['head']); nd /= np.linalg.norm(nd)
    lab_w = VL[:, [qli[q] for q in ('wrist',) if q in qli]].any(1) & OK[:, fa] & OK[:, hb]; dist_ = (V - wp) @ nd
    prim[lab_w & (dist_ < 0)] = fa; prim[lab_w & (dist_ >= 0) & np.isin(prim, [fa])] = hb
# jaw zone: vertices of the lower jaw take the jaw (head otherwise) -- primary forced by the mouth line, not by capsule distance
prim[jawzone & (V[:, 2] < lip_z - 0.02)] = bi['jaw']
W = np.zeros((nv, len(DB)), np.float32); W[np.arange(nv), prim] = 1.0
# diffusion passes
E = np.unique(np.sort(np.r_[Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]], 1), axis=0)
A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(nv, nv)).tocsr(); deg = np.asarray(A.sum(1)).ravel()
def cls_of(b):
    if b.startswith(('finger', 'thumb_02', 'thumb_03', 'toe')): return 'digit'
    if b.startswith(('meta', 'thumb_01', 'hand', 'foot')): return 'handfoot'
    if b.startswith('tail'): return 'tail'
    return 'body'
pc = np.array([cls_of(DB[i]) for i in prim])
ITERS = dict(digit=int(os.environ.get('IT_DIGIT', 12)), handfoot=int(os.environ.get('IT_HF', 30)), tail=int(os.environ.get('IT_TAIL', 70)), body=int(os.environ.get('IT_BODY', 220)))
Ws = sp.csr_matrix(W)
Wd = W.astype(np.float64)
for c in ('digit', 'handfoot', 'tail', 'body'):
    m = pc == c
    for _ in range(ITERS[c]):
        Wn = (A @ Wd) / deg[:, None]; Wn = np.where(OK, Wn, 0); s = Wn.sum(1, keepdims=True); Wn = np.where(s > 0, Wn / np.maximum(s, 1e-12), Wd)
        Wd[m] = 0.5 * Wd[m] + 0.5 * Wn[m]
# prune
order = np.argsort(-Wd, 1)[:, :MAXINF]; Wp = np.zeros_like(Wd); r = np.arange(nv)[:, None]; Wp[r, order] = Wd[r, order]
Wp[Wp < 1e-3] = 0; Wp /= Wp.sum(1, keepdims=True)
S = sp.csr_matrix(Wp.astype(np.float32)); S.eliminate_zeros()
np.savez_compressed(OUT, data=S.data, indices=S.indices, indptr=S.indptr, shape=np.array(S.shape), bones=np.array(DB), config=np.array(CFG),
                    method=np.array('capsule segmentation in semantic masks + region-scaled mesh diffusion %s + prune %d' % (json.dumps(ITERS), MAXINF)))
nnz = np.diff(S.indptr); print(CFG, 'bones', len(DB), 'influences hist', np.bincount(nnz).tolist(), 'max sum err %.2e' % np.abs(np.asarray(S.sum(1)).ravel() - 1).max())
