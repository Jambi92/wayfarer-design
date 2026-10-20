import numpy as np, sys
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
tag,zn=sys.argv[1],sys.argv[2]; lim=float(sys.argv[3]) if len(sys.argv)>3 else 1.5
S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); z=np.load('/home/claude/stc/rp1/zones.npz'); names=list(z['names']); zone=z['zone']
d=np.load('sim_%s_L4_dsp.npy'%tag); m=(zone==names.index(zn))&(d>lim); P=S[m]; dd=d[m]
if len(P)==0: print('none'); sys.exit()
pr=cKDTree(P).query_pairs(0.3,output_type='ndarray'); A=coo_matrix((np.ones(len(pr)),(pr[:,0],pr[:,1])),shape=(len(P),len(P))); n,lab=connected_components(A,directed=False)
rows=sorted([((lab==k).sum(),P[lab==k].mean(0).round(2).tolist(),round(float(dd[lab==k].max()),2)) for k in range(n)],reverse=True)
for r in rows[:int(sys.argv[4]) if len(sys.argv)>4 else 12]: print(r)
