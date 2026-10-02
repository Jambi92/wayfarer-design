# Gate 2A: organic integration of the Gate 2 torso map (same map; living-tissue variation, interdigitation, fibre tension).
import numpy as np, sys
from scipy.spatial import cKDTree
import g1, g2, g3
from g1 import ss, smin, smax, BIG
RNG=np.random.default_rng(20261002)
def bez(p0,c,p1,n=160):
    t=np.linspace(0,1,n)[:,None]; p0,c,p1=map(np.asarray,(p0,c,p1)); return (1-t)**2*p0+2*(1-t)*t*c+t**2*p1
class Band:
    """Curved fascial/muscular band on the (x,u) surface chart: width/height vary organically along its length,
    edges carry different tension (one crisper, one softer), fibres striate along its length."""
    def __init__(s,pts,w,h,edge=(0.25,0.45),stri=0.09,lam=1.15,seed=0,mod=0.18,fade=(0.06,0.10)):
        s.P=np.asarray(pts,float); s.T=cKDTree(s.P); s.n=len(s.P); s.w=w; s.h=h; s.edge=edge; s.stri=stri; s.lam=lam; s.fade=fade
        r=np.random.default_rng(seed); s.ph=r.uniform(0,2*np.pi,6); s.mod=mod
        d=np.gradient(s.P,axis=0); s.D=d/np.linalg.norm(d,axis=1,keepdims=True)
    def __call__(s,x,u):
        q=np.stack([x,u],-1); dist,i=s.T.query(q); t=i/(s.n-1)
        side=np.sign((q[:,0]-s.P[i,0])*s.D[i,1]-(q[:,1]-s.P[i,1])*s.D[i,0])
        m=1+s.mod*np.sin(2*np.pi*(1.7*t)+s.ph[0])+0.5*s.mod*np.sin(2*np.pi*(3.9*t)+s.ph[1])
        w=(s.w[0]+(s.w[1]-s.w[0])*t)*m; h=(s.h[0]+(s.h[1]-s.h[0])*t)*(1+0.8*s.mod*np.sin(2*np.pi*2.3*t+s.ph[2]))
        a=np.where(side>0,s.edge[0],s.edge[1]); prof=1-ss(a*w,w,dist)
        fade=ss(0.0,s.fade[0],t)*(1-ss(1-s.fade[1],1.0,t))
        sd=side*dist
        stri=s.stri*np.cos(2*np.pi*sd/s.lam+0.9*np.sin(2*np.pi*2.1*t+s.ph[3]))*prof*(1-ss(0.6*w,w,dist))
        return h*prof*fade+stri*fade
def jit(v,s,a): return v+a*s
SIDES=(-1.0,1.0)
BANDS={}
for sg in SIDES:
    r=np.random.default_rng(int(7+sg)); j=lambda a: r.uniform(-a,a)
    L=[]
    # long oblique chain: gentle S-curve thorax -> pelvic platform
    L.append(Band(bez((14.6+j(.3),133.5+j(.4)),(13.2+j(.5),119.0+j(.8)),(6.2+j(.25),103.5)),(4.3,3.0),(0.95,0.50),edge=(0.22,0.42),seed=int(11+sg),mod=0.16,stri=0.035,lam=1.8))
    # costal arch: sternal apex -> costal margin, curving, fading into the lateral rib relief
    ca_end=(13.0+j(.3),124.0+j(.4))
    arch=np.vstack([bez((1.3,134.0),(7.6+j(.4),131.6+j(.5)),ca_end,110)[:-1],bez(ca_end,(15.6+j(.4),119.5+j(.6)),(17.4+j(.3),113.5+j(.5)),70)])
    L.append(Band(arch,(2.0,1.8),(0.85,0.15),edge=(0.15,0.30),seed=int(21+sg),stri=0.025,mod=0.10,fade=(0.03,0.18)))
    L.append(Band(np.zeros((2,2))+[[-50,-50],[-51,-51]],(0.1,0.1),(0.0,0.0)))            # placeholder keeps band indices stable
    # interdigitating tongues: broad, soft wedges where the shield margin hands load down-and-out into the oblique chain
    for k,(u0,ln,wd,ht) in enumerate(((126.0+j(.7),8.5+j(.8),2.6,0.30),(118.4+j(.8),9.5+j(.9),2.9,0.34),(110.8+j(.7),7.0+j(.7),2.3,0.26))):
        hw=6.4+(3.8-6.4)*np.clip((132.0-u0)/27.0,0,1)
        p0=(hw-1.0,u0+1.0); p1=(hw+ln*0.55,u0-ln*0.83); c=((p0[0]+p1[0])/2+0.7,(p0[1]+p1[1])/2+0.3)
        L.append(Band(bez(p0,c,p1,80),(wd,0.7),(ht,0.03),edge=(0.10,0.22),seed=int(41+10*k+sg),stri=0.0,mod=0.12,fade=(0.30,0.45)))
    # pectoral fan: three fascicles, different widths/prominence/curvature/termination, converging on the humerus
    ins=np.array([17.4+j(.2),146.3+j(.3)])
    for k,(u0,w0,hh,bow,fd) in enumerate(((150.4,2.5,0.34,0.9,0.30),(146.0+j(.4),3.4,0.56,-0.5,0.18),(141.4+j(.4),2.3,0.44,1.4,0.26))):
        p0=np.array([1.8,u0]); c=(p0+ins)/2+np.array([0.0,bow]); L.append(Band(bez(p0,c,ins),(w0,1.5),(hh,0.16),edge=(0.26,0.46),seed=int(61+10*k+sg),stri=0.03,lam=1.7,mod=0.2,fade=(0.08,fd)))
    BANDS[sg]=L
def organic_noise(x,u,amp=0.10):
    # low-amplitude, anisotropic (mostly longitudinal/oblique) tissue undulation; side-specific phases
    v=np.zeros_like(x)
    for k,(kx,ku,a,ph) in enumerate(((0.55,0.22,1.0,0.3),(0.31,0.48,0.8,1.7),(0.82,0.35,0.5,2.9),(0.21,0.71,0.6,4.1))):
        v+=a*np.sin(kx*x+ku*u+ph+0.4*np.sign(x))
    return amp*v/2.9
def heights(X,U):
    ax=np.abs(X); h=np.zeros_like(X)
    # ventral shield: continuous; width breathes along its length; crown drifts; edge tension varies by side
    sgn=np.where(X>=0,1.0,-1.0)
    base=6.4+(3.8-6.4)*np.clip((132.0-U)/27.0,0,1)
    hw=base*(1+0.07*np.sin(0.21*U+0.6*sgn)+0.04*np.sin(0.53*U+1.3+0.9*sgn))
    edge=np.where(sgn>0,1.3,1.8)
    sh=(1-ss(hw-edge,hw+0.25,ax))*ss(103.0,108.5,U)*(1-ss(130.5,133.8,U))
    crown_x=0.35*np.sin(0.17*U+0.4)                                     # crown line drifts slightly off-axis
    crown=0.85+0.28*(1-ss(0.0,hw*0.75,np.abs(X-crown_x)))*(0.75+0.25*np.sin(0.29*U+0.8))
    # shallow compression/extension zones: irregular, oblique, NOT aligned across the midline (no segmentation)
    dep=np.zeros_like(X)
    for (cx,cu,rx,ru,rot,d) in ((2.6,124.2,2.8,1.7,0.5,0.14),(-3.0,119.6,2.4,1.9,-0.6,0.12),(1.4,112.8,2.9,1.6,0.3,0.10),(-2.2,127.6,2.0,1.5,-0.3,0.08)):
        ca,sa=np.cos(rot),np.sin(rot); px=(X-cx)*ca+(U-cu)*sa; pu=-(X-cx)*sa+(U-cu)*ca
        dep+=d*(1-ss(0.3,1.0,np.sqrt((px/rx)**2+(pu/ru)**2)))
    h+=sh*(crown-dep)
    # margin groove only where no tongue crosses it (integration, not a panel edge)
    gx=hw+0.7; groove=0.30*(1-ss(0.25,0.95,np.abs(ax-gx)))*ss(104.0,108.0,U)*(1-ss(128.0,131.0,U))
    for sg in SIDES:
        m=(sgn==sg)
        if not m.any(): continue
        bsum=np.zeros(m.sum())
        for k,b in enumerate(BANDS[sg]): bsum+=b(ax[m],U[m])
        tongues=sum(b(ax[m],U[m]) for b in BANDS[sg][3:6])
        groove[m]*=np.clip(1-2.2*tongues,0,1)
        h[m]+=bsum
    h-=groove
    h+=organic_noise(X,U)*ss(104.0,110.0,U)*(1-ss(148.0,152.0,U))
    return h
def field(X,F,U):
    e=g2.field(X,F,U)
    w=g3.weight(X,F,U); m=w>1e-4
    if m.any():
        Xm,Fm,Um=X[m],F[m],U[m]
        tb=g3.TB(np.stack([Xm,Fm,Um],-1))
        b=tb+0.15
        cw=g3.chest_w(Xm,Um); cp=g3.chest_plane(Xm,Fm,Um); b=b*(1-cw)+smax(b,cp,2.4)*cw
        # restrained B1 tension on the lateral thorax/flank (load-path regions without human organisation):
        ax=np.abs(Xm); wd=ss(14.0,16.5,ax)*ss(113.0,118.0,Um)*(1-ss(140.0,146.0,Um))
        b=b+0.45*wd*(e[m]-tb)
        b=b-heights(Xm,Um)
        e[m]=e[m]*(1-w[m])+b*w[m]
    return e
import wf_saurin_body8 as B8
B8.sdf=lambda X,F,U: field(X,F,U)
B8.BOX=g3.B8.BOX if False else (-22.0,22.0,-10.0,24.0,99.0,158.0)
if __name__=="__main__":
    import time; t=time.time(); v,f=B8.mesh(float(sys.argv[1]) if len(sys.argv)>1 else 0.3,log=lambda *a: None)
    np.savez_compressed(sys.argv[2] if len(sys.argv)>2 else "edit4_mc.npz",v=v,f=f); print("DONE",len(v),len(f),round(time.time()-t,1))
