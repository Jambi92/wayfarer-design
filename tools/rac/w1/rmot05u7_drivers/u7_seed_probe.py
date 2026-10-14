import numpy as np, trimesh, json
from collections import defaultdict
S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
s3=trimesh.load(S+'/u3/GO-05S-S3.obj',process=False); Vs=np.asarray(s3.vertices); F=np.asarray(s3.faces)
R=np.load(S+'/u6fx/GO-05U6_cp3/out/return.npz'); i=R['s3_vid1']-1; V=Vs.copy(); mv=~np.all(R['V']==Vs[i].astype(np.float32),1); V[i[mv]]=R['V'][mv]
m=trimesh.Trimesh(V,F,process=False)
seeds=[61522,61771,62027,61586,61183,62063]
nb=defaultdict(set); vf=defaultdict(list)
for k,f in enumerate(F):
    for x in f: vf[int(x)].append(k); nb[int(x)].update(int(y) for y in f if y!=x)
print('seed adjacency:',{s:[t for t in seeds if t in nb[s]] for s in seeds})
inc=sorted({f for s in seeds for f in vf[s]}); verts=sorted({int(v) for f in inc for v in F[f]}); ring=[v for v in verts if v not in seeds]
print('incident faces',len(inc),'verts in them',len(verts),'ring',len(ring))
U6T=set(json.load(open('reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json'))['target_vertices']); print('U6 target in ring',[v for v in ring if v in U6T])
P=np.load('reviews/rac-rmot05u2-proposal/proposal_sets.npz'); E=set(P['proposed_editable'].tolist()); RG=set(P['proposed_frozen_ring'].tolist())
lab=np.load('reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_face_labels.npy'); print('seed class',{s:('U2ring' if s in RG else 'E' if s in E else 'prot') for s in seeds}); print('labels of incident faces',np.bincount(lab[inc]).tolist())
# dihedral edges in corridor
adj=m.face_adjacency; ae=m.face_adjacency_edges; fn=m.face_normals
dih=np.degrees(np.arccos(np.clip((fn[adj[:,0]]*fn[adj[:,1]]).sum(1),-1,1))); mid=V[ae].mean(1)
box=(mid[:,0]>27.0)&(mid[:,0]<30.6)&(mid[:,1]>-15.5)&(mid[:,1]<-11.0)&(mid[:,2]>169.4)&(mid[:,2]<172.3)
o=np.argsort(-dih*box)[:25]
for k in o: print(round(float(dih[k]),1), ae[k].tolist(), np.round(mid[k],2).tolist(), ['S' if v in seeds else 'r' if v in ring else 'U6' if v in U6T else '-' for v in ae[k]])
