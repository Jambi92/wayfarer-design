import numpy as np
z=np.load('g7_surf.npz'); d=np.abs(z['disp'].astype(float))*10; s=np.load('cur_s7.npz')
C=np.empty((len(d),3),np.float32); C[:]=(0.35,0.36,0.40)
C[d>=0.3]=(0.92,0.66,0.25); C[d>0.8]=(0.85,0.22,0.18)
np.savez('ac10.npz',P=s['P'],f=s['f'],C=C); print((d>=0.3).mean(),(d>0.8).mean())
