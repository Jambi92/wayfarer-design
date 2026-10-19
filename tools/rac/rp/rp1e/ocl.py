import numpy as np, sys
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
z=np.load(sys.argv[1]); zn=sys.argv[2] if len(sys.argv)>2 else None
S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); names=list(np.load('/home/claude/stc/rp1/zones.npz')['names'])
idx,op,d,zo=z['idx'],z['op'],z['d'],z['zone']
if zn: m=zo==names.index(zn); idx,op,d,zo=idx[m],op[m],d[m],zo[m]
P=S[idx]; pr=cKDTree(P).query_pairs(0.3,output_type='ndarray')
A=coo_matrix((np.ones(len(pr)),(pr[:,0],pr[:,1])),shape=(len(P),len(P))); n,lab=connected_components(A,directed=False)
rows=[]
for k in range(n):
    m=lab==k
    rows.append((m.sum(),names[zo[m][0]],P[m].mean(0).round(2).tolist(),round(float(d[m].max()),1),round(float(op[m].mean()),2),round(float((op[m]>=0.5).mean()),2)))
for r in sorted(rows,reverse=True)[:int(sys.argv[3]) if len(sys.argv)>3 else 15]: print(r)
