# apply the cranial (head-local) warps to a display-variant head patch (world coords) without the body machinery
import numpy as np, sys
sys.path.insert(0,'/tmp/claude-0/rodin/v1'); import vary
class _L: pass
def warp_patch(P,p,eye):
    L=_L(); n=len(P); z=np.zeros(n)
    L.N=np.zeros((n,3)); L.mus=z; L.fat=z; L.fat_conc=z; L.tail=z; L.arm=z; L.leg=z; L.head=vary.ss((P[:,2]-166)/8.0); L.torso=1-L.head
    C=np.load(vary.AXIS); L.C=C; L.k=np.zeros(n,int); L.s=z; T=np.gradient(C,axis=0); T/=np.linalg.norm(T,axis=1)[:,None]; L.T=T
    L.Nn=np.stack([np.zeros(len(T)),-T[:,2],T[:,1]],1); L.ox=z; L.on=z; L.ot=z; L.side=np.where(P[:,0]>=0,1.0,-1.0)
    ii=np.arange(200); L.cen={(a,b):(np.zeros(200),np.zeros(200)) for a in ('leg','arm') for b in (1,-1)}; L.torso_cf=np.zeros(200)
    q=dict(p); q['_hmeas']=1.0; q['height']=1.0
    return vary.warp(P,L,q,eye=eye)
