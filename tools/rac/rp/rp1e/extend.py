# extend.py IN.npz SPEC.json OUT.npz : extend a digit tube beyond its last ring (12 verts) with rings from source plane loops, new tip cap.
# SPEC: {"ring":[12 ids], "prev":[12 ids], "dir":[x,y,z], "steps":[d1,d2,...] (cm beyond last ring centre), "rad":2.0, "tipback":0.2, "tipspread":0.45, "maxr":2.5, "capshrink":1.0}
import sys, json, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0,'/home/claude/stc/rp1e')
from planeslice import plane_loops
from orient import orient_patch, check
inp,specp,out=sys.argv[1:4]; S=json.load(open(specp))
z=np.load(inp); V=z['V'].astype(float); F=[[int(x) for x in f if x>=0] for f in z['F']]; col=np.load(inp.replace('.npz','_col.npy'))
SRC=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); kS=cKDTree(SRC)
ring=S['ring']; prev=set(S['prev']); rs=set(ring)
# cap faces: faces touching ring verts not lying between ring and prev, plus faces of cap-interior verts
capv=set()
cand=[k for k,f in enumerate(F) if set(f)&rs and not set(f)<=(rs|prev)]
for k in cand: capv|=set(F[k])-rs
capf=set(k for k,f in enumerate(F) if set(f)&capv or k in cand)
assert all(set(F[k])<=(rs|capv) for k in capf),'cap region not isolated'
TD=np.array(S['dir'],float); TD/=np.linalg.norm(TD)
NV=[list(p) for p in V]; NC=list(col); cc=int(col[ring[0]])
def add(p): NV.append(list(p)); NC.append(cc); return len(NV)-1
c0=V[ring].mean(0); rings=[ring]; last=V[ring]
for si,d in enumerate(S['steps']):
    nd=np.array(S['dirs'][si],float) if 'dirs' in S else TD; nd/=np.linalg.norm(nd)
    p=c0+TD*d; L=[P for P,cl in plane_loops(p,nd) if cl and np.linalg.norm(P-p,axis=1).min()<S.get('rad',2.0)]
    assert L,('no loop',d); P=min(L,key=lambda P:np.linalg.norm(P.mean(0)-p))
    assert np.linalg.norm(P-P.mean(0),axis=1).max()<S.get('maxr',2.5),('loop too big',d)
    Q=np.vstack([P,P[:1]]); s_=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]
    pts=[]
    for u in np.arange(12)/12*s_[-1]:
        k=int(np.clip(np.searchsorted(s_,u),1,len(s_)-1)); al=(u-s_[k-1])/max(s_[k]-s_[k-1],1e-12); pts.append(Q[k-1]+(Q[k]-Q[k-1])*al)
    pts=np.array(pts); sc=S.get('scale',1.0); pts=pts.mean(0)+(pts-pts.mean(0))*sc
    # orientation + start matching previous ring
    best=None
    for flip in (False,True):
        R=pts[::-1] if flip else pts
        for sh in range(12):
            Rr=np.roll(R,-sh,axis=0); cst=np.sum(np.linalg.norm((Rr-Rr.mean(0))-(last-last.mean(0)),axis=1))
            if best is None or cst<best[0]: best=(cst,Rr)
    last=best[1]; rings.append([add(q) for q in last])
G=[f for k,f in enumerate(F) if k not in capf]; Fn=[]
for a,b in zip(rings[:-1],rings[1:]):
    for i in range(12): Fn.append([a[i],a[(i+1)%12],b[(i+1)%12],b[i]])
l=rings[-1]; P=np.array([NV[v] for v in l]); c=P.mean(0); hw=np.linalg.norm(P-c,axis=1).max()
idx=kS.query_ball_point(c,2.0); Q=SRC[idx]; Q=Q[((Q-c)@TD>0)&(np.linalg.norm((Q-c)-np.outer((Q-c)@TD,TD),axis=1)<0.8*hw)]
tipP=Q[np.argmax(Q@TD)] if len(Q) else c+TD*0.3
if S.get('tipmax') is not None: tipP=c+TD*min((tipP-c)@TD,S['tipmax'])
t=[]
for k in range(4):
    dk=0.5*(P[(3*k+1)%12]+P[(3*k+2)%12])-c; t.append(add(tipP-TD*S.get('tipback',0.2)+S.get('tipspread',0.45)*dk))
for k in range(4):
    Fn.append([l[3*k],l[3*k+1],l[3*k+2],t[k]]); Fn.append([l[3*k+2],l[(3*k+3)%12],t[(k+1)%4],t[k]])
Fn.append([t[0],t[1],t[2],t[3]])
Fn=orient_patch(G,Fn); G+=Fn; dd,bb=check(G)
if dd or bb: raise SystemExit('topology dup %d bnd %d'%(dd,bb))
used=sorted(set(i for f in G for i in f)); remap={o:n for n,o in enumerate(used)}
V2=np.array([NV[i] for i in used]); G2=[[remap[i] for i in f] for f in G]; C2=np.array([NC[i] for i in used])
Fa=np.full((len(G2),4),-1)
for k,f in enumerate(G2): Fa[k,:len(f)]=f
np.savez_compressed(out,V=V2,F=Fa); np.save(out.replace('.npz','_col.npy'),C2); np.save(out.replace('.npz','_remap.npy'),np.array([remap.get(i,-1) for i in range(len(V))]))
json.dump({'rings':[[remap[v] for v in r] for r in rings]},open(out.replace('.npz','_meta.json'),'w'))
print('V',len(V2),'F',len(G2),'cap faces removed',len(capf),'new rings',len(rings)-1)
