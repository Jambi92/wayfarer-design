# cagecolnn.py CAGE SRCCOL OUT [OLD] : cage colour = colour of nearest source vertex
import numpy as np, sys
from scipy.spatial import cKDTree
S=np.load('/home/claude/stc/rp1/weld.npz')['V']; sc=np.load(sys.argv[2]); V=np.load(sys.argv[1])['V']
d,i=cKDTree(S).query(V); c=sc[i]; np.save(sys.argv[3],c)
if len(sys.argv)>4:
    o=np.load(sys.argv[4]); ch=np.where(o!=c)[0]; print('changed',len(ch))
    import collections; print(collections.Counter(zip(o[ch].tolist(),c[ch].tolist())).most_common(20))
