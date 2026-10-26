# ears.py : ear tube from a rectangular head-grid port; rings = ear sections by planes x = const (arclength sampled)
import numpy as np, sys, trimesh
sys.path.insert(0,'/tmp/claude-0/rt')
from common import *
from cage import unit
from hands import capgrid
EAR_ROWS=(198.0,208.5)          # head stations spanning the port
EAR_COLS={'l':(25,29),'r':(11,15)}
EAR_X=[8.5,9.1,9.7,10.3,10.8]
def crescent(m,x,sg,K,win):
    s=m.section(plane_origin=[sg*x,0,0],plane_normal=[1.0,0,0])
    best=None
    for e in s.discrete:
        c=e.mean(0)
        if not (win[0]<c[2]<win[1] and -5<c[1]<4): continue
        if best is None or len(e)>len(best): best=e
    e=best[:-1] if np.allclose(best[0],best[-1]) else best
    seg=np.linalg.norm(np.diff(np.vstack([e,e[:1]]),axis=0),axis=1); cs=np.r_[0,np.cumsum(seg)]
    lo=np.argmin(e[:,2]); t0=cs[lo]; P_=cs[-1]
    out=[]
    for k in range(K):
        t=(t0+P_*k/K)%P_; i=min(np.searchsorted(cs,t,side='right')-1,len(e)-1); u=(t-cs[i])/max(seg[i],1e-9)
        out.append(e[i]+(e[(i+1)%len(e)]-e[i])*u)
    return np.array(out)
_CACHE={}
SN_=None
import os
def crescent_poly(m,x,sg,win):
    s=m.section(plane_origin=[sg*x,0,0],plane_normal=[1.0,0,0]); best=None
    for e_ in s.discrete:
        c=e_.mean(0)
        if not (win[0]<c[2]<win[1] and -5<c[1]<4): continue
        if best is None or len(e_)>len(best): best=e_
    return best[:-1] if np.allclose(best[0],best[-1]) else best
def fit_ring(E,prevP):
    """sample the closed polyline E at the previous ring's normalised arclength parameters, with the rotation and
    direction that minimise the distance to the previous ring (no twist, spacing inherited)"""
    def cum(P):
        sg_=np.linalg.norm(np.diff(np.vstack([P,P[:1]]),axis=0),axis=1); return np.r_[0,np.cumsum(sg_)]
    sp=cum(prevP); sk=sp[:-1]/sp[-1]; Q=np.vstack([E,E[:1]]); ce=cum(E); L_=ce[-1]
    def ev(t):
        t=(t%1.0)*L_; i=np.clip(np.searchsorted(ce,t,side='right')-1,0,len(E)-1); seg=np.maximum(ce[i+1]-ce[i],1e-12); u=(t-ce[i])/seg
        return Q[i]+(Q[i+1]-Q[i])*u[:,None]
    best=None
    for d in (1,-1):
        for ph in np.linspace(0,1,720,endpoint=False):
            P=ev(ph+d*sk); c=np.linalg.norm(P-prevP,axis=1).sum()
            if best is None or c<best[0]: best=(c,P)
    return best[1]
def build_ear(C,rings,rowidx,s,full_mesh):
    sg=1 if s=='l' else -1; c0,c1=EAR_COLS[s]; r0,r1=rowidx
    a=c1-c0; b=r1-r0; K=2*(a+b)
    loop=[rings[r0][k] for k in range(c0,c1)]+[rings[i][c1] for i in range(r0,r1)]+[rings[r1][k] for k in range(c1,c0,-1)]+[rings[i][c0] for i in range(r1,r0,-1)]
    keys=[(r0,k) for k in range(c0,c1)]+[(i,c1) for i in range(r0,r1)]+[(r1,k) for k in range(c1,c0,-1)]+[(i,c0) for i in range(r1,r0,-1)]
    assert len(set(loop))==K
    C.tag('ear_root_'+s,loop)
    prev=loop; prevP=np.array([C.V[i] for i in loop])
    KT_=len(rings[0]); mir=lambda p: np.array([-p[0],p[1],p[2]])
    if s=='r' and 'l' in _CACHE and os.environ.get('EARMIR','0')=='1':
        # right ear: mirror of the authored left-ear rings (same topology), snapped to the right-ear source surface
        Lk,LR=_CACHE['l']; pos={kk:i for i,kk in enumerate(Lk)}
        perm=[pos[(i,(KT_-k)%KT_)] for (i,k) in keys]
        import igl as _igl
        _ear=SN_.sub(['ear_r'])
        for PL in LR:
            P=np.array([mir(PL[j]) for j in perm])
            _,_,P=_igl.point_mesh_squared_distance(P,SN_.V,_ear.faces)
            cur=C.add(P); C.strip(prev,cur,'ear_'+s); prev=cur; prevP=P
    else:
      LR=[]
      for x in (EAR_X if s=='l' else [float(v) for v in os.environ.get('EARXR','8.5,9.1,9.7,10.3,10.8').split(',')]):
        P=crescent(full_mesh,x,sg,K,(195,212))
        best=None
        for d in (1,-1):
            for sh in range(K):
                idx=[(sh+d*k)%K for k in range(K)]
                cost=np.linalg.norm(prevP-P[idx],axis=1).sum()
                if best is None or cost<best[0]: best=(cost,idx)
        P=P[best[1]]; LR.append(P)
        cur=C.add(P); C.strip(prev,cur,'ear_'+s); prev=cur; prevP=P
      _CACHE[s]=(keys,LR)
    tip=prevP.mean(0)+np.array([sg*0.4,0,0])
    # rotate the rim ring so the 2 x (K/2-2) cap grid runs ALONG the crescent (short rungs across it) -> no crossing grid lines
    Pr=np.array([C.V[i] for i in prev]); Cc=K//2-2
    sh=min(range(K),key=lambda h: sum(np.linalg.norm(Pr[(h+j)%K]-Pr[(h+2*Cc+2-j)%K]) for j in range(Cc+1)))
    ring=[prev[(sh+j)%K] for j in range(K)]
    capgrid(C,ring,2,Cc,'ear_'+s,tip,pull=0.0,push=np.array([sg*0.12,0,0]))   # crescent rim: no centroid pull
    return K
