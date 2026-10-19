import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V']; d=np.load(sys.argv[1]); outp=sys.argv[2]; sg=float(sys.argv[3]) if len(sys.argv)>3 else 1
X=S[:,0] if sg>0 else 4-S[:,0]; m=(X>4)&(X<24)&(S[:,1]>-62)&(S[:,1]<-36)&(S[:,2]>186)
P=S[m]; dd=d[m]
fig,ax=plt.subplots(1,3,figsize=(24,8))
for a,(i,j) in zip(ax,[(0,2),(1,2),(0,1)]):
    o=np.argsort(dd); a.scatter(P[o,i],P[o,j],s=1.5,c=np.clip(dd[o],0,10),cmap='jet',vmin=0,vmax=10); a.set_aspect('equal'); a.grid(alpha=.3)
plt.tight_layout(); plt.savefig(outp,dpi=60)
