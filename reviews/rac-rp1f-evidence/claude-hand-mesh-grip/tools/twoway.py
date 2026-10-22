# twoway.py IN.npz OUT.npz cx,cy,cz,R [ITERS] : bounded two-way fit of the production patch to the accepted sculpt
# (reference points far from the production pull their nearest production vertices; then closest-point projection and a
# light tangential relax). Vertex-only, topology unchanged, protected vertices untouched.
import sys,numpy as np,igl,json; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from hm import *
from scipy.spatial import cKDTree
z=dict(np.load(sys.argv[1])); out=sys.argv[2]; reg=np.array([float(x) for x in sys.argv[3].split(',')]); it=int(sys.argv[4]) if len(sys.argv)>4 else 30
P=z['V']*np.array([1,-1,1]); Q=z['Q']; prot=np.zeros(len(P),bool); prot[z['old2new'][z['prot']]]=True
R,F,mat=load107()
c=reg[:3]; r=reg[3]
pv=np.where((np.linalg.norm(P-c,axis=1)<r)&~prot)[0]; w=np.clip((r-np.linalg.norm(P[pv]-c,axis=1))/(0.3*r),0,1)
rv=np.where(np.linalg.norm(R-c,axis=1)<r*0.85)[0]
rf=F[(np.linalg.norm(R[F].mean(1)-c,axis=1)<r+1)]
qs=np.where((np.linalg.norm(P[Q].mean(1)-c,axis=1)<r+0.5))[0]; T=np.vstack([Q[qs][:,[0,1,2]],Q[qs][:,[0,2,3]]])
nb=[[] for _ in range(len(P))]
for q in Q[qs]:
    for i in range(4): nb[q[i]].append(q[(i+1)%4]); nb[q[i]].append(q[(i-1)%4])
lp=-np.ones(len(P),int); lp[pv]=np.arange(len(pv))
for k in range(it):
    sd,ti,cp=igl.point_mesh_squared_distance(R[rv],P,T); d=np.sqrt(sd)
    far=d>0.03
    print('iter',k,'ref->prod max mm %.2f  n>0.3mm %d'%(d.max()*10,far.sum()),flush=True)
    if not far.any(): break
    kd=cKDTree(P[pv]); _,nn=kd.query(R[rv][far],k=3)
    acc=np.zeros((len(pv),3)); cnt=np.zeros(len(pv))
    for j in range(3):
        np.add.at(acc,nn[:,j],R[rv][far]-P[pv][nn[:,j]]); np.add.at(cnt,nn[:,j],1)
    m=cnt>0; P[pv[m]]+=0.5*(w[m,None]*acc[m]/cnt[m,None])
    # tangential smoothing + projection back onto the sculpt
    L=np.array([P[nb[v]].mean(0) if nb[v] else P[v] for v in pv])
    P[pv]=P[pv]+0.3*w[:,None]*(L-P[pv])
    _,_,cp2=igl.point_mesh_squared_distance(P[pv],R,rf); P[pv]=P[pv]+w[:,None]*(cp2-P[pv])
z['V']=P*np.array([1,-1,1]); np.savez_compressed(out,**z)
