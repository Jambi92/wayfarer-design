# ringfit.py CAGE COL OUT spec.json ; spec=[{"loop":[ids], "z":z or null(mean), "mode":"angle"|"arc", "frac":1.0}]
import numpy as np, sys, json
from earsl import slice_loops
from matplotlib.path import Path
cg,colf,out,spec=sys.argv[1:5]; SP=json.load(open(spec))
z=np.load(cg); V=z['V'].copy(); F=z['F']
for row in SP:
    ring=row['loop']; cur=V[ring]; zz=row.get('z') or float(cur[:,2].mean()); c=cur[:,:2].mean(0)
    Ls=[P for P,cl in slice_loops(2,zz) if cl]
    inside=[P for P in Ls if Path(P[:,:2]).contains_point(c)]
    P=min(inside,key=lambda P:len(P)) if inside else min(Ls,key=lambda P:np.linalg.norm(P[:,:2]-c,axis=1).min())
    fr=row.get('frac',1.0)
    if row.get('mode','angle')=='angle':
        th=np.arctan2(P[:,1]-c[1],P[:,0]-c[0])
        for i,v in enumerate(ring):
            t=np.arctan2(cur[i,1]-c[1],cur[i,0]-c[0]); d=np.abs(np.angle(np.exp(1j*(th-t))))
            # ray-cast: among outline points near the angle take the farthest
            cand=np.where(d<np.radians(2.5))[0]
            if len(cand)==0: cand=[int(np.argmin(d))]
            k=cand[int(np.argmax(np.linalg.norm(P[cand,:2]-c,axis=1)))]
            V[v]=cur[i]+fr*(np.r_[P[k,:2],zz]-cur[i]) if row.get('flatz',True) else cur[i]+fr*(P[k]-cur[i])
    print('ring',len(ring),'z %.1f'%zz,'moved max %.1f'%np.linalg.norm(V[ring]-cur,axis=1).max())
np.savez_compressed(out,V=V,F=F); np.save(out.replace('.npz','_col.npy'),np.load(colf))
