import numpy as np, sys
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); F=w['F'].astype(np.int64)
C=S[F].mean(1)
def g(lo,hi):
    m=((C>lo)&(C<hi)).all(1); T=F[m]
    if len(T)==0: return None
    E=np.sort(np.vstack([T[:,[0,1]],T[:,[1,2]],T[:,[2,0]]]),axis=1); u,c=np.unique(E,axis=0,return_counts=True)
    vs=np.unique(T); chi=len(vs)-len(u)+len(T)
    be=u[c==1]
    # boundary loops count = components of boundary edge graph
    if len(be):
        idx={v:i for i,v in enumerate(np.unique(be))}; a=np.array([idx[v] for v in be[:,0]]); b=np.array([idx[v] for v in be[:,1]])
        nb=connected_components(coo_matrix((np.ones(len(a)),(a,b)),shape=(len(idx),len(idx))),directed=False)[0]
    else: nb=0
    # components of patch
    iv={v:i for i,v in enumerate(vs)}; a=np.array([iv[v] for v in E[:,0]]); b=np.array([iv[v] for v in E[:,1]])
    nc=connected_components(coo_matrix((np.ones(len(a)),(a,b)),shape=(len(vs),len(vs))),directed=False)[0]
    return (2*nc-chi-nb)/2, nc, nb
for name,lo,hi in eval(sys.argv[1]):
    print(name, g(np.array(lo),np.array(hi)))
