# v004_lib.py : MPFB Family Base v004 (margin-hardening successor of frozen Marchfolk v003, order a18371c) -- shared loaders.
#   * frozen v003 base read from the frozen hm08 map (face list, map rows) + the v003 core UVs (asserted identical to the frozen face list);
#   * the four accepted family configurations (MF-M-R, MF-F-R, SK208-C1R, SKF208): hm08 R-6 bodies (identical hm08 face list / src_index);
#   * the family reference surface for barycentric rows: the Marchfolk configuration-average hm08 surface A = (MF-M + MF-F) / 2 (the v003
#     definition), triangulated as the R-6 source (hm08 quad 0-1-2 / 0-2-3), so a barycentric row lies exactly on every race's own source surface.
import json, hashlib, numpy as np, scipy.sparse as sp
from core3lib import *
FROZEN_MAP = '/mnt/user-data/outputs/rp3/MF_M_REF_RP3_retopo_v003_hm08_map.npz'
CORE3 = '/tmp/claude-0/rt/m3/v3/core_final.npz'
NAT = {'MF-M-R': '/tmp/claude-0/rt/m3/src/MF-M-R_native.npz', 'MF-F-R': '/tmp/claude-0/rt/m3/src/MF-F-R_native.npz',
       'SK208-C1R': '/tmp/claude-0/rt/sk/src/SK208-C1R_native.npz', 'SKF208': '/tmp/claude-0/rt/sk/src/SKF208_native.npz'}
R6 = {'MF-M-R': '/home/claude/wayfarer-design/reviews/reference-assets/r6/MF-M-R_r6.npz', 'MF-F-R': '/home/claude/wayfarer-design/reviews/reference-assets/r6/MF-F-R_r6.npz',
      'SK208-C1R': '/home/claude/wayfarer-design/reviews/rac-w3d-evidence/geometry/SK208-C1R_r6.npz', 'SKF208': '/home/claude/wayfarer-design/reviews/reference-assets/r6/SKF208_r6.npz'}
import os as _os
for _e in filter(None, _os.environ.get('EXTRA_NAT', '').split(',')):   # diagnostic only (order c6c7940): extra race configs "ID=NATIVE.npz=R6.npz" scored alongside the four
    _i, _n, _r = _e.split('='); NAT[_i] = _n; R6[_i] = _r
CFG = list(NAT)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def csr(z, pre='M_'): return sp.csr_matrix((z[pre + 'data'], z[pre + 'indices'], z[pre + 'indptr']), shape=tuple(z[pre + 'shape']))
def load_base():
    fm = np.load(FROZEN_MAP); c3 = np.load(CORE3); M3 = csr(fm); Q3 = np.asarray(fm['Q']).astype(np.int64)
    assert np.array_equal(Q3, c3['Q']) and abs(csr(c3) - M3).max() == 0, 'core_final != frozen map'
    C = {}
    for cid, p in NAT.items():
        n = np.load(p); C[cid] = dict(Vh=n['V'].astype(float), meta=json.loads(str(n['meta'])))
        assert np.array_equal(n['Q'], fm['hm08_Q']) and np.array_equal(n['src_index'], fm['src_index']), cid
    n = np.load(NAT['MF-M-R']); Qh = np.asarray(n['Q']); UVh = n['UV'].astype(float)
    A = 0.5 * (C['MF-M-R']['Vh'] + C['MF-F-R']['Vh'])
    chart = np.load('/tmp/claude-0/rt/m3/v3_base.npz')['chart']
    return dict(M3=M3, Q3=Q3, UV3=c3['UV'].astype(float), hm08_Q=np.asarray(fm['hm08_Q']), src_index=fm['src_index'], C=C, Qh=Qh, UVh=UVh, A=A, chart=chart, frozen_map_sha=sha(FROZEN_MAP))
def corner_uvs(Q, UV, nV):
    """per-vertex list of distinct corner UVs (seam vertex = more than one)"""
    d = [set() for _ in range(nV)]
    for f, q in enumerate(Q):
        for k, v in enumerate(q): d[v].add(tuple(np.round(UV[f, k], 6)))
    return d
