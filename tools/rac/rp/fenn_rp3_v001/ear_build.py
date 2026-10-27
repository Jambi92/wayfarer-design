# ear_build.py HEAD CAND OUTDIR [--canon canon.json] [--write-canon] [--probe key=val,...]
# Order bdcd6a6: realise the shared Fenn ear branch on one accepted CF2 head (HEAD = FNL4-CF2 | FNF181-CF2) for one candidate (E1 / E2 / E3).
# Every vertex outside the two branch zones keeps its v005 index order and its exact CF2 family-realization position; the 2 x 1,181 v005
# ear-zone interior vertices and 2 x 1,206 ear-zone faces are replaced by the branch patch (same patch topology for every head / candidate).
# Writes OUTDIR/<HEAD>_<CAND>_branch.npz (V, Q, M weight/zone proxy map, src_index, meta, branch map) and a JSON record.
import sys, os, json, pickle, numpy as np, scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ear_branch_lib as E
from scipy.spatial import cKDTree
a = sys.argv[1:]; HEAD, CAND, OUT = a[:3]; os.makedirs(OUT, exist_ok=True)
CANON = a[a.index('--canon') + 1] if '--canon' in a else None; WRITE = '--write-canon' in a
PROBE = dict(kv.split('=') for kv in a[a.index('--probe') + 1].split(',')) if '--probe' in a else {}
RT = '/tmp/claude-0/rt/fn/cf'
fz = np.load('%s/fam/%s_fam.npz' % (RT, HEAD)); Q0 = np.asarray(fz['Q']); V0 = fz['V'].astype(float); si = fz['src_index']
M0 = sp.csr_matrix((fz['M_data'], fz['M_indices'], fz['M_indptr']), shape=tuple(fz['M_shape']))
r6p = '/home/claude/wayfarer-design/reviews/reference-assets/r6/%s_r6.npz' % HEAD; z6 = np.load(r6p); we = M0 @ z6['w_ears'][si].astype(float)
p = dict(E.CAND[CAND]); geo = dict(E.GEO)
for k, v in PROBE.items():                          # geometry-only readiness probes (same topology)
    if k in geo: geo[k] = float(v)
    elif k == 'taper_ex': p['taper'] = (p['taper'][0], p['taper'][1], float(v))
    else: p[k] = float(v)
HH, sc = E.head_scale(r6p)
Lo = E.canonical_layout()                            # canonical layout (deterministic; E2 metric)
canon = json.load(open(CANON)) if CANON and os.path.exists(CANON) else {}
removed = []; patches = {}; recs = {}
for side, sg in (('l', 1), ('r', -1)):
    rd = E.root_data(V0, Q0, we, sg); rd['V_loop'] = V0[rd['loop']]
    skull, sk_v = E.skull_field(V0, Q0, rd, sg)
    R = E.realize(Lo, rd, skull, p, sc, canon=canon.get(side), geo=geo)
    canon[side] = R['rec']['canon']
    P, F, base = E.patch_mesh(Lo, R, rd['loop'])
    patches[side] = (P, F, rd, R); removed += rd['interior'].tolist(); recs[side] = R['rec']
    recs[side]['root_loop_v005'] = rd['loop'].tolist(); recs[side]['frame'] = dict(O=rd['O'].tolist(), n=rd['n'].tolist(), b=rd['b'].tolist(), u=rd['u'].tolist())
if WRITE and CANON: json.dump(canon, open(CANON, 'w'), indent=1)
# ---- assemble
rem = np.zeros(len(V0), bool); rem[removed] = True
efaces = np.zeros(len(Q0), bool)
for side in patches: efaces[patches[side][2]['faces']] = True
keep = np.nonzero(~rem)[0]; v2b = -np.ones(len(V0), int); v2b[keep] = np.arange(len(keep))
side_off = {}; Vb = [V0[keep]]; Qb = [v2b[Q0[~efaces]]]; nxt = len(keep); new_rows = []; part = ['v005'] * len(keep); side_of = [''] * len(keep)
for side in ('l', 'r'):
    P, F, rd, R = patches[side]; off = nxt; L = rd['loop']; side_off[side] = off
    Fg = np.where(F < 0, v2b[L[np.clip(-1 - F, 0, None)]], F + off); Vb.append(P); Qb.append(Fg); nxt += len(P)
    part += [str(x) for x in Lo['part']] + ['cuff'] * (len(P) - len(Lo['part'])); side_of += [side] * len(P)
Vb = np.concatenate(Vb); Qb = np.concatenate(Qb); assert (Qb >= 0).all()
# ---- orientation: v005 faces fixed; propagate to branch faces through shared edges
nk = int((~efaces).sum()); fixed = np.zeros(len(Qb), bool); fixed[:nk] = True
ed = {}
for fi, q in enumerate(Qb):
    for k in range(4): ed.setdefault((min(q[k], q[(k + 1) % 4]), max(q[k], q[(k + 1) % 4])), []).append(fi)
from collections import deque
done = fixed.copy(); seed = sorted({f for fs in ed.values() if len(fs) == 2 and fixed[fs[0]] != fixed[fs[1]] for f in fs if fixed[f]}); dq = deque(seed)
def dirs(q): return {(q[k], q[(k + 1) % 4]) for k in range(4)}
while dq:
    f = dq.popleft(); df = dirs(Qb[f])
    for k in range(4):
        e = (min(Qb[f][k], Qb[f][(k + 1) % 4]), max(Qb[f][k], Qb[f][(k + 1) % 4]))
        for g in ed[e]:
            if done[g]: continue
            if dirs(Qb[g]) & df: Qb[g] = Qb[g][::-1]
            done[g] = True; dq.append(g)
assert done.all(), (~done).sum()
# ---- fairing (order §5 / §12): biharmonic (uniform umbrella) solve for the new skull skin inside the root (cuff) and the ONE bounded v005
# transition ring outside the root (v005 vertices sharing a face with the root loop). Root loop, the rest of v005 and the ear sheet are fixed.
FAIR = os.environ.get('EAR_FAIR', '1') == '1'; part_a = np.array(part, dtype='<U12'); trans = set()
for side in ('l', 'r'):
    rd_ = patches[side][2]; zone_ = set(np.unique(Q0[rd_['faces']]).tolist())
    for fi in np.nonzero(np.isin(Q0, rd_['loop']).any(1) & ~efaces)[0]:
        for v in Q0[fi]:
            if int(v) not in zone_: trans.add(int(v2b[v]))
trans = np.array(sorted(trans)); fair_rec = dict(transition_ring_vertices=int(len(trans)))
if FAIR:
    unk = np.r_[np.nonzero(part_a == 'cuff')[0], trans]
    Eg = np.unique(np.sort(np.concatenate([Qb[:, [0, 1]], Qb[:, [1, 2]], Qb[:, [2, 3]], Qb[:, [3, 0]]]), 1), axis=0); nV_ = len(Vb)
    Ag = sp.coo_matrix((np.ones(2 * len(Eg)), (np.r_[Eg[:, 0], Eg[:, 1]], np.r_[Eg[:, 1], Eg[:, 0]])), shape=(nV_, nV_)).tocsr()
    dg = np.asarray(Ag.sum(1)).ravel(); Lg = sp.identity(nV_) - sp.diags(1 / dg) @ Ag; B2 = (Lg.T @ Lg).tocsr()
    isU = np.zeros(nV_, bool); isU[unk] = True; kn = np.nonzero(~isU)[0]
    from scipy.sparse.linalg import spsolve
    rhs = -(B2[unk][:, kn] @ Vb[kn]); X0_ = Vb[trans].copy()
    Vb[unk] = np.stack([spsolve(B2[unk][:, unk].tocsc(), rhs[:, k]) for k in range(3)], 1)
    dt = np.linalg.norm(Vb[trans] - X0_, axis=1)
    fair_rec.update(transition_ring_displacement_cm=dict(mean=float(dt.mean()), p95=float(np.percentile(dt, 95)), max=float(dt.max())), unknowns=int(len(unk)))
part_a[trans] = 'transition'; part = list(part_a)
# ---- cuff quad relaxation on the faired surface: tangential angle-based + Laplacian smoothing, re-projected onto the faired cuff
if os.environ.get('EAR_RELAX', '1') == '1':
    cuffv = np.nonzero(np.isin(part_a, ['cuff', 'transition']))[0]; cf_ = np.nonzero(np.isin(part_a, ['cuff', 'transition'])[Qb].any(1))[0]
    g_ = np.linspace(0, 1, 9); Sm = []
    for q in Qb[cf_]:
        P_ = Vb[q]; Sm.append(((1 - g_[:, None, None]) * (1 - g_[None, :, None]) * P_[0] + g_[:, None, None] * (1 - g_[None, :, None]) * P_[1]
                               + g_[:, None, None] * g_[None, :, None] * P_[2] + (1 - g_[:, None, None]) * g_[None, :, None] * P_[3]).reshape(-1, 3))
    Sm = np.concatenate(Sm); tS_ = cKDTree(Sm)
    nb_ = [set() for _ in range(len(Vb))]
    for q in Qb[cf_]:
        for k in range(4): nb_[q[k]].update({int(q[(k + 1) % 4]), int(q[(k - 1) % 4])})
    for it_ in range(int(os.environ.get('EAR_RELAX_IT', '25'))):
        Vn = Vb.copy()
        for v in cuffv:
            ns_ = np.array(sorted(nb_[v])); P_ = Vb[ns_]; c_ = P_.mean(0); nrm = np.linalg.svd(P_ - c_)[2][2]
            d_ = P_ - Vb[v]; d_ -= np.outer(d_ @ nrm, nrm); e1 = d_[0] / (np.linalg.norm(d_[0]) + 1e-12); e2 = np.cross(nrm, e1)
            o_ = np.argsort(np.arctan2(d_ @ e2, d_ @ e1)); P_ = P_[o_]; m_ = len(P_); cand = []
            for j in range(m_):
                pj = P_[j]; a1 = P_[(j - 1) % m_] - pj; a2 = P_[(j + 1) % m_] - pj; vv = Vb[v] - pj; Lv = np.linalg.norm(vv)
                bis = a1 / (np.linalg.norm(a1) + 1e-12) + a2 / (np.linalg.norm(a2) + 1e-12)
                if np.linalg.norm(bis) < 1e-9: cand.append(Vb[v]); continue
                bis /= np.linalg.norm(bis); bis = bis if bis @ vv >= 0 else -bis; cand.append(pj + Lv * bis)
            Vn[v] = 0.5 * Vb[v] + 0.5 * (0.5 * np.mean(cand, 0) + 0.5 * c_)
        _, ii = tS_.query(Vn[cuffv]); Vn[cuffv] = Sm[ii]; Vb = Vn
# ---- local untangling (bpy BVH): cuff / transition vertices of self-intersecting branch faces (+2 rings) are relaxed towards their
# neighbours and lowered towards the skull side until no pair touching the branch remains (bounded rounds; logged)
unt = dict(rounds=0, pairs=[])
try:
    import bpy  # noqa: F401
    from mathutils.bvhtree import BVHTree
    HAVE_BVH = True
except Exception:
    HAVE_BVH = False
if HAVE_BVH and os.environ.get('EAR_UNTANGLE', '1') == '1':
    movable = np.isin(part_a, ['cuff', 'transition']); brv = part_a != 'v005'
    for side in ('l', 'r'):                                     # the rim-end cross sections of the junction ring may also relax
        P_, F_, rd_, R_ = patches[side]; off_ = side_off[side]
        for row in (Lo['rim'][0], Lo['rim'][-1]):
            for v in row[1:-1]: movable[off_ + v] = True
        Jl = list(Lo['J'])                                       # attachment corners c0 / c1 and their junction neighbours may relax too
        for k_ in ('c0', 'c1'):
            i_ = Jl.index(Lo['info']['corners'][k_])
            for d_ in (-1, 0, 1): movable[off_ + Jl[(i_ + d_) % len(Jl)]] = True
    near = np.zeros(len(Vb), bool)
    for side in ('l', 'r'):
        c_ = Vb[np.array(side_of) == side].mean(0); near |= np.linalg.norm(Vb - c_, axis=1) < 9
    cuff_f = np.nonzero(np.isin(part_a, ['cuff', 'transition'])[Qb].any(1))[0]; Fsel = np.nonzero(near[Qb].all(1))[0]; tri = np.r_[Qb[Fsel][:, [0, 1, 2]], Qb[Fsel][:, [0, 2, 3]]]; qid = np.r_[Fsel, Fsel]
    nbrs = [[] for _ in range(len(Vb))]
    for q in Qb:
        for k in range(4): nbrs[q[k]] += [q[(k + 1) % 4], q[(k - 1) % 4]]
    nbrs = [np.unique(x) for x in nbrs]; nrm_side = {}
    for side in ('l', 'r'): nrm_side[side] = patches[side][2]['n']
    sidev = np.array(side_of + [''] * 0)
    for rnd in range(80):
        bvh = BVHTree.FromPolygons(Vb.tolist(), tri.tolist(), all_triangles=True, epsilon=0.0); bad = set()
        for i, j in bvh.overlap(bvh):
            fi, fj = qid[i], qid[j]
            if fi != fj and not (set(Qb[fi]) & set(Qb[fj])) and (brv[Qb[fi]].any() or brv[Qb[fj]].any()): bad.add((min(fi, fj), max(fi, fj)))
        cfq = Qb[cuff_f]; Lq = np.linalg.norm(Vb[cfq] - Vb[np.roll(cfq, -1, 1)], axis=2); hi = cuff_f[Lq.max(1) / np.maximum(Lq.min(1), 1e-9) > 7.0]
        unt['pairs'].append(len(bad)); unt.setdefault('aspect_gt7', []).append(int(len(hi)))
        if not bad and not len(hi): break
        vs = set()
        for a_, b_ in bad: vs.update(Qb[a_].tolist()); vs.update(Qb[b_].tolist())
        for f_ in hi: vs.update(Qb[f_].tolist())
        for _ in range(3 if rnd < 20 else 5): vs.update(int(w) for v in list(vs) for w in nbrs[v])
        vs = np.array([v for v in vs if movable[v]])
        for _ in range(1):
            Vn = Vb.copy()
            for v in vs: Vn[v] = 0.85 * Vb[v] + 0.15 * Vb[nbrs[v]].mean(0)
            Vb = Vn
        for v in vs:                                              # lower slightly towards the head (along the side's root normal)
            sd = side_of[v] if v < len(side_of) and side_of[v] else ('l' if Vb[v, 0] > 0 else 'r'); Vb[v] -= (0.02 if part_a[v] == 'cuff' else 0.005) * nrm_side[sd]
        unt['rounds'] = rnd + 1
fair_rec['untangle'] = unt
# ---- weight / zone proxy map: v005 rows for kept vertices; branch vertices take the row of the nearest removed v005 ear vertex (same side)
rows = [M0[keep]]
for side in ('l', 'r'):
    P, F, rd, R = patches[side]; old = rd['interior']; t = cKDTree(V0[old]); _, i = t.query(P); rows.append(M0[old[i]])
Mb = sp.vstack(rows).tocsr()
# smooth the weight proxy over the branch graph (root loop / transition rows fixed) so neighbouring branch vertices carry near-identical skinning
brm = np.array([pp not in ('v005', 'transition') for pp in part]); Eg2 = np.unique(np.sort(np.concatenate([Qb[:, [0, 1]], Qb[:, [1, 2]], Qb[:, [2, 3]], Qb[:, [3, 0]]]), 1), axis=0)
Ag2 = sp.coo_matrix((np.ones(2 * len(Eg2)), (np.r_[Eg2[:, 0], Eg2[:, 1]], np.r_[Eg2[:, 1], Eg2[:, 0]])), shape=(len(Vb), len(Vb))).tocsr()
Sg = sp.diags(1 / np.asarray(Ag2.sum(1)).ravel()) @ Ag2; Pb = sp.diags(brm.astype(float)); Pk = sp.diags((~brm).astype(float))
for _ in range(int(os.environ.get('EAR_WSMOOTH', '12'))):
    Mb = (Pk @ Mb + Pb @ (0.5 * Mb + 0.5 * (Sg @ Mb))).tocsr(); Mb.data[np.abs(Mb.data) < 1e-6] = 0; Mb.eliminate_zeros()
meta = json.loads(str(fz['meta']))
bmap = dict(v005_to_branch=v2b.astype(np.int32), removed_v005=np.nonzero(rem)[0].astype(np.int32), removed_faces_v005=np.nonzero(efaces)[0].astype(np.int32))
np.savez_compressed('%s/%s_%s_branch.npz' % (OUT, HEAD, CAND), V=Vb.astype(np.float64), Q=Qb.astype(np.int32), M_data=Mb.data, M_indices=Mb.indices, M_indptr=Mb.indptr,
                    M_shape=np.array(Mb.shape), src_index=si, hm08_Q=fz['hm08_Q'], meta=fz['meta'], part=np.array(part), side=np.array(side_of), **bmap)
rec = dict(head=HEAD, cand=CAND, params=p, geo=geo, HH_cm=HH, head_scale=sc, verts=int(len(Vb)), faces=int(len(Qb)), v005_verts=int(len(V0)), v005_faces=int(len(Q0)),
           kept_v005_verts=int(len(keep)), removed_v005_verts=int(rem.sum()), removed_v005_faces=int(efaces.sum()), patch_verts=int(len(patches['l'][0])), patch_faces=int(len(patches['l'][1])),
           sides=recs, probe=PROBE, fairing=fair_rec)
json.dump(rec, open('%s/%s_%s_branch.json' % (OUT, HEAD, CAND), 'w'), indent=1, default=float)
print(json.dumps({k: v for k, v in rec.items() if k != 'sides'}, default=float)); print({s: {k: v for k, v in recs[s].items() if k not in ('root_loop_v005', 'frame')} for s in recs})
