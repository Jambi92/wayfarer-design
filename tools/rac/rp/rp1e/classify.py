# blender-python classify.py -- SIM.npz OUT.json : cluster L4 self-x pairs and measure fold/contact, source gap, openness, face size
import sys, numpy as np, json, bpy, mathutils
from mathutils.bvhtree import BVHTree
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
a=sys.argv[sys.argv.index('--')+1:]; sp,outp=a[0],a[1]
z=np.load(sp); V=z['V'].copy(); V[:,1]*=-1; Q=z['Q']; P=np.load(sp.replace('.npz','_pairs.npy'))
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
zn=np.load('/home/claude/stc/rp1/zones.npz'); zone=zn['zone']; names=list(zn['names'])
col=np.load('col_r2.npy')
fn=np.cross(S[SF[:,1]]-S[SF[:,0]],S[SF[:,2]]-S[SF[:,0]]); vn=np.zeros_like(S)
for k in range(3): np.add.at(vn,SF[:,k],fn)
vn/=np.linalg.norm(vn,axis=1,keepdims=True)+1e-12
bvh=BVHTree.FromPolygons(S.tolist(),SF.tolist())
kS=cKDTree(S)
C=np.array([V[q[q>=0]].mean(0) for q in Q])
def nrm(q):
    q=q[q>=0]; n=np.cross(V[q[2]]-V[q[0]],V[q[3%len(q)]]-V[q[1]]); return n/(np.linalg.norm(n)+1e-12)
X=np.array([0.5*(C[i]+C[j]) for i,j in P]) if len(P) else np.zeros((0,3))
pr=cKDTree(X).query_pairs(0.6,output_type='ndarray') if len(X) else np.zeros((0,2),int)
A=coo_matrix((np.ones(len(pr)),(pr[:,0],pr[:,1])),shape=(len(X),len(X))); n,lab=connected_components(A,directed=False)
dirs=np.array([[x,y,zz] for x in (-1,0,1) for y in (-1,0,1) for zz in (-1,0,1) if (x,y,zz)!=(0,0,0)],float); dirs/=np.linalg.norm(dirs,axis=1,keepdims=True)
res=[]
for k in range(n):
    idx=np.where(lab==k)[0]; c=X[idx].mean(0)
    d,i=kS.query(c); zname=str(names[zone[i]])
    dots=[float(nrm(Q[P[t][0]])@nrm(Q[P[t][1]])) for t in idx[:200]]
    es=[np.linalg.norm(V[Q[P[t][0]][0]]-V[Q[P[t][0]][1]]) for t in idx[:200]]
    # source gap near the cluster: opposing-normal pairs among source verts within 1.2 cm
    nb=kS.query_ball_point(c,1.2)
    gap=None
    if len(nb)>3:
        nb=np.array(nb); T=cKDTree(S[nb]); dd,jj=T.query(S[nb],k=min(40,len(nb)))
        best=9
        for r in range(len(nb)):
            for dist,j in zip(dd[r][1:],jj[r][1:]):
                if vn[nb[r]]@vn[nb[j]]<-0.5 and (S[nb[j]]-S[nb[r]])@vn[nb[r]]>0: best=min(best,dist); break
        gap=float(best) if best<9 else None
    # openness: from the nearest source point, offset 0.05 along its normal, fraction of rays escaping 3 cm
    p0=S[i]+vn[i]*0.05; esc=0
    for dv in dirs:
        hit=bvh.ray_cast(mathutils.Vector(p0),mathutils.Vector(dv),3.0)
        if hit[0] is None: esc+=1
    amp=0.0
    for t in idx[:400]:
        for fi in P[t]:
            h=bvh.find_nearest(mathutils.Vector(C[fi]))
            if h[0] is not None: amp=max(amp,h[3])
    cs=sorted(set(int(col[kS.query(C[t])[1]]) for pr_ in P[idx[:100]] for t in pr_))
    res.append(dict(n=int(len(idx)),centre=c.round(2).tolist(),zone=zname,dot_med=float(np.median(dots)),face=float(np.median(es)),gap=gap,open=esc/len(dirs),cols=cs,amp_mm=amp*10))
res.sort(key=lambda r:-r['n'])
json.dump(res,open(outp,'w'),indent=0)
for r in res[:40]: print('%5d %-18s c=%s dot=%.2f face=%.3f gap=%s open=%.2f cols=%s amp=%.2fmm'%(r['n'],r['zone'],r['centre'],r['dot_med'],r['face'],None if r['gap'] is None else round(r['gap'],3),r['open'],r['cols'],r['amp_mm']))
