import numpy as np, g1
from g1 import blurred, sd
a=np.arange(-17,17.01,0.6); b=np.arange(-23,13.01,0.6); c=np.arange(146,174.01,0.6)
A,B,C=np.meshgrid(a,b,c,indexing="ij"); out=np.empty(A.size,np.float32); X,F,U=A.ravel(),B.ravel(),C.ravel(); n=len(X)
for i in range(0,n,200000): s=slice(i,i+200000); out[s]=blurred(lambda q: sd(g1.P1,g1.f1,q),X[s],F[s],U[s],3.0); print(i,n,flush=True)
np.savez("blur_neck.npz",a=a,b=b,c=c,d=out.reshape(A.shape)); print("DONE")
