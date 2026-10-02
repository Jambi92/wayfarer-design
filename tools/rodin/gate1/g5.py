# Gate 3: head / neck / thorax integration on the locked Gate 2A body.
# Accepted TS6.1 cranium replaces the Rodin head; a cervical loft carries it into the B1 shoulder/thorax; layered dorsal,
# lateral and ventral cervical load paths (3-D bands) terminate into the Gate 2A shoulder/chest system.
import numpy as np, sys
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline, PchipInterpolator
from scipy.ndimage import spline_filter, map_coordinates
sys.path.insert(0,"/tmp/claude-0/rb")
import wf_saurin_body8 as B8
import g1, g4
from g1 import ss, smin, smax, BIG
from wf_saurin_body8 import round_cone
z=np.load("blur_neck.npz"); _A,_B,_C=z["a"],z["b"],z["c"]; _CO=spline_filter(z["d"].astype(np.float64),order=3)
def NB(X,F,U): return map_coordinates(_CO,np.stack([(X-_A[0])/0.6,(F-_B[0])/0.6,(U-_C[0])/0.6]),order=3,prefilter=False,mode="nearest")
# ---- cervical loft: section centre (F,U), half-width, ventral extent, dorsal extent, chamfers
NECK=[(-5.2,150.0,14.0,12.5,14.5,1.22,1.20),(-4.6,156.0,11.8,10.4,13.6,1.20,1.18),(-3.9,161.5,9.4,8.2,12.0,1.20,1.18),
      (-2.9,166.5,7.4,6.9,9.8,1.20,1.19),(-1.8,171.0,5.8,6.2,7.6,1.22,1.22),(-1.1,175.5,5.2,5.0,6.6,1.25,1.25)]
def _path(n=300):
    pts=np.array([[0.0,a[0],a[1]] for a in NECK]); s=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(pts,axis=0),axis=1))])
    cs=CubicSpline(s,pts); ss_=np.linspace(0,s[-1],n); P=cs(ss_); D=cs(ss_,1); D/=np.linalg.norm(D,axis=1,keepdims=True)
    par=np.array([a[2:] for a in NECK]); sec=np.stack([PchipInterpolator(s,par[:,j])(ss_) for j in range(par.shape[1])],1)
    N=np.cross(D,np.array([1.0,0,0])); N/=np.linalg.norm(N,axis=1,keepdims=True)      # ventral (+F) direction for an upward axis
    return P,D,N,sec
NP,ND,NN,NS=_path(); _NT=cKDTree(NP)
def loft(X,F,U):
    Q=np.stack([X,F,U],-1); dist,i=_NT.query(Q,distance_upper_bound=30.0); ok=np.isfinite(dist); out=np.full(X.shape,BIG)
    i=i[ok]; r=Q[ok]-NP[i]; along=(r*ND[i]).sum(1); x=r[:,0]; f=(r*NN[i]).sum(1)
    hw,dV,dD,cv,cb=NS[i].T
    q=g1.plane_q2(x,f,hw,hw,dV,dD,cv,cb,k=13.0); sz=np.minimum(hw,np.minimum(dV,dD))
    e=np.where((i==0)&(along<0),-along/(0.9*sz),np.where((i==len(NP)-1)&(along>0),along/(0.9*sz),0.0))
    out[ok]=np.where(q>0,np.sqrt(q*q+e*e)-1,q-1+e)*sz; return out
# ---- layered cervical load paths (3-D bands, partly sunk into the loft so they read as tissue planes)
def chain(P,pts,r):
    d=np.full(P[0].shape,BIG)
    for a,b,ra,rb in zip(pts[:-1],pts[1:],r[:-1],r[1:]): d=np.minimum(d,round_cone(P,np.array(a),np.array(b),ra,rb))
    return d
def bands(X,F,U):
    Pa=(np.abs(X),F,U); out=np.full(X.shape,BIG)
    def add(P,pts,r,sink): 
        nonlocal out; out=smin(out,chain(P,pts,r)+sink,1.2)
    # DORSAL: paired broad nuchal planes occiput -> upper scapular region / medial dorsal thorax (not a trapezius cape)
    add(Pa,[(2.8,-6.2,180.0),(4.6,-9.8,170.5),(7.0,-12.6,161.0),(9.8,-13.4,152.5)],[2.4,3.4,3.8,2.8],2.3)
    # dorsal midline: occipital crest -> B1 dorsal axial strap (continuous axial line skull -> sacrum)
    add((X,F,U),[(0.0,-8.4,183.0),(0.0,-12.0,171.0),(0.0,-15.6,161.0),(0.0,-17.4,155.0)],[0.9,1.1,1.2,1.2],0.0)
    # LATERAL layer 1: posterior/temporal cranial base -> cervical column -> lateral shoulder (acromial) foundation
    add(Pa,[(4.4,-4.8,176.0),(6.4,-6.4,167.0),(9.8,-7.6,159.5),(15.0,-6.0,155.6)],[2.0,2.9,3.1,2.4],1.9)
    # LATERAL layer 2: mandibular base -> lateral clavicular strap, a separate flatter plane in front of layer 1
    add(Pa,[(4.2,2.6,170.6),(5.9,1.4,163.5),(8.6,0.6,157.0),(12.2,1.0,154.2)],[2.2,2.9,2.9,2.1],2.1)
    # VENTRAL: one broad, low throat sheet from the deep jaw base spreading onto the chest shield (no cords, no organ)
    add(Pa,[(2.2,2.0,170.0),(2.6,3.4,164.0),(3.2,5.4,158.0),(3.6,7.4,154.0)],[3.4,4.2,4.4,3.4],3.2)
    return out
SINK=0.0
def head(X,F,U): return B8.head((X,F,U))
def field(X,F,U):
    e=g4.field(X,F,U)
    zone=U>148.0
    if not zone.any(): return e
    Xz,Fz,Uz=X[zone],F[zone],U[zone]; ez=e[zone]; e0=ez.copy(); ax=np.abs(Xz)
    # 1) soften B1's human neck cords / trapezius cape at the cervicothoracic base (low-pass of B1's own surface)
    wb=(1-ss(9.0,13.0,ax))*ss(150.5,154.0,Uz)
    nb=NB(Xz,Fz,Uz)+0.1
    ez=ez*(1-wb)+nb*wb
    # 2) remove the Rodin head + neck column above the cervical cut (shoulders beyond |x|~15 untouched)
    ucut=157.0+7.0*ss(10.0,15.5,ax)
    ez=smax(ez,Uz-ucut,2.0)
    # 3) cervical loft, accepted TS6.1 cranium, layered load paths
    ez=smin(ez,loft(Xz,Fz,Uz),4.0)
    ez=smin(ez,bands(Xz,Fz,Uz)+SINK,2.2)
    ez=smin(ez,head(Xz,Fz,Uz),3.0)
    tw=ss(148.6,151.8,Uz)                                  # every Gate-3 change fades out above the locked Gate-2A torso
    e[zone]=e0+(ez-e0)*tw; return e
B8.sdf=lambda X,F,U: field(X,F,U)
B8.BOX=(-22.0,22.0,-26.0,28.0,146.0,190.5)
if __name__=="__main__":
    import time; t=time.time(); v,f=B8.mesh(float(sys.argv[1]) if len(sys.argv)>1 else 0.2,log=lambda *a: None)
    np.savez_compressed(sys.argv[2] if len(sys.argv)>2 else "edit5_mc.npz",v=v,f=f); print("DONE",len(v),len(f),round(time.time()-t,1))
