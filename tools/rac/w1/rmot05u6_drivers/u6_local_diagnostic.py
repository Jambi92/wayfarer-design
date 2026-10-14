# diagnostic only: describe local geometry around the target (no candidate generation)
import numpy as np, trimesh, json
from collections import defaultdict
S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
s3=trimesh.load(S+'/u3/GO-05S-S3.obj',process=False); Vs=np.asarray(s3.vertices); F=np.asarray(s3.faces)
R=np.load('reviews/rac-rmot05u-evidence/checks/return/return.npz'); i=R['s3_vid1']-1; V=Vs.copy(); mv=~np.all(R['V']==Vs[i].astype(np.float32),1); V[i[mv]]=R['V'][mv]
SE=json.load(open('reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json')); T=SE['target_vertices']
ring=set(np.load('reviews/rac-rmot05u2-proposal/proposal_sets.npz')['proposed_frozen_ring'].tolist())
m=trimesh.Trimesh(V,F,process=False); vn=m.vertex_normals
nb=defaultdict(set)
for f in F:
    for x in f:
        for y in f:
            if x!=y: nb[int(x)].add(int(y))
for v in T:
    c=V[list(nb[v])].mean(0); off=(V[v]-c)@vn[v]
    print(v, np.round(V[v],3), 'nbrs',sorted(nb[v]), 'normal',np.round(vn[v],2),'offset_from_ring_centroid_along_n',round(float(off),3))
print('---- outlier faces per offender (baseline)')
fn=m.face_normals; vf=defaultdict(list)
for k,f in enumerate(F):
    for x in f: vf[int(x)].append(k)
for v in (61303,61581,61580,62065):
    n=fn[vf[v]]; c=n.mean(0); c/=np.linalg.norm(c); dev=np.degrees(np.arccos(np.clip(n@c,-1,1)))
    print(v,[(int(f),F[f].tolist(),round(float(d),1)) for f,d in sorted(zip(vf[v],dev),key=lambda t:-t[1])[:3]])
