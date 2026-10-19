import numpy as np, json, sys
from scipy.spatial import cKDTree
cg=sys.argv[1]
S=np.load('/home/claude/stc/rp1/weld.npz')['V']; sc=np.load('col_r2.npy')
V=np.load(cg)['V']; c=np.load(cg.replace('.npz','_col.npy'))
d,i=cKDTree(S).query(V); m=(c==1)&(sc[i]==16)
J=json.load(open(cg.replace('.npz','_axT.json'))); keep=set(J['rings']['JT'])|set(J['rings']['T1'])
m&=~np.isin(np.arange(len(V)),list(keep)); c[m]=16; np.save(cg.replace('.npz','_col.npy'),c); print('tail recol',m.sum())
