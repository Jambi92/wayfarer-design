# pockgen.py IN.npz SPEC.json OUT.npz : replace the star of given cage vertices by a pocket tube that follows a source cavity.
# SPEC: {"remove":[vids], "mouth":[x,y,z], "axis":[ax,ay,az], "up":[ux,uy,uz], "depths":[d0,d1,...], "K":8,
#        "col": c or null (srccol), "tgcol":"col file", "capback":0.1}
# Rings: plane through mouth+axis*d (normal axis), closed source loop nearest the axis point, K arc-length samples starting
# at the extreme along 'up', running towards axis x up.  Patch boundary (link of removed verts) -> ring0 by arc-fraction cells,
# rings joined by quads, last ring capped (K=8: 3 quads; K=6: 2 quads; K=4: 1 quad).
import sys, json, numpy as np
from collections import defaultdict
from scipy.spatial import cKDTree
sys.path.insert(0,'/home/claude/stc/rp1e')
from planeslice import plane_loops
from orient import orient_patch, check
inp,specp,out=sys.argv[1:4]; S=json.load(open(specp))
z=np.load(inp); V=z['V'].astype(float); F=[[int(x) for x in f if x>=0] for f in z['F']]; col=np.load(inp.replace('.npz','_col.npy'))
SRC=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); scol=np.load(S.get('srccolfile','/home/claude/stc/rp1e/col_r2.npy')); kS=cKDTree(SRC)
rem=set(S.get('remove',[]))
patch=[k for k,f in enumerate(F) if any(set(f)==set(q) for q in S['facev'])] if 'facev' in S else S['faces'] if 'faces' in S else [k for k,f in enumerate(F) if set(f)&rem]
# boundary loop of the patch
de=defaultdict(int)
for k in patch:
    f=F[k]
    for i in range(len(f)): de[(f[i],f[(i+1)%len(f)])]+=1
bd=[(a,b) for (a,b) in de if (b,a) not in de]
nxt={a:b for a,b in bd}; assert len(nxt)==len(bd),'boundary not a simple loop'
B=[bd[0][0]]
while True:
    b=nxt[B[-1]]
    if b==B[0]: break
    B.append(b)
assert len(B)==len(bd),('patch boundary has several loops',len(B),len(bd))
assert not (set(B)&rem)
m=np.array(S['mouth'],float); a=np.array(S['axis'],float); a/=np.linalg.norm(a); up=np.array(S['up'],float); up-= (up@a)*a; up/=np.linalg.norm(up); rt=np.cross(a,up)
K=S.get('K',8)
NV=[list(p) for p in V]; NC=list(col)
def add(p,c): NV.append(list(np.asarray(p,float))); NC.append(int(c)); return len(NV)-1
rings=[]
for (dr,rr) in S.get('rims',[]):
    pts=[]
    for k in range(K):
        th=np.pi/2-2*np.pi*k/K   # start at up, run towards rt
        p=m+a*dr+rr*(np.cos(th)*rt+np.sin(th)*up)
        pts.append(SRC[kS.query(p)[1]] if S.get('rimsnap',True) else p)
    cc=S.get('col')
    rings.append([add(p, cc if cc is not None else scol[kS.query(p)[1]]) for p in pts])
for d in S['depths']:
    c=m+a*d
    L=[P for P,cl in plane_loops(c,a) if cl and np.linalg.norm(P-c,axis=1).min()<S.get('rad',2.0)]
    assert L,('no loop at depth',d)
    P=min(L,key=lambda P:np.linalg.norm(P.mean(0)-c))
    if S.get('maxloop') and np.linalg.norm(P-P.mean(0),axis=1).max()>S['maxloop']: raise SystemExit('loop too big at depth %g'%d)
    k0=int(np.argmax(P@up)); P2=np.roll(P,-k0,axis=0)
    xx=(P2-c)@rt; yy=(P2-c)@up; area=0.5*np.sum(xx*np.roll(yy,-1)-np.roll(xx,-1)*yy)
    if area>0: P2=np.vstack([P2[:1],P2[1:][::-1]])
    Q=np.vstack([P2,P2[:1]]); s_=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]
    pts=[]
    for u in np.arange(K)/K*s_[-1]:
        k=int(np.clip(np.searchsorted(s_,u),1,len(s_)-1)); al=(u-s_[k-1])/max(s_[k]-s_[k-1],1e-12); pts.append(Q[k-1]+(Q[k]-Q[k-1])*al)
    cc=S.get('col')
    rings.append([add(p, cc if cc is not None else scol[kS.query(p)[1]]) for p in pts])
# faces
G=[f for k,f in enumerate(F) if k not in set(patch)]; Fn=[]
def frac_arc(l):
    P=np.array([NV[v] for v in l]); Qq=np.vstack([P,P[:1]]); s_=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Qq,axis=0),axis=1))]; return s_[:-1]/s_[-1]
def cells(small,big,fs,fb):
    ms=len(small); n=len(big); dd=lambda x,y: abs(((x-y+0.5)%1.0)-0.5)
    own=[int(np.argmin([dd(fs[i],fb[j]) for i in range(ms)])) for j in range(n)]; Fs=[]
    for j in range(n):
        j2=(j+1)%n; i1,i2=own[j],own[j2]
        if i1==i2: Fs.append([small[i1],big[j],big[j2]])
        else:
            k=i1; steps=(i2-i1)%ms
            if steps==1: Fs.append([small[i1],big[j],big[j2],small[i2]])
            else:
                Fs.append([small[k],big[j],big[j2]])
                while k!=i2: Fs.append([small[k],big[j2],small[(k+1)%ms]]); k=(k+1)%ms
    return Fs
# orient B and ring0 consistently by angle around the axis
def ang(p):
    q=np.asarray(p)-m; return np.arctan2(q@up,q@rt)
def orient(l):
    t=np.unwrap([ang(NV[v]) for v in l+l[:1]]); return l if t[-1]>t[0] else l[::-1]
Bo=orient(B); R0=orient(rings[0])
k0=int(np.argmin([abs(np.angle(np.exp(1j*(ang(NV[v])-ang(NV[R0[0]]))))) for v in Bo])); Bo=Bo[k0:]+Bo[:k0]
if len(Bo)>=len(R0): Fn+=cells(R0,Bo,frac_arc(R0),frac_arc(Bo))
else: Fn+=cells(Bo,R0,frac_arc(Bo),frac_arc(R0))
# ring direction consistency: rings sampled the same way (start up, towards rt)
for r1,r2 in zip(rings[:-1],rings[1:]):
    for i in range(K): Fn.append([r1[i],r1[(i+1)%K],r2[(i+1)%K],r2[i]])
l=rings[-1]
caps={8:([0,1,2,3],[0,3,4,7],[4,5,6,7]),6:([0,1,2,3],[0,3,4,5]),4:([0,1,2,3],)}[K]
for q in caps: Fn.append([l[i] for i in q])
Fn=orient_patch(G,Fn); G+=Fn; dd_,bb=check(G)
if dd_ or bb: raise SystemExit('topology dup %d bnd %d'%(dd_,bb))
used=sorted(set(i for f in G for i in f)); remap={o:n for n,o in enumerate(used)}
V2=np.array([NV[i] for i in used]); G2=[[remap[i] for i in f] for f in G]; C2=np.array([NC[i] for i in used])
Fa=np.full((len(G2),4),-1)
for k,f in enumerate(G2): Fa[k,:len(f)]=f
np.savez_compressed(out,V=V2,F=Fa); np.save(out.replace('.npz','_col.npy'),C2); np.save(out.replace('.npz','_remap.npy'),np.array([remap.get(i,-1) for i in range(len(V))]))
json.dump({'rings':[[remap[v] for v in r] for r in rings],'B':[remap[v] for v in B]},open(out.replace('.npz','_meta.json'),'w'))
print('V',len(V2),'F',len(G2),'B',len(B),'removed',len(rem))
