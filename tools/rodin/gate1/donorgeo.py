import numpy as np
z=np.load("src.npz"); P2=z["P2"]; f2=z["f2"]
c0x,c0f,yaw=np.load("donor_align.npy")
def align(P):
    Q=P.copy(); x=P[:,0]-c0x; f=P[:,1]-c0f
    Q[:,0]=x*np.cos(yaw)-f*np.sin(yaw); Q[:,1]=x*np.sin(yaw)+f*np.cos(yaw)+c0f; return Q
Q2=align(P2)
def centreline():
    T=Q2[(Q2[:,1]<-34)&(Q2[:,2]<110)]; C=[]
    for fv in np.arange(-36,-121,-1.0):
        m=np.abs(T[:,1]-fv)<0.5
        if m.sum()>6: C.append([0.0,fv,T[m,2].mean()])
    C=np.array(C)
    from scipy.ndimage import gaussian_filter1d
    C[:,2]=gaussian_filter1d(C[:,2],2.0); return C
if __name__=="__main__":
    C=centreline(); seg=np.linalg.norm(np.diff(C,axis=0),axis=1); s=np.concatenate([[0],np.cumsum(seg)])
    T=Q2[(Q2[:,1]<-30)&(Q2[:,2]<112)]
    for i in range(0,len(C),4):
        j0,j1=max(i-1,0),min(i+1,len(C)-1); t=C[j1]-C[j0]; t/=np.linalg.norm(t)
        d=(T-C[i])@t; m=np.abs(d)<0.5; S=T[m]-C[i]; nrm=np.cross(t,[1,0,0]); 
        w=np.ptp(S[:,0]); h=np.ptp(S@nrm); cu=(S@nrm).mean()
        print("s%6.1f f%6.1f u%6.1f slope%5.0f  width %.1f  height %.1f  (centre off %.1f)"%(s[i],C[i,1],C[i,2],np.degrees(np.arctan2(-t[2],-t[1])),w,h,cu))
