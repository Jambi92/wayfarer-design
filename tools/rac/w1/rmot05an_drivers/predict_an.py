# 05AN predictor: cumulative reference = frozen 05AL baseline normals for triangles that exist there; repaired-checkpoint normals for
# rotated/new triangles. Flags: flips (dot<0), >60 deg cumulative rotation, adjacent folds >60 deg; also reference-free local
# inversion (face normal > 90 deg from its 1-ring mean) introduced by the step.
import sys; sys.path.insert(0,'/home/claude/al'); import numpy as np, scipy.sparse as sp, dryrun as D
from predict2 import face_adj, nrm, adjfold
BASE=np.load('/home/claude/al/out/after_VF.npz')
def reference(F, Vstart):
    sB=set(map(tuple,np.sort(BASE['F'],1))); isnew=np.array([tuple(r) not in sB for r in np.sort(F,1)])
    ref=nrm(BASE['V'],F); ref[isnew]=nrm(Vstart,F)[isnew]; return ref,isnew
def ringang(X,F,vf):
    N=nrm(X,F); acc=vf.T@(vf@N)-3*N; acc/=np.maximum(np.linalg.norm(acc,axis=1),1e-30)[:,None]; return np.degrees(np.arccos(np.clip((N*acc).sum(1),-1,1)))
def laplace_iter(V,Avg,M,n,f=1.0):
    co=V.copy(); fade=(f*(1-M))[:,None]
    for _ in range(n): co=co+(Avg@co-co)*fade
    return co
def predict(V,F,M,proposal,ref=None,Vstart=None):
    if ref is None: ref,_=reference(F,V if Vstart is None else Vstart)
    fa,fb=face_adj(F); vf=sp.csr_matrix((np.ones(F.size),(F.ravel(),np.repeat(np.arange(len(F)),3))),shape=(len(V),len(F)))
    r0=ringang(V,F,vf); S=proposal(V); dot=(nrm(S,F)*ref).sum(1)
    fl=set(np.flatnonzero(dot<0).tolist()); nr=set(np.flatnonzero(dot<0.5).tolist())-fl; adj=adjfold(S,F,fa,fb,fl|nr)-fl-nr
    r1=ringang(S,F,vf); loc=set(np.flatnonzero((r1>90)&(r0<=90)).tolist())
    return dict(flips=sorted(fl),near60=sorted(nr),adj=sorted(adj),local_new_inversions=sorted(loc),S=S)
