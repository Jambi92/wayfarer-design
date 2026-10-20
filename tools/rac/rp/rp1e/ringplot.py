import numpy as np, json, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
z=np.load(sys.argv[1]);V=z['V'];m=json.load(open(sys.argv[1].replace('.npz','_meta.json'))); dis=[int(x) for x in sys.argv[3].split(',')]
views=[(1,2),(0,2),(0,1)]
fig,ax=plt.subplots(len(dis),3,figsize=(27,8*len(dis))); ax=np.atleast_2d(ax)
for row,di in enumerate(dis):
    rs=m['rings'][di]
    for a,(i,j) in zip(ax[row],views):
        for k,r in enumerate(rs[:5]):
            P=V[r+r[:1]]; a.plot(P[:,i],P[:,j],'-o',ms=3,label='r%d'%k)
            for t,v in enumerate(r): a.text(V[v,i],V[v,j],str(t),fontsize=8)
        a.legend(); a.grid(alpha=.3); a.set_aspect('equal'); a.set_title('digit %d axes %d,%d'%(di,i,j))
plt.tight_layout(); plt.savefig(sys.argv[2],dpi=50)
