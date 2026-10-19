# tailcol.py COL_IN COL_OUT : source tail colour 16 = trunk-colour component on the tail side of the junction ring J (cut 0.25 cm around J)
import numpy as np, sys
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V']; F=w['F']
c=np.load(sys.argv[1]).copy(); J=np.load('tailJ.npz')['J']
# dense J polyline
Q=np.vstack([J,J[:1]]); D=[]
for a,b in zip(Q[:-1],Q[1:]):
    n=int(np.ceil(np.linalg.norm(b-a)/0.05))+1
    for t in np.linspace(0,1,n): D.append(a+(b-a)*t)
D=np.array(D); d,_=cKDTree(D).query(S); cut=d<float(__import__("os").environ.get("CUT","0.35"))
m=(c==1)&~cut
E=np.vstack([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); e=E[m[E[:,0]]&m[E[:,1]]]
A=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(S),len(S))); n,lab=connected_components(A,directed=False)
tip=np.where(m&(S[:,1]>10))[0]; tl=np.bincount(lab[tip]).argmax()
tail=m&(lab==tl); print('tail verts',tail.sum(),'trunk',m.sum())
c[tail]=16
# cut verts: assign by nearest non-cut neighbour side (tail if closer to tail verts)
idx=np.where(cut&(c==1))[0]
dt,_=cKDTree(S[tail]).query(S[idx]); db,_=cKDTree(S[(c==1)&~cut]).query(S[idx])
c[idx[dt<db]]=16
np.save(sys.argv[2],c); print('tail total',(c==16).sum())
