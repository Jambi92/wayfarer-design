import sys; sys.path.insert(0,'/home/claude/aq'); import numpy as np, aqsim as A, aqmetrics as Q, ramp as RP, json
from scipy.spatial import cKDTree
V=Q.V0; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; M0=np.load(sys.argv[1]); M=M0.copy(); C=-0.007919; NS=[150,175,200]; log=[]
for it in range(6):
    res,S=A.flags2(V,F,M,C,NS); bad=set()
    for n,r in res.items(): bad|=set().union(*[set(v) for v in r.values()])
    summ={n:{k:len(v) for k,v in r.items()} for n,r in res.items()}; print(it,summ,flush=True); log.append(dict(cycle=it,flags=summ,sites=len(bad)))
    if not bad: break
    d,_=cKDTree(V[F[np.array(sorted(bad))]].mean(1)).query(V); d*=1000; bump=np.clip((20-d)/12,0,1); M=np.where(M0<1,np.maximum(M,bump),M0); M=RP.ramp(M)
print('bumped verts',(M>M0+1e-6).sum()); np.save(sys.argv[2],M); json.dump(log,open(sys.argv[2].replace('.npy','_log.json'),'w'),indent=1)
r1,S=A.flags2(V,F,M,C,[150]); print('depth',Q.profile_depth(V),Q.profile_depth(S),'pw',Q.pelvis_width(S)-Q.pelvis_width(V),'thigh',Q.thigh_radius(S),'seam',Q.hip_seam_proxy(S))
