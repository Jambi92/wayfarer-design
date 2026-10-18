import numpy as np, sys; sys.path.insert(0,'/home/claude/av'); from avlib import *
from scipy.optimize import brentq
def heel_weights(V1,side,dheel,base,zlow=0.018,ztop=0.060,t0=0.18,t1=0.45):
    fm,ax,perp=frame(V1,side); X=V1[fm]; c=X.mean(0); s=(V1-c)@ax; sf=s[fm]; t=(s-sf.min())/np.ptp(sf)
    m=(np.sign(V0[:,0])==SG[side])&(V0[:,2]<ztop)
    zf=1-ss((V1[:,2]-zlow)/(ztop-zlow)); hs=1-ss((t-t0)/(t1-t0))
    d=np.where(m,zf*(base+dheel*hs),0.0); dmax=base+dheel
    return d/dmax, dmax
def solve_heel(V1,side,target=0.0035):
    m0=measure(V1,side); fm,_,_=frame(V1,side); base=float(V1[fm,2].min())
    def f(dh):
        w,dm=heel_weights(V1,side,dh,base); V=V1.copy(); V[:,2]-=w*dm; return measure(V,side)['heel']/100-target
    dh=brentq(f,0.0,0.03); w,dm=heel_weights(V1,side,dh,base); V=V1.copy(); V[:,2]-=w*dm
    return w,dm,V,base,dh
