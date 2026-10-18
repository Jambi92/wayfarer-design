# RM-OT-05AV planning library (cloud diagnostics only). Units: metres.
import numpy as np
V0=np.load('/home/claude/at/final/ac3.npz')['V'].astype(float)
F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']
Wv=np.load('/home/claude/ao/vgroups.npz'); names=list(Wv['names']); Wt=Wv['W']; lab=Wt.argmax(1)
SG={'L':1,'R':-1}
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
def frame(V,side):
    fm=lab==names.index(f'foot_{side}'); X=V[fm]; c=X.mean(0); _,_,vt=np.linalg.svd((X-c)[:,:2],full_matrices=False); ax=np.r_[vt[0],0]
    if ax[1]>0: ax=-ax
    return fm,ax,np.array([-ax[1],ax[0],0])
def ringmask(side):
    w_=Wt[:,names.index(f'shin_{side}')]; w2=Wt[:,names.index(f'foot_{side}')]; return (w_>0.25)&(w_<0.75)&(w2>0.25)
def leg(side,zb): return (np.sign(V0[:,0])==SG[side])&(V0[:,2]<zb)
def scale_plan(side,za,zb):
    """weights (z fade) and pivot = weighted ring centroid (keeps ring mean fixed)"""
    w=np.zeros(len(V0)); m=leg(side,zb); w[m]=1-ss((V0[m,2]-za)/(zb-za))
    r=ringmask(side); P=(w[r,None]*V0[r]).sum(0)/w[r].sum()
    return w,P
def apply_scale(V,w,P,yaw_deg,sx,sy):
    th=np.radians(yaw_deg); c,s=np.cos(th),np.sin(th); R=np.array([[c,-s,0],[s,c,0],[0,0,1]]); A=R@np.diag([sx,sy,1])@R.T
    return V+w[:,None]*(((V-P)@A.T+P)-V)
def measure(V,side):
    fm,ax,perp=frame(V,side); X=V[fm]; c=X.mean(0); s=(X-c)@ax; L=np.ptp(s); t=(s-s.min())/L
    zr=lambda a,b: float(X[(t>=a)&(t<=b),2].min())
    pl=X[X[:,2]<0.03]; wfp=np.ptp((pl-c)@perp)
    heel=zr(0,0.15); ball=zr(0.65,0.82); cont=X[:,2]<0.003
    return dict(length=L*100,width_fp=wfp*100,width_full=np.ptp((X-c)@perp)*100,heel=heel*100,mid=zr(0.35,0.6)*100,ball=ball*100,toes=zr(.85,1)*100,heel_lift=(heel-ball)*100,
                contact=[float(t[cont].min()),float(t[cont].max())] if cont.sum() else None,ncont=int(cont.sum()),yaw=float(np.degrees(np.arctan2(-ax[0],ax[1]))))
