# slidering.py CAGE COL OUT 'id:ytarget:side;...' : move thigh-ring verts along the source z-outline to the point with given y on the inner side
import numpy as np, sys
from earsl import slice_loops
z=np.load(sys.argv[1]); V=z['V'].copy(); F=z['F']
for it in sys.argv[4].split(';'):
    i,yt,sd=it.split(':'); i=int(i); yt=float(yt); zz=V[i,2]
    best=None
    for P,c in slice_loops(2,zz):
        m=(P[:,0]>-6)&(P[:,0]<8)&(P[:,1]>-60)&(P[:,1]<-30)
        if not m.any(): continue
        Q=P[m]; Q=Q[(Q[:,0]<1.3) if sd=='R' else (Q[:,0]>1.3)]
        if not len(Q): continue
        k=np.argmin(abs(Q[:,1]-yt)+0.2*abs(Q[:,0]-V[i,0])); cand=Q[k]
        if best is None or abs(cand[1]-yt)<abs(best[1]-yt): best=cand
    print(i,V[i].round(2),'->',best.round(2)); V[i]=best
np.savez_compressed(sys.argv[3],V=V,F=F); np.save(sys.argv[3].replace('.npz','_col.npy'),np.load(sys.argv[2]))
