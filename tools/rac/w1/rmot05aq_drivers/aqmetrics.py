import numpy as np
from scipy.spatial import cKDTree
V0=np.load('/home/claude/ao/ao2/ao2_VF.npz')['V']; z0=V0[:,2].min(); Z=(V0[:,2]-z0)*100
W=np.load('/home/claude/ao/vgroups.npz'); names=list(W['names']); Wt=W['W']; lab=Wt.argmax(1)
R=np.load('/home/claude/aj/regions_05AI.npz'); P=np.load('/home/claude/ag/protected_05AF.npz'); tr=lab==names.index('trunk')
def projection(V):
    out={}
    for s,sg in (('L',1),('R',-1)):
        m=(sg*V0[:,0]>0.06)&(Z>85)&(Z<115)&~P['all']&(V0[:,1]>-0.40)
        out[s]=round(float(V[m,1].max()*1000),2)
    return out
def profile_depth(V):
    # mean posterior depth (Y, mm) of the buttock band 92-108 cm lateral to the tail, per side: average of the 200 most posterior vertices
    out={}
    for s,sg in (('L',1),('R',-1)):
        m=np.flatnonzero((sg*V0[:,0]>0.06)&(Z>92)&(Z<108)&~P['all'])
        top=m[np.argsort(-V0[m,1])[:200]]; out[s]=round(float(V[top,1].mean()*1000),2)
    return out
def pelvis_width(V):
    m=tr&(Z>98)&(Z<112)&~P['tail']; return round(float(np.ptp(V[m,0])*1000),2)
# skeletal hip landmark: centroid of the thigh/trunk weight-blend ring (0.25 < w_thigh < 0.75), i.e. the rig's hip joint blend
HB={}; HS={}
for s in 'LR':
    w=Wt[:,names.index(f'thigh_{s}')]; HB[s]=np.flatnonzero((w>0.25)&(w<0.75))
    A=lab==names.index(f'thigh_{s}'); d,_=cKDTree(V0[tr]).query(V0[A]); HS[s]=np.flatnonzero(A)[d<0.01]
def hip_skeletal(V): return {s:round(float(np.linalg.norm(V[i].mean(0)-V0[i].mean(0))*1000),4) for s,i in HB.items()}
def hip_seam_proxy(V): return {s:round(float(np.linalg.norm(V[i].mean(0)-V0[i].mean(0))*1000),4) for s,i in HS.items()}
def thigh_radius(V, zlo=70):
    out={}
    for s in 'LR':
        m=(lab==names.index(f'thigh_{s}'))&(Z>zlo); C0=V0[m]; mu=C0.mean(0); _,_,vt=np.linalg.svd(C0-mu,full_matrices=False); ax=vt[0]
        rr=lambda C: np.linalg.norm((C-mu)-np.outer((C-mu)@ax,ax),axis=1).mean(); out[s]=round(float((rr(V[m])/rr(C0)-1)*100),3)
    return out
# --- 05AQ §5 skeletal hip landmark ---
# The blend has no armature. Hip-joint core = the rig's thigh/trunk weight-blend ring (0.25 < w_thigh < 0.75) minus the
# authorised AC3 soft-tissue region (final mask < 1). Those vertices are hard-masked, so the landmark (their centroid) tracks the
# skeletal hip blend and is insensitive to valid glute-fold soft-tissue motion. Diagnostic only: the angle-binned centroid of the
# full ring (includes the moving glute fold) and the retired surface-seam proxy.
_MQ=np.load('/home/claude/aq/mask_v4.npy')
HC={s:i[_MQ[i]>=1.0] for s,i in HB.items()}
def hip_core(V): return {s:round(float(np.linalg.norm(V[i].mean(0)-V0[i].mean(0))*1000),4) for s,i in HC.items()}
def hip_ring_binned(V):
    out={}
    for s,i in HB.items():
        c=V0[i].mean(0); X=V0[i]-c; _,_,vt=np.linalg.svd(X,full_matrices=False); a=np.arctan2(X@vt[1],X@vt[0]); b=((a+np.pi)/(2*np.pi)*36).astype(int)%36
        cb=lambda Y: np.array([Y[b==k].mean(0) for k in range(36) if (b==k).any()]).mean(0); out[s]=round(float(np.linalg.norm(cb(V[i])-cb(V0[i]))*1000),4)
    return out
