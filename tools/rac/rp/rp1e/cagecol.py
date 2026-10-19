import numpy as np, json, sys
from scipy.spatial import cKDTree
cg=sys.argv[1]; colp=sys.argv[2]
z=np.load(cg); V=z['V']; meta=json.load(open(cg.replace('.npz','_meta.json')))
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V']; col=np.load(colp)
d,i=cKDTree(S).query(V); cc=col[i].copy()
import os
segp=cg.replace('.npz','_seg.json')
if os.path.exists(segp):
    sg=json.load(open(segp)); armall=set()
    for s_ in sg: armall|=set(sg[s_]['arm'])
    for v in range(len(V)):
        if v in armall: cc[v]=2
        elif cc[v]==2 and 115<V[v,2]<170: cc[v]=1
for s,m in meta.items():
    for role,t in m['tubes'].items():
        for r in t['rings']: cc[r]=4 if role in ('index','ring') else (5 if role=='thumb' else 3)
    for nm in m['P']: cc[m['P'][nm]]=3
np.save(cg.replace('.npz','_col.npy'),cc); print(np.bincount(cc))
