import numpy as np, g1
from g1 import blurred, sd
a=np.arange(-21,21.01,0.6); b=np.arange(-8,22.01,0.6); c=np.arange(98,160.01,0.6)
A,B,C=np.meshgrid(a,b,c,indexing="ij"); out=np.empty(A.size,np.float32)
X,F,U=A.ravel(),B.ravel(),C.ravel(); n=len(X); step=200000
for i in range(0,n,step):
    s=slice(i,i+step); out[s]=blurred(lambda q: sd(g1.P1,g1.f1,q),X[s],F[s],U[s],3.5); print(i,n,flush=True)
np.savez("blur_torso.npz",a=a,b=b,c=c,d=out.reshape(A.shape))
print("DONE")
