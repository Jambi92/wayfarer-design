import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fs=sys.argv[2:]; x=np.linspace(0,8,321); u=np.linspace(0,9,361)
fig,ax=plt.subplots(1,6,figsize=(24,5))
cols=['k','r','b','g','m']
for j,fn in enumerate(fs):
    z=np.load(fn)
    for i,fv in enumerate(['8','6','4','2','0','-2']):
        ax[i].contour(x,u,z[fv],[0],colors=cols[j],linewidths=1.2); ax[i].set_title('F='+fv); ax[i].set_aspect('equal'); ax[i].set_xlim(1,8); ax[i].set_ylim(1,8); ax[i].grid(alpha=.3)
plt.tight_layout(); plt.savefig(sys.argv[1],dpi=70)
