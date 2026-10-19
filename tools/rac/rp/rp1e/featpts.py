# featpts.py : exact crease/arm feature points on source slices
import numpy as np
from earsl import slice_loops
def curve_near(axis,val,p0,R=8):
    best=None
    for P,c in slice_loops(axis,val):
        d=np.linalg.norm(P-p0,axis=1).min()
        if best is None or d<best[0]: best=(d,P)
    return best[1]
def arc_from(P,i,direction,s):
    n=len(P); L=0; k=i
    while True:
        k2=(k+direction)%n; seg=np.linalg.norm(P[k2]-P[k])
        if L+seg>=s: al=(s-L)/max(seg,1e-12); return P[k]+(P[k2]-P[k])*al
        L+=seg; k=k2
def tip_and_walls(axis,val,tip_guess,s=0.3,win=1.5):
    """find the tip as the curve point near tip_guess that is a local extreme, and the two wall points at arc s"""
    P=curve_near(axis,val,tip_guess); d=np.linalg.norm(P-tip_guess,axis=1); cand=np.where(d<win)[0]
    # tip = point maximising distance from the mouth direction: use farthest from the curve centroid of the local window
    loc=P[cand]; c=P[np.where(d<4*win)[0]].mean(0)
    it=cand[int(np.argmax(np.linalg.norm(loc-c,axis=1)))]
    return P[it],arc_from(P,it,1,s),arc_from(P,it,-1,s),P
if __name__=='__main__':
    import sys
    print(tip_and_walls(1,-48.1,np.array([-2.4,-48.1,100.1]))[:3])
