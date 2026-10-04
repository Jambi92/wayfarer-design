# final brow/orbit: field on the convergence base inside the head box (run once with BROW_INT=0 and once with =1)
import numpy as np, sys
import g10
z=np.load('/tmp/claude-0/rodin/c11/g14_body.npz'); V=z['V']; x,f,u=V.T
inb=(np.abs(x)<16)&(f>-34)&(f<28)&(u>161)&(u<203)
idx=np.where(inb)[0]; e=np.full(len(V),np.nan)
for s in range(0,len(idx),50000):
    j=idx[s:s+50000]; e[j]=g10.field(*V[j].T)
np.save(sys.argv[1],e); print('done',len(idx))
