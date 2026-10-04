import numpy as np
from scipy.spatial import cKDTree
z=np.load('g15_surf.npz'); np.savez('cs15.npz',P=z['V'],f=z['F'],R=np.zeros(len(z['V']),np.int8))
pal={1:(0.80,0.45,0.25),2:(0.95,0.80,0.30),3:(0.55,0.35,0.75),4:(0.35,0.65,0.85),5:(0.40,0.75,0.45),6:(0.20,0.20,0.22),7:(0.95,0.95,0.95)}
r=np.load('g15reg.npz'); C=np.zeros((len(z['V']),3),np.float32)
for k,c in pal.items(): C[r['FAM']==k]=c
np.savez('map15.npz',P=z['V'],f=z['F'],C=C)
S0=np.load('/tmp/claude-0/rodin/c11/g14_surf.npz')['V']; d,ii=cKDTree(S0).query(z['V']); np.save('dsurf15.npy',d); np.save('nn15.npy',ii)
dm=d*10; t=np.clip(dm/8.0,0,1); H=np.empty((len(d),3),np.float32); H[:]=(0.33,0.34,0.38); m=dm>0.1; tt=t[m]
H[m]=np.stack([0.35+0.6*tt,0.36+0.5*np.clip(1-abs(tt-0.45)*2,0,1)-0.2*tt,0.40-0.3*tt],1)
np.savez('heat15.npz',P=z['V'],f=z['F'],C=np.clip(H,0,1)); print('ok')
