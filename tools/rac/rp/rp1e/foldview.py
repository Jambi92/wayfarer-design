import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
# render faces of a sim mesh in a box, from several view directions, with intersecting faces red (painter's algorithm, flat shading)
mp=sys.argv[1]; box=np.array([float(v) for v in sys.argv[2].split(',')]).reshape(3,2); out=sys.argv[3]
z=np.load(mp); V=z['V']*np.array([1,-1,1]); Q=z['Q']; P=np.load(mp.replace('.npz','_pairs.npy'))
bad=set(P.ravel().tolist())
c=np.array([V[q[q>=0]].mean(0) for q in Q]); m=((c>box[:,0])&(c<box[:,1])).all(1); idx=np.where(m)[0]
views=[('front -Y',np.array([0,1,0]),(0,2)),('side +X',np.array([-1,0,0]),(1,2)),('below',np.array([0,0,1]),(0,1)),('side -X',np.array([1,0,0]),(1,2))]
fig,axs=plt.subplots(1,4,figsize=(28,8))
L=np.array([0.3,-0.6,0.7]); L/=np.linalg.norm(L)
for a,(nm,vd,(i,j)) in zip(axs,views):
    depth=c[idx]@vd; order=idx[np.argsort(-depth)]  # far first (vd points away from viewer)
    polys=[];cols=[]
    for k in order:
        q=Q[k][Q[k]>=0]; p=V[q]; n=np.cross(p[1]-p[0],p[2]-p[0]); n/=np.linalg.norm(n)+1e-12
        sh=0.35+0.65*abs(n@L); polys.append(p[:,[i,j]])
        cols.append((1,0.1,0.1) if k in bad else (sh,sh,sh))
    if nm=='side +X': a.invert_xaxis()
    a.add_collection(PolyCollection(polys,facecolors=cols,edgecolors=(0,0,0,0.15),linewidths=0.2))
    a.set_xlim(box[i]); a.set_ylim(box[j]); a.set_aspect('equal'); a.set_title(nm)
plt.savefig(out,dpi=60,bbox_inches='tight')
