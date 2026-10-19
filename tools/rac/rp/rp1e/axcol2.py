"""Axilla pocket ownership by wall orientation (design only).
In each axilla pocket box, a source vertex with a close (< GAP cm) opposite-facing surface across the gap is a contact-wall vertex;
it becomes arm (2) if its normal points medially (toward the trunk), trunk (1) if laterally. Labels are then cleaned by
majority over the vertex 1-ring (3 passes). Usage: python3 axcol2.py COL_IN COL_OUT [GAP]"""
import numpy as np, sys
from scipy.spatial import cKDTree
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F'].astype(np.int64)
col=np.load(sys.argv[1]).copy(); GAP=float(sys.argv[3]) if len(sys.argv)>3 else 1.5
fn=np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]]); fn/=np.linalg.norm(fn,axis=1,keepdims=True)+1e-12
vn=np.zeros_like(V); 
for k in range(3): np.add.at(vn,F[:,k],fn)
vn/=np.linalg.norm(vn,axis=1,keepdims=True)+1e-12
E=np.unique(np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1),axis=0)
for s,sg in (('R',-1),('L',1)):
    box=(V[:,0]*sg>13)&(V[:,0]*sg<27)&(V[:,2]>126)&(V[:,2]<160)&(V[:,1]>-50)&(V[:,1]<-14)&((col==1)|(col==2))
    idx=np.where(box)[0]; X=V[idx]; N=vn[idx]; T=cKDTree(X)
    # opposite-facing neighbour within GAP along -normal direction
    pairs=T.query_ball_point(X,GAP); wall=np.zeros(len(idx),bool)
    for a,nb in enumerate(pairs):
        nb=np.array(nb)
        if len(nb)<2: continue
        d=X[nb]-X[a]; along=d@N[a]
        ok=(N[nb]@N[a]<-0.3)&(along>0.02)   # facing us, in front of our surface (outside the body)
        wall[a]=ok.any()
    medial=(N[:,0]*(-sg))>0.0   # R arm (x<0) medial normal points +x
    lab=np.where(medial,2,1)
    sel=idx[wall]; col_new=col.copy(); col_new[sel]=lab[wall]
    # cleanup majority on 1-ring restricted to box
    nbr={}
    m=box[E[:,0]]&box[E[:,1]]
    for a,b in E[m]: nbr.setdefault(a,[]).append(b); nbr.setdefault(b,[]).append(a)
    for it in range(3):
        c2=col_new.copy()
        for v in sel:
            ns=nbr.get(v,[])
            if ns: c2[v]=np.bincount(col_new[ns],minlength=3)[1:3].argmax()+1
        col_new=c2
    print(s,'pocket wall verts',wall.sum(),'-> arm',(col_new[sel]==2).sum(),'trunk',(col_new[sel]==1).sum(),'changed vs in',(col_new[sel]!=col[sel]).sum())
    col=col_new
np.save(sys.argv[2],col); print(np.bincount(col))
