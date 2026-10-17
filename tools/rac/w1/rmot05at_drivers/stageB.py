# 05AT Stage B predictor from a Stage-A geometry: N masked Laplacian events with Mask B. Transition edges = edges touching a vertex
# with Mask A or Mask B < 1 that is not in the Mask-A belly (M_A < 0.5). Increase vs GO-05AO_AC2; abs > 35 counted only for edges < 35 deg at Stage A.
import sys, json; sys.path[:0]=['/home/claude/at','/home/claude/as','/home/claude/aq','/home/claude/al','/home/claude/an']; import numpy as np, aqmetrics as Q, aqsim as A, dryrun as D, predict_an as PA, atmask as T
from predict2 import face_adj, nrm
from scipy.sparse.csgraph import connected_components
import scipy.sparse as sp
V=Q.V0; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; SA=np.load(sys.argv[1])['V']; MA=np.load('maskA.npy'); MB=np.load(sys.argv[2]); St=np.load('/home/claude/ar/sets.npz')
fa,fb=face_adj(F); ang=lambda X: np.degrees(np.arccos(np.clip((nrm(X,F)[fa]*nrm(X,F)[fb]).sum(1),-1,1))); a0=ang(V); aA=ang(SA)
fminA=MA[F].min(1); fmaxA=MA[F].max(1); fminB=MB[F].min(1); bellyA=(fmaxA[fa]<0.5)&(fmaxA[fb]<0.5)
trans=~bellyA&((fminA[fa]<1)|(fminA[fb]<1)|(fminB[fa]<1)|(fminB[fb]<1)); Avg=D.adjacency(F,len(V)); s0=set(A.si(V,F).tolist()); HC={s:i[MA[i]>=1] for s,i in Q.HB.items()}
nf=len(F); rows=[]; X=SA.copy(); done=0
for n in [int(x) for x in sys.argv[3].split(',')]:
    X=PA.laplace_iter(X,Avg,MB,n-done); done=n; a1=ang(X); d=a1-a0
    e=np.flatnonzero(trans&(d>10)); chains=[]
    if len(e):
        k,lab=connected_components(sp.coo_matrix((np.ones(len(e)),(fa[e],fb[e])),shape=(nf,nf)),directed=False); fl=np.unique(np.r_[fa[e],fb[e]])
        for cpt in np.unique(lab[fl]):
            fs=fl[lab[fl]==cpt]; p=V[F[fs]].reshape(-1,3); sp_=float(np.linalg.norm(p.max(0)-p.min(0))*1000)
            if sp_>40: chains.append(round(sp_,1))
    dd=np.linalg.norm(X-V,axis=1)*1000
    r=dict(events=n,si=len(set(A.si(X,F).tolist())-s0),flips=len(D.flips(V,X,F)),collapse=len(A.collapse(V,X,F)),trans_max_inc=round(float(d[trans].max()),2),trans_n20=int((trans&(d>20)).sum()),
           abs35_new=int((trans&(aA<35)&(a1>35)).sum()),chains=chains,ring=round(float(dd[St['ring']].max()),3),core=float(dd[St['core']].max()),pelvis_pct=round((Q.pelvis_width(X)/Q.pelvis_width(V)-1)*100,3),
           hip={s:round(float(np.linalg.norm(X[i].mean(0)-V[i].mean(0))*1000),4) for s,i in HC.items()},thigh=Q.thigh_radius(X),belly_change_from_A_mm=round(float(np.linalg.norm(X-SA,axis=1)[MA<0.1].max()*1000),3))
    rows.append(r); print(json.dumps(r),flush=True); np.savez(f'simB_{sys.argv[4]}_{n}.npz',V=X,F=F)
json.dump(rows,open(f'tableB_{sys.argv[4]}.json','w'),indent=1)
