import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
p=sys.argv[1]; s=sys.argv[2]; out=sys.argv[3]
C=np.load(p)*np.array([1,-1,1])
q=np.load('segH_%s.npz'%s); u=q['used']; V=np.load('/home/claude/stc/rp1/weld.npz')['V'][u]
lo=V.min(0)-1; hi=V.max(0)+1; m=((C>lo)&(C<hi)).all(1); C=C[m]; print(len(C))
fig,ax=plt.subplots(1,3,figsize=(33,12))
for a,(i,j,k,sg) in zip(ax,[(0,1,2,1),(0,2,1,1),(1,2,0,-1 if s=='R' else 1)]):
    o=np.argsort(sg*V[:,k]); a.scatter(V[o,i],V[o,j],c='0.8',s=2); a.scatter(C[:,i],C[:,j],c='r',s=8); a.set_aspect('equal'); a.grid(True)
plt.savefig(out,dpi=40,bbox_inches='tight')
