# find the largest ventral fullness that keeps thoracic depth/width <= 1.00 on a given body (the creator CONSTRAIN)
import numpy as np, pickle, sys, json; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); sys.path.insert(0,'/tmp/claude-0/rodin/v5')
import vary, metrics, tissue, fsets3
from sets import NARROW
L=pickle.load(open('/tmp/claude-0/rodin/v1/Lbase.pkl','rb')); z=np.load(vary.REF_BASE); V=z['V'].astype(float); F=z['F'].astype(np.int64); L._u0=V[:,2]; L._f0=V[:,1]
sys.path.insert(0,'/tmp/claude-0/rb'); import wf_saurin_head63 as H; eye=(H.eye_centers()[0],H.eye_centers()[1])
x0,f0,u0=V.T; tor=L.torso>0.6
def dw(p):
    P=tissue.fwarp(V,L,dict(p),eye=eye); x,f,u=P.T
    w=np.ptp(x[tor&(u0>=118)&(u0<=140)]); m=tor&(np.abs(u0-132)<2)&(np.abs(x0)<4); return np.ptp(f[m])/w
res={}
for nm,base in (('Narrow',fsets3.R(NARROW)),('Narrow + fat high',fsets3.R(NARROW,{'fat':1.0}))):
    lo,hi=0.0,3.0
    if dw(dict(base,vfull=hi))<=1.0: res[nm]=3.0; continue
    for _ in range(7):
        mid=(lo+hi)/2
        if dw(dict(base,vfull=mid))<=1.0: lo=mid
        else: hi=mid
    res[nm]=round(lo,2); print(nm,lo,flush=True)
json.dump(res,open('/tmp/claude-0/rodin/v5/clamp.json','w'))
