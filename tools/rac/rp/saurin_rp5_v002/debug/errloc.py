import sys,numpy as np,igl; sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v002'); import sa_geo as G
z=np.load(sys.argv[1]); Vc=z['V']; Q=z['Q']; T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]
d=np.sqrt(igl.point_mesh_squared_distance(G.V,Vc,T)[0])*10
for th in (1.5,3):
    bad=np.nonzero(d>th)[0]; import collections; print(th,len(bad),collections.Counter(G.LAB[bad]).most_common(8))
from scipy.sparse.csgraph import connected_components
bad=np.nonzero(d>1.5)[0]; sub=G.G[bad][:,bad]; nc,l=connected_components(sub,directed=False)
cl=sorted([(d[bad[l==k]].max(),len(bad[l==k]),np.round(G.V[bad[l==k]].mean(0),1).tolist(),G.LAB[bad[l==k]][0]) for k in range(nc)],reverse=True)
for c in cl[:25]: print(round(c[0],1),c[1],c[2],c[3])
np.save(sys.argv[1]+'.err.npy',d.astype(np.float32))
e=np.linalg.norm(Vc[Q]-Vc[np.roll(Q,-1,1)],axis=2); print('zero-ish edges',int((e<1e-3).sum()))
