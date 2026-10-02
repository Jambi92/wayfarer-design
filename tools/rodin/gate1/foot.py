# Saurin plantigrade foot (Gate 4): rearfoot/heel -> structured midfoot -> metatarsal fan -> long articulated digits -> claws.
# Local frame: s forward along the foot axis, l lateral (+ = outer side), z up; origin = ankle centre projected to ground.
import numpy as np, sys
sys.path.insert(0,"/tmp/claude-0/rb")
from wf_saurin_body8 import smin, smax, ellipsoid, round_cone, BIG
def _rc(P,a,b,ra,rb): return round_cone(P,np.array(a,float),np.array(b,float),ra,rb)
DIG=[ # base l, base s, angle(deg, + lateral), phalanx lengths, radius at base, tip radius
    (-5.0,12.2,-15.0,[2.6,2.3],1.85,1.30),
    (-2.5,13.6,-6.0,[3.0,2.6,2.2],1.62,1.08),
    (0.0,14.2,0.0,[3.1,2.7,2.3,1.9],1.62,1.02),
    (2.4,13.4,7.0,[2.9,2.5,2.1,1.7],1.52,0.98),
    (4.6,12.0,17.0,[2.6,2.1,1.7],1.40,0.92)]
MET=[((-2.6,6.6,4.2),(-5.0,12.2,1.65),1.85,1.55),((-1.3,6.8,4.4),(-2.5,13.6,1.55),1.55,1.30),((0.0,6.9,4.5),(0.0,14.2,1.55),1.55,1.30),
     ((1.3,6.8,4.3),(2.4,13.4,1.50),1.50,1.26),((2.5,6.6,4.0),(4.6,12.0,1.45),1.45,1.20)]
def digit(P,base,ang,lens,r0,r1):
    a=np.radians(ang); d=np.array([np.sin(a),np.cos(a),0.0]); out=np.full(P[0].shape,BIG)
    p=np.array([base[0],base[1],1.75]); n=len(lens); rad=np.linspace(r0,r1,n+1)
    for k,L in enumerate(lens):
        zdrop=-0.10 if k<n-1 else -0.45                              # resting arc: joints slightly raised, last phalanx angled down
        q=p+d*L+np.array([0,0,zdrop])
        out=smin(out,_rc(P,p,q,rad[k],rad[k+1]*1.04),0.35)
        if k<n-1: out=smin(out,np.sqrt((P[0]-q[0])**2+(P[1]-q[1])**2+(P[2]-q[2]-0.08)**2)-(rad[k+1]+0.07),0.35)   # joint (knuckle) swelling
        p=q
    # claw grows from the terminal phalanx: keratin sheath continuous with it, curving down to the ground
    c1=p+d*1.45+np.array([0,0,-0.30]); c2=c1+d*1.35+np.array([0,0,-0.85])
    out=smin(out,_rc(P,p,c1,rad[-1]*0.92,rad[-1]*0.58),0.25)
    out=smin(out,_rc(P,c1,c2,rad[-1]*0.58,0.06),0.12)
    return out
def foot_local(l,s,z):
    P=(l,s,z)
    e=_rc(P,(0.0,-1.0,8.6),(0.0,-3.2,2.7),3.5,2.9)                            # calcaneal column: ankle -> heel pad (stance contact)
    e=smin(e,ellipsoid(P,np.array([0.0,-2.6,1.6]),(3.1,3.3,1.6)),1.4)          # heel contact pad
    e=smin(e,_rc(P,(0.0,-0.4,9.6),(0.1,3.6,5.0),3.9,3.5),2.4)                 # talar / ankle block
    e=smin(e,ellipsoid(P,np.array([0.2,5.2,3.7]),(4.4,4.6,2.8)),2.0)           # tarsal block (structured midfoot)
    for a,b,ra,rb in MET: e=smin(e,_rc(P,a,b,ra,rb),1.3)                       # metatarsal fan
    e=smin(e,ellipsoid(P,np.array([0.0,12.6,1.05]),(6.3,2.6,1.05)),1.2)        # forefoot contact pad (metatarsal heads)
    e=smin(e,ellipsoid(P,np.array([-1.6,8.5,1.2]),(2.6,3.6,1.2))+0.45,1.6)     # medial arch: held off the ground (structure, not slab)
    for bl,bs,ang,lens,r0,r1 in DIG: e=smin(e,digit(P,(bl,bs),ang,lens,r0,r1),0.75)
    e=smax(e,-z,0.5)                                                           # flat plantigrade contact plane
    return e
def foot_world(X,F,U,ankle,toe_out_deg,side):
    """ankle=(x,f) ground position below the ankle joint; side=+1 right (x>0), -1 left; lateral = outward."""
    a=np.radians(toe_out_deg)*side; ca,sa=np.cos(a),np.sin(a)
    dx=X-ankle[0]; df=F-ankle[1]
    s=dx*sa+df*ca; l=(dx*ca-df*sa)*side
    return foot_local(l/1.14,s/1.04,U/1.10)*1.04                     # broader, slightly larger build (length ~0.18H)
if __name__=="__main__":
    import wf_saurin_body8 as B8
    B8.sdf=lambda X,F,U: foot_world(X,F,U,(0.0,0.0),5.0,1.0); B8.BOX=(-10.0,10.0,-10.0,30.0,-0.5,14.0)
    v,f=B8.mesh(0.12,log=lambda *a:None); np.savez("foot_test.npz",P=v,f=f,R=np.zeros(len(v),int)); print(len(v), v.min(0).round(1), v.max(0).round(1))
