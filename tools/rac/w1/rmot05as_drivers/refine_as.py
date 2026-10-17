# 05AS mask-only refinement against the strict dihedral gate: sites with a predicted new dihedral increase > 18 deg (any of 10/15/20/25
# events), or SI / flips / collapse, get a smooth 30 mm protective bump (fed into the mask build before the C1 relaxation and the
# Lipschitz feather, so the bump is itself feathered). Ring target <= 2.0 mm (model) for the ~1.4x real/model margin.
import sys, json; sys.path[:0]=['/home/claude/as','/home/claude/aq','/home/claude/al','/home/claude/an']; import numpy as np, aqmetrics as Q, aqsim as A, dryrun as D, predict_an as PA, dihed as DH, asmask as AM
from scipy.spatial import cKDTree
V=Q.V0; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; St=np.load('/home/claude/ar/sets.npz'); Avg=D.adjacency(F,len(V)); vn=A.vnormals(V,F)
extra=np.zeros(len(V)); NS=[10,15,20,25]; log=[]
for it in range(int(sys.argv[2])):
    M,S,zone=AM.build(extra=extra); G=DH.Gate(V,F,M); Y=V+vn*(-0.007919*(1-M))[:,None]; X=Y; done=0; sites=[]; rec={}
    for n in NS:
        X=PA.laplace_iter(X,Avg,M,n-done); done=n; g,d=G.eval(X); si=A.si(X,F); col=A.collapse(V,X,F)
        fl=np.flatnonzero((np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]])*np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]])).sum(1)<0)
        ring=float((np.linalg.norm(X-V,axis=1)*1000)[St['ring']].max())
        rec[n]=dict(inc=g['max_inc_transition'],n20=g['n_inc20_transition'],abs35=g['n_abs_over35_new'],si=len(si),flips=len(fl),col=len(col),ring=round(ring,2),chains=len(g['chains_over_40mm']))
        e=np.flatnonzero(G.trans&(d>18)); sites+=list(G.c[e])+list(V[F[np.r_[si,fl,col].astype(int)]].mean(1)) if (len(si)+len(fl)+len(col)) else list(G.c[e])
        if ring>2.0: sites+=list(V[St['ring']][np.argsort(-(np.linalg.norm(X-V,axis=1))[St['ring']])[:20]])
    print(it,rec,flush=True); log.append(dict(cycle=it,result=rec,sites=len(sites)))
    if not sites: break
    dd,_=cKDTree(np.array(sites)).query(V); extra=np.maximum(extra,np.clip((30-dd*1000)/20,0,1))
np.save(sys.argv[1],M); json.dump(log,open(sys.argv[1].replace('.npy','_log.json'),'w'),indent=1)
print('extra-protected verts',(extra>0).sum(),'M<0.5',(M<0.5).sum())
