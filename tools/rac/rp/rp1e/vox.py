import numpy as np, igl, time, sys
s=sys.argv[1]; h=float(sys.argv[2])  # voxel cm
w=np.load('weld.npz'); V=w['V'].astype(np.float64); F=w['F'].astype(np.int64)
m=w['w_hand_'+s]>0.5; lo=V[m].min(0)-1.0; hi=V[m].max(0)+1.0
ax=[np.arange(lo[i],hi[i],h) for i in range(3)]; G=np.stack(np.meshgrid(*ax,indexing='ij'),-1).reshape(-1,3)
t=time.time(); wn=igl.fast_winding_number(V,F,G); print('fwn',time.time()-t,len(G))
inside=(wn>0.5).reshape(len(ax[0]),len(ax[1]),len(ax[2]))
np.savez_compressed('/home/claude/stc/rp1e/vox_%s.npz'%s,inside=inside,lo=lo,h=h,shape=inside.shape)
print(inside.shape, inside.sum())
