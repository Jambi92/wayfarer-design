# Gate 5: forelimb / wrist / hand reconstruction on the accepted Gate 4 body.
import numpy as np, sys
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline
from scipy.ndimage import spline_filter, map_coordinates, gaussian_filter1d
import g7
from g1 import ss, smin, smax, BIG
import hand
z=np.load("blur_arms.npz"); GR={}
for sg in (-1,1):
    k="%d"%(sg>0); GR[sg]=(z["a"+k],z["b"+k],z["c"+k],spline_filter(z["d"+k].astype(np.float64),order=3))
def AB(X,F,U,sg):
    a,b,c,co=GR[sg]; return map_coordinates(co,np.stack([(X-a[0])/0.7,(F-b[0])/0.7,(U-c[0])/0.7]),order=3,prefilter=False,mode="nearest")
SK={-1:dict(S=(-23.5,-6.0,147.0),E=(-30.5,-4.5,117.0),W=(-36.8,6.0,97.0)),
     1:dict(S=( 23.0,-5.0,147.0),E=( 28.8,-3.5,117.0),W=( 35.2,7.0,97.0))}
def seg_dist(Q,A,B):
    A=np.asarray(A,float); B=np.asarray(B,float); v=B-A; t=np.clip(((Q-A)@v)/(v@v),0,1); return np.linalg.norm(Q-(A+t[:,None]*v),axis=1),t
_AV=np.load("arm_vert_mask.npy"); _AT=cKDTree(g7.g6.g5.g1.P1[_AV])
def arm_weight(X,F,U,sg):
    S=SK[sg]; Q=np.stack([X,F,U],-1)
    d1,_=seg_dist(Q,S["S"],S["E"]); d2,_=seg_dist(Q,S["E"],S["W"]); dh=np.linalg.norm(Q-np.asarray(S["W"]),axis=1)
    w=np.maximum.reduce([1-ss(9.5,12.5,d1),1-ss(7.8,10.5,d2),1-ss(21.0,24.0,dh)])
    w*=ss(19.6,21.2,np.abs(X))                                           # torso locked (|x| < 19.6)
    da,_=_AT.query(Q,distance_upper_bound=8.0); da=np.where(np.isfinite(da),da,8.0)
    dh_new=hand.hand_world(X,F,U,S["W"],S["E"],sg)
    w*=np.maximum(1-ss(4.0,7.0,da),1-ss(1.0,4.0,dh_new))               # only near B1's own arm or the new hand (hip/thigh stay locked)
    return w
def base_arm(X,F,U,sg):
    # base = low-pass of B1 arm + the closed upper body (blur_arms.py), so the arm grows out of the shoulder mass with no deltoid cap/rim
    S=SK[sg]; e=AB(X,F,U,sg)+0.15
    Q=np.stack([X,F,U],-1); _,t=seg_dist(Q,S["E"],S["W"]); e=e+0.5*ss(0.55,1.0,t)   # forearm narrows into the wrist
    a=hand.frame(S["W"],S["E"],sg)[0]; e=smax(e,(Q-np.asarray(S["W"]))@a-1.8,1.8)                                          # remove the old Rodin hand beyond the wrist
    e=smin(e,hand.hand_world(X,F,U,S["W"],S["E"],sg),2.4)
    return e
def axis_pt(S,s):
    A,B,C=map(np.array,(S["S"],S["E"],S["W"])); return A+(B-A)*s if s<=1 else B+(C-B)*(s-1)
def project(P,sg,it=6):
    P=P.copy(); h=0.05
    for _ in range(it):
        f0=base_arm(*P.T,sg); g=np.stack([(base_arm(*(P+np.array(d)*h).T,sg)-f0)/h for d in ((1,0,0),(0,1,0),(0,0,1))],1)
        n=g/(np.linalg.norm(g,axis=1,keepdims=True)+1e-9); P=P-f0[:,None]*n
    return P
class APath:
    def __init__(s_,sg,stations,w,h,seed,n=220,mod=0.12,fade=(0.15,0.25),edge=0.4,R=9.0):
        S=SK[sg]; pts=[]
        for (s,th) in stations:
            c=axis_pt(S,max(s,0.0)); t=np.radians(th); pts.append(c+R*np.array([np.sin(t)*sg,np.cos(t),0.0]))
        P=np.array(pts); t=np.linspace(0,1,len(P)); tt=np.linspace(0,1,n); Q=project(CubicSpline(t,P)(tt),sg)
        for _ in range(2):
            L=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]); u=np.linspace(0,L[-1],n)
            Q=np.stack([np.interp(u,L,Q[:,j]) for j in range(3)],1); Q=gaussian_filter1d(Q,4.0,axis=0,mode="nearest"); Q=project(Q,sg,it=3)
        ph=np.random.default_rng(seed).uniform(0,6.3,2)
        s_.w=np.interp(tt,t,w)*(1+mod*np.sin(2*np.pi*1.4*tt+ph[0])); hh=np.interp(tt,t,h)*(1+mod*np.sin(2*np.pi*2.2*tt+ph[1]))
        s_.h=hh*ss(0,fade[0],tt)*(1-ss(1-fade[1],1,tt)); s_.T=cKDTree(Q); s_.edge=edge
    def __call__(s_,Q):
        d,i=s_.T.query(Q,distance_upper_bound=10.0); out=np.zeros(len(Q)); ok=np.isfinite(d)
        w=s_.w[i[ok]]; out[ok]=s_.h[i[ok]]*(1-ss(s_.edge*w,w,d[ok])); return out
PATHS={}; NEG={}
for sg in (-1,1):
    sd=int(70+sg); L=[]
    # SHOULDER: overlapping clavicular / acromial / scapular fans converging on the lateral humerus (no deltoid ball)
    L.append(APath(sg,[(0.0,25),(0.30,42),(0.55,62)],[3.8,3.2,2.2],[0.55,0.65,0.30],sd+1,fade=(0.3,0.35)))
    L.append(APath(sg,[(0.0,90),(0.28,86),(0.55,76)],[4.2,3.6,2.4],[0.55,0.70,0.30],sd+2,fade=(0.3,0.35)))
    L.append(APath(sg,[(0.0,158),(0.30,128),(0.55,98)],[3.6,3.2,2.2],[0.50,0.60,0.28],sd+3,fade=(0.3,0.35)))
    # UPPER ARM: long anterior flexor plane (continues into the medial forearm), posterior extensor plane + lateral slip
    L.append(APath(sg,[(0.20,8),(0.60,4),(0.95,-4),(1.15,-28)],[3.8,3.6,2.8,2.0],[0.55,0.75,0.55,0.25],sd+4))
    L.append(APath(sg,[(0.06,176),(0.50,180),(0.92,184),(1.02,182)],[4.4,4.2,3.2,2.2],[0.55,0.85,0.70,0.35],sd+5))
    L.append(APath(sg,[(0.25,140),(0.65,150),(0.98,160)],[2.6,2.4,1.8],[0.35,0.50,0.25],sd+6))
    # ELBOW: posterior extension ridge, medial/lateral epicondylar stabilisers
    L.append(APath(sg,[(0.90,180),(1.0,180),(1.08,178)],[2.0,2.2,1.8],[0.40,0.60,0.35],sd+7,n=100,fade=(0.3,0.35)))
    L.append(APath(sg,[(0.88,-96),(0.98,-100),(1.08,-96)],[2.4,2.6,2.0],[0.35,0.55,0.30],sd+8,n=100,fade=(0.3,0.35)))
    L.append(APath(sg,[(0.84,96),(0.96,92),(1.10,88)],[1.8,2.0,1.6],[0.35,0.50,0.30],sd+9,n=100,fade=(0.3,0.35)))
    # FOREARM: flexor mass (palmar/medial), extensor mass (dorsal), spiral rotational band, ulnar load ridge, distal tendons
    L.append(APath(sg,[(1.04,-85),(1.35,-62),(1.70,-50),(1.96,-42)],[4.2,3.8,2.4,1.4],[0.60,0.80,0.50,0.25],sd+10,fade=(0.15,0.15)))
    L.append(APath(sg,[(1.04,104),(1.40,120),(1.75,130),(1.96,134)],[3.8,3.4,2.2,1.3],[0.55,0.75,0.45,0.22],sd+11,fade=(0.15,0.15)))
    L.append(APath(sg,[(0.78,72),(1.10,56),(1.50,36),(1.95,16)],[3.0,2.8,2.0,1.2],[0.45,0.65,0.45,0.22],sd+12))
    L.append(APath(sg,[(1.06,-150),(1.50,-160),(1.95,-166)],[1.4,1.3,1.1],[0.35,0.45,0.25],sd+13,edge=0.5))
    L.append(APath(sg,[(1.72,122),(1.98,128)],[0.8,0.7],[0.22,0.18],sd+14,n=60,fade=(0.3,0.2),edge=0.5))
    L.append(APath(sg,[(1.72,-46),(1.98,-40)],[0.8,0.7],[0.22,0.18],sd+15,n=60,fade=(0.3,0.2),edge=0.5))
    PATHS[sg]=L
    NEG[sg]=APath(sg,[(0.95,12),(1.0,4),(1.05,-6)],[3.4,3.8,3.2],[0.22,0.30,0.20],sd+16,n=80,fade=(0.35,0.35),edge=0.0)    # anterior hinge (cubital) depression
def heights(X,F,U,sg):
    Q=np.stack([X,F,U],-1); acc=np.zeros(len(X))
    for p in PATHS[sg]: v=p(Q); acc+=v*v
    return np.sqrt(acc)-NEG[sg](Q)
def field(X,F,U):
    e=g7.field(X,F,U)
    for sg in (-1,1):
        m=np.sign(X)==sg
        if not m.any(): continue
        idx=np.where(m)[0]; w=arm_weight(X[idx],F[idx],U[idx],sg); k=w>1e-4
        if not k.any(): continue
        ii=idx[k]; b=base_arm(X[ii],F[ii],U[ii],sg)
        S=SK[sg]; Q=np.stack([X[ii],F[ii],U[ii]],-1); a=hand.frame(S["W"],S["E"],sg)[0]
        hz=1-ss(-1.5,0.5,(Q-np.asarray(S["W"]))@a)                          # no surface paths on the new hand
        b=b-heights(X[ii],F[ii],U[ii],sg)*hz
        e[ii]=e[ii]*(1-w[k])+b*w[k]
    return e
import wf_saurin_body8 as B8
B8.sdf=lambda X,F,U: field(X,F,U)
B8.BOX=(-47.0,47.0,-22.0,26.0,72.0,160.0)
if __name__=="__main__":
    import time; t=time.time(); v,f=B8.mesh(float(sys.argv[1]) if len(sys.argv)>1 else 0.2,log=lambda *a: None)
    np.savez_compressed(sys.argv[2] if len(sys.argv)>2 else "edit8_mc.npz",v=v,f=f); print("DONE",len(v),len(f),round(time.time()-t,1))
