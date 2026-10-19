import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V']; d=np.load(sys.argv[1]); box=np.array([float(v) for v in sys.argv[2].split(',')]).reshape(3,2); outp=sys.argv[3]
m=((S>box[:,0])&(S<box[:,1])).all(1); P=S[m]; dd=d[m]
fig,ax=plt.subplots(1,3,figsize=(24,8))
for a,(i,j) in zip(ax,[(0,2),(1,2),(0,1)]):
    o=np.argsort(dd); a.scatter(P[o,i],P[o,j],s=1.2,c=np.clip(dd[o],0,6),cmap='jet',vmin=0,vmax=6); a.set_aspect('equal'); a.grid(alpha=.3)
plt.tight_layout(); plt.savefig(outp,dpi=60)
