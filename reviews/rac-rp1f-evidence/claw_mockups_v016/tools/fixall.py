# blender-python fixall.py -- IN.npz OUT.npz NIT BL SMW [EXCL.json] : final-resolution crossing resolution (v014 ruling 10 / order 913d0e4 8,10)
# Each iteration: global quad BVH self-overlap -> vertices of crossing quads (+1 ring) are moved toward their closest point on the frozen
# source (side-restricted where an explicit side rule applies) and lightly smoothed.  Only those vertices move; topology unchanged.
# EXCL.json: list of {"centre":[x,y,z] (blender cm), "R":r, "mid":y_plane (blender), "Bmask":file, "Cmask":file} side rules (M1-type).
import sys, json, numpy as np, bpy, igl
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]; inp,out=a[0],a[1]; NIT=int(a[2]); BL=float(a[3]); SMW=float(a[4]); rules=json.load(open(a[5])) if len(a)>5 else []
z=np.load(inp); V=z['V'].astype(float).copy(); Q=z['Q']; polys=[list(map(int,q[q>=0])) for q in Q]; sv=[set(p) for p in polys]
import os
w=np.load(os.environ.get('SRC','/home/claude/stc/rp1/weld_a.npz')); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
if os.environ.get('EXCL'):
    _k=np.ones(len(SF),bool)
    for _f in os.environ['EXCL'].split(','): _k[np.load(_f)]=False
    SFg=SF[_k]
else: SFg=SF
nb=[set() for _ in range(len(V))]
for q in polys:
    for i in range(4): nb[q[i]].update((q[i-1],q[(i+1)%4]))
fl=np.array([1,-1,1]); hist=[]; moved=np.zeros(len(V),bool)
import os
REG=os.environ.get('REG')
if REG:
    rg=np.array([float(x) for x in REG.split(',')]); rc=rg[:3]*fl; QCq=V[Q].mean(1); qsel=np.where(np.linalg.norm(QCq-rc,axis=1)<rg[3]+0.5)[0]
else: qsel=np.arange(len(polys))
psub=[polys[i] for i in qsel]
for it in range(NIT):
    t=BVHTree.FromPolygons(V.tolist(),psub,all_triangles=False,epsilon=0.0)
    pr=[(qsel[i],qsel[j]) for i,j in t.overlap(t) if i<j and not (sv[qsel[i]]&sv[qsel[j]])]; hist.append(len(pr)); print('iter',it,'pairs',len(pr),flush=True)
    if not pr: break
    vs=set()
    for i,j in pr: vs.update(polys[i]); vs.update(polys[j])
    ring=set(vs)
    for v in vs: ring.update(nb[v])
    vs=np.array(sorted(ring)); done=np.zeros(len(vs),bool)
    for R in rules:
        c=np.array(R['centre'])*fl; m=np.linalg.norm(V[vs]-c,axis=1)<R['R']
        if not m.any(): continue
        if 'n' in R:   # plane side rule (blender frame normal/point), source faces in the ball on the other side are excluded
            n_=np.array(R['n'])*fl; p_=np.array(R['p'])*fl; sideB=(V[vs]-p_)@n_>0
            SCb=S[SF].mean(1); inb=np.linalg.norm(SCb-c,axis=1)<R['R']+0.5; sgf=(SCb-p_)@n_>0
            exA=np.where(inb&~sgf)[0]; exB=np.where(inb&sgf)[0]
        else:
            sideB=V[vs,1]>-R['mid']   # analysis frame y = -blender y
            exA=np.load(R['Cmask']); exB=np.load(R['Bmask'])
        for sm,ex in ((m&sideB,exA),(m&~sideB,exB)):
            if sm.any():
                keep=np.ones(len(SF),bool); keep[ex]=False
                if 'SFg' in globals() and len(SFg)!=len(SF): pass
                _,_,cp=igl.point_mesh_squared_distance(V[vs[sm]],S,SF[keep]); V[vs[sm]]=(1-BL)*V[vs[sm]]+BL*cp
        done|=m
    if (~done).any():
        _,_,cp=igl.point_mesh_squared_distance(V[vs[~done]],S,SFg); V[vs[~done]]=(1-BL)*V[vs[~done]]+BL*cp
    V2=V.copy()
    for v in vs: V2[v]=(1-SMW)*V[v]+SMW*np.mean(V[list(nb[v])],axis=0)
    V=V2; moved[vs]=True
np.savez_compressed(out,V=V,F=z['F'],Q=Q); np.save(out.replace('.npz','_moved.npy'),np.where(moved)[0])
print('history',hist,'moved verts',int(moved.sum()))
