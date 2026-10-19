# recolour.py SRC_COL_IN SRC_COL_OUT : split L/R limbs, head, hands, feet into separate ownership colours (by connected component)
import numpy as np, sys
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V']; F=w['F']
c=np.load(sys.argv[1]).copy(); out=c.copy()
E=np.vstack([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]])
def comps(col):
    m=c==col; e=E[m[E[:,0]]&m[E[:,1]]]
    A=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(S),len(S))); n,lab=connected_components(A,directed=False)
    return m,lab
m,lab=comps(2)
for l in np.unique(lab[m]):
    idx=np.where(m&(lab==l))[0]; P=S[idx]; cz=P[:,2].mean(); cx=P[:,0].mean()
    if P[:,2].max()>183 and cz>180: new=2
    elif P[:,2].max()<=98: new=10 if cx>1.2 else 11
    elif cz>110: new=4 if cx>2 else 5
    else:
        # small crease-wall pieces: follow the leg on that side
        new=10 if cx>1.2 else 11
    out[idx]=new
for col,newR in ((3,12),(6,13),(7,14),(8,15)):
    mm=c==col; out[mm&(S[:,0]<2)]=newR
np.save(sys.argv[2],out)
u,n=np.unique(out,return_counts=True); print(dict(zip(u.tolist(),n.tolist())))
