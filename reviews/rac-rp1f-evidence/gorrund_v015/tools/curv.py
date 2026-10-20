# mean curvature of the v014 production near given centres -> npy (per vertex, 0 elsewhere)
import numpy as np, igl, sys, json
z=np.load('/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/designs/design_v014_production_L4.npz'); V=z['V']*np.array([1,-1,1]); F=z['F'][:,::-1].astype(np.int64)
cs=json.load(open(sys.argv[1])); R=float(sys.argv[2]); H=np.zeros(len(V))
for c in cs:
    fm=np.linalg.norm(V[F].mean(1)-np.array(c),axis=1)<R; Fl=F[fm]; u=np.unique(Fl); loc=-np.ones(len(V),int); loc[u]=np.arange(len(u))
    _,_,k1,k2,_=igl.principal_curvature(V[u],loc[Fl],radius=5); H[u]=0.5*(k1+k2)
np.save(sys.argv[3],H); print(np.percentile(H[H!=0],[2,50,98]))
