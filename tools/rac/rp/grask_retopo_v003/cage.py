# cage.py : authored quad cage for the RP2 Grask production retopology (analysis frame, cm)
# Structure: axial tube (torso -> neck -> head, crown grid cap); legs from a crotch split; arms through rectangular
# ports in the torso side; hands = palm tube with finger ports in the distal cap grid and a thumb port on the radial
# side; feet = leg tube bent into the foot with toe ports in the distal cap grid; face rings by inset; ears by ports.
import numpy as np, json, sys
sys.path.insert(0,'/tmp/claude-0/rt')
from common import *
class Cage:
    def __init__(s): s.V=[]; s.F=[]; s.FP=[]; s.tags={}   # face part labels; named authored edge loops
    def tag(s,name,ids): s.tags[name]=[int(i) for i in ids]
    def add(s,P):
        i=len(s.V); s.V+=[np.asarray(p,float) for p in P]; return list(range(i,i+len(P)))
    def quad(s,a,b,c,d,part): s.F.append([a,b,c,d]); s.FP.append(part)
    def strip(s,r1,r2,part,closed=True):
        n=len(r1); assert n==len(r2),(n,len(r2))
        for k in range(n if closed else n-1):
            k2=(k+1)%n; s.quad(r1[k],r1[k2],r2[k2],r2[k],part)
    def arrays(s): return np.array(s.V),np.array(s.F),np.array(s.FP)
def unit(v): v=np.asarray(v,float); return v/np.linalg.norm(v)
def angles_uniform(K,off=0.0): return off+2*np.pi*np.arange(K)/K
def fill_misses(P,ok,c):
    """replace missed ray points by angular interpolation of radius"""
    if ok.all(): return P
    K=len(P); idx=np.nonzero(ok)[0]
    if len(idx)==0: return P
    r=np.linalg.norm(P-c,axis=1)
    for i in np.nonzero(~ok)[0]:
        # nearest valid neighbours on both sides
        d=(idx-i)%K; j1=idx[np.argmin(d)]; d2=(i-idx)%K; j0=idx[np.argmin(d2)]
        t=((i-j0)%K)/max(((j1-j0)%K),1)
        u0=(P[j0]-c)/max(r[j0],1e-9); u1=(P[j1]-c)/max(r[j1],1e-9)
        u=unit(u0*(1-t)+u1*t); P[i]=c+u*(r[j0]*(1-t)+r[j1]*t)
    return P
def grid_cap(ring,rows,cols,interior_fn):
    """ring: list of 2*(rows+cols) vertex ids around a rows x cols quad grid boundary, starting at corner (0,0) going along
    the first row (cols edges), then down the last column, back along the last row, up the first column.
    returns grid index array G[(rows+1),(cols+1)] with boundary ids filled and interior ids from interior_fn(i,j)."""
    R,C=rows,cols; G=-np.ones((R+1,C+1),int); k=0
    for j in range(C): G[0,j]=ring[k]; k+=1
    for i in range(R): G[i,C]=ring[k]; k+=1
    for j in range(C,0,-1): G[R,j]=ring[k]; k+=1
    for i in range(R,0,-1): G[i,0]=ring[k]; k+=1
    for i in range(1,R):
        for j in range(1,C): G[i,j]=interior_fn(i,j,G)
    return G
def fix_quad_winding(Q):
    """make winding consistent (BFS over shared edges), then outward by signed volume (caller checks)."""
    import collections
    Q=Q.copy(); nF=len(Q)
    emap=collections.defaultdict(list)
    for fi,q in enumerate(Q):
        for k in range(4): a,b=q[k],q[(k+1)%4]; emap[(min(a,b),max(a,b))].append(fi)
    seen=np.zeros(nF,bool)
    for start in range(nF):
        if seen[start]: continue
        seen[start]=True; dq=collections.deque([start])
        while dq:
            f=dq.popleft(); q=Q[f]
            for k in range(4):
                a,b=q[k],q[(k+1)%4]
                for g in emap[(min(a,b),max(a,b))]:
                    if g==f or seen[g]: continue
                    r=Q[g]; 
                    # same directed edge in g means inconsistent -> flip g
                    same=any(r[j]==a and r[(j+1)%4]==b for j in range(4))
                    if same: Q[g]=r[::-1]
                    seen[g]=True; dq.append(g)
    return Q
def signed_volume(V,Q):
    T=np.concatenate([Q[:,[0,1,2]],Q[:,[0,2,3]]]); a,b,c=V[T[:,0]],V[T[:,1]],V[T[:,2]]
    return np.einsum('ij,ij->i',a,np.cross(b,c)).sum()/6

def loop_dir(q,a,b):
    """+1 if the loop q (points relative to centre) runs counter-clockwise in the (a,b) plane, else -1 (signed area)"""
    x=q@a; y=q@b; A=(x*np.roll(y,-1)-np.roll(x,-1)*y).sum()
    return 1.0 if A>=0 else -1.0
def arc_resample(P,w=1.0):
    """closed ring P -> K points equally spaced in arclength starting at P[0]; blended with the input by w"""
    K=len(P); Q=np.vstack([P,P[:1]]); seg=np.linalg.norm(np.diff(Q,axis=0),axis=1); cs=np.r_[0,np.cumsum(seg)]
    t=cs[-1]*np.arange(K)/K; out=np.zeros_like(P)
    for k,tk in enumerate(t):
        i=min(np.searchsorted(cs,tk,side='right')-1,K-1); u=(tk-cs[i])/max(seg[i],1e-12); out[k]=Q[i]+(Q[i+1]-Q[i])*u
    return (1-w)*P+w*out
def arc_resample_phase(P,w=1.0):
    """move ring points along the ring polygon toward equal arclength spacing, with the phase (rotation) chosen to
    minimise the movement (no twist); w=1 fully uniform"""
    K=len(P); Q=np.vstack([P,P[:1]]); seg=np.linalg.norm(np.diff(Q,axis=0),axis=1); cs=np.r_[0,np.cumsum(seg)]; Lt=cs[-1]
    s=cs[:-1]/Lt; k=np.arange(K)/K
    ph=np.angle(np.mean(np.exp(2j*np.pi*(s-k))))/(2*np.pi)
    d=((k+ph)-s+0.5)%1.0-0.5; t=((s+w*d)%1.0)*Lt
    out=np.zeros_like(P)
    for i,tk in enumerate(t):
        j=min(np.searchsorted(cs,tk,side='right')-1,K-1); u=(tk-cs[j])/max(seg[j],1e-12); out[i]=Q[j]+(Q[j+1]-Q[j])*u
    return out
