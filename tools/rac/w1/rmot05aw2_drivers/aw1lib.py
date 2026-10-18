# 05AW1 cloud planning library on the welded-nail topology (diagnostics only)
import numpy as np, sys, scipy.sparse as sp
sys.path.insert(0,'/home/claude/aw'); sys.path.insert(0,'/home/claude/av')
import nails2 as N2
from avlib import ss
Vold=np.load('/home/claude/av/real/final.npz')['V']
import os
from scipy.spatial import cKDTree
D=np.load(os.environ.get('AW1_TOPO','/home/claude/aw1/sim_weld_VF.npz')); V0=D['V']; F=D['F']
_dist,new2old=cKDTree(Vold).query(V0); isnew=_dist>1e-7
if not os.environ.get('AW1_ALLOWNEW'): assert not isnew.any()
_kn,_in=np.unique(np.round(V0,7),axis=0,return_inverse=True); wid=_in.ravel()
dup_left=np.bincount(wid)[wid]>1         # still-duplicated (unmerged) vertices
def frames():
    out={}
    for n in N2.NAILS:
        fr=N2.nail_frame(Vold,n); fr['fm']=fr['fm'][new2old]; out[n]=fr
    return out
FR=frames()
def adjacency(F,n):
    E=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); A=sp.coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(n,n)).tocsr()
    A=((A+A.T)>0).astype(float); deg=np.asarray(A.sum(1)).ravel(); return sp.diags(1/np.maximum(deg,1))@A
Avg=adjacency(F,len(V0))
def vnormals(X):
    fn=np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]]); v=np.zeros_like(X)
    for i in range(3): np.add.at(v,F[:,i],fn)
    return v/np.maximum(np.linalg.norm(v,axis=1),1e-30)[:,None]
def smooth(X,M,n):
    fade=(1-M)[:,None]
    for _ in range(n): X=X+(Avg@X-X)*fade
    return X
def inflate(X,M,c): return X+vnormals(X)*(c*(1-M))[:,None]
def nail_coords(X,n):
    fr=FR[n]; Dd=X-fr['Pp']; return (Dd@fr['e'])/fr['L'], Dd@fr['lat'], Dd@fr['n'], fr
def plate_weight(X,n,s0=-0.15,s1=1.15,xw=0.55,ramp_s=0.12,ramp_x=0.25,depth=0.008):
    s,x,d,fr=nail_coords(X,n); W=fr['W']
    gs=ss((s-s0)/ramp_s)*(1-ss((s-s1)/ramp_s))
    gx=1-ss((np.abs(x)-xw*W)/(ramp_x*W))
    gd=ss((d+depth)/0.003)
    w=gs*gx*gd; w[~fr['fm']]=0; return w
from scipy.sparse.csgraph import dijkstra
_E=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]])
_Ew=np.linalg.norm(V0[_E[:,0]]-V0[_E[:,1]],axis=1)
G=sp.coo_matrix((_Ew,(_E[:,0],_E[:,1])),shape=(len(V0),)*2).tocsr(); G=G.maximum(G.T)
def nearest(p,mask=None):
    d=np.linalg.norm(V0-p,axis=1)
    if mask is not None: d[~mask]=1e9
    return int(np.argmin(d))
def geo(src,limit=0.06): return dijkstra(G,directed=False,indices=[src],limit=limit)[0]
def ellipse_weight(n,margin=0.0035,ramp=0.003,limit=0.06,scap=1.1):
    fr=FR[n]; a=nearest(fr['Pp'],fr['fm']); b=nearest(fr['Pd'],fr['fm'])
    da=geo(a,limit); db=geo(b,limit); Lg=da[b]
    t=(da+db)-(Lg+2*margin)
    w=1-ss(t/ramp); w[~np.isfinite(t)]=0
    sn=((V0-fr['Pp'])@fr['e'])/fr['L']; w*=1-ss((sn-scap)/0.15)
    return w,da,db,Lg
def relax(X,M,n):
    fade=(1-M)[:,None]
    for _ in range(n):
        nv=vnormals(X); d=Avg@X-X; d-=(d*nv).sum(1)[:,None]*nv; X=X+d*fade
    return X
def hc_smooth(X,M,n,alpha=0.5,beta=0.5,O=None):
    """HC (Vollmer) shape-preserving Laplacian, Blender Surface-Smooth style; alpha = weight of ORIGINAL position"""
    fade=(1-M)[:,None]; O=X.copy() if O is None else O
    for _ in range(n):
        P=Avg@X; B=P-(alpha*O+(1-alpha)*X); Q=P-(beta*B+(1-beta)*(Avg@B)); X=X+(Q-X)*fade
    return X
_deg=np.bincount(F.ravel(),minlength=len(V0))
_v3=(_deg==3)
_A=(Avg>0).astype(float)
v3pin=_v3|((_A@_v3.astype(float))>0)      # valence-3 vertices and their 1-ring (kept fixed by all masks)
