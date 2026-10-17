# 05AT Stage A predictor: exact UI deflate (0.020 / -100 px = -7.919 mm x (1-M_A)) + N masked Laplacian events (Mask A).
# Belly = edges whose faces are all M_A < 0.5; band = remaining edges touching any M_A < 1 vertex. Increases vs GO-05AO_AC2.
import sys, json; sys.path[:0]=['/home/claude/as','/home/claude/aq','/home/claude/al','/home/claude/an']; import numpy as np, aqmetrics as Q, aqsim as A, dryrun as D, predict_an as PA
from predict2 import face_adj, nrm
V=Q.V0; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; M=np.load(sys.argv[1]); St=np.load('/home/claude/ar/sets.npz')
fa,fb=face_adj(F); n0=nrm(V,F); a0=np.degrees(np.arccos(np.clip((n0[fa]*n0[fb]).sum(1),-1,1)))
fmax=M[F].max(1); fmin=M[F].min(1); belly=(fmax[fa]<0.5)&(fmax[fb]<0.5); band=~belly&((fmin[fa]<1)|(fmin[fb]<1))
Avg=D.adjacency(F,len(V)); Y=V+A.vnormals(V,F)*(-0.007919*(1-M))[:,None]; s0=set(A.si(V,F).tolist()); HC={s:i[M[i]>=1] for s,i in Q.HB.items()}
rows=[]; X=Y; done=0
for n in [int(x) for x in sys.argv[2].split(',')]:
    X=PA.laplace_iter(X,Avg,M,n-done); done=n
    n1=nrm(X,F); a1=np.degrees(np.arccos(np.clip((n1[fa]*n1[fb]).sum(1),-1,1))); d=a1-a0
    fl=len(D.flips(V,X,F)); si=len(set(A.si(X,F).tolist())-s0); dd=np.linalg.norm(X-V,axis=1)*1000
    r=dict(events=n,si=si,flips=fl,collapse=len(A.collapse(V,X,F)),belly_max_inc=round(float(d[belly].max()),2),belly_n25=int((d[belly]>25).sum()),band_max_inc=round(float(d[band].max()),2),band_n12=int((d[band]>12).sum()),
        ring=round(float(dd[St['ring']].max()),3),core=float(dd[St['core']].max()),pelvis_pct=round((Q.pelvis_width(X)/Q.pelvis_width(V)-1)*100,3),
        hip={s:round(float(np.linalg.norm(X[i].mean(0)-V[i].mean(0))*1000),4) for s,i in HC.items()},thigh=Q.thigh_radius(X),depth={s:round(Q.profile_depth(X)[s]-Q.profile_depth(V)[s],2) for s in 'LR'})
    rows.append(r); print(json.dumps(r),flush=True); np.savez(f'simA_{sys.argv[3]}_{n}.npz',V=X,F=F)
json.dump(rows,open(f'tableA_{sys.argv[3]}.json','w'),indent=1)
