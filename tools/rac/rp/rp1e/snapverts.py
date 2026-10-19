# snapverts.py in.npz out.npz ids(comma) [offset_cm] : move listed cage verts to their nearest source surface point (+offset along source normal)
import numpy as np,sys
from scipy.spatial import cKDTree
z=np.load(sys.argv[1]); V=z['V'].copy(); F=z['F']
ids=[int(x) for x in sys.argv[3].split(',')]; off=float(sys.argv[4]) if len(sys.argv)>4 else 0.0
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F']
C=S[SF].mean(1); t=cKDTree(C)
for i in ids:
    _,f=t.query(V[i],k=32); best=None
    for fi in f:
        a,b,c=S[SF[fi]]
        # closest point on triangle (approx via barycentric clamp)
        ab,ac,ap=b-a,c-a,V[i]-a; n=np.cross(ab,ac); n/=np.linalg.norm(n)
        p=V[i]-n*np.dot(V[i]-a,n)
        M=np.array([ab,ac]).T; uv=np.linalg.lstsq(M,p-a,rcond=None)[0]; u,v=np.clip(uv,0,1)
        if u+v>1: s=u+v; u/=s; v/=s
        q=a+u*ab+v*ac; d=np.linalg.norm(q-V[i])
        if best is None or d<best[0]: best=(d,q,n)
    print(i,V[i].round(3),'->',best[1].round(3),'d',round(best[0],3)); V[i]=best[1]+off*best[2]
np.savez_compressed(sys.argv[2],V=V,F=F)
