import sys,numpy as np,bpy,igl,json
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]; inp,out=a[0],a[1]; NIT=int(a[2]) if len(a)>2 else 6; BL=float(a[3]) if len(a)>3 else 0.5; SMW=float(a[4]) if len(a)>4 else 0.3
z=np.load(inp); V=z['V'].astype(float).copy(); Q=z['Q']; polys=[list(map(int,q[q>=0])) for q in Q]; sv=[set(p) for p in polys]
w=np.load('/home/claude/stc/rp1/weld_a.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
MK='/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/m1_masks/'
Bw=np.load(MK+'Rhand_B_wall_source_faces.npy'); Cw=np.load(MK+'Rhand_C_wall_source_faces.npy')
kB=np.ones(len(SF),bool); kB[Cw]=False; kC=np.ones(len(SF),bool); kC[Bw]=False
c=np.array([-33.0,40.0,93.3]); QC=V[Q].mean(1); sel=np.where(np.linalg.norm(QC-c,axis=1)<3.5)[0]
nb={}
for q in polys:
    for i in range(4): nb.setdefault(q[i],set()).update((q[i-1],q[(i+1)%4]))
for it in range(NIT):
    P=[polys[i] for i in sel]; t=BVHTree.FromPolygons(V.tolist(),P,all_triangles=False,epsilon=0.0)
    pr=[(sel[i],sel[j]) for i,j in t.overlap(t) if i<j and not (sv[sel[i]]&sv[sel[j]])]
    pr=[p for p in pr if np.linalg.norm(QC[p[0]]-c)<3.0]
    print('iter',it,'region pairs',len(pr))
    if not pr: break
    vs=set()
    for i,j in pr: vs.update(polys[i]); vs.update(polys[j])
    ring=set(vs)
    for v in vs: ring.update(nb[v])
    vs=np.array(sorted(ring))
    # side by the slit mid-plane (analysis frame y = +40.8): y>40.8 -> B side (blender y<-40.8)
    sideB=V[vs,1]>40.8
    for m,keep in ((sideB,kB),(~sideB,kC)):
        if m.any():
            _,_,cp=igl.point_mesh_squared_distance(V[vs[m]],S,SF[keep]); V[vs[m]]=(1-BL)*V[vs[m]]+BL*cp
    # light smoothing of the moved set to avoid kinks
    V2=V.copy()
    for v in vs: V2[v]=(1-SMW)*V[v]+SMW*np.mean(V[list(nb[v])],axis=0)
    V=V2; QC=V[Q].mean(1)
np.savez_compressed(out,V=V,F=z['F'],Q=Q)
