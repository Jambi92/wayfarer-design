# Gate 7 geometry references on the frozen Gate 6 body (canonical frame x,f,u cm): claws, pads, eyes, skeleton.
import numpy as np, sys, os
sys.path.insert(0,'/tmp/claude-0/rb')
import hand, foot
os.environ.setdefault('HEAD_SCALE','1.08')
import wf_saurin_head64 as H64
AT=np.array([0.0,3.0,179.3])
ARM={-1:dict(S=(-23.5,-6.0,147.0),E=(-30.5,-4.5,117.0),W=(-36.8,6.0,97.0)),1:dict(S=(23.0,-5.0,147.0),E=(28.8,-3.5,117.0),W=(35.2,7.0,97.0))}
LEG={-1:dict(H=(-13.0,3.5,86.0),K=(-17.4,2.8,62.0),A=(-26.4,0.2,9.6),toe=6.0),1:dict(H=(13.0,3.5,86.0),K=(15.2,3.0,62.0),A=(21.6,1.6,9.6),toe=6.0)}
def _rot(v,axis,ang): return hand._rot(np.asarray(v,float),np.asarray(axis,float),ang)
def hand_claws_local():
    segs=[]; pads=[]
    for base,head,sp,lens,fx,r in hand.FING:
        p=np.array(head,float); d=_rot([1.0,0,0],[0,0,1.0],np.radians(sp)); side=np.cross(d,[0,0,1.0]); rad=[r,r*0.86,r*0.74,r*0.62]
        for k,(L,f) in enumerate(zip(lens,fx)):
            d=_rot(d,side,-np.radians(f)); q=p+d*L
            pads.append(((p+q)/2+np.array([0,0,rad[k+1]*0.6]),rad[k+1]*0.9))       # digital pad on the palmar (+c) side of each phalanx
            p=q
        dc=_rot(d,side,-np.radians(22)); c1=p+dc*1.35; c2=c1+_rot(dc,side,-np.radians(30))*1.15
        segs+=[(p+dc*0.25,c1,rad[-1]*0.95,rad[-1]*0.55),(c1,c2,rad[-1]*0.55,0.05)]
    nrm=lambda v: np.asarray(v,float)/np.linalg.norm(v)
    h=np.array([4.8,4.3,1.8]); j1=h+3.4*nrm((0.82,-0.32,0.30)); j2=j1+2.6*nrm((0.72,-0.58,0.20))
    c1=j2+1.2*nrm((0.55,-0.62,0.42)); c2=c1+1.0*nrm((0.25,-0.55,0.80)); segs+=[(j2+0.2*nrm(c1-j2),c1,0.88,0.52),(c1,c2,0.52,0.05)]
    pads+=[((j1+j2)/2+np.array([0,0,0.7]),1.0)]
    pads+=[(np.array([4.4,2.5,1.9]),1.6),(np.array([5.6,-2.6,1.6]),1.5),(np.array([7.4,-0.2,1.3]),1.8)]   # thenar, hypothenar, distal palm pads
    return segs,pads
def to_world_hand(P,sg):
    S=ARM[sg]; a,b,c=hand.frame(S['W'],S['E'],sg); return np.asarray(S['W'])+P[...,0:1]*a+P[...,1:2]*b+P[...,2:3]*c
def foot_claws_local():
    segs=[]; pads=[]
    for bl,bs,ang,lens,r0,r1 in foot.DIG:
        a=np.radians(ang); d=np.array([np.sin(a),np.cos(a),0.0]); p=np.array([bl,bs,1.75]); n=len(lens); rad=np.linspace(r0,r1,n+1)
        for k,L in enumerate(lens):
            q=p+d*L+np.array([0,0,-0.10 if k<n-1 else -0.45]); pads.append(((p+q)/2+np.array([0,0,-rad[k+1]*0.8]),rad[k+1]*0.9)); p=q
        c1=p+d*1.45+np.array([0,0,-0.30]); c2=c1+d*1.35+np.array([0,0,-0.85])
        segs+=[(p+d*0.3,c1,rad[-1]*0.92,rad[-1]*0.58),(c1,c2,rad[-1]*0.58,0.06)]
    pads+=[(np.array([0.0,-2.6,0.6]),3.0),(np.array([0.0,12.6,0.4]),2.6),(np.array([2.6,6.0,0.4]),1.8)]   # heel, metatarsal-head band, lateral midfoot
    return segs,pads
def to_world_foot(P,sg):
    S=LEG[sg]; a=np.radians(S['toe'])*sg; ca,sa=np.cos(a),np.sin(a)
    l=P[...,0]*1.14*sg; s=P[...,1]*1.04; z=P[...,2]*1.10
    dx=l*ca+s*sa; df=-l*sa+s*ca
    return np.stack([S['A'][0]+dx,S['A'][1]+df,z],-1)
def world_claws_pads():
    segs=[]; pads=[]
    for sg in (-1,1):
        s,p=hand_claws_local(); segs+=[(to_world_hand(a,sg),to_world_hand(b,sg),ra,rb,'hand') for a,b,ra,rb in s]; pads+=[(to_world_hand(c,sg),r,'hand') for c,r in p]
        s,p=foot_claws_local(); segs+=[(to_world_foot(a,sg),to_world_foot(b,sg),ra*1.08,rb*1.08,'foot') for a,b,ra,rb in s]; pads+=[(to_world_foot(c,sg),r*1.08,'foot') for c,r in p]
    return segs,pads
def eyes_world():
    (e1,e2),er,yaw=H64.eye_centers(); return [np.array(e1)+AT,np.array(e2)+AT],er,yaw
def seg_dist(P,a,b):
    v=b-a; t=np.clip(((P-a)@v)/(v@v),0,1); return np.linalg.norm(P-(a+np.outer(t,v)),axis=1),t
