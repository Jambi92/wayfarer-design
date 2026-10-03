# Gate 6 regional integration layers (on top of the Gate 5 field chain with the TS6.3 skull).
import numpy as np, os
from scipy.ndimage import spline_filter, map_coordinates, gaussian_filter1d
from scipy.interpolate import CubicSpline
from scipy.spatial import cKDTree
from g1 import ss, smin, smax
import hand
GR={}
def grid(name):
    if name not in GR:
        z=np.load("blur6_%s.npz"%name); GR[name]=(z["a"],z["b"],z["c"],spline_filter(z["d"].astype(np.float64),order=3))
    return GR[name]
def LP(name,X,F,U):
    a,b,c,co=grid(name); h=a[1]-a[0]
    return map_coordinates(co,np.stack([(X-a[0])/h,(F-b[0])/h,(U-c[0])/h]),order=3,prefilter=False,mode="nearest")
def ell_w(X,F,U,c,r,fade):
    q=np.sqrt(((X-c[0])/r[0])**2+((F-c[1])/r[1])**2+((U-c[2])/r[2])**2); return 1-ss(1-fade,1,q)
HANDS={-1:((-36.8,6.0,97.0),(-30.5,-4.5,117.0)),1:((35.2,7.0,97.0),(28.8,-3.5,117.0))}
def away_from_hands(X,F,U):
    w=np.ones(len(X))
    for sg,(W,E) in HANDS.items():
        m=(np.sign(X)==sg)&(np.abs(X)>17)&(U<112)&(U>66)
        if m.any(): w[m]=ss(1.0,3.0,hand.hand_world(X[m],F[m],U[m],W,E,sg))
    return w
class SPath:
    """surface path: control points in world cm, projected onto base(X,F,U); normal offset with width/height profiles"""
    def __init__(s_,base,pts,w,h,seed,n=240,mod=0.14,fade=(0.18,0.25),edge=0.35):
        P=np.array(pts,float); t=np.linspace(0,1,len(P)); tt=np.linspace(0,1,n); Q=s_.proj(base,CubicSpline(t,P)(tt))
        for _ in range(2):
            L=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]); u=np.linspace(0,L[-1],n)
            Q=np.stack([np.interp(u,L,Q[:,j]) for j in range(3)],1); Q=gaussian_filter1d(Q,4.0,axis=0,mode="nearest"); Q=s_.proj(base,Q,3)
        ph=np.random.default_rng(seed).uniform(0,6.3,2)
        s_.w=np.interp(tt,t,w)*(1+mod*np.sin(2*np.pi*1.3*tt+ph[0])); hh=np.interp(tt,t,h)*(1+mod*np.sin(2*np.pi*2.1*tt+ph[1]))
        s_.h=hh*ss(0,fade[0],tt)*(1-ss(1-fade[1],1,tt)); s_.T=cKDTree(Q); s_.edge=edge; s_.Q=Q
    @staticmethod
    def proj(base,P,it=6):
        P=P.copy(); h=0.05
        for _ in range(it):
            f0=base(*P.T); g=np.stack([(base(*(P+np.array(d)*h).T)-f0)/h for d in ((1,0,0),(0,1,0),(0,0,1))],1)
            n=g/(np.linalg.norm(g,axis=1,keepdims=True)+1e-9); P=P-f0[:,None]*n
        return P
    def __call__(s_,Q):
        d,i=s_.T.query(Q,distance_upper_bound=12.0); out=np.zeros(len(Q)); ok=np.isfinite(d)
        w=s_.w[i[ok]]; out[ok]=s_.h[i[ok]]*(1-ss(s_.edge*w,w,d[ok])); return out
def rss(paths,Q):
    acc=np.zeros(len(Q))
    for p in paths: v=p(Q); acc+=v*v
    return np.sqrt(acc)
