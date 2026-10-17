# 05AM predictor: proposed step (one AK1-equivalent Surface Smooth, f=0.78) and 2x stress (8 sequential) from the CURRENT checkpoint,
# judged CUMULATIVELY against the frozen 05AL baseline (the gate reference), with a margin:
#   flip      = face normal reversed vs 05AL baseline (dot < 0)
#   near      = face normal rotated > 60 deg vs 05AL baseline (watch margin)
#   adj       = faces adjacent to a flipped/near face with dihedral > 60 deg after the dry run
import sys; sys.path.insert(0,'/home/claude/al'); import numpy as np, dryrun as D
from predict2 import face_adj, nrm, adjfold
BASE=np.load('/home/claude/al/out/after_VF.npz')
def predict(V,F,M,f=0.78,nstress=8,base=None,step='surface',smooth_fn=None):
    VB=BASE['V'] if base is None else base; nb=nrm(VB,F); Avg=D.adjacency(F,len(V)); fa,fb=face_adj(F)
    def judge(S):
        dot=(nrm(S,F)*nb).sum(1); fl=set(np.flatnonzero(dot<0).tolist()); nr=set(np.flatnonzero(dot<np.cos(np.radians(60))).tolist())-fl
        return fl,nr,adjfold(S,F,fa,fb,fl|nr)-fl-nr
    S1=smooth_fn(V) if smooth_fn else D.run(V,F,M,f,Avg=Avg); f1,n1,a1=judge(S1)
    S=V.copy(); f2=set(); n2=set(); a2=set()
    for k in range(nstress):
        S=smooth_fn(S) if smooth_fn else D.run(S,F,M,f,Avg=Avg); a,b,c=judge(S); f2|=a; n2|=b; a2|=c
    d1=np.linalg.norm(S1-V,axis=1)*1000; m1=d1>0.01
    return dict(step_flips=sorted(f1),step_near60=sorted(n1),step_adj=sorted(a1),x2_flips=sorted(f2),x2_near60=sorted(n2-f2),x2_adj=sorted(a2),
                step_stats=dict(median=float(np.median(d1[m1])) if m1.any() else 0,p95=float(np.percentile(d1[m1],95)) if m1.any() else 0,max=float(d1.max())),S1=S1)
