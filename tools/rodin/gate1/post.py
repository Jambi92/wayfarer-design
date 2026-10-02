# Seam fairing: Laplacian relaxation in a narrow band around the zip seam, plus crease relaxation on the donor tail.
import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.csgraph import dijkstra
z=np.load("g1_body_raw.npz"); V=z["V"].copy(); F=z["F"]; seam=z["seam"]; nA=int(z["nA"])
V0=V.copy()
E=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); w=np.linalg.norm(V[E[:,0]]-V[E[:,1]],axis=1)
G=coo_matrix((w,(E[:,0],E[:,1])),shape=(len(V),)*2).tocsr(); G=G.maximum(G.T)
A=coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(len(V),)*2).tocsr(); A=((A+A.T)>0).astype(float)
deg=np.asarray(A.sum(1)).ravel(); L=diags(1/np.maximum(deg,1))@A
def relax(sel_w,it,lam=0.5):
    global V
    for _ in range(it):
        Vn=L@V; V=V+(lam*sel_w)[:,None]*(Vn-V)
BAND=2.5
d=dijkstra(G,indices=seam,min_only=True,limit=BAND+0.5)
wb=np.where(np.isfinite(d),np.clip(1-d/BAND,0,1),0.0)
relax(wb,30)
# donor-tail crease rings: high dihedral angle edges on the tail (F < -36)
fn=np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]]); fn/=np.linalg.norm(fn,axis=1,keepdims=True)+1e-12
key=np.sort(E,1); fid=np.tile(np.arange(len(F)),3); o=np.lexsort((key[:,1],key[:,0])); ks=key[o]; fs=fid[o]
same=(ks[1:]==ks[:-1]).all(1); i=np.where(same)[0]
ang=np.degrees(np.arccos(np.clip((fn[fs[i]]*fn[fs[i+1]]).sum(1),-1,1)))
cre=np.unique(ks[i][ang>18].ravel()); cre=cre[V[cre,1]<-36]
dc=dijkstra(G,indices=cre,min_only=True,limit=2.0) if len(cre) else np.full(len(V),np.inf)
wc=np.where(np.isfinite(dc),np.clip(1-dc/1.5,0,1),0.0); wc[V[:,1]>=-36]=0
relax(wc,20)
# donor tail: Taubin relaxation (volume-preserving) to dissolve B2's transverse crease rings; fades in from the junction
wt=np.clip((-V0[:,1]-40.0)/6.0,0,1); wt[:nA]=0
for _ in range(40):
    V=V+(0.5*wt)[:,None]*((L@V)-V); V=V+(-0.53*wt)[:,None]*((L@V)-V)
mv=np.linalg.norm(V-V0,axis=1)
print("seam band verts",(wb>0).sum(),"tail crease verts",(wc>0).sum(),"max move %.2f cm"%mv.max())
pres=np.arange(nA); print("preserved-B1 verts moved > 0.01 cm:",(mv[pres]>0.01).sum(),"of",nA,"; max %.2f cm, max seam distance of a moved one %.2f cm"%(mv[pres].max(),np.nanmax(np.where(mv[pres]>0.01,d[pres],np.nan))))
np.savez("g1_body.npz",V=V,F=F,nA=nA,moved=mv)
