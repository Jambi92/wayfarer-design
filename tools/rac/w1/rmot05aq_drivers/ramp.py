# 05AQ mask v3: guarantee a minimum-width feather at every border of the sculpt region (the v2 mask had hard 1 -> 0.4 steps where
# the 05AF protected sets were re-imposed after diffusion: tail junction / genital / sacral strip). M = max(M, 1 - d/r), d = 3-D
# distance to the nearest hard (M = 1) vertex or duplicate-position seam vertex (30 mm); r = R_TAIL near tail/tail-junction/genital/perineal/sacral strip, R_OTHER elsewhere.
import sys; sys.path.insert(0,'/home/claude/aq'); import numpy as np, aqmetrics as Q
from scipy.spatial import cKDTree
def ramp(M, r_tail=0.040, r_other=0.025):
    V=Q.V0; P=np.load('/home/claude/ag/protected_05AF.npz'); X=V[:,0]*100
    hard=M>=1.0; soft=~hard
    tailish=P['tail']|P['tail_junction']|P['genital']|P['perineal']|((np.abs(X)<=4)&(Q.Z>100)&hard)
    k,inv,cnt=np.unique(np.round(V,7),axis=0,return_inverse=True,return_counts=True); seam=cnt[inv.ravel()]>1  # position-welded seam vertices: Blender smooths them as open-boundary vertices
    out=M.copy()
    for H,r in ((hard,r_other),(tailish,r_tail),(seam,0.030)):
        d,_=cKDTree(V[H]).query(V[soft]); out[soft]=np.maximum(out[soft],np.clip(1-d/r,0,1))
    return out
if __name__=='__main__':
    M=np.load(sys.argv[1]); O=ramp(M); np.save(sys.argv[2],O)
    F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; e=np.unique(np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1),axis=0)
    for m,n in ((M,'in'),(O,'out')): j=np.abs(m[e[:,0]]-m[e[:,1]]); print(n,'jump>0.2',(j>0.2).sum(),'>0.1',(j>0.1).sum(),'max',j.max().round(3),'M<0.5',(m<0.5).sum())
