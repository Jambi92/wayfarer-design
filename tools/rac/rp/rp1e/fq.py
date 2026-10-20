# fq.py CAGE.npz [nold] : quality of faces touching new verts (index>=nold): normal agreement with source normal, aspect
import numpy as np, sys, igl
from scipy.spatial import cKDTree
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
N=igl.per_vertex_normals(S,SF); kS=cKDTree(S)
z=np.load(sys.argv[1]); V=z['V']; F=[[int(x) for x in f if x>=0] for f in z['F']]; n0=int(sys.argv[2])
ds=[];asp=[]
for f in F:
    if max(f)<n0: continue
    P=V[f]; n=np.zeros(3)
    for i in range(len(f)): n+=np.cross(P[i],P[(i+1)%len(f)])
    n/=np.linalg.norm(n)+1e-12; c=P.mean(0); ds.append(n@N[kS.query(c)[1]])
    e=[np.linalg.norm(P[i]-P[(i+1)%len(f)]) for i in range(len(f))]; asp.append(max(e)/max(min(e),1e-6))
ds=np.array(ds); asp=np.array(asp); print('new faces',len(ds),'min dot %.2f  n<0.3: %d  n<0: %d  max aspect %.1f  n asp>8: %d'%(ds.min(),(ds<0.3).sum(),(ds<0).sum(),asp.max(),(asp>8).sum()))
