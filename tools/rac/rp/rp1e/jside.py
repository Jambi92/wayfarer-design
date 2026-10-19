import numpy as np, json, sys
from scipy.spatial import cKDTree
cg,ring,jin,out=sys.argv[1:5]; FS=float(sys.argv[5])
S=np.load('/home/claude/stc/rp1/weld.npz')['V']; kd=cKDTree(S)
z=np.load(cg);V=z['V'];R=json.load(open(ring))['rungs']; J=json.load(open(jin))
for a,b in R[:-1]:
    k='%d,%d'%(a,b)
    if k in J: continue
    mid=(V[a]+V[b])/2; d,i=kd.query(mid); J[k]=(mid+FS*(S[i]-mid)).tolist()
json.dump(J,open(out,'w'))
