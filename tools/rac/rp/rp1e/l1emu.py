# l1emu.py: emulate the sim stack at level 1 (limit surface, then Nearest per dominant colour); returns V1, F1 (quads)
import sys, numpy as np, scipy.sparse as sp
from scipy.spatial import cKDTree
sys.path.insert(0,'/home/claude/stc/rp1e')
from ccmat import cc_step, limit_matrix
_T={}
def target(c):
    if c not in _T:
        t=np.load('/home/claude/stc/rp1e/tg_r2m5_c%d.npz'%c)['V']; _T[c]=(cKDTree(t),t)
    return _T[c]
def l1(V,F,col,L=1,snap=True,box=None):
    n=len(V); M=sp.identity(n,format='csr'); cur=F; W=None
    cols=sorted(set(col.tolist())); oh=sp.csr_matrix((np.ones(n),(np.arange(n),np.searchsorted(cols,col))),shape=(n,len(cols)))
    P=V.copy(); OH=oh
    for _ in range(L):
        S,cur=cc_step(len(P),cur); Lm=limit_matrix(S.shape[0],cur)@S
        P=Lm@P; OH=(S@OH)
        if snap:
            dom=np.array(cols)[np.asarray(OH.argmax(1)).ravel()]
            idx=np.arange(len(P)) if box is None else np.where(np.all((P>box[0])&(P<box[1]),axis=1))[0]
            for c in set(dom[idx].tolist()):
                m=idx[dom[idx]==c]; kd,t=target(c); P[m]=t[kd.query(P[m])[1]]
    return P,cur
