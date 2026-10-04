# TS6.5: Cranial Keratin Display System test variants on the frozen TS6.3 skull (head-local, unscaled; head64 applies +8 %).
# Display bases are anchored ON the skull surface (bisection on the skull field) so structures grow from attachment regions
# without reshaping the skull: skull unchanged, display = smin(skull, keratin, small k) only where the display exists.
import os, numpy as np
import wf_saurin_head63 as H
from wf_saurin_head61 import horn, blade, capsule, smin
P=H.P; EYE=H.EYE
RINGS=[(-60.0,0,-5,0.1,0.1),(-59.0,0,-5,0.1,0.1)]
def surf_u(x,f,lo=-2.0,hi=14.0):
    x=np.atleast_1d(np.asarray(x,float)); f=np.atleast_1d(np.asarray(f,float)); a=np.full(x.shape,lo); b=np.full(x.shape,hi)
    for _ in range(40):
        m=(a+b)/2; inside=H.head_sdf(x,f,m,RINGS,-59.0)<0; a=np.where(inside,m,a); b=np.where(inside,b,m)
    return (a+b)/2
def S(x,f,sink=0.25): return (x,f,float(surf_u(x,f)[0])-sink)          # anchor point on the roof surface, slightly sunk (broad footprint)
def _sym(fn): return lambda X,F,U: fn(np.abs(X),F,U)
def ridge(pts,r0,r1):                                                 # low keratin ridge lying along the surface
    return lambda X,F,U: horn(X,F,U,pts[0],pts[1],pts[2],r0,r1,n=16)
def build(name):
    if name=="minimal_ridges":       # nearly flat paired parietal ridges along the temporal line
        p=[S(3.9,2.5,0.05),S(4.3,-3.5,0.05),S(3.6,-9.5,0.05)]
        return _sym(ridge(p,0.42,0.22))
    if name=="low_hornlets":         # postorbital brow hornlets + squamosal corner hornlets + low posterior parietal hornlets
        a=S(4.6,3.6); b=S(4.4,-3.2); c=S(2.6,-9.4)
        h1=lambda X,F,U: horn(X,F,U,a,(a[0]+0.5,a[1]-0.6,a[2]+0.9),(a[0]+0.8,a[1]-1.2,a[2]+1.5),0.62,0.10)
        h2=lambda X,F,U: horn(X,F,U,b,(b[0]+0.5,b[1]-0.9,b[2]+0.9),(b[0]+0.8,b[1]-1.8,b[2]+1.5),0.72,0.10)
        h3=lambda X,F,U: horn(X,F,U,c,(c[0]+0.2,c[1]-1.0,c[2]+0.8),(c[0]+0.4,c[1]-2.0,c[2]+1.2),0.70,0.10)
        return _sym(lambda X,F,U: smin(smin(h1(X,F,U),h2(X,F,U),0.2),h3(X,F,U),0.2))
    if name=="swept_paired":         # swept-back paired horns from the squamosal/temporal corners
        b=S(4.1,-4.6,0.45)
        if H.BROW_INT >= 4:   # convergence: slimmer base that starts further forward and lies along the cranial surface (grown, not socketed)
            r=S(3.95,-2.9,0.62); tip=(b[0]+1.0,b[1]-12.5,b[2]+0.2)
            return _sym(lambda X,F,U: horn(X,F,U,r,(r[0]+1.05,r[1]-6.2,r[2]+1.15),tip,0.98,0.14))
        return _sym(lambda X,F,U: horn(X,F,U,b,(b[0]+1.2,b[1]-6.5,b[2]+1.4),(b[0]+1.0,b[1]-12.5,b[2]+0.2),1.30,0.14))
    if name=="crest":                # dorsal-midline keratin crest + very low paired side ridges
        roof=lambda F: surf_u(np.zeros_like(F),F)
        side=_sym(ridge([S(3.3,0.5,0.05),S(3.7,-5.0,0.05),S(3.2,-9.5,0.05)],0.36,0.18))
        return lambda X,F,U: smin(blade(X,F,U,-11.5,2.0,roof,CREST_H,0.50,peak=0.38),side(X,F,U),0.3)
    if name=="mixed_asym":           # paired up-curving posterior horns (left ~15 % shorter) + unequal brow hornlets
        bR=S(3.6,-7.4,0.45); bL=S(-3.6,-7.4,0.45); a1=S(4.6,3.6); a2=S(4.7,1.2); a3=S(-4.6,3.6)
        hR=lambda X,F,U: horn(X,F,U,bR,(bR[0]+1.1,bR[1]-3.6,bR[2]+2.0),(bR[0]+1.3,bR[1]-7.2,bR[2]+3.6),1.10,0.12)
        hL=lambda X,F,U: horn(X,F,U,bL,(bL[0]-1.0,bL[1]-3.1,bL[2]+1.7),(bL[0]-1.2,bL[1]-6.1,bL[2]+3.0),1.10,0.13)
        b1=lambda X,F,U: horn(X,F,U,a1,(a1[0]+0.4,a1[1]-0.5,a1[2]+0.8),(a1[0]+0.7,a1[1]-1.0,a1[2]+1.3),0.55,0.09)
        b2=lambda X,F,U: horn(X,F,U,a2,(a2[0]+0.4,a2[1]-0.5,a2[2]+0.6),(a2[0]+0.6,a2[1]-1.0,a2[2]+1.0),0.45,0.08)
        b3=lambda X,F,U: horn(X,F,U,a3,(a3[0]-0.4,a3[1]-0.5,a3[2]+0.8),(a3[0]-0.7,a3[1]-1.0,a3[2]+1.3),0.55,0.09)
        return lambda X,F,U: smin(smin(smin(smin(hR(X,F,U),hL(X,F,U),0.2),b1(X,F,U),0.2),b2(X,F,U),0.2),b3(X,F,U),0.2)
    return None
DISPLAY=os.environ.get("DISPLAY_VARIANT","")
CREST_H=float(os.environ.get("CREST_H","2.40"))   # Gate 7 closure: crest constrained to ~<=2.5 cm above the roof (was 3.2 -> 3.27 cm)
_D=build(DISPLAY) if DISPLAY else None
def head_sdf(X,F,U,neck_rings,cut_u):
    d=H.head_sdf(X,F,U,neck_rings,cut_u)
    if _D is None: return d
    k=(np.abs(X)<9)&(F>-22)&(F<9)&(U>2)
    if k.any():
        d=d.copy(); d[k]=smin(d[k],_D(X[k],F[k],U[k]),0.5)          # keratin grows out of the skull surface (blended footprint)
    return d
def eye_centers(): return H.eye_centers()
