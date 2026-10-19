# blender-python devclass.py -- SIM_TAG zone lim [maxclusters] : deviation clusters with source gap (opposed sheet) + openness
import sys, numpy as np, bpy, mathutils, json
from mathutils.bvhtree import BVHTree
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
a=sys.argv[sys.argv.index('--')+1:]; tag,zn,lim=a[0],a[1],float(a[2]); mc=int(a[3]) if len(a)>3 else 12
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
zz=np.load('/home/claude/stc/rp1/zones.npz'); zone=zz['zone']; names=list(zz['names'])
d=np.load('sim_%s_L4_dsp.npy'%tag)
fn=np.cross(S[SF[:,1]]-S[SF[:,0]],S[SF[:,2]]-S[SF[:,0]]); vn=np.zeros_like(S)
for k in range(3): np.add.at(vn,SF[:,k],fn)
vn/=np.linalg.norm(vn,axis=1,keepdims=True)+1e-12
bvh=BVHTree.FromPolygons(S.tolist(),SF.tolist()); kS=cKDTree(S)
m=(d>lim)&((zone==names.index(zn)) if zn!='all' else True); idx=np.where(m)[0]; P=S[idx]
pr=cKDTree(P).query_pairs(1.0,output_type='ndarray'); A=coo_matrix((np.ones(len(pr)),(pr[:,0],pr[:,1])),shape=(len(P),len(P)))
n,lab=connected_components(A,directed=False)
dirs=np.array([[x,y,z] for x in (-1,0,1) for y in (-1,0,1) for z in (-1,0,1) if (x,y,z)!=(0,0,0)],float); dirs/=np.linalg.norm(dirs,axis=1,keepdims=True)
res=[]
for k in sorted(range(n),key=lambda k:-(lab==k).sum())[:mc]:
    ii=idx[lab==k]; dd=d[ii]; j=ii[np.argmax(dd)]
    # gap: ray from the worst point along its normal (outward) -> first hit distance (opposite sheet)
    gaps=[]
    for t in ii[np.argsort(-d[ii])][:20]:
        h=bvh.ray_cast(mathutils.Vector(S[t]+vn[t]*0.002),mathutils.Vector(vn[t]),5.0)
        gaps.append(h[3] if h[0] is not None else 9.9)
    esc=0
    for dv in dirs:
        h=bvh.ray_cast(mathutils.Vector(S[j]+vn[j]*0.05),mathutils.Vector(dv),3.0)
        if h[0] is None: esc+=1
    res.append(dict(n=int(len(ii)),max_mm=float(dd.max()),centre=S[ii].mean(0).round(2).tolist(),worst=S[j].round(2).tolist(),gap_mm_med=float(np.median(gaps)*10),gap_mm_min=float(np.min(gaps)*10),open=esc/len(dirs)))
for r in res: print('%5d max %5.1f c=%s gap med %.1f min %.1f mm open %.2f'%(r['n'],r['max_mm'],r['centre'],r['gap_mm_med'],r['gap_mm_min'],r['open']))
json.dump(res,open('dev_%s_%s.json'%(tag,zn),'w'))
