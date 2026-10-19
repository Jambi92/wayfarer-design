import numpy as np, sys
from scipy.spatial import cKDTree
w=np.load('/home/claude/stc/rp1/weld_a.npz'); S=w['V']; z=np.load('/home/claude/stc/rp1/zones.npz'); zone=z['zone']; names=list(z['names'])
wb=np.load('/home/claude/stc/rp1/weld.npz')
seg={}
for h in 'RL':
    q=np.load('segH_%s.npz'%h); seg[h]=(q['used'],q['lab'])
lab=np.full(len(S),-1)
for h in 'RL': lab[seg[h][0]]=seg[h][1]+(0 if h=='R' else 10)
T=cKDTree(S)
for p in sys.argv[1:]:
    C=np.load(p)
    if not len(C): print(p,0); continue
    d,i=T.query(C); zz=zone[i]
    out={names[k]:int((zz==k).sum()) for k in range(len(names)) if (zz==k).sum()}
    g=C[zz==0]; out['gen_u>125']=int((g[:,2]>125).sum()); out['gen_60-125']=int(((g[:,2]>60)&(g[:,2]<=125)).sum()); out['gen_u<60']=int((g[:,2]<=60).sum())
    hl=lab[i][lab[i]>=0]; out['handlabels']=dict(zip(*[x.tolist() for x in np.unique(hl,return_counts=True)]))
    print(p,out)
