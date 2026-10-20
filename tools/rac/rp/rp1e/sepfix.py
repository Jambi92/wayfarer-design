# blender-python sepfix.py -- IN.npz OUT.npz [step_cm] [maxdisp_cm] [iters] : final-resolution collision-safe local relaxation (P3).
# Opposed intersecting quads: both move back along their own outward normal (into their own body) by 'step' per iteration;
# folded pairs (normals agreeing): their vertices get one tangential Laplacian step.  Displacements are 1-ring smoothed,
# accumulated, and capped at maxdisp per vertex.  Only vertices of intersecting faces (and their smoothing ring) ever move.
import sys, numpy as np, bpy, mathutils
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]; inp,out=a[0],a[1]; step=float(a[2]) if len(a)>2 else 0.004; maxd=float(a[3]) if len(a)>3 else 0.06; NIT=int(a[4]) if len(a)>4 else 60
z=np.load(inp); V=z['V'].astype(float).copy(); Q=z['Q']; V0=V.copy()
polys=[list(map(int,q[q>=0])) for q in Q]; sv=[set(q) for q in polys]; P=np.array(polys)
nb=[[] for _ in range(len(V))]
for q in polys:
    for i in range(4): nb[q[i]].append(q[(i+1)%4]); nb[q[i]].append(q[(i-1)%4])
def fnorm(idx):
    A=V[P[idx]]; n=np.cross(A[:,2]-A[:,0],A[:,3]-A[:,1]); return SG*n/(np.linalg.norm(n,axis=1)[:,None]+1e-12)
hist=[]
# orientation sign: analysis-frame products are y-mirrored (inward winding); make normals outward
TT=np.array([[q[0],q[1],q[2]] for q in polys]+[[q[0],q[2],q[3]] for q in polys]); vol=np.einsum('ij,ij->i',V[TT[:,0]],np.cross(V[TT[:,1]],V[TT[:,2]])).sum()/6; SG=1.0 if vol>0 else -1.0
print('orientation sign',SG)
for it in range(NIT):
    t=BVHTree.FromPolygons(V.tolist(),polys,all_triangles=False,epsilon=0.0)
    pr=[(i,j) for i,j in t.overlap(t) if i<j and not (sv[i]&sv[j])]
    hist.append(len(pr))
    if not pr: break
    pr=np.array(pr); ni=fnorm(pr[:,0]); nj=fnorm(pr[:,1]); dot=(ni*nj).sum(1)
    D=np.zeros_like(V); cnt=np.zeros(len(V)); fold=set()
    for (i,j),a_,b_,d in zip(pr,ni,nj,dot):
        if d>0.3:
            fold.update(polys[i]); fold.update(polys[j])
        else:
            for v in polys[i]: D[v]-=a_*step; cnt[v]+=1
            for v in polys[j]: D[v]-=b_*step; cnt[v]+=1
    m=cnt>0; D[m]/=cnt[m][:,None]
    # smooth displacement over 1-ring (2 passes) so the push is a smooth bump
    act=set(np.where(m)[0])
    for _ in range(2):
        ring=set(act)
        for v in list(act): ring.update(nb[v])
        D2=D.copy()
        for v in ring:
            ns=nb[v]; D2[v]=0.5*D[v]+0.5*np.mean(D[ns],axis=0)
        D=D2; act=ring
    for v in fold:
        D[v]+=0.5*(np.mean(V[nb[v]],axis=0)-V[v])
    Vn=V+D; tot=Vn-V0; L=np.linalg.norm(tot,axis=1); big=L>maxd; Vn[big]=V0[big]+tot[big]*(maxd/L[big])[:,None]
    V=Vn
np.savez_compressed(out,V=V,F=z['F'],Q=Q); disp=np.linalg.norm(V-V0,axis=1)
np.save(out.replace('.npz','_disp.npy'),disp.astype(np.float32))
print('pairs per iter',hist[:5],'...',hist[-3:],'final',hist[-1],'moved verts',int((disp>1e-6).sum()),'max disp mm %.3f'%(disp.max()*10))
