# ident_apply.py : transfer an identity delta defined on the 13 380-vertex body (H topology) onto production v001.
# body delta -> Grask branch base (13 386; exact hm08 vertices by index, branch vertices from the nearest body vertex)
# -> smooth subdivision operator SS (the production's own) -> added to v001.
import numpy as np, scipy.sparse as sp
from scipy.spatial import cKDTree
R='/tmp/claude-0/rp2/'
_b=np.load(R+'sstar_ppu.npz'); _s=np.load(R+'sstar.npz')
_d,_i=cKDTree(_s['V']).query(_b['V'])
_SS=None
def SS():
    global _SS
    if _SS is None:
        d=np.load(R+'cand_s3_SS.npz'); _SS=sp.csr_matrix((d['data'],d['indices'],d['indptr']),shape=tuple(d['shape']))
    return _SS
def to_base(D13380): return D13380[_i]            # body vertex order == S*/H order
def to_prod(D13380): return SS()@D13380            # SS columns are the 13 380 body vertices
def apply(D13380, base='cand_v001b.npz'):
    P=dict(np.load(R+base)); P['V']=P['V']+to_prod(D13380); return P
