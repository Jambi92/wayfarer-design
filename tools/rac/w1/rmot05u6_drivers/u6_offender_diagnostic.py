# diagnostic only: outlier faces + offsets for the remaining offenders in a given return
import sys, numpy as np, trimesh
from collections import defaultdict
S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
s3=trimesh.load(S+'/u3/GO-05S-S3.obj',process=False); Vs=np.asarray(s3.vertices); F=np.asarray(s3.faces)
R=np.load(sys.argv[1]); i=R['s3_vid1']-1; V=Vs.copy(); mv=~np.all(R['V']==Vs[i].astype(np.float32),1); V[i[mv]]=R['V'][mv]
m=trimesh.Trimesh(V,F,process=False); fn=m.face_normals; vn=m.vertex_normals; vf=defaultdict(list); nb=defaultdict(set)
for k,f in enumerate(F):
    for x in f: vf[int(x)].append(k); nb[int(x)].update(int(y) for y in f if y!=x)
for v in map(int,sys.argv[2:]):
    n=fn[vf[v]]; c=n.mean(0); c/=np.linalg.norm(c); dev=np.degrees(np.arccos(np.clip(n@c,-1,1)))
    off=(V[v]-V[list(nb[v])].mean(0))@vn[v]
    print(v,np.round(V[v],3),'n',np.round(vn[v],2),'offset',round(float(off),3),[(int(f),F[f].tolist(),round(float(d),1)) for f,d in sorted(zip(vf[v],dev),key=lambda t:-t[1])[:3]])
