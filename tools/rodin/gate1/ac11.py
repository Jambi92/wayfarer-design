import numpy as np
D=np.load('g7_surf.npz'); C=np.load('g7_surfc.npz'); mv=np.linalg.norm(C['V'].astype(float)-D['V'].astype(float),axis=1)*10
K=np.empty((len(mv),3),np.float32); K[:]=(0.35,0.36,0.40); K[mv>=0.2]=(0.92,0.66,0.25); K[mv>0.6]=(0.85,0.22,0.18)
np.savez('ac11.npz',P=C['V'],f=C['F'],C=K); print((mv>=0.2).mean(),(mv>0.6).mean())
