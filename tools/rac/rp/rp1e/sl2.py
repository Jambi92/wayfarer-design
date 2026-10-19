import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from earsl import slice_loops
ax_i=int(sys.argv[1]); vals=[float(x) for x in sys.argv[2].split(',')]; box=[float(x) for x in sys.argv[3].split(',')]; outp=sys.argv[4]
oth=[k for k in range(3) if k!=ax_i]; n=len(vals); c=4; r=(n+c-1)//c
cg=sys.argv[5] if len(sys.argv)>5 else None
fig,axs=plt.subplots(r,c,figsize=(5*c,5*r)); axs=np.array(axs).ravel()
for a,val in zip(axs,vals):
    for P,cl in slice_loops(ax_i,val):
        a.plot(P[:,oth[0]],P[:,oth[1]],'k-' if cl else 'g-',lw=0.8)
    a.set_xlim(box[0],box[1]); a.set_ylim(box[2],box[3]); a.set_aspect('equal'); a.set_title('%s=%.1f'%('xyz'[ax_i],val)); a.grid(alpha=.3)
plt.tight_layout(); plt.savefig(outp,dpi=60)
