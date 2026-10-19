# loopcut.py IN.npz IN_col.npy OUT.npz RINGA(ids comma) RINGB(ids comma) FRACS(comma) [overrides.json]
# Insert edge loops into the face strip between ring A and ring B (faces with 2 verts on each ring); new verts placed at
# the fraction along each rung (A->B) then snapped to the nearest source point; overrides.json {"rungA:rungB:frac": [x,y,z]}
import numpy as np, sys, json
from scipy.spatial import cKDTree
from orient import check
z=np.load(sys.argv[1]); V=z['V'].astype(float).tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(sys.argv[2]).tolist()
RA=set(int(t) for t in sys.argv[4].split(',')); RB=set(int(t) for t in sys.argv[5].split(',')); fr=[float(t) for t in sys.argv[6].split(',')]
ov=json.load(open(sys.argv[7])) if len(sys.argv)>7 else {}
S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); kd=cKDTree(S)
rung={}
def newverts(a,b):
    key=(a,b)
    if key in rung: return rung[key]
    ids=[]
    for f in fr:
        k='%d:%d:%g'%(a,b,f)
        if k in ov: p=np.array(ov[k])
        else:
            p=np.array(V[a])+f*(np.array(V[b])-np.array(V[a])); p=S[kd.query(p)[1]]
        V.append(p.tolist()); cc.append(cc[a] if f<0.5 else cc[b]); ids.append(len(V)-1)
    rung[key]=ids; return ids
G=[]; ns=0
for f in F:
    ina=[v in RA for v in f]; inb=[v in RB for v in f]
    if len(f)==4 and sum(ina)==2 and sum(inb)==2:
        # find rotation so that f = [a0,a1,b1,b0] (a0->a1 along A)
        for r in range(4):
            g=f[r:]+f[:r]
            if g[0] in RA and g[1] in RA and g[2] in RB and g[3] in RB: break
        else: G.append(f); continue
        a0,a1,b1,b0=g; c0=[a0]+newverts(a0,b0)+[b0]; c1=[a1]+newverts(a1,b1)+[b1]
        for k in range(len(c0)-1): G.append([c0[k],c1[k],c1[k+1],c0[k+1]])
        ns+=1
    else: G.append(f)
# non-strip faces touching a cut rung: insert the rung's new verts, then split the polygon
def split_poly(g):
    out=[]
    while len(g)>4:
        out.append(g[:4]); g=[g[0]]+g[3:]
    out.append(g); return out
H=[]
for f in G:
    m=len(f); g=[]; changed=False
    for i in range(m):
        a,b=f[i],f[(i+1)%m]; g.append(a)
        if (a,b) in rung: g+=rung[(a,b)]; changed=True
        elif (b,a) in rung: g+=rung[(b,a)][::-1]; changed=True
    H+= split_poly(g) if changed and len(g)>4 else [g]
G=[f for f in H if len(f)>=3]
d,b=check(G); print('strip faces',ns,'rungs',len(rung),'dup',d,'bnd',b)
if d or b: raise SystemExit('topology')
Fa=np.full((len(G),4),-1)
for k,f in enumerate(G): Fa[k,:len(f)]=f
np.savez_compressed(sys.argv[3],V=np.array(V),F=Fa); np.save(sys.argv[3].replace('.npz','_col.npy'),np.array(cc))
json.dump({'%d:%d'%k:v for k,v in rung.items()},open(sys.argv[3].replace('.npz','_rungs.json'),'w'))
