import numpy as np, sys
from scipy.spatial import cKDTree
wa=np.load('/home/claude/stc/rp1/weld_a.npz')['V']; S=np.load('/home/claude/stc/rp1/weld.npz')['V']; z=np.load('/home/claude/stc/rp1/zones.npz'); zone=z['zone']; names=list(z['names'])
T=cKDTree(wa); hi=names.index('head_muzzle_ears')
for p in sys.argv[1:]:
    C=np.load(p); d,i=T.query(C[:,:3]); h=i[zone[i]==hi]; P=S[h]
    earL=((P[:,0]>4)&(P[:,1]<-36)&(P[:,1]>-62)&(P[:,2]>186)); earR=((P[:,0]<-4)&(P[:,1]<-36)&(P[:,1]>-62)&(P[:,2]>186))
    rest=~(earL|earR)
    print(p,'head',len(h),'earL',earL.sum(),'earR',earR.sum(),'rest',rest.sum(),'rest z<183',(rest&(P[:,2]<183)).sum())
