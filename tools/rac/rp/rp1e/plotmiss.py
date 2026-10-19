import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=sys.argv[1]; p=sys.argv[2]; labs=[int(x) for x in sys.argv[3].split(',')]; out=sys.argv[4]
q=np.load('segH_%s.npz'%s); u=q['used']; l=q['lab']; V=np.load('/home/claude/stc/rp1/weld.npz')['V']
d=np.load(p.replace('.npz','_dsp.npy'))
sel=u[np.isin(l,labs)]; X=V[sel]; D=d[sel]
fig,ax=plt.subplots(2,3,figsize=(33,22))
for a,(i,j,k,sg) in zip(ax.ravel(),[(0,1,2,1),(0,1,2,-1),(0,2,1,1),(0,2,1,-1),(1,2,0,1),(1,2,0,-1)]):
    o=np.argsort(sg*X[:,k]); sc=a.scatter(X[o,i],X[o,j],c=np.clip(D[o],0,3),s=4,cmap='inferno',vmin=0,vmax=3); a.set_aspect('equal'); a.grid(True)
    a.set_title('view from %s%d'%('+' if sg>0 else '-',k))
plt.savefig(out,dpi=35,bbox_inches='tight')
