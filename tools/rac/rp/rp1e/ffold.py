import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
p=sys.argv[1]; s=sys.argv[2]; out=sys.argv[3]
C=np.load(p)*np.array([1,-1,1])
q=np.load('fseg_%s.npz'%s); V=np.load('/home/claude/stc/rp1/weld.npz')['V'][q['used']]; l=q['lab']
m=(C[:,2]<17)&(np.sign(C[:,0])==(1 if s=='L' else -1)); C=C[m]
cm={0:'r',1:'g',2:'b',3:'m',9:'0.8'}; col=np.array([cm[x] for x in l])
fig,ax=plt.subplots(1,3,figsize=(33,12))
for a,(i,j,k,sg) in zip(ax,[(0,1,2,1),(1,2,0,1 if s=='R' else -1),(0,1,2,-1)]):
    o=np.argsort(sg*V[:,k]); a.scatter(V[o,i],V[o,j],c=col[o],s=1,alpha=0.3); a.scatter(C[:,i],C[:,j],c='k',s=10); a.set_aspect('equal'); a.grid(True)
plt.savefig(out,dpi=40,bbox_inches='tight')
