import numpy as np, json, sys, os
from scipy.spatial import cKDTree
cg=sys.argv[1]; colp=sys.argv[2]
z=np.load(cg); V=z['V']; meta=json.load(open(cg.replace('.npz','_meta.json')))
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V']; col=np.load(colp)
d,i=cKDTree(S).query(V); cc=col[i].copy()
import os
tc={'t1':3,'t2':4,'t3':3,'t4':4} if os.environ.get('TC','1')=='1' else {'t1':5,'t2':4,'t3':5,'t4':4}
for s,m in meta.items():
    for nm,r in m['rings'].items(): cc[np.array(r)]=3 if nm in ('K','S5','S4') else cc[np.array(r)]
    for nm,T in m['tubes'].items():
        for r in T[int(os.environ.get('SKIP0','0')):]: cc[np.array(r)]=tc[nm]
np.save(cg.replace('.npz','_col.npy'),cc); print(np.bincount(cc))
