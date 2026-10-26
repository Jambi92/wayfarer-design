# rayproj.py IN.npz OUT.npz [maxd] : (Blender python) move each production vertex along its normal (both ways, up to maxd cm)
# onto the nearest source surface of its own or adjacent part whose normal agrees; then caller re-runs nearest projection.
import sys, numpy as np, json
sys.path.insert(0,'/tmp/claude-0/rt')
a=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
import bpy
from mathutils.bvhtree import BVHTree
from mathutils import Vector
from common import PARTS, PID, ADJ
z=np.load(a[0]); V=z['V'].astype(float); Q=z['Q']; FP=z['FP']; maxd=float(a[2]) if len(a)>2 else 2.0
M=np.load('/tmp/claude-0/src3d/v5/v005.npz'); SV=M['V'].astype(float); SF=M['Q'].astype(int); fl=np.load('/tmp/claude-0/rt/flab.npy')
# vertex part = majority of incident faces
import scipy.sparse as sp
Mvp=sp.coo_matrix((np.ones(Q.size),(Q.ravel(),np.repeat(FP,4))),shape=(len(V),len(PARTS))).tocsr(); vp=np.asarray(Mvp.argmax(1)).ravel()
n=np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,1]]); N=np.zeros_like(V)
for k in range(4): np.add.at(N,Q[:,k],n)
N/=np.maximum(np.linalg.norm(N,axis=1),1e-12)[:,None]
fn=np.cross(SV[SF[:,1]]-SV[SF[:,0]],SV[SF[:,2]]-SV[SF[:,0]]); fn/=np.maximum(np.linalg.norm(fn,axis=1),1e-12)[:,None]
out=V.copy(); moved=0
SKIP={PID[p] for p in PARTS if p.startswith(('hand','thumb','index','middle','ring','pinky','hallux','toe'))}
for p in np.unique(vp):
    if p in SKIP: continue
    ids=[p]+[PID[q] for q in ADJ.get(PARTS[p],())]
    fidx=np.nonzero(np.isin(fl,ids))[0]
    used=np.unique(SF[fidx]); rm=-np.ones(len(SV),int); rm[used]=np.arange(len(used))
    bvh=BVHTree.FromPolygons([Vector(v) for v in SV[used]],rm[SF[fidx]].tolist())
    for i in np.nonzero(vp==p)[0]:
        o=Vector(V[i]); best=None
        for sgn in (1,-1):
            d=Vector(N[i]*sgn); oo=o.copy(); acc=0.0
            for _ in range(4):
                hit,nrm,fi,dist=bvh.ray_cast(oo,d,maxd-acc)
                if hit is None: break
                acc+=dist
                if (np.array(nrm)@N[i])>=0.3:
                    if best is None or acc<best[0]: best=(acc,np.array(hit))
                    break
                oo=hit+d*1e-4
        if best is not None: out[i]=best[1]; moved+=1
np.savez(a[1],V=out,Q=Q,FP=FP); print('ray-projected',moved,'of',len(V))
