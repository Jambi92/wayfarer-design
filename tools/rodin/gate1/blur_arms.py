import numpy as np, g1
from g1 import blurred, sd
R=np.load("/tmp/claude-0/rodin/adopt/b1_regions.npz")["R"]; P=g1.P1
armv=(R==4)|((R==3)&(np.abs(P[:,0])>19.5))
np.save("arm_vert_mask.npy",armv)
FA=g1.f1[armv[g1.f1].all(1)|(P[g1.f1][:,:,2]>98.0).all(1)]   # closed around the shoulder/armpit (open cut only at U 98, far from the arm)

out={}
for sg in (-1,1):
    a=np.arange(18,45.01,0.7)*sg; a=np.sort(a); b=np.arange(-21,22.01,0.7); c=np.arange(72,160.01,0.7)
    A,B,C=np.meshgrid(a,b,c,indexing="ij"); X,F,U=A.ravel(),B.ravel(),C.ravel(); n=len(X); res=np.empty(n,np.float32)
    for i in range(0,n,200000): s=slice(i,i+200000); res[s]=blurred(lambda q: sd(P,FA,q),X[s],F[s],U[s],2.8); print(sg,i,n,flush=True)
    out["a%d"%(sg>0)]=a; out["b%d"%(sg>0)]=b; out["c%d"%(sg>0)]=c; out["d%d"%(sg>0)]=res.reshape(A.shape)
np.savez("blur_arms.npz",**out); print("DONE")
