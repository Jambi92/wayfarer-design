import numpy as np, sys, igl
from scipy.spatial import cKDTree
p=sys.argv[1]; m=np.load(p); V=m['V']*np.array([1,-1,1]); F=m['F']
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
d,I,C=igl.point_mesh_squared_distance(V,S,SF); d=np.sqrt(d)*10
np.save(p.replace('.npz','_p2s.npy'),d.astype(np.float32))
lab=np.full(len(S),-1)
for h,off in [('R',0),('L',10)]:
    q=np.load('segH_%s.npz'%h); lab[q['used']]=q['lab']+off
vl=lab[SF[I,0]]
for k in sorted(set(vl.tolist())):
    if k<0: continue
    x=d[vl==k]; bad=V[vl==k][x>1.5]
    print(k,'n',len(x),'over1.5',int((x>1.5).sum()),'max %.1f'%x.max(), bad.mean(0).round(1) if len(bad) else '')
