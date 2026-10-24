# nailsmooth.py IN OUT ITERS : extra Taubin smoothing restricted to nail-fold bands (hands: SDF groove distance < 0.45 cm)
import sys, numpy as np, trimesh, scipy.sparse as sp
sys.path.insert(0,'/tmp/claude-0/src3d/v4/tools')
from hand_model import DEF, scaled, finger_chain, nail_groove
from hand_frame import frame
d=np.load(sys.argv[1]); V=d['V'].astype(float).copy(); F=d['Q'].astype(np.int64); it=int(sys.argv[3])
p=scaled(DEF); w=np.zeros(len(V))
for side in ('L','R'):
    W,M=frame(side); L=(V-W)@M; near=np.linalg.norm(L-[20,0,-4],axis=1)<16
    gs=[]
    for nm,f in p['fingers'].items():
        J,dirs,dors=finger_chain(f['mcp'],f['L'],f['splay'],f['flex']); g,_=nail_groove(L[near],J[2],dirs[2],dors[2],f['L'][2],f['r'][3],p['flat'],p['nail']); gs.append(g)
    g=np.min(gs,0); ww=np.clip(1-(g-0.0)/0.45,0,1); w[near]=np.maximum(w[near],ww)
print('weighted verts',(w>0).sum())
m=trimesh.Trimesh(V,F,process=False); A=m.edges_sparse.astype(float); deg=np.asarray(A.sum(1)).ravel(); Lp=sp.diags(1/deg)@A
for k in range(it):
    for lam in (0.5,-0.53):
        V=V+(lam*w)[:,None]*(Lp@V-V)
np.savez(sys.argv[2],**{**{k:d[k] for k in d.files},'V':V,'nail_smooth_w':w})
