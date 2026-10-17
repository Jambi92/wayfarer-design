# 05AR predictor loop: exact UI deflate model (strength 0.020, -100 px = -7.919 mm x (1-M) along original normals) then masked
# Laplacian Smooth bracketed at 150/175/200 events (real UI ran ~1.16x). Mask-only refinement: fold/SI/collapse sites get feathered
# bumps; continuity-ring vertices predicted > 2.6 mm are raised; then the 50 mm Lipschitz limit is re-imposed.
import sys, json; sys.path[:0]=['/home/claude/ar','/home/claude/aq']; import numpy as np, aqsim as A, aqmetrics as Q, armask as AR
from scipy.spatial import cKDTree
V=Q.V0; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; M0=np.load(sys.argv[1]); St=np.load('sets.npz'); S=St['S']; ring=St['ring']; core=St['core']
RT=float(sys.argv[4]) if len(sys.argv)>4 else 2.6
DUP=np.load("dup.npy")
M=M0.copy(); C=-0.007919; NS=[150,175,200]; log=[]
for it in range(int(sys.argv[3]) if len(sys.argv)>3 else 8):
    res,Sv=A.flags2(V,F,M,C,NS); bad=set()
    for n,r in res.items(): bad|=set().union(*[set(v) for v in r.values()])
    dr=np.linalg.norm(Sv-V,axis=1)*1000  # at 200 events (worst)
    summ={n:{k:len(v) for k,v in r.items()} for n,r in res.items()}; rmax=float(dr[ring].max()); cmax=float(dr[core].max())
    print(it,summ,'ring max mm',round(rmax,3),'core max',cmax,flush=True); log.append(dict(cycle=it,flags=summ,ring_max_mm_200ev=round(rmax,3),core_max_mm=cmax,sites=len(bad)))
    if not bad and rmax<=RT: break
    if bad:
        d,_=cKDTree(V[F[np.array(sorted(bad))]].mean(1)).query(V); d*=1000; M=np.where(S,np.maximum(M,np.clip((20-d)/12,0,1)),1.0)
    hi=ring&(dr>RT); M[hi]=1-(1-M[hi])*np.clip((RT-0.4)/dr[hi],0,1)
    M[DUP]=1.0; M=AR.lipschitz(M,V,F,0.05); M[~S]=1.0
np.save(sys.argv[2],M); json.dump(log,open(sys.argv[2].replace('.npy','_log.json'),'w'),indent=1)
r,Sv=A.flags2(V,F,M,C,[175]); print('raised verts',(M>M0+1e-6).sum(),'depth',Q.profile_depth(V),Q.profile_depth(Sv),'pw',Q.pelvis_width(Sv)-Q.pelvis_width(V),'thigh',Q.thigh_radius(Sv))
np.savez(sys.argv[2].replace('.npy','_sim175.npz'),V=Sv,F=F)
