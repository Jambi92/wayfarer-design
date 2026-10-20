# junction.py IN.npz SPEC.json OUT.npz : join a tube end ring to the side of another tube (creates a handle when both tubes are connected elsewhere).
# SPEC: {"ring":[ids],"prev":[ids],"target_faces":[[vids],...] (disk on the other tube), "mid":0.5 (optional intermediate ring blend 0..1, snapped), "nmid":0}
import sys, json, numpy as np
from collections import defaultdict
from scipy.spatial import cKDTree
sys.path.insert(0,'/home/claude/stc/rp1e')
from orient import orient_patch, check
inp,specp,out=sys.argv[1:4]; S=json.load(open(specp))
z=np.load(inp); V=z['V'].astype(float); F=[[int(x) for x in f if x>=0] for f in z['F']]; col=np.load(inp.replace('.npz','_col.npy'))
SRC=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); kS=cKDTree(SRC)
ring=S['ring']; rs=set(ring); prev=set(S['prev'])
cand=[k for k,f in enumerate(F) if set(f)&rs and not set(f)<=(rs|prev)]
capv=set(v for k in cand for v in F[k])-rs
capf=set(k for k,f in enumerate(F) if k in cand or set(f)&capv)
tf=[k for k,f in enumerate(F) if any(set(f)==set(q) for q in S['target_faces'])]
assert len(tf)==len(S['target_faces']),('target faces not found',len(tf))
de=defaultdict(int)
for k in tf:
    f=F[k]
    for i in range(len(f)): de[(f[i],f[(i+1)%len(f)])]+=1
bd=[(a,b) for (a,b) in de if (b,a) not in de]; nxt={a:b for a,b in bd}; assert len(nxt)==len(bd)
B=[bd[0][0]]
while nxt[B[-1]]!=B[0]: B.append(nxt[B[-1]])
assert len(B)==len(bd),'target disk boundary not one loop'
interior=set(v for k in tf for v in F[k])-set(B)
NV=[list(p) for p in V]; NC=list(col)
def add(p,c): NV.append(list(p)); NC.append(int(c)); return len(NV)-1
cR=V[ring].mean(0); cB=V[B].mean(0); ax=cB-cR; ax/=np.linalg.norm(ax)
up=np.cross(ax,[0,0,1.0]); up=up if np.linalg.norm(up)>0.2 else np.cross(ax,[1.0,0,0]); up/=np.linalg.norm(up); rt=np.cross(ax,up)
def ang(p,c): q=np.asarray(p)-c; return np.arctan2(q@up,q@rt)
def orient(l,c):
    t=np.unwrap([ang(NV[v],c) for v in l+l[:1]]); return l if t[-1]>t[0] else l[::-1]
R0=orient(list(ring),cR); B0=orient(B,cB)
rings=[R0]
for t in S.get('mids',[]):
    # intermediate ring: blend ring and target loop by arc fraction, snap to source
    fr=lambda l: (lambda P: (lambda s: s[:-1]/s[-1])(np.r_[0,np.cumsum(np.linalg.norm(np.diff(np.vstack([P,P[:1]]),axis=0),axis=1))]))(np.array([NV[v] for v in l]))
    fb=fr(B0); fa=fr(R0); k0=int(np.argmin([abs(np.angle(np.exp(1j*(ang(NV[v],cB)-ang(NV[R0[0]],cR))))) for v in B0])); Bs=B0[k0:]+B0[:k0]; fb=fr(Bs)
    pts=[]
    for i,v in enumerate(R0):
        j=int(np.argmin([abs(((fa[i]-x+0.5)%1)-0.5) for x in fb])); p=(1-t)*np.array(NV[v])+t*np.array(NV[Bs[j]])
        pts.append(SRC[kS.query(p)[1]] if S.get('snap',True) else p)
    rings.append([add(p,NC[ring[0]]) for p in pts])
G=[f for k,f in enumerate(F) if k not in capf and k not in set(tf)]; Fn=[]
n=len(ring)
for a,b in zip(rings[:-1],rings[1:]):
    for i in range(n): Fn.append([a[i],a[(i+1)%n],b[(i+1)%n],b[i]])
def frac_arc(l):
    P=np.array([NV[v] for v in l]); Q=np.vstack([P,P[:1]]); s=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]; return s[:-1]/s[-1]
def cells(small,big,fs,fb):
    ms=len(small); nb=len(big); dd=lambda x,y: abs(((x-y+0.5)%1.0)-0.5)
    own=[int(np.argmin([dd(fs[i],fb[j]) for i in range(ms)])) for j in range(nb)]; Fs=[]
    for j in range(nb):
        j2=(j+1)%nb; i1,i2=own[j],own[j2]
        if i1==i2: Fs.append([small[i1],big[j],big[j2]])
        else:
            k=i1; steps=(i2-i1)%ms
            if steps==1: Fs.append([small[i1],big[j],big[j2],small[i2]])
            else:
                Fs.append([small[k],big[j],big[j2]])
                while k!=i2: Fs.append([small[k],big[j2],small[(k+1)%ms]]); k=(k+1)%ms
    return Fs
L=rings[-1]; cL=np.mean([NV[v] for v in L],axis=0)
k0=int(np.argmin([abs(np.angle(np.exp(1j*(ang(NV[v],cB)-ang(NV[L[0]],cL))))) for v in B0])); Bo=B0[k0:]+B0[:k0]
Fn+= cells(L,Bo,frac_arc(L),frac_arc(Bo)) if len(Bo)>=len(L) else cells(Bo,L,frac_arc(Bo),frac_arc(L))
Fn=orient_patch(G,Fn); G+=Fn; dd_,bb=check(G)
if dd_ or bb: raise SystemExit('topology dup %d bnd %d'%(dd_,bb))
used=sorted(set(i for f in G for i in f)); remap={o:k for k,o in enumerate(used)}
V2=np.array([NV[i] for i in used]); G2=[[remap[i] for i in f] for f in G]; C2=np.array([NC[i] for i in used])
Fa=np.full((len(G2),4),-1)
for k,f in enumerate(G2): Fa[k,:len(f)]=f
np.savez_compressed(out,V=V2,F=Fa); np.save(out.replace('.npz','_col.npy'),C2); np.save(out.replace('.npz','_remap.npy'),np.array([remap.get(i,-1) for i in range(len(V))]))
print('V',len(V2),'F',len(G2),'B',len(B),'removed cap',len(capf),'target faces',len(tf),'interior',len(interior))
