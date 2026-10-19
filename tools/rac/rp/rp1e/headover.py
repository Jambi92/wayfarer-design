import numpy as np, sys
S=np.load('/home/claude/stc/rp1/weld.npz')['V']; z=np.load('/home/claude/stc/rp1/zones.npz'); zone=z['zone']; names=list(z['names']); hi=names.index('head_muzzle_ears')
d=np.load(sys.argv[1]); m=(zone==hi); P=S[m]; dd=d[m]; o=dd>1.5
print('head pts',m.sum(),'over',o.sum(), '%.2f%%'%(o.mean()*100), 'max %.1f'%dd.max())
boxes={'earL':(4,24,-62,-36,186,210),'earR':(-20,0,-62,-36,186,210),'grooveR':(-8,0,-52,-42,172,183),'grooveL':(4,12,-52,-42,172,183),
 'chin/jaw other':(-14,18,-70,-36,160,186),'muzzle front':(-14,18,-75,-55,176,200),'eyes/brow':(-14,18,-62,-50,186,200)}
used=np.zeros(len(P),bool)
for k,(x0,x1,y0,y1,z0,z1) in boxes.items():
    b=(P[:,0]>x0)&(P[:,0]<x1)&(P[:,1]>y0)&(P[:,1]<y1)&(P[:,2]>z0)&(P[:,2]<z1)&~used; used|=b
    print('%-15s pts %6d over %5d (%.1f%%) max %.1f'%(k,b.sum(),(o&b).sum(),100*(o&b).sum()/max(b.sum(),1),dd[b].max() if b.any() else 0))
r=~used; print('%-15s pts %6d over %5d max %.1f'%('rest',r.sum(),(o&r).sum(),dd[r].max()))
Q=P[o&r]
if len(Q): print(' rest over bbox',Q.min(0).round(1),Q.max(0).round(1))
