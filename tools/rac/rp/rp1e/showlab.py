import numpy as np,sys,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
s=sys.argv[1]
z=np.load('/home/claude/stc/rp1e/lab_%s.npz'%s);lab=z['lab'];lo=z['lo'];h=float(z['h'])
w=np.load('weld.npz');V=w['V'];m=w['w_hand_'+s]>0.5
I=np.argwhere(lab>0);P=I*h+lo;L=lab[tuple(I.T)]
d,i=cKDTree(P).query(V[m]);vl=L[i]
np.save('/home/claude/stc/rp1e/vlab_%s.npy'%s,np.c_[np.where(m)[0],vl])
X=V[m];cm={1:'0.7',2:'orange',3:'r',4:'g',5:'b',6:'m',7:'c'}
fig,ax=plt.subplots(2,3,figsize=(27,20))
for a,(i_,j,k,sg) in zip(ax.ravel(),[(0,2,1,-1),(0,2,1,1),(1,2,0,1),(1,2,0,-1),(0,1,2,1),(0,1,2,-1)]):
    o=np.argsort(sg*X[:,k]); a.scatter(X[o,i_],X[o,j],c=[cm[q] for q in vl[o]],s=0.5); a.set_aspect('equal')
    a.set_title('axes %d,%d viewed from %s%d'%(i_,j,'+' if sg>0 else '-',k))
plt.savefig('/home/claude/stc/rp1e/lab_%s.png'%s,dpi=45,bbox_inches='tight')
