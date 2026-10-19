# axrings.py SIDE : construct the R/L axilla junction ring J (crease tips + apex + shoulder top) and its arm/trunk lips
import numpy as np, sys, json, os
from scipy.spatial import cKDTree
from axcrease import spike
S=np.load('/home/claude/stc/rp1/weld.npz')['V']; col=np.load(os.environ.get('SRCCOL','col_r2.npy'))
side=sys.argv[1]; sg=1 if side=='R' else -1
mx=lambda x: x if side=='R' else 4-x    # mirror helper (R design frame)
arm=5 if side=='R' else 4
xr=(-26,-12) if side=='R' else (16,30)
kd=cKDTree(S); kdA=cKDTree(S[col==arm]); SA=S[col==arm]; kdT=cKDTree(S[col==1]); ST=S[col==1]
def proj(p,which=None):
    if which=='A': d,i=kdA.query(p); return SA[i]
    if which=='T': d,i=kdT.query(p); return ST[i]
    d,i=kd.query(p); return S[i]
# front crease (tip line, z up), lips; back crease
front=[]; back=[]
from earsl import slice_loops
FST=float(os.environ.get('FSTEP','0.5'))
for z in np.arange(142.5,153.6,FST):
    f=spike(z,xr,(-48,-33),+1)
    if f and f['depth']>0.3:
        t=f['tip']; best=t
        for P,c in slice_loops(2,z):
            m=(np.linalg.norm(P[:,:2]-t[:2],axis=1)<2.0)
            if m.any() and len(P)<len(f['P']):
                i=np.argmax(np.where(m,P[:,1],-1e9))
                if P[i,1]>best[1]: best=P[i]
        front.append((best,f['lA'],f['lB']))
SMW=int(os.environ.get('TSM','1'))
if SMW>0 and len(front)>2:
    T=np.array([f[0] for f in front]); T2=T.copy()
    for i in range(len(T)):
        lo,hi=max(0,i-SMW),min(len(T),i+SMW+1); T2[i,:2]=T[lo:hi,:2].mean(0)
        if os.environ.get('TYMAX')=='1' and T[i,2]<float(os.environ.get('TYZ','153.6')): T2[i,1]=T[lo:hi,1].max()
    T2=np.array([proj(p) for p in T2]); front=[(T2[i],a,b) for i,(t,a,b) in enumerate(front)]
import os
if side=='L' and os.environ.get('LBACK','1')=='1':
    for zz,x,y in ((142.5,24.2,-30.0),(144,24.9,-28.6),(146,25.2,-27.8),(148,25.4,-27.3),(150,25.5,-27.1),(152,25.6,-27.0)):
        t=proj(np.array([x,y,zz])); back.append((t,proj(t+np.array([1.2,0.4,0])),proj(t+np.array([-1.2,-0.4,0]))))
else:
  for z in np.arange(142.5,152.1,1.0):
    b=spike(z,xr,(-34,-18),-1)
    if b and b['depth']>0.1: back.append((b['tip'],b['lA'],b['lB']))
def armside(p,q):  # which of two lips is on the arm side: arm = more lateral (smaller x for R)
    return (p,q) if sg*(p[0]-q[0])<0 else (q,p)
J=[];JA=[];JT=[]
# apex segment (from back-bottom tip to front-bottom tip), at z ~141.4
apex=[np.array([mx(-18.6),-31.0,141.6]),np.array([mx(-19.2),-33.0,141.3]),np.array([mx(-19.8),-35.0,141.6])]
for p in apex:
    q=proj(p); J.append(q)
    JA.append(proj(q+np.array([-sg*1.2,0,-1.4]),'A')); JT.append(proj(q+np.array([sg*1.2,0,-1.4]),'T'))
for t,a,b in front:
    J.append(t); la,lb=armside(a,b); JA.append(la); JT.append(lb)
# shoulder top (front-top -> back-top), designed points projected to the surface
top=[(-20.5,-42.5,155),(-22.5,-41.5,158),(-24.5,-38.5,160),(-25.0,-34.0,161),(-24.5,-29.5,160),(-22.5,-26.0,157.5),(-21.0,-24.5,155)]
for p in top:
    q=proj(np.array([mx(p[0]),p[1],p[2]])); J.append(q)
    # lips: arm side = outward/down (lateral), trunk side = medial/up
    JA.append(proj(q+np.array([-sg*1.5,0,-0.8]))); JT.append(proj(q+np.array([sg*1.5,0,0.8])))
for t,a,b in back[::-1]:
    J.append(t); la,lb=armside(a,b); JA.append(la); JT.append(lb)
J=np.array(J); JA=np.array(JA); JT=np.array(JT)
DMIN=float(os.environ.get('DMIN','1.2'))
for k in range(len(J)):
    for arr,wh in ((JA,'A'),(JT,'T')):
        d=arr[k]-J[k]; n=np.linalg.norm(d)
        if n<DMIN:
            if n<1e-3:
                t=J[(k+1)%len(J)]-J[k-1]; d=np.cross(t,[0,0,1.0]) if wh=='A' else -np.cross(t,[0,0,1.0]); n=np.linalg.norm(d)
            arr[k]=proj(J[k]+d/n*DMIN,wh)
np.savez(os.environ.get('JOUT','axJ2_%s.npz'%side),J=J,JA=JA,JT=JT)
print(side,'J pts',len(J),'front',len(front),'back',len(back))
