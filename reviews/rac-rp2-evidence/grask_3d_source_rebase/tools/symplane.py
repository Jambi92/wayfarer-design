import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
def sym_plane(P,cap=3.0,x0=None):
    """bilateral symmetry plane n.x=d of point set P (normal parameterized by yaw/roll about +x), minimizing the truncated reflection distance"""
    tree=cKDTree(P)
    def nrm(a): yaw,roll=np.radians(a[0]),np.radians(a[1]); n=np.array([np.cos(yaw)*np.cos(roll),np.sin(yaw),np.sin(roll)]); return n/np.linalg.norm(n)
    def f(a):
        n=nrm(a); M=P-2*((P@n-a[2])[:,None])*n; d,_=tree.query(M); return np.minimum(d,cap).mean()
    best=None
    for y0 in (-6,-3,0,3,6):
        for r0 in (-3,0,3):
            r=minimize(f,[y0,r0,np.median(P[:,0]) if x0 is None else x0],method='Nelder-Mead',options=dict(xatol=1e-3,fatol=1e-5,maxiter=400))
            if best is None or r.fun<best.fun: best=r
    n=nrm(best.x); return n,best.x[2],best.x,best.fun
