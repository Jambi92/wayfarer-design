import numpy as np
from scipy.spatial import cKDTree
V0=np.load('/home/claude/ao/ao2/ao2_VF.npz')['V']; z0=V0[:,2].min(); Z=(V0[:,2]-z0)*100
W=np.load('/home/claude/ao/vgroups.npz'); names=list(W['names']); lab=W['W'].argmax(1)
R=np.load('/home/claude/aj/regions_05AI.npz'); P=np.load('/home/claude/ag/protected_05AF.npz')
tr=lab==names.index('trunk')
def projection(V):
    out={}
    for s,sg in (('L',1),('R',-1)):
        m=(sg*V0[:,0]>0.06)&(Z>88)&(Z<112)&~P['all']&(V0[:,1]>-0.40)
        out[s]=round(float(V[m,1].max()*1000),2)   # posterior-most Y (mm) of each buttock, lateral to the tail root
    return out
def pelvis_width(V):
    m=tr&(Z>98)&(Z<112)&~P['tail']; return round(float(np.ptp(V[m,0])*1000),2)
JI={}
for s in 'LR':
    A=lab==names.index(f'thigh_{s}'); d,_=cKDTree(V0[tr]).query(V0[A]); JI[s]=np.flatnonzero(A)[d<0.01]
def hip(V): return {s:round(float(np.linalg.norm(V[i].mean(0)-V0[i].mean(0))*1000),4) for s,i in JI.items()}
def thigh_radius(V, zlo=78):
    out={}
    for s in 'LR':
        m=(lab==names.index(f'thigh_{s}'))&(Z>zlo); C0=V0[m]; mu=C0.mean(0); _,_,vt=np.linalg.svd(C0-mu,full_matrices=False); ax=vt[0]
        rr=lambda C: np.linalg.norm((C-mu)-np.outer((C-mu)@ax,ax),axis=1).mean()
        out[s]=round(float((rr(V[m])/rr(C0)-1)*100),3)
    return out
