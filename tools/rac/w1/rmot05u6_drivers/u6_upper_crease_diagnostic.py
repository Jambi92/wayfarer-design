# diagnostic only: classify rough vertices near the crease line above the cap (read-only)
import sys, json, numpy as np, trimesh
from collections import defaultdict
S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
s3=trimesh.load(S+'/u3/GO-05S-S3.obj',process=False); Vs=np.asarray(s3.vertices); F=np.asarray(s3.faces)
R=np.load(sys.argv[1]); i=R['s3_vid1']-1; V=Vs.copy(); mv=~np.all(R['V']==Vs[i].astype(np.float32),1); V[i[mv]]=R['V'][mv]
P=np.load('reviews/rac-rmot05u2-proposal/proposal_sets.npz'); E=set(P['proposed_editable'].tolist()); ring=set(P['proposed_frozen_ring'].tolist())
T=set(json.load(open('reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json'))['target_vertices'])
fn=trimesh.Trimesh(V,F,process=False).face_normals; vf=defaultdict(list)
for k,f in enumerate(F):
    for x in f: vf[int(x)].append(k)
box=(V[:,0]>27.0)&(V[:,0]<30.5)&(V[:,1]>-15.5)&(V[:,1]<-11.0)&(V[:,2]>166.5)&(V[:,2]<172.5)
out=[]
for v in np.where(box)[0]:
    n=fn[vf[int(v)]]; c=n.mean(0); c/=np.linalg.norm(c); r=float(np.degrees(np.arccos(np.clip(n@c,-1,1))).max())
    out.append((round(r,1),int(v),np.round(V[v],2).tolist(),'TARGET' if v in T else 'RING(frozen)' if v in ring else 'EDITABLE-outside-target' if v in E else 'PROTECTED(outside U2)'))
print(len(out));
for o in sorted(out,reverse=True)[:25]: print(o)
