# finefit.py ZB ZT : fine fit of the coarse donor onto source skin outside the cloth zone (smooth offset field), donor part kept
import sys, numpy as np, igl, scipy.sparse as sp
from scipy.sparse.linalg import factorized
ZB,ZT=float(sys.argv[1]),float(sys.argv[2]); LAM=float(sys.argv[3]) if len(sys.argv)>3 else 400.0
S=np.load('/tmp/claude-0/src3d/in/front_aligned.npz'); SV=S['V'].astype(float); SF=S['Q'].astype(np.int64)
C=np.load('/tmp/claude-0/src3d/work/donor_coarse.npz'); X=C['V'].astype(float); Q=C['Q']
def cloth_zone(P):
    x,f,z=P[:,0],P[:,1],P[:,2]; ax=np.abs(x)
    band=(z>105)&(z<133.5)
    front=(f>0)&(ax<15.5)&(z>91)&(z<=106)
    back=(f<-1)&(ax<17.5)&(z>91)&(z<=106)
    return band|front|back
reg=(X[:,2]>ZB-10)&(X[:,2]<ZT+10)&(np.abs(X[:,0])<26)
d2,fi,cp=igl.point_mesh_squared_distance(X[reg],SV,SF)
off=np.zeros_like(X); off[reg]=cp-X[reg]; dist=np.sqrt(d2)
w=np.zeros(len(X)); ok=reg.copy(); ok[reg]=(dist<4.0)&~cloth_zone(cp); w[ok]=10.0
# ensure seam rows are fully valid
seam=reg&((np.abs(X[:,2]-ZB)<2.5)|(np.abs(X[:,2]-ZT)<2.5))&(np.abs(X[:,0])<22.5); w[seam]=np.maximum(w[seam],100.0)
e=np.r_[Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]; n=len(X)
A=sp.coo_matrix((np.ones(2*len(e)),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),(n,n)).tocsr(); A.data[:]=1
L=sp.diags(np.asarray(A.sum(1)).ravel())-A
# solve only on region (others: offset 0 fixed far away)
M=sp.diags(w+1e-6)+LAM*L
s=factorized(M.tocsc()); Dsm=np.stack([s(w*off[:,j]) for j in range(3)],1)
Y=X+Dsm
np.savez('/tmp/claude-0/src3d/work/donor_fine.npz',V=Y,Q=Q,valid=w,region=reg)
print('valid in region',int(w[reg].sum()),'of',int(reg.sum()),'| mean |offset| valid %.2f cm'%np.linalg.norm(off[ok],axis=1).mean())
for zz in (ZB,ZT):
    m=(np.abs(Y[:,2]-zz)<0.6)&(np.abs(Y[:,0])<22.5)
    d,_,_=igl.point_mesh_squared_distance(Y[m],SV,SF); print('seam z',zz,'donor->src dist max %.2f mean %.2f mm'%(np.sqrt(d).max()*10,np.sqrt(d).mean()*10))
