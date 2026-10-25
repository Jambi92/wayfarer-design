# wireh.py MESH OUT.png crop az,el : wireframe with T-4 violators (hard limits) in red, soft violators orange
import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
d=np.load(sys.argv[1]); V=d['V']; F=d['Q']; x,f,z=V.T
ang=[]
for i in range(4):
    a=V[F[:,(i-1)%4]]-V[F[:,i]]; b=V[F[:,(i+1)%4]]-V[F[:,i]]
    ang.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
ang=np.stack(ang,1); el=np.stack([np.linalg.norm(V[F[:,(i+1)%4]]-V[F[:,i]],axis=1) for i in range(4)],1)
asp=(el[:,0]+el[:,2])/np.maximum(el[:,1]+el[:,3],1e-12); asp=np.maximum(asp,1/np.maximum(asp,1e-12))
hard=(ang.min(1)<20)|(ang.max(1)>160)|(asp>8); soft=~(((ang>=45)&(ang<=135)).all(1)&(asp<=4))
sys.path.insert(0,'/tmp/claude-0/rt'); from common import PARTS
_vp=np.zeros(len(V),int); _vp[F.ravel()]=np.repeat(d['FP'],4); part=np.array(PARTS)[_vp]
handpart=np.char.startswith(part.astype(str),('hand','thumb','index','middle','ring','pinky')) if False else np.array([p.startswith(('hand','thumb','index','middle','ring','pinky')) for p in part])
m=eval(sys.argv[3]); keep=m[F].all(1); F=F[keep]; hard=hard[keep]; soft=soft[keep]
az,elv=[float(v) for v in sys.argv[4].split(',')]; a=np.radians(az); e=np.radians(elv)
cam=np.array([np.cos(e)*np.sin(a),np.cos(e)*np.cos(a),np.sin(e)]); right=np.cross([0,0,1.0],cam); right/=np.linalg.norm(right); up=np.cross(cam,right)
T=V[F]; N=np.cross(T[:,2]-T[:,0],T[:,3]-T[:,1]); N/=np.linalg.norm(N,axis=1)[:,None]+1e-12
vis=N@cam>0; T=T[vis]; N=N[vis]; hard=hard[vis]; soft=soft[vis]
o=np.argsort(T.mean(1)@cam); T=T[o]; N=N[o]; hard=hard[o]; soft=soft[o]
P2=np.stack([T@right,T@up],-1); sh=0.4+0.55*np.clip(N@cam,0,1)
col=np.stack([sh*0.85,sh*0.83,sh*0.8],1)
plain=len(sys.argv)>5 and sys.argv[5]=='plain'
if not plain: col[soft]=np.stack([sh[soft],sh[soft]*0.65,sh[soft]*0.2],1)
if not plain: col[hard]=np.stack([sh[hard],sh[hard]*0.1,sh[hard]*0.1],1)
fig=plt.figure(figsize=(8,8),dpi=int(sys.argv[6]) if len(sys.argv)>6 else 110); ax=fig.add_axes([0,0,1,1]); ax.set_aspect('equal'); ax.axis('off')
ax.add_collection(PolyCollection(P2,facecolors=col,edgecolors=(0.1,0.1,0.15,0.6),linewidths=0.3)); ax.autoscale_view(); fig.savefig(sys.argv[2])
