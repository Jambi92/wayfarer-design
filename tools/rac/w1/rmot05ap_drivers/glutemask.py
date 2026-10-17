# RM-OT-05AP posterior mask by vertex ID: sculptable = 05AI glute region + posterior upper-thigh continuity band
# (thigh-dominant, behind the thigh's own axis, z > 85 cm), minus every 05AF protected set (tail, tail junction, genital,
# perineal, ...). Mask = 1 elsewhere; inside, a wide diffusion feather (k iterations, gain) ramps 1 -> 0 from the boundary.
import sys, numpy as np
sys.path.insert(0,'/home/claude/al'); import dryrun as D
def build(V, F, lab, names, k=400, gain=2.0, zband=85.0):
    z0=V[:,2].min(); Z=(V[:,2]-z0)*100
    R=np.load('/home/claude/aj/regions_05AI.npz'); P=np.load('/home/claude/ag/protected_05AF.npz')
    S=R['glute'].copy()
    for s in 'LR':
        th=lab==names.index(f'thigh_{s}'); yc=np.median(V[th&(Z>85),1])
        S|=th&(Z>zband)&(V[:,1]>yc)
    S&=~P['all']
    Avg=D.adjacency(F,len(V)); c=(~S).astype(float)
    for _ in range(k): c=Avg@c
    m=np.ones(len(V)); m[S]=np.clip(gain*c[S],0,1); return m,S
