# region_fair.py : screened smoothing of production positions inside a soft region mask (outside: unchanged).
import numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import spsolve
def region_fair(P0, Q, r, lam, it=1):
    """solve (I + lam*diag(r) L) X = P0; r in [0,1] per vertex. Uniform-graph Laplacian. Repeated 'it' times."""
    n=len(P0); e=np.r_[Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]
    A=sp.coo_matrix((np.ones(2*len(e)),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),(n,n)).tocsr(); A.data[:]=1
    d=np.asarray(A.sum(1)).ravel(); L=sp.diags(np.ones(n))-sp.diags(1/d)@A
    M=(sp.eye(n)+lam*sp.diags(r)@L).tocsc()
    from scipy.sparse.linalg import splu
    lu=splu(M); X=P0.copy()
    for _ in range(it): X=np.stack([lu.solve(X[:,j]) for j in range(3)],1)
    return X
