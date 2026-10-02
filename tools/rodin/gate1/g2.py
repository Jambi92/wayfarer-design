# Gate 1 refinement field: g1 field + (R1) sacral/caudal structure, (R2) caudofemoral pelvis-femur bands, (R3) quiet ventral transition.
import numpy as np, sys
import g1
from g1 import ss, smin, smax, BIG
from wf_saurin_body8 import ellipsoid, round_cone
# ---- R3: perineal bridge: closes the slot between the neutral saddle and the tail underside (no aperture, no cavity)
def perineal(X,F,U): return ellipsoid((X,F,U),np.array([0.0,-2.0,94.0]),(6.0,7.5,3.6))
# ---- R2: caudofemoral load bands (reptilian caudofemoralis analogue): ventrolateral caudal base -> posterior proximal femur
CF_A=np.array([6.5,-27.0,89.0]); CF_B=np.array([11.0,-2.5,81.5])
def caudofemoral(X,F,U):
    Pa=(np.abs(X),F,U); return round_cone(Pa,CF_A,CF_B,3.6,3.4)
# ---- R1: platform planar definition: the root's own sections get crisper planes + stronger dorsolateral bevels and a
#      flatter sacral crown on the platform only (F > -34); the free-tail morph zone and donor are untouched
def root2(X,F,U):
    Q=np.stack([X,F,U],-1); dist,idx=g1._RT.query(Q,distance_upper_bound=30.0); ok=np.isfinite(dist); out=np.full(X.shape,BIG)
    if not ok.any(): return out
    i=idx[ok]; r=Q[ok]-g1.RP[i]; along=(r*g1.RT[i]).sum(1); x=r[:,0]; f=-(r*g1.RN[i]).sum(1)
    hw,dV,dD,cv,cb=g1.RS[i].T.copy()
    w=ss(-34.0,-28.0,g1.RP[i,1])*(1-ss(-6.0,-1.0,g1.RP[i,1]))          # platform window along the axis
    dD=dD-1.0*w; cb=cb-0.14*w; cv=cv-0.06*w
    k=11.0+13.0*w
    tb=np.clip(0.5+f/(0.9*(dV+dD)),0,1); tb=tb*tb*(3-2*tb); ax=np.abs(x)/hw
    t=np.stack([ax,f/dV,-f/dD,(ax+f/dV)/cv,(ax-f/dD)/cb]); m=t.max(0)
    q=m+np.log(np.exp(k*(t-m)).sum(0))/k-np.log(1.6)/k
    sz=np.minimum(hw,np.minimum(dV,dD)); last=i==len(g1.RP)-1; first=i==0
    e=np.where(last&(along>0),along/(0.9*sz),np.where(first&(along<0),-along/(0.9*sz),0.0))
    out[ok]=np.where(q>0,np.sqrt(q*q+e*e)-1,q-1+e)*sz; return out
# ---- R1: paired epaxial bands converging from the lumbar dorsum into the tail dorsum (directional transition)
def epaxial(X,F,U):
    idx=np.where((g1.RP[:,1]<=-4.0)&(g1.RP[:,1]>=-34.0))[0]
    pts=g1.RP[idx]+g1.RN[idx]*(g1.RS[idx,2][:,None]-4.6)
    off=np.linspace(8.5,5.0,len(idx))
    A=pts.copy(); A[:,0]=off
    from scipy.spatial import cKDTree
    t=cKDTree(A); d,i=t.query(np.stack([np.abs(X),F,U],-1),distance_upper_bound=12.0)
    r=np.linspace(4.0,2.8,len(idx)); out=np.full(X.shape,BIG); ok=np.isfinite(d); out[ok]=d[ok]-r[i[ok]]; return out
def field(X,F,U):
    Q=np.stack([X,F,U],-1); b1=g1.sd(g1.P1,g1.f1,Q)
    c=smax(b1,g1.carve_keep(X,F,U),1.5)
    wc=g1.crotch_w(X,F,U); m=wc>1e-3
    if m.any():
        bl=g1.CROTCH_BLUR(np.stack([X[m],F[m],U[m]],-1))+0.6
        ell=(np.sqrt(((F[m]+4)/19.0)**2+((U[m]-104)/16.0)**2)-1)*16.0
        bl=smax(bl,ell,2.5); c[m]=c[m]*(1-wc[m])+bl*wc[m]
    c=smin(c,perineal(X,F,U),3.0)                                  # R3 before the tail joins
    r=smin(root2(X,F,U),g1.ridge(X,F,U),1.2); dn=np.full(X.shape,BIG); md=F<-31.0
    if md.any(): dn[md]=g1.donor(X[md],F[md],U[md])
    t=ss(g1.J0,g1.J1,-F)
    tail=np.where(t<=0,r,np.where(t>=1,dn,(1-t)*np.minimum(r,BIG)+t*np.minimum(dn,BIG)))
    e=smin(c,tail,g1.K_ROOT)
    e=smin(e,caudofemoral(X,F,U),5.0)
    e=smin(e,ellipsoid((np.abs(X),F,U),np.array([8.6,-10.0,89.5]),(4.6,4.2,4.2)),3.0)   # close the band/thigh/platform pocket
    e=smin(e,epaxial(X,F,U),2.6)
    return e
import wf_saurin_body8 as B8
B8.sdf=lambda X,F,U: field(X,F,U)
B8.BOX=(-27.0,27.0,-52.0,22.0,70.0,122.0)
if __name__=="__main__":
    import time; t=time.time(); step=float(sys.argv[1]) if len(sys.argv)>1 else 0.35
    v,f=B8.mesh(step,log=lambda *a: None)
    np.savez_compressed(sys.argv[2] if len(sys.argv)>2 else "edit2_mc.npz",v=v,f=f); print("DONE",len(v),len(f),round(time.time()-t,1))
