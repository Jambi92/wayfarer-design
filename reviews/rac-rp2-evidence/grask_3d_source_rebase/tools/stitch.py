# stitch.py ZB ZT OUT.npz : replace the source trunk/legs band (ZB..ZT) by the fitted donor patch, zipper the 3 boundary loops
import sys, numpy as np, scipy.sparse as sp, trimesh, igl
from scipy.sparse.csgraph import connected_components
ZB,ZT=float(sys.argv[1]),float(sys.argv[2])
S=np.load('/tmp/claude-0/src3d/in/front_aligned.npz'); SV=S['V'].astype(float); SF=S['Q'].astype(np.int64)
D=np.load('/tmp/claude-0/src3d/work/donor_fine.npz'); DV=D['V'].astype(float); DQ=D['Q']; DF=np.r_[DQ[:,[0,1,2]],DQ[:,[0,2,3]]].astype(np.int64)
def band_trunk(V,F):
    c=V[F].mean(1); inb=(c[:,2]>ZB)&(c[:,2]<ZT); idx=np.nonzero(inb)[0]
    # face adjacency within band by shared vertices
    sub=F[idx]; n=len(V)
    rows=np.repeat(np.arange(len(idx)),3); A=sp.coo_matrix((np.ones(len(rows)),(rows,sub.ravel())),(len(idx),n)).tocsr()
    G=A@A.T; nc,lab=connected_components(G,directed=False)
    keep=np.zeros(len(F),bool)
    for k in range(nc):
        m=lab==k; cc=c[idx[m]]
        if (np.abs(cc[:,0])<2).any(): keep[idx[m]]=True
    return keep
sb=band_trunk(SV,SF); db=band_trunk(DV,DF)
SFk=SF[~sb]; DFk=DF[db]
def loops(F):
    e=np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]; es=np.sort(e,1); u,inv,c=np.unique(es,axis=0,return_inverse=True,return_counts=True)
    be=e[c[inv]==1]   # directed boundary edges
    from collections import Counter
    oc=Counter(be[:,0].tolist()); print('boundary edges',len(be),'pinched',sum(1 for v in oc.values() if v>1))
    nxt={a:b for a,b in be}; seen=set(); L=[]
    for a in nxt:
        if a in seen: continue
        lp=[a]; seen.add(a); b=nxt[a]
        while b!=a and b not in seen and b in nxt: lp.append(b); seen.add(b); b=nxt[b]
        if b!=a: print('open/pinched boundary chain of',len(lp))
        L.append(np.array(lp))
    return L
Ls=loops(SFk); Ld=loops(DFk)
print('source loops',[(len(l),SV[l].mean(0).round(1).tolist()) for l in Ls],'donor loops',[(len(l),DV[l].mean(0).round(1).tolist()) for l in Ld])
Ls=[l for l in Ls if len(l)>20]; Ld=[l for l in Ld if len(l)>20]
def key(V,l): c=V[l].mean(0); return c
pairs=[]
for ls in Ls:
    cs=key(SV,ls); j=np.argmin([np.linalg.norm(key(DV,ld)-cs) for ld in Ld]); pairs.append((ls,Ld[j]))
# snap donor loop vertices onto source loop polyline and blend nearby donor vertices
Y=DV.copy()
for ls,ld in pairs:
    P=SV[ls]; seg0=P; seg1=np.roll(P,-1,0)
    for i in ld:
        q=Y[i]; d=seg1-seg0; t=np.clip(((q-seg0)*d).sum(1)/((d*d).sum(1)+1e-12),0,1); proj=seg0+t[:,None]*d; k=np.argmin(np.linalg.norm(proj-q,axis=1)); Y[i]=proj[k]
# zipper: both loops oriented; source boundary edges are oriented one way, donor patch boundary opposite (complementary surfaces) -> align by angle param
newF=[]; nS=len(SV)
for ls,ld in pairs:
    cs=SV[ls].mean(0)
    def ang(P): return np.arctan2(P[:,1]-cs[1],P[:,0]-cs[0])
    a_s=ang(SV[ls]); a_d=ang(Y[ld])
    # make both loops run in increasing angle order direction-consistent: compute signed area direction
    def dirn(P): x=P[:,0]-cs[0]; y=P[:,1]-cs[1]; return np.sign(np.sum(x*np.roll(y,-1)-np.roll(x,-1)*y))
    S_=ls.copy(); D_=ld.copy()
    if dirn(SV[S_])<0: S_=S_[::-1]
    if dirn(Y[D_])<0: D_=D_[::-1]
    # start points: nearest pair
    i0=np.argmin(ang(SV[S_])); S_=np.roll(S_,-i0); j0=np.argmin(np.linalg.norm(Y[D_]-SV[S_[0]],axis=1)); D_=np.roll(D_,-j0)
    i=j=0; ns=len(S_); nd=len(D_); tri=[]
    while i<ns or j<nd:
        a=S_[i%ns]; b=D_[j%nd]; an=S_[(i+1)%ns]; bn=D_[(j+1)%nd]
        if i>=ns: tri.append((a,bn+nS,b+nS)); j+=1; continue
        if j>=nd: tri.append((a,an,b+nS)); i+=1; continue
        # choose shorter diagonal
        if np.linalg.norm(SV[an]-Y[b])<np.linalg.norm(Y[bn]-SV[a]): tri.append((a,an,b+nS)); i+=1
        else: tri.append((a,bn+nS,b+nS)); j+=1
    newF+=tri
V=np.r_[SV,Y]; F=np.r_[SFk,DFk+nS,np.array(newF)]
m=trimesh.Trimesh(V,F,process=False); m.remove_unreferenced_vertices()
# fix orientation consistently
trimesh.repair.fix_winding(m); trimesh.repair.fix_normals(m)
e=np.sort(m.edges,1); u,c=np.unique(e,axis=0,return_counts=True)
print('verts',len(m.vertices),'faces',len(m.faces),'boundary',(c==1).sum(),'nonmanifold',(c>2).sum(),'watertight',m.is_watertight,'euler',m.euler_number,'components',len(m.split(only_watertight=False)))
np.savez(sys.argv[3],V=m.vertices,Q=m.faces,nsrc=nS)
