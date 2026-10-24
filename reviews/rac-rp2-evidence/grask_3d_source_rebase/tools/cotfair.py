import numpy as np, igl, scipy.sparse as sp
from scipy.sparse.linalg import splu
def cot_fair(P0,F,r,lam,it=2):
    """(M - lam R L) X = M X0 ; geometric screened fairing inside per-vertex weight r (0..1); lam in cm^2"""
    Xc=P0.astype(float); F=F.astype(np.int64)
    for _ in range(it):
        L=igl.cotmatrix(Xc,F); M=igl.massmatrix(Xc,F,igl.MASSMATRIX_TYPE_BARYCENTRIC)+sp.eye(len(Xc))*1e-6
        lu=splu((M-lam*sp.diags(r)@L).tocsc()); B=M@Xc
        Xc=np.stack([lu.solve(B[:,j]) for j in range(3)],1)
    return Xc
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
