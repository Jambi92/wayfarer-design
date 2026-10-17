import sys, json; sys.path[:0]=['/home/claude/at','/home/claude/as','/home/claude/aq','/home/claude/al','/home/claude/an']; import numpy as np, aqmetrics as Q, aqsim as A, dryrun as D, predict_an as PA, atmask as T
from predict2 import face_adj, nrm
V=Q.V0; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; fa,fb=face_adj(F); a0=np.degrees(np.arccos(np.clip((nrm(V,F)[fa]*nrm(V,F)[fb]).sum(1),-1,1))); Avg=D.adjacency(F,len(V)); vn=A.vnormals(V,F); z0=V[:,2].min()
for args in sys.argv[1:]:
    kw=eval('dict('+args+')'); M=T.mask_log(**kw); X=PA.laplace_iter(V+vn*(-0.007919*(1-M))[:,None],Avg,M,120)
    d=np.degrees(np.arccos(np.clip((nrm(X,F)[fa]*nrm(X,F)[fb]).sum(1),-1,1)))-a0; fmax=M[F].max(1); fmin=M[F].min(1); belly=(fmax[fa]<0.5)&(fmax[fb]<0.5); band=~belly&((fmin[fa]<1)|(fmin[fb]<1))
    b=np.linalg.norm(X-V,axis=1)*1000; post=(Q.Z>90)&(Q.Z<110)&(np.abs(V[:,0])>0.06)&(V[:,1]>-0.32)
    print(args,'| band max',round(float(d[band].max()),1),'n>12',int((band&(d>12)).sum()),'belly max',round(float(d[belly].max()),1),'| mean posterior move mm',round(float(b[post].mean()),2),'M<0.1',(M<0.1).sum(),flush=True)
