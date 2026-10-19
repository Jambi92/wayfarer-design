import numpy as np, sys
from scipy.spatial import cKDTree
w=np.load('/home/claude/stc/rp1/weld_a.npz'); S=w['V']; z=np.load('/home/claude/stc/rp1/zones.npz'); zone=z['zone']; names=list(z['names'])
T=cKDTree(S)
for p in sys.argv[1:]:
    C=np.load(p)
    if not len(C): print(p,0); continue
    d,i=T.query(C[:,:3]); zz=zone[i]
    out={str(names[k]):int((zz==k).sum()) for k in range(len(names)) if (zz==k).sum()}
    g=C[zz==0]
    out['axilla(gen z130-165)']=int(((g[:,2]>130)&(g[:,2]<165)).sum()); out['perin(gen z80-115,|x|<20)']=int(((g[:,2]>80)&(g[:,2]<115)&(abs(g[:,0])<20)).sum())
    out['gen other']=len(g)-out['axilla(gen z130-165)']-out['perin(gen z80-115,|x|<20)']
    print(p,len(C),out)
