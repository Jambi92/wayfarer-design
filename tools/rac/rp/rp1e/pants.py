# pants.py IN.npz SPEC.json OUT.npz : merge two tube ends (B leg ring, C leg ring) into one tube through a shared crease chain
# (manifold slit-tip termination, ruling 4.2), then blob rings from source sections and a cap.
# SPEC: {"Bring":[12], "Bnext":[ids of a ring beyond], "Cring":[12], "Cnext":[...], "b_in":[5 ring positions], "c_in":[5 ring positions],
#        "crease":[[x,y,z]x5 bottom->top], "Msec":x, "Msplit":y, "rings":[x,...], "n":16}
import sys, json, numpy as np
from collections import deque
from scipy.spatial import cKDTree
sys.path.insert(0,'/home/claude/stc/rp1e')
from planeslice import plane_loops
from orient import orient_patch, check
inp,specp,out=sys.argv[1:4]; S=json.load(open(specp))
z=np.load(inp); V=z['V'].astype(float); F=[[int(x) for x in f if x>=0] for f in z['F']]; col=np.load(inp.replace('.npz','_col.npy'))
SRC=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); scol=np.load('/home/claude/stc/rp1e/col_r3.npy'); kS=cKDTree(SRC)
adj=[set() for _ in range(len(V))]
for f in F:
    for i in range(len(f)): adj[f[i]].add(f[(i+1)%len(f)]); adj[f[i]].add(f[i-1])
def beyond(ring,nxt):
    rs=set(ring); seen=set(nxt); dq=deque(nxt)
    while dq:
        v=dq.popleft()
        for u in adj[v]:
            if u in rs or u in seen: continue
            seen.add(u); dq.append(u)
    return seen
Bb=beyond(S['Bring'],S['Bnext']); Cb=beyond(S['Cring'],S['Cnext']); assert not (Bb&Cb),'B and C beyond-regions touch'
assert len(Bb)<2000 and len(Cb)<2000,('beyond region too large',len(Bb),len(Cb))
rem=Bb|Cb; G=[f for f in F if not (set(f)&rem)]
NV=[list(p) for p in V]; NC=list(col)
def add(p,c=None): NV.append(list(np.asarray(p,float))); NC.append(int(c) if c is not None else int(scol[kS.query(p)[1]])); return len(NV)-1
b=S['Bring']; c=S['Cring']; n=len(b)
Fn0=[]
def legext(r,xe,side):
    R0=np.array([NV[v] for v in r]); c0=R0.mean(0); u,sv,vt=np.linalg.svd(R0-c0); nrm=vt[2]
    tc=np.mean(S['crease'],axis=0)
    if (tc-c0)@nrm<0: nrm=-nrm
    p0=c0+nrm*xe
    loops=[P for P,cl in plane_loops(p0,nrm) if cl]
    loops=[P for P in loops if np.linalg.norm(P.mean(0)-p0)<3]
    P=min(loops,key=lambda P:np.linalg.norm(P.mean(0)-p0))
    Q=np.vstack([P,P[:1]]); s_=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]
    pts=np.array([Q[int(np.clip(np.searchsorted(s_,u),1,len(Q)-1))] for u in np.arange(n)/n*s_[-1]])
    last=np.array([NV[v] for v in r]); best=None
    for flip in (False,True):
        R_=pts[::-1] if flip else pts
        for sh in range(n):
            Rr=np.roll(R_,-sh,axis=0); cst=np.sum(np.linalg.norm((Rr-Rr.mean(0))-(last-last.mean(0)),axis=1))
            if best is None or cst<best[0]: best=(cst,Rr)
    nr=[add(p,NC[r[0]]) for p in best[1]]
    for i in range(n): Fn0.append([r[i],r[(i+1)%n],nr[(i+1)%n],nr[i]])
    return nr
for xe in S.get('legext',[]):
    b=legext(b,xe,-1); c=legext(c,xe,1)

def pos(r,i): return r[i%len(r)]
bi=S['b_in']; ci=S['c_in']   # ring positions, inner arcs bottom->top
t=[add(p) for p in S['crease']]
Fn=list(Fn0)
for k in range(4):
    Fn.append([b[bi[k]%n],b[bi[k+1]%n],t[k+1],t[k]]); Fn.append([c[ci[k]%n],c[ci[k+1]%n],t[k+1],t[k]])
# outer arcs: B continues forward from b_in[-1] (top) around to b_in[0] (bottom); C goes the other way
def outer(r,inn):
    top,bot=inn[-1],inn[0]; step=1 if (inn[1]-inn[0])%len(r)==1 else -1
    arc=[]; k=top
    while True:
        k=(k+step)%len(r); arc.append(k)
        if k==bot: break
    return arc   # ends with bot
bo=outer(b,bi); co=outer(c,ci); assert len(bo)==8 and len(co)==8,(len(bo),len(co))
# M ring from the source section at Msec, split at y=Msplit into B side and C side, 7 samples each (top->bottom, excluding ends)
x0=S['Msec']; loops=[P for P,cl in plane_loops(np.array([x0,S['Msplit'],93.0]),np.array([1.0,0,0])) if cl]
P=min(loops,key=lambda P:np.linalg.norm(P.mean(0)-np.array([x0,S['Msplit'],93.0])))
def side_samples(P,sgn,m):
    # points of the loop on one side of y=Msplit, ordered from the top crossing to the bottom crossing
    ys=P[:,1]-S['Msplit']; ins=(sgn*ys>0)
    # rotate so the run of 'ins' is contiguous
    k0=np.where(~ins)[0][0]; Pr=np.roll(P,-k0,axis=0); ir=np.roll(ins,-k0)
    idx=np.where(ir)[0]; seg=Pr[idx[0]:idx[-1]+1]
    if seg[0,2]<seg[-1,2]: seg=seg[::-1]   # start at top
    s=np.r_[0,np.cumsum(np.linalg.norm(np.diff(seg,axis=0),axis=1))]
    return [seg[int(np.clip(np.searchsorted(s,u),0,len(seg)-1))] for u in np.linspace(0,s[-1],m+2)[1:-1]]
Bp=[add(p,NC[b[0]]) for p in side_samples(P,-1,7)]; Cp=[add(p,NC[c[0]]) for p in side_samples(P,1,7)]
bseq=[b[k] for k in [bi[-1]]+bo]; tgtB=[t[4]]+Bp+[t[0]]
for k in range(8): Fn.append([bseq[k],bseq[k+1],tgtB[k+1],tgtB[k]])
cseq=[c[k] for k in [ci[-1]]+co]; tgtC=[t[4]]+Cp+[t[0]]
for k in range(8): Fn.append([cseq[k],cseq[k+1],tgtC[k+1],tgtC[k]])
M=[t[4]]+Bp+[t[0]]+Cp[::-1]; N=len(M)
prev=M
for xr in S['rings']:
    loops=[P for P,cl in plane_loops(np.array([xr,S['Msplit'],93.0]),np.array([1.0,0,0])) if cl]
    P=min(loops,key=lambda P:np.linalg.norm(P.mean(0)-np.array([xr,S['Msplit'],93.0])))
    Q=np.vstack([P,P[:1]]); s=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]
    pts=np.array([Q[int(np.clip(np.searchsorted(s,u),1,len(Q)-1))] for u in np.arange(N)/N*s[-1]])
    last=np.array([NV[v] for v in prev]); best=None
    for flip in (False,True):
        R=pts[::-1] if flip else pts
        for sh in range(N):
            Rr=np.roll(R,-sh,axis=0); cst=np.sum(np.linalg.norm((Rr-Rr.mean(0))-(last-last.mean(0)),axis=1))
            if best is None or cst<best[0]: best=(cst,Rr)
    ring=[add(p) for p in best[1]]
    for i in range(N): Fn.append([prev[i],prev[(i+1)%N],ring[(i+1)%N],ring[i]])
    prev=ring
# cap: 16 -> 8 reduction ring pulled toward the source tip, then an 8-gon strip cap
l=prev; Pl=np.array([NV[v] for v in l]); cl=Pl.mean(0); TD=np.array([1.0,0,0])
idx=kS.query_ball_point(cl,2.0); Qs=SRC[idx]; hw=np.linalg.norm(Pl-cl,axis=1).max()
Qs=Qs[((Qs-cl)@TD>0)&(np.linalg.norm((Qs-cl)-np.outer((Qs-cl)@TD,TD),axis=1)<0.6*hw)]
tipP=Qs[np.argmax(Qs@TD)] if len(Qs) else cl+TD*0.4
dep=(tipP-cl)@TD
m=[add(cl+(Pl[(2*k+1)%N]-cl)*S.get('capshrink',0.55)+TD*dep*S.get('capfwd',0.6)) for k in range(N//2)]
h=N//2
for k in range(h):
    Fn.append([l[2*k],l[(2*k+1)%N],m[k]]); Fn.append([l[(2*k+1)%N],l[(2*k+2)%N],m[(k+1)%h],m[k]])
for k in range(h//2-1):
    Fn.append([m[k],m[k+1],m[h-2-k],m[(h-1-k)%h]] if k>0 else [m[0],m[1],m[h-2],m[h-1]])
Fn=[f for f in Fn]
Fn=orient_patch(G,Fn); G+=Fn; dd,bb=check(G)
if dd or bb: raise SystemExit('topology dup %d bnd %d'%(dd,bb))
used=sorted(set(i for f in G for i in f)); remap={o:k for k,o in enumerate(used)}
V2=np.array([NV[i] for i in used]); G2=[[remap[i] for i in f] for f in G]; C2=np.array([NC[i] for i in used])
Fa=np.full((len(G2),4),-1)
for k,f in enumerate(G2): Fa[k,:len(f)]=f
np.savez_compressed(out,V=V2,F=Fa); np.save(out.replace('.npz','_col.npy'),C2); np.save(out.replace('.npz','_remap.npy'),np.array([remap.get(i,-1) for i in range(len(V))]))
json.dump({'crease':[remap[v] for v in t],'M':[remap[v] for v in M]},open(out.replace('.npz','_meta.json'),'w'))
print('V',len(V2),'F',len(G2),'removed verts',len(rem))
