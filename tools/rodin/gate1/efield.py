import numpy as np, sys
import g10
z=np.load('g8_body.npz'); V=z['V']; x,f,u=V.T
inb=((np.abs(x)<16)&(f>-20)&(f<28)&(u>150)&(u<192))|((np.abs(x)<30)&(f>-75)&(f<15)&(u>55)&(u<115))
idx=np.where(inb)[0]; e=np.full(len(V),np.nan)
for s in range(0,len(idx),50000):
    j=idx[s:s+50000]; e[j]=g10.field(*V[j].T)
np.save(sys.argv[1],e); print('done',len(idx))
