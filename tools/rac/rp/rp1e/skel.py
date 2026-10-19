import numpy as np, sys, time
from scipy.spatial import cKDTree
from scipy import ndimage as ndi
from skimage.morphology import skeletonize
s=sys.argv[1]
z=np.load('/home/claude/stc/rp1e/vox_%s.npz'%s); inside=z['inside']; lo=z['lo']; h=float(z['h'])
w=np.load('weld.npz'); V=w['V'].astype(float)
lab=np.full(len(V),-1); lab[w['w_hand_'+s]>0.5]=1; lab[w['w_forearm_'+s]>0.5]=2
idx=np.argwhere(inside); P=lo+idx*h
d,i=cKDTree(V).query(P); keep=(lab[i]==1)&(d<2.4)
hand=np.zeros_like(inside); hand[tuple(idx[keep].T)]=True
# largest component
L,n=ndi.label(hand); sz=np.bincount(L.ravel()); sz[0]=0; hand=L==sz.argmax()
dt=ndi.distance_transform_edt(hand)*h
np.savez_compressed('/home/claude/stc/rp1e/hand_%s.npz'%s,hand=hand,dt=dt.astype(np.float32),lo=lo,h=h)
t=time.time(); sk=skeletonize(hand); print('skel',time.time()-t, sk.sum(), hand.sum())
np.save('/home/claude/stc/rp1e/skel_%s.npy'%s, np.argwhere(sk))
