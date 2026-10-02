# Gate 4: hindlimb / foot load-path reconstruction on the locked Gate 3A body.
import numpy as np, sys
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline
from scipy.ndimage import spline_filter, map_coordinates, gaussian_filter1d
import g6
from g1 import ss, smin, smax, BIG
from wf_saurin_body8 import ellipsoid
import foot
z=np.load("blur_legs.npz"); _A,_B,_C=z["a"],z["b"],z["c"]; _CO=spline_filter(z["d"].astype(np.float64),order=3)
def LB(X,F,U): return map_coordinates(_CO,np.stack([(X-_A[0])/0.7,(F-_B[0])/0.7,(U-_C[0])/0.7]),order=3,prefilter=False,mode="nearest")
# per-side skeleton (from B1's own leg axes; stance unchanged): hip H, knee K, ankle A ; foot toe-out
SK={-1:dict(H=(-13.0,3.5,86.0),K=(-17.4,2.8,62.0),A=(-26.4,0.2,9.6),toe=6.0),
     1:dict(H=( 13.0,3.5,86.0),K=( 15.2,3.0,62.0),A=( 21.6,1.6,9.6),toe=6.0)}
_R=np.load("/tmp/claude-0/rodin/adopt/b1_regions.npz")["R"]
_ARM=cKDTree(g6.g5.g1.P1[(_R==4)&(g6.g5.g1.P1[:,2]>66.0)])
def leg_weight(X,F,U):
    w=(1-ss(74.0,80.0,U))*ss(3.0,6.5,np.abs(X))
    da,_=_ARM.query(np.stack([X,F,U],-1),distance_upper_bound=6.0); da=np.where(np.isfinite(da),da,6.0)
    w*=ss(1.2,3.2,da)                                                # arms/hands are locked: never re-surface near them
    w*=1-(1-ss(-24.0,-18.0,F))*(1-ss(10.0,13.0,np.abs(X)))          # never touch the tail behind/between the legs
    return w
def base_leg(X,F,U):
    """low-pass of B1's own leg (removes human muscle map, knee plate, calf fin), cut above the new foot, + new foot"""
    e=LB(X,F,U)+0.15
    e=e+1.5*(1-ss(13.0,27.0,U))                                     # lower leg tapers into a narrower ankle
    for sg,S in SK.items():
        m=np.sign(X)==sg
        if not m.any(): continue
        K=S["K"]; kw=np.exp(-(((U[m]-(K[2]-2.0))/7.0)**2+((X[m]-K[0])**2+(F[m]-K[1]-5.0)**2)/90.0))   # knee region weight
        acc=np.zeros(m.sum())
        for d in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            acc+=LB(X[m]+3.2*d[0],F[m]+3.2*d[1],U[m]+3.2*d[2])
        e[m]=e[m]*(1-kw)+(acc/6.0+0.25)*kw                              # stronger local low-pass removes the patellar lump / knee plate
        # calf: reduce B1's bulbous calf ball (the propulsion structure is rebuilt as an elongated, tapering mass)
        cc=np.array(axis_pt(S,1.30))+np.array([0.0,-9.5,0.0]); r2=((X[m]-cc[0])**2+(F[m]-cc[1])**2)/40.0+((U[m]-cc[2])/10.0)**2
        e[m]=e[m]+1.8*np.exp(-r2)
    e=smax(e,11.6-U,2.6)
    for sg,S in SK.items():
        m=np.sign(X)==sg
        if m.any(): e[m]=smin(e[m],foot.foot_world(X[m],F[m],U[m],(S["A"][0],S["A"][1]),S["toe"],sg),3.4)
    return e
def axis_pt(S,s):
    H,K,A=map(np.array,(S["H"],S["K"],S["A"]))
    return H+(K-H)*s if s<=1 else K+(A-K)*(s-1)
def project(P,it=6):
    P=P.copy(); h=0.05
    for _ in range(it):
        f0=base_leg(*P.T); g=np.stack([(base_leg(*(P+np.array(d)*h).T)-f0)/h for d in ((1,0,0),(0,1,0),(0,0,1))],1)
        n=g/(np.linalg.norm(g,axis=1,keepdims=True)+1e-9); P=P-f0[:,None]*n
    return P,n
class LPath:
    """surface-conforming load path on the limb (normal offset); stations = (s along H->K->A, angle around the limb:
    0 front, 90 lateral, 180 back, -90 medial); width/height profiles fade at both ends"""
    def __init__(s_,S,sg,stations,w,h,seed,n=260,mod=0.12,fade=(0.15,0.25),edge=0.4,R=10.0):
        pts=[]
        for (s,th) in stations:
            c=axis_pt(S,s); t=np.radians(th); d=np.array([np.sin(t)*sg,np.cos(t),0.0]); pts.append(c+R*d)
        P=np.array(pts); t=np.linspace(0,1,len(P)); cs=CubicSpline(t,P); tt=np.linspace(0,1,n)
        Q,_=project(cs(tt))
        for _ in range(2):
            L=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]); u=np.linspace(0,L[-1],n)
            Q=np.stack([np.interp(u,L,Q[:,j]) for j in range(3)],1); Q=gaussian_filter1d(Q,4.0,axis=0,mode="nearest"); Q,_=project(Q,it=3)
        ph=np.random.default_rng(seed).uniform(0,6.3,2)
        s_.w=np.interp(tt,t,w)*(1+mod*np.sin(2*np.pi*1.4*tt+ph[0])); hh=np.interp(tt,t,h)*(1+mod*np.sin(2*np.pi*2.2*tt+ph[1]))
        s_.h=hh*ss(0,fade[0],tt)*(1-ss(1-fade[1],1,tt)); s_.T=cKDTree(Q); s_.edge=edge
    def __call__(s_,Q):
        d,i=s_.T.query(Q,distance_upper_bound=12.0); out=np.zeros(len(Q)); ok=np.isfinite(d)
        w=s_.w[i[ok]]; out[ok]=s_.h[i[ok]]*(1-ss(s_.edge*w,w,d[ok])); return out
PATHS={}
for sg,S in SK.items():
    L=[]; sd=int(50+sg)
    # THIGH (long directional planes, overlapping; no human quad/ham/adductor map)
    L.append(LPath(S,sg,[(0.12,-5),(0.45,0),(0.80,6),(0.98,4)],[4.6,4.2,3.6,2.8],[0.70,0.95,0.80,0.40],sd+1))          # femorotibial extensor plane
    L.append(LPath(S,sg,[(0.10,70),(0.40,52),(0.72,30),(0.95,18)],[3.8,3.6,3.0,2.4],[0.55,0.75,0.65,0.35],sd+2))       # iliotibial: lateral hip -> anterolateral knee
    L.append(LPath(S,sg,[(0.15,130),(0.50,112),(0.85,96),(1.05,90)],[2.8,2.6,2.2,1.6],[0.45,0.65,0.55,0.30],sd+3))     # iliofibular: posterolateral hip -> lateral knee
    L.append(LPath(S,sg,[(0.12,175),(0.45,170),(0.78,165),(1.00,160)],[3.6,3.4,2.8,2.2],[0.70,0.85,0.70,0.40],sd+4))   # caudofemoral continuation -> knee flexion
    L.append(LPath(S,sg,[(0.15,-150),(0.50,-160),(0.85,-168),(1.05,-170)],[3.2,3.0,2.6,2.0],[0.55,0.70,0.60,0.30],sd+5)) # medial flexor (ischial -> medial knee)
    L.append(LPath(S,sg,[(0.10,-75),(0.45,-85),(0.85,-100)],[5.0,4.4,3.2],[0.40,0.55,0.30],sd+6))                     # adductor plane (medial)
    # KNEE: femoral termination, collateral stabilisation, extensor sheet, posterior flexion volume
    L.append(LPath(S,sg,[(0.86,80),(1.0,88),(1.12,92)],[1.8,1.6,1.4],[0.45,0.60,0.40],sd+7,n=120,fade=(0.25,0.3)))     # lateral collateral ridge
    L.append(LPath(S,sg,[(0.84,-60),(0.98,-70),(1.10,-60)],[2.6,2.8,2.0],[0.35,0.50,0.25],sd+8,n=120,fade=(0.25,0.35))) # medial condylar mass
    L.append(LPath(S,sg,[(0.86,8),(1.0,4),(1.14,-4)],[3.6,3.4,2.6],[0.30,0.35,0.25],sd+9,n=120,fade=(0.3,0.3)))         # extensor sheet over the knee (no patellar cap)
    L.append(LPath(S,sg,[(0.90,178),(1.02,180),(1.12,182)],[3.4,3.6,3.0],[0.40,0.55,0.35],sd+10,n=120,fade=(0.3,0.3)))  # posterior flexion volume
    # LOWER LEG: front/back + medial/lateral organisation; load-bearing tibial line vs propulsion mass
    L.append(LPath(S,sg,[(1.10,-14),(1.45,-18),(1.80,-20),(1.97,-22)],[1.3,1.3,1.2,1.0],[0.45,0.50,0.40,0.20],sd+11,edge=0.5))   # tibial crest (load-bearing line)
    L.append(LPath(S,sg,[(1.10,22),(1.45,26),(1.80,24),(2.00,14),(2.10,6)],[2.6,2.4,1.8,1.1,0.9],[0.60,0.70,0.50,0.35,0.25],sd+12))  # anterior extensor -> dorsal ankle tendon
    L.append(LPath(S,sg,[(1.04,165),(1.25,160),(1.55,168),(1.85,178),(2.02,180)],[4.6,5.2,3.8,1.8,1.3],[0.55,0.80,0.65,0.40,0.32],sd+13,fade=(0.12,0.1)))  # lateral propulsion head -> calcaneal tendon
    L.append(LPath(S,sg,[(1.04,-160),(1.22,-165),(1.45,-172)],[3.8,4.0,2.6],[0.45,0.60,0.30],sd+14,fade=(0.2,0.45)))            # medial propulsion head (shorter, ends higher: asymmetry)
    L.append(LPath(S,sg,[(1.12,100),(1.50,104),(1.88,110),(2.02,118)],[2.2,2.0,1.6,1.2],[0.45,0.55,0.40,0.20],sd+15))         # lateral peroneal band -> lateral ankle
    PATHS[sg]=L
def leg_heights(X,F,U):
    h=np.zeros(len(X)); Q=np.stack([X,F,U],-1)
    for sg,L in PATHS.items():
        m=np.sign(X)==sg
        if not m.any(): continue
        acc=np.zeros(m.sum())
        for p in L: v=p(Q[m]); acc+=v*v
        h[m]=np.sqrt(acc)
    return h*(1-ss(10.5,14.0,U)*0)                 # (feet are not offset: U<11 has no paths)
def field(X,F,U):
    e=g6.field(X,F,U)
    w=leg_weight(X,F,U); m=w>1e-4
    if m.any():
        b=base_leg(X[m],F[m],U[m])
        hm=U[m]>10.0
        if hm.any():
            idx=np.where(m)[0][hm]; b[hm]=b[hm]-leg_heights(X[idx],F[idx],U[idx])*ss(10.0,14.0,U[idx])
        e[m]=e[m]*(1-w[m])+b*w[m]
    return e
import wf_saurin_body8 as B8
B8.sdf=lambda X,F,U: field(X,F,U)
B8.BOX=(-38.0,38.0,-20.0,40.0,-0.6,84.0)
if __name__=="__main__":
    import time; t=time.time(); v,f=B8.mesh(float(sys.argv[1]) if len(sys.argv)>1 else 0.22,log=lambda *a: None)
    np.savez_compressed(sys.argv[2] if len(sys.argv)>2 else "edit7_mc.npz",v=v,f=f); print("DONE",len(v),len(f),round(time.time()-t,1))
