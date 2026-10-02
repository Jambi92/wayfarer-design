import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
z=np.load("src.npz"); P=z["P1"]; f=z["f1"]; R=np.load("/tmp/claude-0/rodin/adopt/b1_regions.npz")["R"]
E=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]); w=np.linalg.norm(P[E[:,0]]-P[E[:,1]],axis=1)
G=coo_matrix((w,(E[:,0],E[:,1])),shape=(len(P),)*2).tocsr(); G=G.maximum(G.T)
U=P[:,2]; ax=np.abs(P[:,0])
arm_seed=np.where((R==4)&((U>80)|(U<50)))[0]
leg_seed=np.where((R==14)&((U<40)|((ax<14)&(U>55)&(U<75))))[0]
da=dijkstra(G,indices=arm_seed,min_only=True,limit=60); dl=dijkstra(G,indices=leg_seed,min_only=True,limit=60)
arm=((R==4)|((da<dl)&(U<82)&(U>38)))
print("arm verts",arm.sum(),"previously R==4:",(R==4).sum())
for u in (45,55,65,75):
    s=arm&(np.abs(U-u)<1); print(u,"arm |x| %.1f..%.1f f %.1f..%.1f"%(ax[s].min(),ax[s].max(),P[s,1].min(),P[s,1].max()) if s.any() else "none")
np.save("arm_mask.npy",arm)
Rc=np.where(arm,21,3); np.savez("handchk.npz",P=P,f=f[:,[0,2,1]],R=Rc)
