import numpy as np, g1
from g1 import blurred, sd
R=np.load("/tmp/claude-0/rodin/adopt/b1_regions.npz")["R"]
keepF=~((R[g1.f1]==4)&(g1.P1[g1.f1][:,:,2]>66.0)).any(1)                     # B1 without arms/hands (they hang right beside the thighs)
FL=g1.f1[keepF]
a=np.arange(-36,36.01,0.7); b=np.arange(-19,21.01,0.7); c=np.arange(8,92.01,0.7)
A,B,C=np.meshgrid(a,b,c,indexing="ij"); keep=np.abs(A)>3.0
out=np.full(A.shape,20.0,np.float32); X,F,U=A[keep],B[keep],C[keep]; n=len(X); res=np.empty(n,np.float32)
for i in range(0,n,200000): s=slice(i,i+200000); res[s]=blurred(lambda q: sd(g1.P1,FL,q),X[s],F[s],U[s],3.2); print(i,n,flush=True)
out[keep]=res; np.savez("blur_legs.npz",a=a,b=b,c=c,d=out); print("DONE")
