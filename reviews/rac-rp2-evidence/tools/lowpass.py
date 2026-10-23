import numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import factorized
def lowpass(Q, n, F, lam, w=None):
    """screened low-pass of per-vertex field F (n x k): (W + lam L) X = W F; w = data weights (default 1)."""
    e=np.r_[Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]
    A=sp.coo_matrix((np.ones(len(e)*2),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),(n,n)).tocsr(); A.data[:]=1
    L=sp.diags(np.asarray(A.sum(1)).ravel())-A
    w=np.ones(n) if w is None else w
    s=factorized((sp.diags(w+1e-9)+lam*L).tocsc()); WF=w[:,None]*F
    return np.stack([s(WF[:,j]) for j in range(F.shape[1])],1)
