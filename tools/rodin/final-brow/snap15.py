# outside the re-surfaced brow zone the regenerated surface equals the accepted convergence surface up to float32 round-off
# (re-ordered sums after re-assembly, <= 0.0004 mm). Snap those vertices to the accepted coordinates so unchanged = bit-identical.
import numpy as np
from scipy.spatial import cKDTree
z=dict(np.load('g15_surf.npz')); np.savez('g15_surf_raw.npz',**z)
S0=np.load('/tmp/claude-0/rodin/c11/g14_surf.npz')['V']; V=z['V']
d,ii=cKDTree(S0).query(V); m=d<1e-4
V=V.copy(); V[m]=S0[ii[m]]; z['V']=V; np.savez('g15_surf.npz',**z)
print('snapped',int(m.sum()),'of',len(V),'max snap mm',float(d[m].max()*10),'unsnapped',int((~m).sum()))
