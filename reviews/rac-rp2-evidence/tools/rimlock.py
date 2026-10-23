# rimlock.py IN OUT REF thr : blend silhouette-rim vertices (front/rear and profile views) onto the closest point of REF.
# w = smoothstep over |n.view| in [0, thr], max over the two view axes; resolution-zone points (closest REF face excluded) untouched.
import sys, numpy as np, igl
R='/tmp/claude-0/rp2/'
P=np.load(sys.argv[1]); V=P['V'].astype(float); Q=P['Q']; Rf=np.load(sys.argv[3]); thr=float(sys.argv[4])
RV=Rf['V'].astype(float); RQ=Rf['Q']; RT=np.r_[RQ[:,[0,1,2]],RQ[:,[0,2,3]]]
ex=np.load(R+'excl_quads.npy'); ex=np.nonzero(ex)[0] if ex.dtype==bool else ex; exT=np.zeros(len(RT),bool); exT[ex]=True; exT[ex+len(RQ)]=True
T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]; N=igl.per_vertex_normals(V,T)
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
w=np.maximum(ss(1-np.abs(N[:,1])/thr), ss(1-np.abs(N[:,0])/thr))
_,fi,cp=igl.point_mesh_squared_distance(V,RV,RT); w[exT[fi]]=0
# smooth the weight field a little so the lock has no hard edge
e=np.r_[Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]
for _ in range(int(sys.argv[5]) if len(sys.argv)>5 else 6):
    s=np.zeros(len(V)); c=np.zeros(len(V)); np.add.at(s,e[:,0],w[e[:,1]]); np.add.at(s,e[:,1],w[e[:,0]]); np.add.at(c,e[:,0],1); np.add.at(c,e[:,1],1); w=0.5*w+0.5*s/c
import os; sys.path.insert(0,R+'tools'); from lowpass import lowpass
DL=w[:,None]*(cp-V); lp=float(os.environ.get('LP','0'))
if lp>0: DL=lowpass(Q,len(V),DL,lp)
V2=V+DL
np.savez(sys.argv[2],**{k:P[k] for k in P.files if k!='V'},V=V2); print('locked frac(w>0.5) %.3f'%(w>0.5).mean())
