# pathbevel.py IN.npz IN_col.npy OUT.npz SPEC.json
# Designed crease insertion: split an open edge path p0..pn of the cage into lipA / tip / lipB.
# Interior path verts p_i (0<i<n) get two new verts a_i (side A) and b_i (side B); faces on side A that used p_i now use a_i,
# faces on side B use b_i; new quads (p_i,p_i+1,a_i+1,a_i) / (p_i+1,p_i,b_i,b_i+1) (ends: a_0=b_0=p_0, a_n=b_n=p_n -> triangles).
# SPEC: {"path":[ids...], "tip":[[x,y,z] per path vert or null], "A":[[x,y,z] per interior vert], "B":[...]}
# Side A = faces to the left of the directed edge p_i->p_i+1 (the face containing p_i->p_i+1 in its winding order).
import numpy as np, sys, json, collections
from orient import check
z=np.load(sys.argv[1]); V=z['V'].astype(float).tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(sys.argv[2]).tolist()
S=json.load(open(sys.argv[4])); path=S['path']; n=len(path)-1
# faces around each vertex
vf=collections.defaultdict(list)
for k,f in enumerate(F):
    for v in f: vf[v].append(k)
def has_dir(f,a,b):
    m=len(f); return any(f[i]==a and f[(i+1)%m]==b for i in range(m))
def edge_face(a,b):
    for k in vf[a]:
        if has_dir(F[k],a,b): return k
    raise SystemExit('no face with directed edge %d->%d'%(a,b))
# rotate around vertex v from face k0 (side) to the face containing the other path edge; collect faces on that side
def fan_side(v, start_face, stop_edge_vertex):
    # walk faces around v starting at start_face, crossing edges (v,x), stopping when reaching a face that contains edge v-stop
    side=[]; k=start_face; seen=set()
    while True:
        side.append(k); seen.add(k)
        f=F[k]; m=len(f); i=f.index(v)
        nxt_v=f[(i-1)%m]      # edge (prev,v) -> cross to the neighbour face that has v->prev
        if nxt_v==stop_edge_vertex: return side
        nk=[q for q in vf[v] if q not in seen and has_dir(F[q],v,nxt_v)]
        if not nk: raise SystemExit('fan walk failed at v %d'%v)
        k=nk[0]
def fan_side_rev(v, start_face, stop_edge_vertex):
    side=[]; k=start_face; seen=set()
    while True:
        side.append(k); seen.add(k)
        f=F[k]; m=len(f); i=f.index(v)
        nxt_v=f[(i+1)%m]
        if nxt_v==stop_edge_vertex: return side
        nk=[q for q in vf[v] if q not in seen and has_dir(F[q],nxt_v,v)]
        if not nk: raise SystemExit('fan walk (rev) failed at v %d'%v)
        k=nk[0]
A={path[0]:path[0],path[-1]:path[-1]}; B=dict(A)
repl={}
for i in range(1,n):
    p,prv,nxt=path[i],path[i-1],path[i+1]
    # side A: left of prv->p and of p->nxt. face with p->nxt is left of the forward edge; walk around p (towards prv)
    kA=edge_face(p,nxt); sideA=fan_side(p,kA,prv)
    kB=edge_face(nxt,p); sideB=fan_side_rev(p,kB,prv)
    pa,pb=S['A'][i-1],S['B'][i-1]
    if pa=='auto' or pb=='auto':
        from scipy.spatial import cKDTree
        global _S,_kd
        try: _kd
        except NameError:
            _S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); _kd=cKDTree(_S)
        P0=np.array(V[p]); off=float(S.get('lipoff',0.6))
        def lip(side):
            c=np.mean([np.mean([V[x] for x in F[k]],axis=0) for k in side],axis=0); d=c-P0; d/=np.linalg.norm(d)+1e-9
            q=P0+off*d
            return (_S[_kd.query(q)[1]] if S.get('lipsnap',True) else q).tolist()
        if pa=='auto': pa=lip(sideA)
        if pb=='auto': pb=lip(sideB)
    V.append(pa); cc.append(cc[p]); a=len(V)-1
    V.append(pb); cc.append(cc[p]); b=len(V)-1
    A[p]=a; B[p]=b
    for k in sideA: repl[(k,p)]=a
    for k in sideB: repl[(k,p)]=b
G=[]
for k,f in enumerate(F): G.append([repl.get((k,v),v) for v in f])
for i in range(n):
    p,q=path[i],path[i+1]
    # side A strip: face left of p->q originally had p->q; now it has A[p]->A[q]; new face must have A[q]->A[p] ... plus p,q
    qa=[p,q,A[q],A[p]]; qa=[v for j,v in enumerate(qa) if v not in qa[:j]]
    qb=[q,p,B[p],B[q]]; qb=[v for j,v in enumerate(qb) if v not in qb[:j]]
    G.append(qa); G.append(qb)
for i,p in enumerate(path):
    if S.get('tip') and S['tip'][i] is not None: V[p]=S['tip'][i]
d,bn=check(G)
if d or bn:
    de=collections.Counter((f[i],f[(i+1)%len(f)]) for f in G for i in range(len(f)))
    print('dup',[e for e,c in de.items() if c>1][:6],'bnd',[e for e in de if (e[1],e[0]) not in de][:6]); raise SystemExit('topology dup %d bnd %d'%(d,bn))
Fa=np.full((len(G),4),-1)
for k,f in enumerate(G): Fa[k,:len(f)]=f
np.savez_compressed(sys.argv[3],V=np.array(V),F=Fa); np.save(sys.argv[3].replace('.npz','_col.npy'),np.array(cc))
print('V',len(V),'F',len(G),'tris',sum(len(f)==3 for f in G))
