# tail cross-section profile along the anatomical axis (station s from the tail tip), from a mesh
import numpy as np, sys
from scipy.spatial import cKDTree
def profile(V, C, smax=None, nb=72):
    tr=cKDTree(C); _,ci=tr.query(V); ci=np.clip(ci,1,len(C)-2)
    T=C[ci+1]-C[ci-1]; T/=np.linalg.norm(T,axis=1,keepdims=True)
    r=V-C[ci]; r-=T*np.einsum('ij,ij->i',r,T)[:,None]
    d=np.cross(np.array([1.0,0,0]),T); d/=np.linalg.norm(d,axis=1,keepdims=True)
    th=np.arctan2(r[:,0],np.einsum('ij,ij->i',r,d)); R=np.linalg.norm(r,axis=1)
    return ci,th,R
if __name__=='__main__':
    z=np.load(sys.argv[1]); V=z[z.files[0]].astype(float); C=np.load('/tmp/claude-0/rodin/g8/axis.npy')
    ci,th,R=profile(V,C)
    tail=(V[:,1]<-20)&(V[:,2]>40)
    S=ci*0.5; out=[]
    for k in range(0,240):
        m=tail&(ci==k)
        if m.sum()<20: continue
        b=((th[m]+np.pi)/(2*np.pi)*72).astype(int)%72; rb=np.zeros(72)
        np.maximum.at(rb,b,R[m]); 
        if (rb==0).sum()>10: continue
        rb[rb==0]=np.median(rb[rb>0]); A=0.5*np.sum(rb**2)*(2*np.pi/72)
        out.append((k*0.5,A,np.sqrt(A/np.pi),C[k][1],C[k][2]))
    out=np.array(out); np.save(sys.argv[2],out)
    for row in out[::6]: print('s %5.1f  area %7.1f cm2  r_eq %5.2f  f %6.1f u %5.1f'%tuple(row))
