# RM-OT-05AT masks. H = hard complement of the 05AR posterior field (free tail excluded from the distance; the root is handled by the
# 05AR core ramp). d_H = 3-D distance to H.
# Mask A (belly authoring): sculptable only deep inside the field: M_A = 1 - smoothstep((d_H - DB) / WA); plus the 05AR root-core ramp
#   (1.0 to 22 mm, smoothstep over 60 mm), duplicate seams pinned 1.0, 50 mm Lipschitz limit.
# Mask B (boundary blend): the 05AS wide-feather mask (80 mm lateral/thigh, 50 mm elsewhere, C1) with the Stage-A belly interior
#   protected: M_B = max(M_AS, smoothstep((d_H - DI0) / WI)), so only the band around Mask A's edge and the outer feather can move.
import sys; sys.path[:0]=['/home/claude/ar','/home/claude/as','/home/claude/aq']; import numpy as np, aqmetrics as Q, armask as AR
from scipy.spatial import cKDTree
V=Q.V0; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; St=np.load('/home/claude/ar/sets.npz'); S=St['S']; P=np.load('/home/claude/ag/protected_05AF.npz'); dup=np.load('/home/claude/ar/dup.npy')
H=(~S)&(~P['tail']); dH,_=cKDTree(V[H]).query(V); dH*=1000
rootcore=St['core']&~P['tail']; dc,_=cKDTree(V[rootcore]).query(V); dc*=1000
ss=lambda t: (lambda u: 3*u**2-2*u**3)(np.clip(t,0,1))
def mask_a(DB=40.0,WA=60.0,D0=22.0,W=60.0):
    M=1-ss((dH-DB)/WA); M=np.maximum(M,1-ss((dc-D0)/W)); M[~S]=1; M[dup]=1; M=AR.lipschitz(M,V,F,0.05); M[~S]=1; M[dup]=1; M[St['core']]=1; return M
def mask_b(DI0=110.0,WI=60.0):
    MB=np.load('/home/claude/as/mask_as2.npy').copy(); MB=np.maximum(MB,ss((dH-DI0)/WI)); MB[dup]=1; MB[St['core']]=1; return MB
if __name__=='__main__':
    MA=mask_a(); MB=mask_b(); np.save('maskA0.npy',MA); np.save('maskB0.npy',MB); np.save('dH.npy',dH)
    print('dH max mm',dH.max().round(1),'A: M<1',(MA<1).sum(),'M<0.1',(MA<0.1).sum(),'| B: M<1',(MB<1).sum(),'M<0.5',(MB<0.5).sum())
    for a,b in [(0,20),(20,40),(40,60),(60,80),(80,100),(100,130),(130,170),(170,300)]:
        m=S&(dH>=a)&(dH<b); print(f'dH {a}-{b}: n {m.sum()} MA {MA[m].mean():.2f} MB {MB[m].mean():.2f}')
# v1 Mask A: keep the proven 05AR (AR1r) mask in the medial / tail-side field and only add protection measured from the LATERAL,
# FRONT-THIGH and LOWER-THIGH hard boundaries (where AR1r folded): M_A = max(M_AR1r, 1 - smoothstep((dL - DB) / WA)).
z0=V[:,2].min(); Zc=(V[:,2]-z0)*100; Xc=V[:,0]*100; thigh=np.isin(Q.lab,[Q.names.index('thigh_L'),Q.names.index('thigh_R')])
HL=H&((np.abs(Xc)>14)|thigh|(Zc<75)); dL,_=cKDTree(V[HL]).query(V); dL*=1000
def mask_a1(DB=30.0,WA=60.0):
    M=np.maximum(np.load('/home/claude/ar/mask_ar5.npy'),1-ss((dL-DB)/WA)); M[~S]=1; M[dup]=1; M=AR.lipschitz(M,V,F,0.05); M[~S]=1; M[dup]=1; M[St['core']]=1; return M
def mask_b1(DI0=90.0,WI=60.0):
    # Mask B: wide AS feather; protect the Stage-A interior measured from the lateral/lower boundaries and the medial core region
    MB=np.load('/home/claude/as/mask_as2.npy').copy(); MB=np.maximum(MB,ss((dL-DI0)/WI)); MB[dup]=1; MB[St['core']]=1; return MB
import dryrun as _D
_Avg=_D.adjacency(F,len(V))
def c1(M,it=40,extra_hard=None):
    hard=(~S)|dup|St['core']|(dc<=22.0)
    if extra_hard is not None: hard=hard|extra_hard
    for _ in range(it): M=np.where(hard,1.0,_Avg@M)
    M=AR.lipschitz(M,V,F,0.05); M[hard]=1.0; return M
ds,_=cKDTree(V[dup&S|dup&St['ring']|dup&(dc<120)]).query(V); ds*=1000
def mask_a3(DB=30.0,WA=60.0,RS=75.0):
    # A1 + C1 seam treatment: smoothstep (zero slope at the seam) from every duplicate-position seam vertex near the field, so pinned
    # seams no longer create Lipschitz cone kinks.
    M=np.maximum(np.load('/home/claude/ar/mask_ar5.npy'),1-ss((dL-DB)/WA)); M=np.maximum(M,1-ss(ds/RS)); M=np.maximum(M,1-ss((dc-22.0)/60.0))
    M[~S]=1; M[dup]=1; M=AR.lipschitz(M,V,F,0.05); M[~S]=1; M[dup]=1; M[St['core']]=1; return M
# v4 (log-mapped) Mask A. Under N Smooth events a vertex is pulled by ~1-(M)^N of the full Laplacian, so a linear ramp near 1.0 still acts
# as a hard edge (M=0.96 is ~99% smoothed after 120 events). The smoothing weight is therefore mapped through the event count:
#   w_s = smoothstep(d / Ls)  (desired fraction of full smoothing),  M_s = 1 + ln(1 - 0.95 w_s) / N
#   w_d = smoothstep((d - DB) / WA)  (deflate weight, belly only),  M = min(M_s, 1 - w_d)
# d = min(distance to the field's hard complement, distance beyond the 22 mm root-core plateau). Seams/core pinned at 1.0.
def mask_log(N=120,Ls=80.0,DB=30.0,WA=60.0):
    d=np.minimum(dH,np.maximum(dc-22.0,0)); ws=ss(d/Ls); Ms=1+np.log(1-0.95*ws)/N; wd=ss((d-DB)/WA); M=np.minimum(Ms,1-wd)
    M[~S]=1; M[dup]=1; M[St['core']]=1; return np.clip(M,0,1)
def mask_log2(N=120,Ls=80.0,DB=30.0,WA=60.0,sites=None,R=35.0):
    # mask_log with local protection: both weights are scaled by smoothstep(dist_to_site / R) around predicted kink sites
    d=np.minimum(dH,np.maximum(dc-22.0,0)); ws=ss(d/Ls); wd=ss((d-DB)/WA)
    if sites is not None and len(sites):
        dsite,_=cKDTree(np.asarray(sites)).query(V); k=ss(dsite*1000/R); ws=ws*k; wd=wd*k
    Ms=1+np.log(1-0.95*ws)/N; M=np.minimum(Ms,1-wd); M[~S]=1; M[dup]=1; M[St['core']]=1; return np.clip(M,0,1)
def mask_bl(N=10,L_out=80.0,D_in=60.0,W_in=60.0):
    # Mask B (boundary blend), log-mapped for a short N-event Smooth: blend weight rises over >= 80 mm from the hard boundary and is
    # switched off again inside the Stage-A belly (beyond ~D_in+W_in), so only the Stage-A transition band moves.
    d=np.minimum(dH,np.maximum(dc-22.0,0)); w=ss(d/L_out)*(1-ss((d-D_in)/W_in)); M=1+np.log(1-0.95*w)/N
    M[~S]=1; M[dup]=1; M[St['core']]=1; return np.clip(M,0,1)
