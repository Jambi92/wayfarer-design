# precompute labels for base and surface (surface inherits base weights/normals via nearest base vertex)
import numpy as np, igl, pickle, sys
sys.path.insert(0,'/tmp/claude-0/rodin/v1'); import vary
from scipy.spatial import cKDTree
b=np.load(vary.REF_BASE); V=b['V'].astype(float); F=b['F'].astype(np.int64)
N=igl.per_vertex_normals(V,F)
# smooth normals a little (composition offsets should follow body form, not facets)
from scipy.sparse import coo_matrix, diags
E=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); A=coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(len(V),)*2).tocsr(); A=((A+A.T)>0).astype(float)
Lu=diags(1/np.asarray(A.sum(1)).ravel())@A
for _ in range(10): N=Lu@N
N/=np.linalg.norm(N,axis=1)[:,None]
Lb=vary.Labels(V,N)
for nm in ('mus','fat','fat_conc','arm','leg','tail','head'):
    w=getattr(Lb,nm)
    for _ in range(40 if nm in ('mus','fat') else 6): w=Lu@w
    setattr(Lb,nm,w)
pickle.dump(Lb,open('/tmp/claude-0/rodin/v1/Lbase.pkl','wb'))
s=np.load(vary.REF_SURF); S=s['V'].astype(float)
d,j=cKDTree(V).query(S)
Ls=vary.Labels.__new__(vary.Labels)
for k,v in Lb.__dict__.items():
    if isinstance(v,np.ndarray) and len(v)==len(V): setattr(Ls,k,v[j])
    else: setattr(Ls,k,v)
# exact tail-frame offsets for surface vertices
C=Lb.C; tr=cKDTree(C); dd,k=tr.query(S); Ls.k=k; Ls.s=k*0.5; o=S-C[k]; Ls.ox=o[:,0]; Ls.on=np.einsum('ij,ij->i',o,Lb.Nn[k]); Ls.ot=np.einsum('ij,ij->i',o,Lb.T[k])
pickle.dump(Ls,open('/tmp/claude-0/rodin/v1/Lsurf.pkl','wb'))
print('ok', len(V), len(S))
