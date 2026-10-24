# wire.py MESH OUT.png "crop-expr" view(elev,azim) : shaded wireframe diagnostic of a local region (matplotlib, painter's algorithm)
import sys, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
d=np.load(sys.argv[1]); V=d['V']; F=d['Q']; x,f,z=V.T
m=eval(sys.argv[3]); F=F[m[F].all(1)]
az,el=[float(v) for v in sys.argv[4].split(',')]
a=np.radians(az); e=np.radians(el)
cam=np.array([np.cos(e)*np.sin(a),np.cos(e)*np.cos(a),np.sin(e)])   # view direction toward camera (x,f,z)
right=np.cross([0,0,1.0],cam); right/=np.linalg.norm(right); up=np.cross(cam,right)
T=V[F]; N=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); N/=np.linalg.norm(N,axis=1)[:,None]+1e-12
vis=N@cam>0; T=T[vis]; N=N[vis]
depth=(T.mean(1)@cam); o=np.argsort(depth); T=T[o]; N=N[o]
P2=np.stack([T@right,T@up],-1)
light=np.array([0.3,0.5,0.8]); light=light/np.linalg.norm(light); sh=0.35+0.6*np.clip(N@(0.6*cam+0.4*light),0,1)
fig=plt.figure(figsize=(8,8),dpi=110); ax=fig.add_axes([0,0,1,1]); ax.set_aspect('equal'); ax.axis('off')
pc=PolyCollection(P2,facecolors=np.stack([sh*0.85,sh*0.83,sh*0.8],1),edgecolors=(0.15,0.15,0.2,0.55),linewidths=0.25)
ax.add_collection(pc); ax.autoscale_view(); fig.savefig(sys.argv[2]); print('tris',len(T))
