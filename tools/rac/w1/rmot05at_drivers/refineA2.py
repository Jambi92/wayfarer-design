import sys, json; sys.path[:0]=['/home/claude/at','/home/claude/as','/home/claude/aq','/home/claude/al','/home/claude/an']; import numpy as np, aqmetrics as Q, aqsim as A, dryrun as D, predict_an as PA, atmask as T
from predict2 import face_adj, nrm
V=Q.V0; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; fa,fb=face_adj(F); a0=np.degrees(np.arccos(np.clip((nrm(V,F)[fa]*nrm(V,F)[fb]).sum(1),-1,1))); Avg=D.adjacency(F,len(V)); vn=A.vnormals(V,F)
c=(V[F[fa]].mean(1)+V[F[fb]].mean(1))/2; sites=[]; log=[]
for it in range(6):
    M=T.mask_log2(sites=sites); fmax=M[F].max(1); fmin=M[F].min(1); belly=(fmax[fa]<0.5)&(fmax[fb]<0.5); band=~belly&((fmin[fa]<1)|(fmin[fb]<1))
    X=V+vn*(-0.007919*(1-M))[:,None]; done=0; new=[]; rec={}
    for n in [100,120,140,160]:
        X=PA.laplace_iter(X,Avg,M,n-done); done=n; d=np.degrees(np.arccos(np.clip((nrm(X,F)[fa]*nrm(X,F)[fb]).sum(1),-1,1)))-a0
        e=np.flatnonzero((band&(d>11))|(belly&(d>24))); new+=list(c[e]); rec[n]=dict(band_max=round(float(d[band].max()),1),n12=int((band&(d>12)).sum()),belly_max=round(float(d[belly].max()),1))
    print(it,rec,'new sites',len(new),flush=True); log.append(dict(cycle=it,res=rec,sites=len(sites)+len(new)))
    if not new: break
    sites+=new
np.save('maskA5.npy',M); np.save('maskA5_sites.npy',np.array(sites)); json.dump(log,open('maskA5_log.json','w'),indent=1)
