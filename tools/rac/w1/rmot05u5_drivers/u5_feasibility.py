# RM-OT-05U5 diagnostic only (never applied to a production file): Laplacian-smooth copies of the pinned 05U baseline
# (4 notch vertices, or all 15 cap vertices; lam 0.1-0.5 x 1-4 iterations) and report in-scope roughness (b) and sliver guard (e).
import numpy as np, trimesh, json, itertools
from collections import defaultdict
S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
s3=trimesh.load(S+'/u3/GO-05S-S3.obj',process=False); Vs=np.asarray(s3.vertices); F=np.asarray(s3.faces)
def geo(p):
    R=np.load(p); i=R['s3_vid1']-1; V=Vs.copy(); mv=~np.all(R['V']==Vs[i].astype(np.float32),1); V[i[mv]]=R['V'][mv]; return V
PS=np.load('reviews/rac-rmot05u2-proposal/proposal_sets.npz'); E=PS['proposed_editable']; A=PS['added_faces']
Vb=geo('reviews/rac-rmot05u-evidence/checks/return/return.npz')
vf=defaultdict(list); nb=defaultdict(set)
for k,f in enumerate(F):
    for v in f: vf[int(v)].append(k)
    for x in f:
        for y in f:
            if x!=y: nb[int(x)].add(int(y))
def rough(V,vs):
    fn=trimesh.Trimesh(V,F,process=False).face_normals; o={}
    for v in vs:
        n=fn[vf[int(v)]]; c=n.mean(0); c/=np.linalg.norm(c); o[int(v)]=float(np.degrees(np.arccos(np.clip(n@c,-1,1))).max())
    return o
def minang(V,fs):
    T=V[F[fs]]; L=np.linalg.norm(T[:,[1,2,0]]-T[:,[2,0,1]],axis=2)
    cs=np.stack([(L[:,(i+1)%3]**2+L[:,(i+2)%3]**2-L[:,i]**2)/(2*L[:,(i+1)%3]*L[:,(i+2)%3]) for i in range(3)],1)
    return np.degrees(np.arccos(np.clip(cs,-1,1))).min(1)
added=np.setdiff1d(np.unique(F[A]),PS['proposed_frozen_ring']); added=np.intersect1d(added,E)
print('editable verts in cap faces',len(added))
mb=minang(Vb,A); rb=rough(Vb,E)
insc=[v for v in rb if v not in (70735,70592,70408)]
print('baseline in-scope over', sorted([(round(rb[v],1),v) for v in insc if rb[v]>36.3],reverse=True))
def smooth(V,vs,lam,it):
    V=V.copy()
    for _ in range(it):
        N=V.copy()
        for v in vs: N[v]=V[v]+lam*(V[list(nb[v])].mean(0)-V[v])
        V=N
    return V
for vs_name,vs in [('notch4',[61581,61303,61580,62065]),('cap',list(added))]:
  for lam in (0.1,0.2,0.35,0.5):
    for it in (1,2,4):
        V=smooth(Vb,vs,lam,it); r=rough(V,E); m=minang(V,A)
        worse=int(((m<mb-0.01)|(m<5)).sum()); over=[v for v in insc if r[v]>36.3]
        print(vs_name,lam,it,'max_in_scope',round(max(r[v] for v in insc),1),'over_in',len(over),'e_worse',worse,'maxmove',round(float(np.linalg.norm(V-Vb,axis=1).max()),3))
