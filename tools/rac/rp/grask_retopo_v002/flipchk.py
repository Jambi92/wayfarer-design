import numpy as np, sys, igl, collections
sys.path.insert(0,'/tmp/claude-0/rt'); from common import *
SV,SF=load_src(); fn=np.cross(SV[SF[:,1]]-SV[SF[:,0]],SV[SF[:,2]]-SV[SF[:,0]]); fn/=np.maximum(np.linalg.norm(fn,axis=1),1e-12)[:,None]
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; FP=z['FP']
FP=np.array([PID[p] for p in FP]) if FP.dtype.kind in 'US' else FP
c=V[Q].mean(1); d,fi,_=igl.point_mesh_squared_distance(c,SV,SF)
n=np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,1]]); n/=np.maximum(np.linalg.norm(n,axis=1),1e-12)[:,None]
m=(n*fn[fi]).sum(1)<0; print('flipped',m.sum(),'of',len(Q)); print(collections.Counter([PARTS[p] for p in FP[m]]).most_common(12))
np.save(sys.argv[1].replace('.npz','_flip.npy'),m)
