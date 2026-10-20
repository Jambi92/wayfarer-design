# remap.py IN.npz OUT.npz "centre" r [--keep-bnd] : final-resolution patch remap (v014 ruling §10).
# The L4 production patch (connected disk of quads around centre, holes filled) keeps its connectivity and its boundary vertices
# (exact weld); its interior vertices are re-placed on the frozen source by a disk-to-disk Tutte map:
#   source region = the source faces enclosed by the projected patch boundary (component not touching the outer ring),
#   both disks are parameterised on the unit circle (boundary by arc length of the projected boundary), interior by uniform Tutte,
#   each patch vertex takes the source point with the same (u,v).
import sys, json, numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import spsolve
from scipy.sparse.csgraph import connected_components, dijkstra
from scipy.spatial import cKDTree
import igl
inp,out=sys.argv[1],sys.argv[2]; c=np.array(eval(sys.argv[3])); r=float(sys.argv[4])
z=np.load(inp); V=z['V'].astype(float).copy(); Q=z['Q'].astype(np.int64); Tp=z['F'].astype(np.int64)
w=np.load('/home/claude/stc/rp1/weld_a.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
if len(sys.argv)>5:
    ex=np.load(sys.argv[5]); keep=np.ones(len(SF),bool); keep[ex]=False; SF=SF[keep]
    import os
    if os.environ.get('LID'):
        # cap each hole left by the excluded (D) faces with a fan lid -> the production crosses the throat as one closed surface
        de_={}
        for f in SF:
            for i_ in range(3): de_[(f[i_],f[(i_+1)%3])]=1
        hb=[(u,v) for (u,v) in de_ if (v,u) not in de_]; nx_={}
        for u,v in hb: nx_.setdefault(u,[]).append(v)
        used_=set(); lids=[]
        for e0 in hb:
            if e0 in used_: continue
            Lp=[e0[0]]; e=e0
            while e not in used_:
                used_.add(e); Lp.append(e[1]); cand=[v for v in nx_[e[1]] if (e[1],v) not in used_]
                if not cand: break
                e=(e[1],cand[0])
            Lp=Lp[:-1]
            cidx=len(S); S=np.vstack([S,S[Lp].mean(0)]); lids.append(len(Lp))
            SF=np.vstack([SF,np.array([[Lp[(k+1)%len(Lp)],Lp[k],cidx] for k in range(len(Lp))])])
        print('lids',lids); np.savez_compressed(sys.argv[2].replace('.npz','_src.npz'),V=S,F=SF)
c=c*np.array([1,-1,1])   # centre given in Blender frame -> analysis frame
nq=len(Q); QC=V[Q].mean(1)
# ---- product patch: faces within r (connected comp of the seed), holes filled
sel=np.linalg.norm(QC-c,axis=1)<r
E=np.vstack([np.c_[Q[:,i],Q[:,(i+1)%4]] for i in range(4)]); fid=np.tile(np.arange(nq),4)
key=np.sort(E,1); order=np.lexsort((key[:,1],key[:,0])); ks=key[order]; fs=fid[order]
same=(ks[1:]==ks[:-1]).all(1); a=fs[:-1][same]; b=fs[1:][same]
A=sp.coo_matrix((np.ones(len(a)),(a,b)),shape=(nq,nq)); A=(A+A.T).tocsr()
def comps(mask):
    idx=np.where(mask)[0]; sub=A[idx][:,idx]; n,l=connected_components(sub,directed=False); return idx,n,l
idx,n,l=comps(sel); seed=np.argmin(np.linalg.norm(QC[idx]-c,axis=1)); P=np.zeros(nq,bool); P[idx[l==l[seed]]]=True
# fill holes: complement components other than the largest
cidx=np.where(~P)[0]; sub=A[cidx][:,cidx]; n2,l2=connected_components(sub,directed=False)
if n2>1:
    big=np.bincount(l2).argmax(); P[cidx[l2!=big]]=True
pf=np.where(P)[0]; pv=np.unique(Q[pf])
# boundary loop
de={}
for f in pf:
    q=Q[f]
    for i in range(4): de[(q[i],q[(i+1)%4])]=1
bd=[(u,v) for (u,v) in de if (v,u) not in de]; nxt=dict(bd); assert len(nxt)==len(bd)
Bl=[bd[0][0]]
while nxt[Bl[-1]]!=Bl[0]: Bl.append(nxt[Bl[-1]])
assert len(Bl)==len(bd),'patch boundary is not a single loop (patch not a disk)'
nv=len(pv); ne=len(set(tuple(sorted(e)) for e in de)); chi=nv-ne+len(pf); assert chi==1,('patch not a disk, chi',chi)
# ---- source region bounded by the projected boundary
_,ib,cp=igl.point_mesh_squared_distance(V[Bl],S,SF)
sv_near=np.unique(SF[np.linalg.norm(S[SF].mean(1)-c,axis=1)<r+1.0])
loc=np.full(len(S),-1); loc[sv_near]=np.arange(len(sv_near))
LF=SF[(loc[SF]>=0).all(1)]; LFl=loc[LF]; LS=S[sv_near]
Ee=np.vstack([LFl[:,[0,1]],LFl[:,[1,2]],LFl[:,[2,0]]]); wgt=np.linalg.norm(LS[Ee[:,0]]-LS[Ee[:,1]],axis=1)
G=sp.coo_matrix((wgt,(Ee[:,0],Ee[:,1])),shape=(len(LS),len(LS))).tocsr(); G=G.maximum(G.T)
kL=cKDTree(LS); _,bv=kL.query(cp)
# subsample the boundary so consecutive samples are >= 2 source edge lengths apart, then join by shortest paths
sedge=np.median(wgt); acc=0; keep=[0]
for i in range(1,len(cp)):
    acc+=np.linalg.norm(cp[i]-cp[i-1])
    if acc>=2.5*sedge: keep.append(i); acc=0
seq=[bv[i] for i in keep]; seq=[v for k_,v in enumerate(seq) if k_==0 or v!=seq[k_-1]]
if len(seq)>1 and seq[-1]==seq[0]: seq=seq[:-1]
cut=[seq[0]]
for t in seq[1:]+[seq[0]]:
    d,pred=dijkstra(G,indices=cut[-1],return_predecessors=True,limit=3.0)
    path=[t]
    while path[-1]!=cut[-1]: path.append(pred[path[-1]]); assert path[-1]>=0,'cut path failed'
    for q in path[::-1][1:]:
        if q==cut[0] and t==seq[0]: break
        if q in cut[1:]: cut=cut[:cut.index(q,1)+1]
        else: cut.append(q)
# simple loop check
assert len(set(cut))==len(cut),'projected boundary self-touches on the source'
cutE=set(tuple(sorted((cut[i],cut[(i+1)%len(cut)]))) for i in range(len(cut)))
# face adjacency not crossing cut edges
fe=np.vstack([np.sort(LFl[:,[0,1]],1),np.sort(LFl[:,[1,2]],1),np.sort(LFl[:,[2,0]],1)]); ff=np.tile(np.arange(len(LF)),3)
o=np.lexsort((fe[:,1],fe[:,0])); fes=fe[o]; ffs=ff[o]; sm=(fes[1:]==fes[:-1]).all(1)
ea=ffs[:-1][sm]; eb=ffs[1:][sm]; ekey=fes[:-1][sm]; okk=np.array([tuple(k) not in cutE for k in ekey])
AF=sp.coo_matrix((np.ones(okk.sum()),(ea[okk],eb[okk])),shape=(len(LF),len(LF))); n3,l3=connected_components(AF,directed=False)
far=np.linalg.norm(LS[LFl].mean(1)-c,axis=1)>r+0.6
inside=[k for k in range(n3) if not far[l3==k].any()]
print('DBG cut',len(cut),'comps',n3,sorted([(int((l3==k).sum()),bool(far[l3==k].any())) for k in range(n3)],reverse=True)[:6]); assert inside,'no enclosed source region'
reg=max(inside,key=lambda k:(l3==k).sum()); RF=LFl[l3==reg]
rv=np.unique(RF); assert set(cut)<=set(rv),'cut loop not on the region boundary'
# ---- Tutte maps
def tutte(nverts,faces,bverts,bpos,X3=None):
    # mean-value-weight embedding (positive weights -> bijective for a convex boundary); uniform if X3 is None
    tris=[]
    for f in faces:
        f=list(f)
        if len(f)==3: tris.append(f)
        else: tris.append([f[0],f[1],f[2]]); tris.append([f[0],f[2],f[3]])
    tris=np.array(tris); W={}
    def addw(i,j,w): W[(i,j)]=W.get((i,j),0.0)+w
    for t in tris:
        for k in range(3):
            i,j,l=t[k],t[(k+1)%3],t[(k+2)%3]
            if X3 is None: addw(i,j,1.0); addw(i,l,1.0); continue
            e1=X3[j]-X3[i]; e2=X3[l]-X3[i]; n1=np.linalg.norm(e1)+1e-12; n2=np.linalg.norm(e2)+1e-12
            a=np.arccos(np.clip(e1@e2/(n1*n2),-1,1)); tt=np.tan(a/2)
            addw(i,j,tt/n1); addw(i,l,tt/n2)
    isb=np.zeros(nverts,bool); isb[bverts]=True; X=np.zeros((nverts,2)); X[bverts]=bpos
    rows=[];cols=[];vals=[]; diag=np.zeros(nverts)
    for (i,j),w in W.items():
        if isb[i]: continue
        rows.append(i);cols.append(j);vals.append(-w); diag[i]+=w
    for i in range(nverts):
        rows.append(i);cols.append(i);vals.append(1.0 if isb[i] else diag[i])
    M=sp.csr_matrix((vals,(rows,cols)),shape=(nverts,nverts)); rhs=np.zeros((nverts,2)); rhs[isb]=X[isb]
    return np.c_[spsolve(M,rhs[:,0]),spsolve(M,rhs[:,1])]
# source param: cut loop on circle by arc length
cl=LS[cut]; seg=np.linalg.norm(np.diff(np.vstack([cl,cl[:1]]),axis=0),axis=1); s=np.r_[0,np.cumsum(seg)]; L=s[-1]; th=2*np.pi*s[:-1]/L
rmap={v:i for i,v in enumerate(rv)}; RFi=np.array([[rmap[v] for v in f] for f in RF])
UVs=tutte(len(rv),RFi,np.array([rmap[v] for v in cut]),np.c_[np.cos(th),np.sin(th)],LS[rv])
# product boundary param: position of each projected boundary point along the cut polyline
cpos=[]
for p in cp:
    best=None
    for i in range(len(cut)):
        a_,b_=cl[i],cl[(i+1)%len(cut)]; d=b_-a_; t=np.clip((p-a_)@d/max(d@d,1e-12),0,1); dist=np.linalg.norm(a_+t*d-p)
        if best is None or dist<best[0]: best=(dist,s[i]+t*seg[i])
    cpos.append(best[1])
cpos=np.array(cpos); 
# make monotone in loop order (unwrap)
ang=2*np.pi*cpos/L
pmap={v:i for i,v in enumerate(pv)}; PF=np.array([[pmap[v] for v in Q[f]] for f in pf])
UVp=tutte(len(pv),PF,np.array([pmap[v] for v in Bl]),np.c_[np.cos(ang),np.sin(ang)],V[pv])
# orientation consistency: if product boundary runs opposite to the cut loop, mirror product param
def sarea(UV,faces):
    t=UV[faces[:,[0,1,2]]]; return np.sum((t[:,1,0]-t[:,0,0])*(t[:,2,1]-t[:,0,1])-(t[:,1,1]-t[:,0,1])*(t[:,2,0]-t[:,0,0]))
# ---- locate and map interior vertices
from matplotlib.tri import Triangulation
tri=Triangulation(UVs[:,0],UVs[:,1],RFi); fnd=tri.get_trifinder()
Pos=LS[rv]; kUV=cKDTree(UVs); newV=V.copy(); bset=set(Bl); miss=0
for v in pv:
    if v in bset: continue
    u=UVp[pmap[v]]; t=fnd(u[0],u[1])
    if t<0:
        miss+=1
        # deterministic fallback: closest point of the nearest source-param triangles (clamped barycentric)
        best=None
        for tt in np.where(np.isin(RFi,kUV.query(u,k=6)[1]).any(1))[0]:
            A_,B_,C_=UVs[RFi[tt]]; M_=np.c_[B_-A_,C_-A_]; l_=np.linalg.lstsq(M_,u-A_,rcond=None)[0]; bc=np.clip(np.r_[1-l_.sum(),l_],0,None); bc/=bc.sum()
            d_=np.linalg.norm(bc@np.array([A_,B_,C_])-u)
            if best is None or d_<best[0]: best=(d_,tt,bc)
        a_,b_,c_=RFi[best[1]]; newV[v]=best[2][0]*Pos[a_]+best[2][1]*Pos[b_]+best[2][2]*Pos[c_]; continue
    a_,b_,c_=RFi[t]; T=np.array([UVs[a_],UVs[b_],UVs[c_]]); M=np.c_[T[1]-T[0],T[2]-T[0]]; l12=np.linalg.solve(M,u-T[0]); bc=np.r_[1-l12.sum(),l12]
    newV[v]=bc[0]*Pos[a_]+bc[1]*Pos[b_]+bc[2]*Pos[c_]
np.savez_compressed(out,V=newV,F=Tp,Q=Q)
moved=np.linalg.norm(newV-V,axis=1)
print('patch faces',len(pf),'verts',len(pv),'boundary',len(Bl),'source region faces',len(RF),'cut',len(cut),'unlocated',miss,'max move mm %.2f'%(moved.max()*10))
