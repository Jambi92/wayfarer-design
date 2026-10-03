# Saurin hand (Gate 5): wrist -> carpal block -> metacarpal/palm framework -> knuckles -> phalanges -> claws.
# Local frame: a = distal (wrist -> fingertips), b = radial (thumb side), c = palmar. Origin at the wrist joint.
import numpy as np, sys
sys.path.insert(0,"/tmp/claude-0/rb")
from wf_saurin_body8 import smin, smax, ellipsoid, round_cone, BIG
def _rc(P,a,b,ra,rb): return round_cone(P,np.asarray(a,float),np.asarray(b,float),ra,rb)
def _rot(v,axis,ang):
    axis=axis/np.linalg.norm(axis); return v*np.cos(ang)+np.cross(axis,v)*np.sin(ang)+axis*np.dot(axis,v)*(1-np.cos(ang))
# digits II-V: metacarpal base/head (a,b,c), spread (deg, + radial), phalanx lengths, flexion at MCP/PIP/DIP (deg), radius
FING=[((3.1,1.9,0.0),(10.1,2.7,-0.25),6.0,[4.7,2.9,2.1],[8,14,10],1.20),
      ((3.2,0.6,0.0),(10.6,0.9,-0.30),1.0,[5.2,3.4,2.4],[9,16,11],1.22),
      ((3.1,-0.7,0.0),(10.1,-1.0,-0.25),-5.0,[4.8,3.1,2.2],[11,18,12],1.15),
      ((2.9,-1.9,0.0),(9.0,-2.7,-0.10),-12.0,[3.8,2.5,1.8],[14,22,14],1.04)]
def finger(P,head,spread,lens,flex,r):
    p=np.array(head,float); d=_rot(np.array([1.0,0,0]),np.array([0,0,1.0]),np.radians(spread))   # spread in the a-b plane
    side=np.cross(d,np.array([0,0,1.0])); out=np.full(P[0].shape,BIG); rad=[r,r*0.86,r*0.74,r*0.62]
    for k,(L,fx) in enumerate(zip(lens,flex)):
        d=_rot(d,side,-np.radians(fx))                                      # flex toward the palm (+c)
        q=p+d*L; out=smin(out,_rc(P,p,q,rad[k],rad[k+1]),0.35)
        out=smin(out,np.sqrt(sum((P[i]-p[i])**2 for i in range(3)))-(rad[k]+0.10),0.35)           # joint (knuckle) mass
        p=q
    dc=_rot(d,side,-np.radians(22)); c1=p+dc*1.35; c2=c1+_rot(dc,side,-np.radians(30))*1.15       # claw from the terminal phalanx
    out=smin(out,_rc(P,p,c1,rad[-1]*0.95,rad[-1]*0.55),0.2); out=smin(out,_rc(P,c1,c2,rad[-1]*0.55,0.05),0.1)
    return out
def thumb(P):
    """opposable thumb: metacarpal angled radially/palmar from the carpus; phalanges swing distally and ulnarly
    across the palm toward the finger pads (opposition)."""
    base=np.array([2.6,2.0,0.5]); h=np.array([4.8,4.3,1.8])
    out=_rc(P,base,h,1.45,1.25)
    def nrm(v): v=np.asarray(v,float); return v/np.linalg.norm(v)
    j1=h+3.4*nrm((0.82,-0.32,0.30)); j2=j1+2.6*nrm((0.72,-0.58,0.20))
    out=smin(out,_rc(P,h,j1,1.25,1.10),0.35); out=smin(out,np.sqrt(sum((P[i]-h[i])**2 for i in range(3)))-1.35,0.35)
    out=smin(out,_rc(P,j1,j2,1.10,0.92),0.35); out=smin(out,np.sqrt(sum((P[i]-j1[i])**2 for i in range(3)))-1.18,0.35)
    c1=j2+1.2*nrm((0.55,-0.62,0.42)); c2=c1+1.0*nrm((0.25,-0.55,0.80))
    out=smin(out,_rc(P,j2,c1,0.88,0.52),0.2); out=smin(out,_rc(P,c1,c2,0.52,0.05),0.1)
    return out
def hand_local(a,b,c):
    P=(a,b,c)
    e=ellipsoid(P,np.array([1.9,0.0,0.1]),(2.5,3.1,1.85))                       # carpal block
    for base,head,_,_,_,r in FING: e=smin(e,_rc(P,base,head,r*1.15,r*1.02),0.9)  # metacarpal framework
    e=smin(e,ellipsoid(P,np.array([6.6,-0.2,0.45]),(4.0,3.2,1.15)),1.1)         # palm (palmar mass between the metacarpals)
    e=smin(e,ellipsoid(P,np.array([5.6,-2.6,0.75]),(3.6,1.25,1.15)),0.9)        # hypothenar ridge (ulnar grip edge)
    e=smin(e,ellipsoid(P,np.array([4.4,2.5,0.95]),(2.8,1.5,1.45)),1.0)          # thenar mass (thumb opposition)
    for base,head,sp,lens,fx,r in FING: e=smin(e,finger(P,head,sp,lens,fx,r),0.55)
    e=smin(e,thumb(P),0.7)
    return e
def frame(W,E,sg):
    """hand frame from wrist W and elbow E: a = continuation of the forearm toward vertical, c = medial (palm faces the body), b = anterior"""
    a=np.asarray(W,float)-np.asarray(E,float); a/=np.linalg.norm(a); a=0.55*a+0.45*np.array([0,0,-1.0]); a/=np.linalg.norm(a)
    c=np.array([-sg,0.0,0.0]); c=c-a*np.dot(c,a); c/=np.linalg.norm(c); b=np.cross(c,a)
    if b[1]<0: b=-b
    return a,b,c
def hand_world(X,F,U,W,E,sg):
    a,b,c=frame(W,E,sg); Q=np.stack([X,F,U],-1)-np.asarray(W,float)
    return hand_local(Q@a,Q@b,Q@c)
if __name__=="__main__":
    import wf_saurin_body8 as B8
    W=(0.0,0.0,20.0); E=(-1.0,-1.0,40.0)
    B8.sdf=lambda X,F,U: hand_world(X,F,U,W,E,1.0); B8.BOX=(-8.0,8.0,-8.0,12.0,0.0,24.0)
    v,f=B8.mesh(0.1,log=lambda *a:None); np.savez("hand_test.npz",P=v,f=f,R=np.zeros(len(v),int)); print(len(v),v.min(0).round(1),v.max(0).round(1))
