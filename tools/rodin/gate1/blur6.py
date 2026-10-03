# Gate 6: low-pass grids of the CURRENT (Gate 5) surface for regional relax / rebuild.
import numpy as np, sys, g1
from g1 import blurred, sd
z=np.load("g5_body.npz"); V=z["V"].astype(np.float64); Fc=z["F"].astype(np.int64)
ZONES={"pelvis":((-28,28,-46,16,54,112),3.0),"torso":((-24,24,-20,19,94,160),2.2),"neck":((-16,16,-20,16,146,182),1.6),
       "legL":((-34,-2,-14,30,-1,72),2.4),"legR":((2,34,-14,30,-1,72),2.4)}
name=sys.argv[1]; box,r=ZONES[name]; h=0.6
a,b,c=(np.arange(box[2*i],box[2*i+1]+h,h) for i in range(3)); A,B,C=np.meshgrid(a,b,c,indexing="ij"); X,F,U=A.ravel(),B.ravel(),C.ravel()
from scipy.ndimage import gaussian_filter
res=np.empty(len(X),np.float32)
for i in range(0,len(X),400000):
    s=slice(i,i+400000); res[s]=sd(V,Fc,np.stack([X[s],F[s],U[s]],-1)); print(name,i,len(X),flush=True)
res=gaussian_filter(res.reshape(A.shape).astype(np.float64),sigma=0.62*r/h,mode="nearest").astype(np.float32).ravel()   # ~ the 27-direction blur at radius r
np.savez("blur6_%s.npz"%name,a=a,b=b,c=c,d=res.reshape(A.shape),r=r); print("DONE",name)
