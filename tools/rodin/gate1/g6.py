# Gate 3A: organic cervical integration. Same loft (silhouette), same TS6.1 head; the cervical layers are rebuilt as
# staggered, overlapping, interdigitating 3-D tissue paths with varying width/depth, cranial-base and mandibular seating,
# and fanned terminations that dissolve into the shoulder/thorax.
import numpy as np, sys
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline
import g5
from g1 import ss, smin, smax, BIG
from wf_saurin_body8 import ellipsoid
def base_field(X,F,U):
    """Gate 3A surface WITHOUT tissue paths (cut B1 + loft + head) - paths are projected onto this."""
    e=g5.g4.field(X,F,U); ax=np.abs(X)
    wb=(1-ss(9.0,13.0,ax))*ss(150.5,154.0,U); e=e*(1-wb)+(g5.NB(X,F,U)+0.1)*wb
    ucut=157.0+7.0*ss(10.0,15.5,ax); e=smax(e,U-ucut,2.0)
    e=smin(e,g5.loft(X,F,U),4.0); e=smin(e,g5.head(X,F,U),3.6); return e
def project(P,it=6):
    P=P.copy(); h=0.05
    for _ in range(it):
        f0=base_field(*P.T)
        g=np.stack([(base_field(*(P+np.array(d)*h).T)-f0)/h for d in ((1,0,0),(0,1,0),(0,0,1))],1)
        n=g/(np.linalg.norm(g,axis=1,keepdims=True)+1e-9); P=P-f0[:,None]*n
    return P,n
class Path3:
    """Surface-conforming tissue path, expressed as a smooth normal offset of the cervical surface: a curve projected
    onto the surface; the offset height h(t) and half-width w(t) vary organically; edges have their own tension; the
    height fades to zero at both ends so the structure emerges from / disappears into neighbouring tissue."""
    def __init__(s,pts,r,h,seed,n=320,mod=0.14,fade=(0.18,0.30),edge=0.42):
        P=np.asarray(pts,float); t=np.linspace(0,1,len(P)); cs=CubicSpline(t,P); tt=np.linspace(0,1,n)
        S,N=project(cs(tt))
        from scipy.ndimage import gaussian_filter1d
        for _ in range(2):                                     # even arc-length resampling + smoothing + re-projection
            L=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(S,axis=0),axis=1))]); u=np.linspace(0,L[-1],n)
            S=np.stack([np.interp(u,L,S[:,j]) for j in range(3)],1); S=gaussian_filter1d(S,4.0,axis=0,mode="nearest"); S,N=project(S,it=3)
        ph=np.random.default_rng(seed).uniform(0,6.3,3)
        s.w=np.interp(tt,t,r)*(1+mod*np.sin(2*np.pi*1.3*tt+ph[0])); hh=1.75*np.interp(tt,t,h)*(1+mod*np.sin(2*np.pi*2.1*tt+ph[1]))
        s.h=hh*ss(0.0,fade[0],tt)*(1-ss(1-fade[1],1.0,tt)); s.S=S; s.T=cKDTree(S); s.edge=edge
    def __call__(s,Q):
        d,i=s.T.query(Q,distance_upper_bound=16.0); out=np.zeros(len(Q)); ok=np.isfinite(d)
        w=s.w[i[ok]]; out[ok]=s.h[i[ok]]*(1-ss(s.edge*w,w,d[ok])); return out
PATHS=[]
for sg in (-1.0,1.0):
    r=np.random.default_rng(int(100+sg)); J=lambda a: r.uniform(-a,a)
    def P(x,f,u,a=0.35): return (sg*(x+J(a)),f+J(a),u+J(a))
    L=[]
    # cranial-base seating: short occipital/posterior-temporal fan diverging into the nuchal mass (staggered)
    L.append(Path3([P(1.2,-9.0,183.0),P(2.2,-10.2,178.6),P(3.0,-11.0,174.8)],[2.6,3.4,3.0],[0.35,0.55,0.30],int(1+sg),fade=(0.25,0.45)))
    L.append(Path3([P(3.4,-8.2,181.6),P(4.6,-9.6,176.8),P(5.8,-10.6,172.2)],[2.2,3.0,2.6],[0.30,0.50,0.25],int(2+sg),fade=(0.25,0.45)))
    L.append(Path3([P(5.0,-5.6,179.6),P(6.1,-7.4,175.0),P(6.9,-8.6,170.8)],[1.8,2.6,2.2],[0.25,0.45,0.20],int(3+sg),fade=(0.25,0.45)))
    # DORSAL deep nuchal mass: broad plane, strongest mid-neck, submerges toward the scapular region
    L.append(Path3([P(2.6,-9.0,177.5),P(4.0,-11.2,170.5),P(5.8,-13.2,164.0),P(7.8,-14.4,158.0)],[4.5,6.0,6.0,5.0],[0.45,0.85,0.75,0.35],int(4+sg),fade=(0.2,0.35)))
    # superficial nuchal slip: narrower, starts lower, crosses the deep mass obliquely and diverges to the scapula
    L.append(Path3([P(5.6,-8.6,174.0),P(7.8,-11.6,166.4),P(10.4,-13.4,158.8),P(12.8,-13.0,152.6)],[2.2,3.2,3.6,3.0],[0.30,0.60,0.55,0.25],int(5+sg),fade=(0.3,0.4)))
    # scapular fan: load spread into the upper scapular region / medial dorsal thorax
    for k,(a,b,ra,ha) in enumerate((((9.4,-14.2,158.0),(12.0,-13.4,151.4),3.2,0.40),((8.6,-14.8,157.6),(8.2,-15.8,151.4),2.8,0.30),((10.4,-13.2,158.6),(14.6,-11.6,152.4),2.6,0.30))):
        L.append(Path3([P(*a),P(*b)],[ra,ra*0.8],[ha,ha*0.7],int(6+k+sg),n=40,fade=(0.3,0.6)))
    # LATERAL layer 1: temporal/postorbital -> lateral cervical system -> acromial shoulder (broadest mid-neck)
    L.append(Path3([P(5.6,-1.6,178.2),P(6.6,-4.8,172.0),P(8.6,-6.7,165.0),P(11.6,-7.4,159.4),P(15.0,-6.0,155.4)],[2.4,3.6,4.6,4.4,3.2],[0.30,0.55,0.75,0.60,0.25],int(10+sg),fade=(0.2,0.3)))
    # LATERAL layer 2: mandibular sling, posterior mandible -> lateral clavicle, in front of / beneath layer 1
    L.append(Path3([P(4.6,4.2,171.2),P(5.8,1.6,167.4),P(7.4,0.1,162.6),P(9.6,0.6,157.6),P(12.2,1.5,154.8)],[2.4,3.2,3.8,3.6,2.6],[0.35,0.55,0.60,0.45,0.20],int(11+sg),fade=(0.12,0.35)))
    # interdigitating slips handing load between the lateral layers (short, crossing, staggered)
    L.append(Path3([P(7.0,0.3,163.6),P(8.6,-3.2,161.2),P(10.4,-6.6,158.8)],[1.8,2.4,2.0],[0.20,0.35,0.20],int(12+sg),n=50,fade=(0.3,0.4)))
    L.append(Path3([P(7.6,-6.0,167.4),P(8.2,-3.4,163.2),P(9.0,-0.8,158.8)],[1.6,2.2,1.8],[0.18,0.30,0.18],int(13+sg),n=50,fade=(0.3,0.4)))
    # mandibular-base sling toward the throat midline: depth under the jaw, no horizontal ledge
    L.append(Path3([P(4.9,3.6,171.4),P(3.4,4.4,168.6),P(1.2,4.4,166.0)],[2.0,2.8,2.4],[0.30,0.45,0.20],int(15+sg),n=60,fade=(0.15,0.5)))
    # VENTRAL throat sheet: broad, low, slightly asymmetric, spreading onto the chest shield in two fingers
    L.append(Path3([P(2.6,4.8,170.4),P(2.5,4.4,166.0),P(3.1,5.6,160.4),P(4.4,7.2,155.8)],[4.0,5.2,5.6,4.6],[0.30,0.45,0.45,0.25],int(16+sg),fade=(0.2,0.3)))
    L.append(Path3([P(3.8,6.8,157.0),P(5.8,9.4,152.6)],[2.4,1.8],[0.30,0.15],int(17+sg),n=40,fade=(0.3,0.6)))
    L.append(Path3([P(2.2,7.4,156.6),P(1.6,9.6,152.4)],[2.2,1.6],[0.28,0.14],int(18+sg),n=40,fade=(0.3,0.6)))
    PATHS+=L
MID=Path3([(0.0,-8.4,183.0),(0.1,-11.6,173.5),(-0.1,-14.6,164.0),(0.0,-17.2,156.0),(0.0,-18.6,149.0)],[1.3,1.6,1.7,1.6,1.5],[0.32,0.42,0.46,0.40,0.3],99,fade=(0.1,0.02),edge=0.35)
def heights(X,F,U):
    Q=np.stack([X,F,U],-1); h=np.zeros(len(X))
    for p in PATHS: v=p(Q); h=h+v*v                       # overlapping tissues combine smoothly (root-sum-square)
    return np.sqrt(h)+MID(Q)
def field(X,F,U):
    e=g5.g4.field(X,F,U)
    zone=U>148.0
    if not zone.any(): return e
    Xz,Fz,Uz=X[zone],F[zone],U[zone]; ez=e[zone]; e0=ez.copy(); ax=np.abs(Xz)
    wb=(1-ss(9.0,13.0,ax))*ss(150.5,154.0,Uz); ez=ez*(1-wb)+(g5.NB(Xz,Fz,Uz)+0.1)*wb
    ucut=157.0+7.0*ss(10.0,15.5,ax); ez=smax(ez,Uz-ucut,2.0)
    ez=smin(ez,g5.loft(Xz,Fz,Uz),4.0)
    ez=smin(ez,g5.head(Xz,Fz,Uz),3.6)                      # slightly wider skull seating than Gate 3 (3.0)
    hm=(Uz>149.0)&(Uz<186.0)
    if hm.any(): ez[hm]=ez[hm]-heights(Xz[hm],Fz[hm],Uz[hm])*(1-ss(176.0,184.0,Uz[hm])*ss(-6.0,-2.0,Fz[hm]))
    tw=ss(148.6,151.8,Uz); e[zone]=e0+(ez-e0)*tw; return e
import wf_saurin_body8 as B8
B8.sdf=lambda X,F,U: field(X,F,U)
B8.BOX=(-22.0,22.0,-26.0,28.0,146.0,190.5)
if __name__=="__main__":
    import time; t=time.time(); v,f=B8.mesh(float(sys.argv[1]) if len(sys.argv)>1 else 0.2,log=lambda *a: None)
    np.savez_compressed(sys.argv[2] if len(sys.argv)>2 else "edit6_mc.npz",v=v,f=f); print("DONE",len(v),len(f),round(time.time()-t,1))
