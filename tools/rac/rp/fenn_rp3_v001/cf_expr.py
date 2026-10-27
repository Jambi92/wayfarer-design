# cf_expr.py WORK OUT.json ID:R6:FAMNPZ ... : order 2de0e28 §12 focused facial readiness sanity (diagnostic, bpy). MPFB 2.0.17 expression-unit targets
# (data/targets/expression/units/caucasian, MakeHuman dm -> analysis cm: (x, z, y) x 10) are added to each source's R-6 full mesh, carried to the family
# realization through its hm08 map (production V = M @ hm08) and checked on the head (non-ear) faces for: new self-intersection pairs (BVH, non-adjacent
# faces), faces whose normal flips against neutral (fold), and -- for blink -- upper / lower lid collision (self-intersections inside the orbit region).
# No production facial weights / correctives are authored; this only catches defects introduced by the authored craniofacial geometry.
import bpy, sys, os, json, gzip, numpy as np, scipy.sparse as sp, mathutils
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
W, OUT = a[:2]; ENT = [x.split(':') for x in a[2:]]
UD = '/home/claude/mpfb2_2017/src/mpfb/data/targets/expression/units/caucasian'
def unit(n):
    D = {}
    for l in gzip.open('%s/%s.target.gz' % (UD, n), 'rt'):
        p = l.split()
        if len(p) == 4: D[int(p[0])] = np.array([float(p[1]), float(p[3]), float(p[2])]) * 10.0
    return D
EX = {'neutral': {}, 'blink': {'eye-left-closure': 1, 'eye-right-closure': 1}, 'look_up (lid follows: opened-up)': {'eye-left-opened-up': 1, 'eye-right-opened-up': 1},
      'look_down (lid follows: slit)': {'eye-left-slit': 1, 'eye-right-slit': 1}, 'smile': {'mouth-corner-puller': 1, 'mouth-upward-retraction': 0.5},
      'anger': {'eyebrows-left-down': 1, 'eyebrows-right-down': 1, 'nose-compression': 0.6, 'mouth-compression': 0.6},
      'surprise': {'eyebrows-left-up': 1, 'eyebrows-right-up': 1, 'eye-left-opened-up': 1, 'eye-right-opened-up': 1, 'mouth-open': 0.7},
      'sadness': {'eyebrows-left-inner-up': 1, 'eyebrows-right-inner-up': 1, 'mouth-depression': 1}}
UC = {n: unit(n) for e in EX.values() for n in e}
res = dict(method=__doc__ if False else 'see header', expressions={k: v for k, v in EX.items()}, not_supported='eye look left / right: eyeball rotation only, no skin expression unit in MPFB 2.0.17', bodies={})
for tag, r6, famp in ENT:
    z = np.load(r6); Vfull = z['V'].astype(float); fz = np.load(famp); si = fz['src_index']; M = sp.csr_matrix((fz['M_data'], fz['M_indices'], fz['M_indptr']), shape=tuple(fz['M_shape'])); Q = np.asarray(fz['Q'])
    wh = M @ z['w_head'][si].astype(float); we = M @ z['w_ears'][si].astype(float); el, er = np.array(z['eye_l']), np.array(z['eye_r'])
    headf = np.nonzero(((wh > 0.5) & (we < 0.05))[Q].all(1))[0]; Qh = Q[headf]
    def tris(V): T = np.r_[Qh[:, [0, 1, 2]], Qh[:, [0, 2, 3]]]; return T
    T = tris(None); fid = np.r_[np.arange(len(Qh)), np.arange(len(Qh))]
    def evalV(V):
        bvh = BVHTree.FromPolygons([mathutils.Vector(v) for v in V.tolist()], T.tolist(), all_triangles=True); pairs = set()
        for i, j in bvh.overlap(bvh):
            fi, fj = fid[i], fid[j]
            if fi == fj or set(Qh[fi]) & set(Qh[fj]): continue
            pairs.add((min(fi, fj), max(fi, fj)))
        n = np.cross(V[Qh[:, 2]] - V[Qh[:, 0]], V[Qh[:, 3]] - V[Qh[:, 1]]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
        c = V[Qh].mean(1); orb = (np.linalg.norm(c - el, axis=1) < 2.3) | (np.linalg.norm(c - er, axis=1) < 2.3)
        return pairs, n, orb
    out = {}; P0, N0, orb = None, None, None
    for e, comp in EX.items():
        Vx = Vfull.copy()
        for un, w in comp.items():
            for i, dv in UC[un].items(): Vx[i] += w * dv
        Vf = M @ Vx[si]; pairs, n, orb_ = evalV(Vf)
        if e == 'neutral': P0, N0, orb = pairs, n, orb_
        new = pairs - P0; flips = int(((n * N0).sum(1) < 0).sum())
        out[e] = dict(selfx_pairs=len(pairs), new_selfx_pairs=len(new), new_selfx_in_orbit=int(sum(1 for p in new if orb[p[0]] or orb[p[1]])), flipped_faces=flips)
    res['bodies'][tag] = out; print(tag, {e: (v['new_selfx_pairs'], v['new_selfx_in_orbit'], v['flipped_faces']) for e, v in out.items()}, flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
