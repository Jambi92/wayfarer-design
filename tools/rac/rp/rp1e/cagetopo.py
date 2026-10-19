import numpy as np
z=np.load('/home/claude/stc/rp1/ck/v004a.npz'); Vc=z['Vc']*[1,-1,1]; Fc=z['Fc']
adj={}
for f in Fc:
    f=f[f>=0]
    for i in range(len(f)):
        a,b=f[i],f[(i+1)%len(f)]; adj.setdefault(a,set()).add(b); adj.setdefault(b,set()).add(a)
