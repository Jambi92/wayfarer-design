# Saurin Gate 1 — pelvis / sacrum / tail-root integration on untouched Rodin B1 (c12) with the B2 (c11) free-tail donor.
# Edit field E = smin( smin( carve(B1), ROOT ), DONOR ). Only the edit zone is re-surfaced; B1 elsewhere stays original.
import numpy as np, igl, sys
from scipy.interpolate import CubicSpline, PchipInterpolator
from scipy.spatial import cKDTree
sys.path.insert(0,"/tmp/claude-0/rb"); import wf_saurin_body8 as B8
from wf_saurin_body8 import smin, smax, BIG
from donorgeo import Q2, f2
z=np.load("src.npz"); P1=z["P1"].astype(np.float64); f1=z["f1"].astype(np.int64)
Q2=Q2.astype(np.float64); f2=f2.astype(np.int64)
SDT=igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER
def sd(V,F,Q): return igl.signed_distance(np.ascontiguousarray(Q,dtype=np.float64),V,F,sign_type=SDT)[0]
def ss(e0,e1,x):
    t=np.clip((x-e0)/(e1-e0),0,1); return t*t*(3-2*t)
# ---------------- carve: gluteal hemispheres + cleft (posterior) and the sexed crotch form (ventral) -----------------
GLUTE_F=-7.0
def carve_keep(X,F,U):
    ax=np.abs(X)
    rho2=(ax/21.0)**2+((U-97.5)/12.5)**2                     # elliptical (not rectangular) gluteal carve footprint
    post=(GLUTE_F-14.0*rho2)-F                               # keep F > f_cut ; the cut recedes smoothly behind the body
    return post
_DIRS=np.array([[x,y,z] for x in (-1,0,1) for y in (-1,0,1) for z in (-1,0,1) if (x,y,z)!=(0,0,0)],float)
_DIRS/=np.linalg.norm(_DIRS,axis=1,keepdims=True)
def blurred(fn,X,F,U,r):
    acc=fn(np.stack([X,F,U],-1)); n=1
    for d in _DIRS: acc=acc+fn(np.stack([X+r*d[0],F+r*d[1],U+r*d[2]],-1)); n+=1
    return acc/n
from scipy.interpolate import RegularGridInterpolator
import os
def _blur_grid(name,V,Fc,box,r,h=0.5):
    fn="blur_%s.npz"%name
    if os.path.exists(fn):
        z=np.load(fn); return RegularGridInterpolator((z["a"],z["b"],z["c"]),z["d"],bounds_error=False,fill_value=None)
    a,b,c=(np.arange(box[2*i],box[2*i+1]+h,h) for i in range(3)); A,B,C=np.meshgrid(a,b,c,indexing="ij")
    d=blurred(lambda q: sd(V,Fc,q),A.ravel(),B.ravel(),C.ravel(),r).reshape(A.shape).astype(np.float32)
    np.savez(fn,a=a,b=b,c=c,d=d); return RegularGridInterpolator((a,b,c),d,bounds_error=False,fill_value=None)
def crotch_w(X,F,U):
    rho=np.sqrt((X/11.0)**2+((F-6.0)/11.0)**2+((U-92.5)/10.0)**2); return 1-ss(0.6,1.0,rho)
from wf_saurin_body8 import ellipsoid

# ---------------- new root: sacral platform -> caudal base -> join with donor ----------------------------------------
ROOT=[ # F,     U,    hw,   dV,   dD,   cv,   cb
 (-2.0, 109.0,  9.0,  6.0,  8.0, 1.25, 1.25),
 (-8.0, 104.5, 14.0,  9.0, 10.0, 1.24, 1.24),
 (-14.0, 99.0, 16.0, 10.0, 10.5, 1.24, 1.22),
 (-23.0, 95.0, 13.8, 10.2, 10.0, 1.25, 1.23),
 (-31.0, 91.5, 11.2, 10.5, 10.3, 1.26, 1.25),
 (-37.0, 88.4,  9.8, 10.4, 10.4, 1.28, 1.28),
 (-40.0, 85.9,  9.3, 10.2, 10.2, 1.30, 1.30),
 (-44.0, 81.1,  8.6,  9.3,  9.3, 1.32, 1.32),
 (-47.0, 78.8,  8.0,  8.6,  8.6, 1.34, 1.34),
]
def _path(n=700):
    pts=np.array([[0.0,a[0],a[1]] for a in ROOT]); seg=np.linalg.norm(np.diff(pts,axis=0),axis=1); s=np.concatenate([[0],np.cumsum(seg)])
    cs=CubicSpline(s,pts,bc_type="natural"); ss_=np.linspace(0,s[-1],n); P=cs(ss_); D=cs(ss_,1); D/=np.linalg.norm(D,axis=1,keepdims=True)
    par=np.array([a[2:] for a in ROOT]); sec=np.stack([PchipInterpolator(s,par[:,j])(ss_) for j in range(par.shape[1])],1)
    N=np.cross(D,np.array([1.0,0,0])); N/=np.linalg.norm(N,axis=1,keepdims=True); return P,D,N,sec
RP,RT,RN,RS=_path(); _RT=cKDTree(RP)
def plane_q2(x,f,wV,wD,dV,dD,cv,cb,k=11.0):
    tb=np.clip(0.5+f/(0.9*(dV+dD)),0,1); tb=tb*tb*(3-2*tb); w=wD+(wV-wD)*tb; ax=np.abs(x)/w
    t=np.stack([ax,f/dV,-f/dD,(ax+f/dV)/cv,(ax-f/dD)/cb]); m=t.max(0)
    return m+np.log(np.exp(k*(t-m)).sum(0))/k-np.log(1.6)/k
def root(X,F,U):
    Q=np.stack([X,F,U],-1); dist,idx=_RT.query(Q,distance_upper_bound=30.0); ok=np.isfinite(dist); out=np.full(X.shape,BIG)
    if not ok.any(): return out
    i=idx[ok]; r=Q[ok]-RP[i]; along=(r*RT[i]).sum(1); x=r[:,0]; f=-(r*RN[i]).sum(1)
    hw,dV,dD,cv,cb=RS[i].T; q=plane_q2(x,f,hw,hw,dV,dD,cv,cb); sz=np.minimum(hw,np.minimum(dV,dD))
    last=i==len(RP)-1; first=i==0
    e=np.where(last&(along>0),along/(0.9*sz),np.where(first&(along<0),-along/(0.9*sz),0.0))
    out[ok]=np.where(q>0,np.sqrt(q*q+e*e)-1,q-1+e)*sz; return out
# restrained dorsal axial ridge: continues B1's dorsal midline strap over the sacral platform onto the tail dorsum
_ri=np.where((RP[:,1]<=-1.0)&(RP[:,1]>=-42.0))[0]
RIDGE=RP[_ri]+RN[_ri]*(RS[_ri,2][:,None]-0.9)
_rs=(RP[_ri,1]-RP[_ri[0],1])/(RP[_ri[-1],1]-RP[_ri[0],1]); RIDGE_R=1.5-0.9*_rs
_RT2=cKDTree(RIDGE)
def ridge(X,F,U):
    Q=np.stack([X,F,U],-1); d,i=_RT2.query(Q,distance_upper_bound=15.0); out=np.full(X.shape,BIG); ok=np.isfinite(d)
    out[ok]=d[ok]-RIDGE_R[i[ok]]; return out
# ---------------- donor: B2 free tail beyond the cut plane at C0 -----------------------------------------------------
C0=np.array([0.0,-40.0,85.9]); TC=np.array([0.0,-np.cos(np.radians(48)),-np.sin(np.radians(48))])
def donor(X,F,U):
    Q=np.stack([X,F,U],-1); d=sd(Q2,f2,Q)
    wb=ss(-72.0,-62.0,F)                                   # 1 near the root, 0 distal (fine tip untouched)
    mb=wb>1e-3
    if mb.any():
        bl=DONOR_BLUR(np.stack([X[mb],F[mb],U[mb]],-1))
        d[mb]=d[mb]*(1-wb[mb])+bl*wb[mb]
    d=smax(d,F+31.0,0.4)                  # B2 body/legs excluded; the B2 root flare is overridden by the morph
    return d
# ---------------- edit field ------------------------------------------------------------------------------------------
K_ROOT=5.0; J0=35.0; J1=47.0
def field(X,F,U,parts=False):
    Q=np.stack([X,F,U],-1); b1=sd(P1,f1,Q)
    c=smax(b1,carve_keep(X,F,U),1.5)
    # crotch: replace the sexed form by a low-pass (blurred-SDF) version of the local B1 surface, then trim forward
    wc=crotch_w(X,F,U); m=wc>1e-3
    if m.any():
        bl=CROTCH_BLUR(np.stack([X[m],F[m],U[m]],-1))+0.6     # +0.6: recede slightly so nothing reads as a mound
        ell=(np.sqrt(((F[m]+4)/19.0)**2+((U[m]-104)/16.0)**2)-1)*16.0
        bl=smax(bl,ell,2.5)
        c[m]=c[m]*(1-wc[m])+bl*wc[m]
    # root -> donor: SDF morph over the junction (no union crease); donor alone beyond, root alone before
    r=smin(root(X,F,U),ridge(X,F,U),1.2); dn=np.full(X.shape,BIG); md=F<-31.0
    if md.any(): dn[md]=donor(X[md],F[md],U[md])
    t=ss(J0,J1,-F)
    tail=np.where(t<=0,r,np.where(t>=1,dn,(1-t)*np.minimum(r,BIG)+t*np.minimum(dn,BIG)))
    e=smin(c,tail,K_ROOT)
    return (e,b1) if parts else e
CROTCH_BLUR=_blur_grid("crotch",P1,f1,(-12,12,-6,18,81,104),4.0)
DONOR_BLUR=_blur_grid("donor",Q2,f2,(-13,13,-73,-32,48,110),2.5)
B8.sdf=lambda X,F,U: field(X,F,U)
B8.BOX=(-32.0,32.0,-124.0,28.0,38.0,124.0)
if __name__=="__main__":
    import time; t=time.time(); step=float(sys.argv[1]) if len(sys.argv)>1 else 0.35
    v,f=B8.mesh(step,log=lambda *a: print(*a,round(time.time()-t,1),flush=True))
    np.savez_compressed(sys.argv[2] if len(sys.argv)>2 else "edit_mc.npz",v=v,f=f); print("DONE",len(v),len(f),round(time.time()-t,1))
