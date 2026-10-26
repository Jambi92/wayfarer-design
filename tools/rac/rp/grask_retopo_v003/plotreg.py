# plotreg.py MESH.npz cx,cf,cu R nx,nf,nu OUT.png : orthographic wire of a region viewed along -n, hard quads red
import numpy as np,sys,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
z=np.load(sys.argv[1]);V=z['V'];Q=z['Q'];c=np.array(sys.argv[2].split(','),float);R=float(sys.argv[3]);n=np.array(sys.argv[4].split(','),float);n/=np.linalg.norm(n)
u=np.cross(n,[0,0,1.0]); 
if np.linalg.norm(u)<1e-3: u=np.cross(n,[0,1.0,0])
u/=np.linalg.norm(u); w=np.cross(n,u)
fc=V[Q].mean(1); m=(np.linalg.norm(fc-c,axis=1)<R)&(((V[Q]-c)@n).mean(1)>-R*0.6)
ang=[]
for i in range(4):
    a=V[Q[:,(i-1)%4]]-V[Q[:,i]]; b=V[Q[:,(i+1)%4]]-V[Q[:,i]]
    ang.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
ang=np.stack(ang,1); hard=(ang.min(1)<20)|(ang.max(1)>160)
F=np.nonzero(m)[0]; F=F[np.argsort(((V[Q[F]]-c)@n).mean(1))]
P=np.stack([(V[Q[F]]-c)@u,(V[Q[F]]-c)@w],2)
nrm=np.cross(V[Q[F,2]]-V[Q[F,0]],V[Q[F,3]]-V[Q[F,1]]); front=(nrm@n)>0
col=[(1,.3,.3) if hard[f] else ((.85,.85,.9) if fr else (.6,.6,.65)) for f,fr in zip(F,front)]
fig=plt.figure(figsize=(8,8)); ax=fig.add_subplot(111); ax.add_collection(PolyCollection(P,facecolors=col,edgecolors='k',linewidths=0.4))
ax.set_xlim(-R,R); ax.set_ylim(-R,R); ax.set_aspect('equal'); ax.set_title(sys.argv[5].split('/')[-1]+' hard=%d'%hard[F].sum()); fig.savefig(sys.argv[5],dpi=90); print('ok')
