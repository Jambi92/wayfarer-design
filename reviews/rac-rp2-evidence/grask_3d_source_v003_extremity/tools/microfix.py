# microfix.py IN OUT : fair clusters of micro-triangles (area << neighbourhood) and their 2-ring on hands/feet/eyes
import sys, numpy as np, igl, scipy.sparse as sp
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from region_fair import region_fair
d=np.load(sys.argv[1]); X=d['V'].astype(float); F=d['Q'].astype(np.int64); n=len(X); Q4=np.c_[F,F[:,0]]
TT,_=igl.triangle_triangle_adjacency(F); e=np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]
tot=np.zeros(n); THR=float(sys.argv[3]) if len(sys.argv)>3 else 0.25
for it in range(4):
    Ar=igl.doublearea(X,F)/2; c=X[F].mean(1); ax=np.abs(c[:,0])
    reg=((ax>20)&(c[:,2]<112)&(c[:,2]>60))|(c[:,2]<15)|((ax<7)&(c[:,2]>196)&(c[:,2]<210)&(c[:,1]>3))
    nb=Ar[TT]; ref=np.median(np.c_[nb,Ar[TT[TT]].reshape(len(F),-1)],1)
    m=reg&(Ar<THR*ref)
    print('iter',it,'micro faces',m.sum())
    if m.sum()==0: break
    r=np.zeros(n); r[F[m].ravel()]=1
    for _ in range(2):
        s=np.zeros(n); np.maximum.at(s,e[:,0],r[e[:,1]]); r=np.maximum(r,0.75*s)
    X=region_fair(X,Q4,r,1.5,it=3); tot=np.maximum(tot,r)
out={k:d[k] for k in d.files}; out['V']=X; out['microfix_weight']=tot
np.savez(sys.argv[2],**out)
