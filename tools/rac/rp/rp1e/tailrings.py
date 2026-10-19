# tailrings.py : tail-root junction ring J (crease tips + bottom + top) and lips (tail side / body side), from z-slices
import numpy as np, json
from earsl import slice_loops
from scipy.spatial import cKDTree
S=np.load('/home/claude/stc/rp1/weld.npz')['V']; kd=cKDTree(S)
def curve_near(z,p):
    best=None
    for P,c in slice_loops(2,z):
        d=np.linalg.norm(P[:,:2]-p[:2],axis=1).min()
        if best is None or d<best[0]: best=(d,P)
    return best[1]
def arc_pt(P,i,dirn,s):
    n=len(P); L=0; k=i
    while True:
        k2=(k+dirn)%n; seg=np.linalg.norm(P[k2]-P[k])
        if L+seg>=s: al=(s-L)/max(seg,1e-12); return P[k]+(P[k2]-P[k])*al
        L+=seg; k=k2
def crease(z,guess,s=1.2):
    P=curve_near(z,guess); d=np.linalg.norm(P[:,:2]-guess[:2],axis=1); i=int(np.argmin(d))
    # refine: tip = local extreme of -y (most negative y) within 0.8 of guess
    c=np.where(d<0.8)[0]; i=c[int(np.argmin(P[c,1]))]
    b1=arc_pt(P,i,1,s); b2=arc_pt(P,i,-1,s)
    # tail side = larger y (toward the tail)
    tl,bd=(b1,b2) if b1[1]>b2[1] else (b2,b1)
    return P[i],tl,bd
R=[(105.0,(0.3,-25.5)),(106,(-1.2,-24.2)),(108,(-1.8,-23.5)),(110,(-2.0,-23.4)),(112,(-1.8,-23.6)),(113,(-1.2,-23.8)),(114,(0.0,-24.2)),(115,(0.7,-24.7)),(116,(1.2,-25.5))]
L=[(116,(4.0,-26.0)),(115,(4.7,-25.3)),(114,(5.3,-24.8)),(113,(5.8,-24.3)),(112,(6.3,-24.0)),(110,(6.5,-23.8)),(108,(6.0,-24.0)),(106,(5.0,-24.8)),(105,(3.7,-26.0))]
J=[];JA=[];JT=[]
for z,g in R:
    t,tl,bd=crease(z,np.array(g)); J.append(t); JA.append(tl); JT.append(bd)
# top
p=kd.query([2.5,-27.3,117.1])[1]; t=S[p]; J.append(t); JA.append(S[kd.query(t+[0,1.4,-0.6])[1]]); JT.append(S[kd.query(t+[0,-0.6,1.3])[1]])
for z,g in L:
    t,tl,bd=crease(z,np.array(g)); J.append(t); JA.append(tl); JT.append(bd)
# bottom (tail underside meets the cleft top), from L to R
for x,y in ((3.0,-27.2),(2.0,-27.6),(1.0,-27.1)):
    t=S[kd.query([x,y,104.78])[1]]; J.append(t); JA.append(S[kd.query(t+[0,1.4,-0.3])[1]]); JT.append(S[kd.query(t+[0,-1.6,-0.6])[1]])
J=np.array(J); JA=np.array(JA); JT=np.array(JT)
np.savez('tailJ.npz',J=J,JA=JA,JT=JT); print('J',len(J))
for a,b,c in zip(J,JA,JT): print(a.round(1),b.round(1),c.round(1))
