# cagerecol.py CAGE COL_IN COL_OUT : cage colours matching recolour.py
import numpy as np, sys
V=np.load(sys.argv[1])['V']; c=np.load(sys.argv[2]).copy(); o=c.copy()
for i,(p,k) in enumerate(zip(V,c)):
    if k==2:
        if p[2]>183: o[i]=2
        elif p[2]<105: o[i]=10 if p[0]>1.2 else 11
        else: o[i]=4 if p[0]>2 else 5
    elif k in (3,6,7,8) and p[0]<2: o[i]={3:12,6:13,7:14,8:15}[k]
np.save(sys.argv[3],o); u,n=np.unique(o,return_counts=True); print(dict(zip(u.tolist(),n.tolist())))
