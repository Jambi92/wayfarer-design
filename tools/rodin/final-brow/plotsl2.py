import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
x=np.linspace(4,7.5,281); u=np.linspace(3.5,7.5,321); ks=['4.5','4','3.5','3','2.5','2','1.5']
fig,ax=plt.subplots(1,7,figsize=(28,5)); cols='krbgm'
for j,fn in enumerate(sys.argv[2:]):
    z=np.load(fn)
    for i,k in enumerate(ks): ax[i].contour(x,u,z[k],[0],colors=cols[j]); ax[i].set_title('F='+k); ax[i].set_aspect('equal'); ax[i].grid(alpha=.3)
plt.tight_layout(); plt.savefig(sys.argv[1],dpi=60)
