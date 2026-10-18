import numpy as np,sys,json,pymeshlab;sys.path.insert(0,'/home/claude/aw1');import aw1lib as L
from scipy.sparse.csgraph import dijkstra
vf,gate,prev,out=sys.argv[1:5]
X=np.load(vf)['V'];k,iv=np.unique(np.round(X,7),axis=0,return_inverse=True);Fw=iv.ravel()[L.F]
ms=pymeshlab.MeshSet();ms.add_mesh(pymeshlab.Mesh(k,Fw));ms.compute_selection_by_self_intersections_per_face()
ids=np.flatnonzero(ms.current_mesh().face_selection_array()).tolist()+json.load(open(gate))['folded_face_ids']
seed=np.unique(L.F[ids].ravel()) if ids else np.zeros(0,int)
w=np.load(prev) if prev!='none' else np.zeros(len(X))
if len(seed):
    d=dijkstra(L.G,directed=False,indices=seed,limit=0.006,min_only=True);w2=1-L.ss((d-0.001)/0.002);w2[~np.isfinite(d)]=0;w2[~np.load('support_S.npy')]=0;w=np.maximum(w,w2)
np.save(out,w);print('seeds',len(seed))
