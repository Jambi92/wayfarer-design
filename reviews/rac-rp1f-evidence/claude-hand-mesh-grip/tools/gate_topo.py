# gate_topo.py IN.npz : topology + face shape + duplicate/degenerate checks for a quad production mesh (analysis frame)
import sys,numpy as np,json; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from hm import *
from scipy.sparse.csgraph import connected_components
z=np.load(sys.argv[1]); V=z['V']*np.array([1,-1,1]); Q=z['Q']
E=np.vstack([Q[:,[i,(i+1)%4]] for i in range(4)]); key=np.sort(E,1); u,inv,c=np.unique(key,axis=0,return_inverse=True,return_counts=True)
# directed duplicates (orientation consistency)
du=np.unique(E,axis=0,return_counts=True)[1]
A=sp.coo_matrix((np.ones(len(u)),(u[:,0],u[:,1])),shape=(len(V),len(V))); ncomp,lab=connected_components(A,directed=False)
used=np.zeros(len(V),bool); used[Q.ravel()]=True
chi=len(V)-len(u)+len(Q)
deg=np.linalg.norm(np.cross(V[Q[:,1]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,0]]),axis=1)
from scipy.spatial import cKDTree
pairs=cKDTree(V).query_pairs(1e-6)
def ang(a,b,c):
    x=a-b; y=c-b; return np.degrees(np.arccos(np.clip((x*y).sum(1)/(np.linalg.norm(x,axis=1)*np.linalg.norm(y,axis=1)+1e-30),-1,1)))
Aq=np.stack([ang(V[Q[:,(i-1)%4]],V[Q[:,i]],V[Q[:,(i+1)%4]]) for i in range(4)],1)
el=np.linalg.norm(V[Q]-V[np.roll(Q,1,1)],axis=2); asp=el.max(1)/np.maximum(el.min(1),1e-30)
R=dict(vertices=len(V),quads=len(Q),quad_pct=100.0,components=int(ncomp),boundary_edges=int((c==1).sum()),nonmanifold_edges=int((c>2).sum()),
       directed_edge_duplicates=int((du>1).sum()),euler=int(chi),genus=(2-chi)/2,unused_vertices=int((~used).sum()),coincident_vertex_pairs_lt_1e6cm=len(pairs),
       degenerate_quads_area_lt_1e8cm2=int((deg<1e-8).sum()),min_edge_mm=float(el.min()*10),
       T4_angles_45_135_pct=float(100*(((Aq>=45)&(Aq<=135)).all(1)).mean()),T4_aspect_le4_pct=float(100*(asp<=4).mean()))
print(json.dumps(R,indent=1))
if len(sys.argv)>2: json.dump(R,open(sys.argv[2],'w'),indent=1)
