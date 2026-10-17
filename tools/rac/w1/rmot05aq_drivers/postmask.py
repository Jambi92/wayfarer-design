# RM-OT-05AQ broad posterior mask by vertex ID.
# Region S = 05AI glute region + lateral/posterior hip soft tissue (trunk-dominant, z 88-118 cm, behind the pelvis mid-plane,
# outside a sacral midline strip) + posterior upper thigh (thigh-dominant, behind the thigh axis, z > ZLO) ; minus every 05AF
# protected set (tail, tail junction, genital, perineal, ...). Mask = 1 outside S. Inside S the mask ramps 1 -> 0 by graph
# diffusion of the outside indicator (k iterations, gain), so every border (tail ring, sacrum, lower thigh, front thigh, torso)
# is feathered; the protected cores themselves stay exactly 1.0.
import sys, numpy as np
sys.path.insert(0,'/home/claude/al'); import dryrun as D
def build(V, F, lab, names, zlo=70.0, k=250, gain=2.0, sacral_half_cm=4.0):
    z0=V[:,2].min(); Z=(V[:,2]-z0)*100; X=V[:,0]*100; Yc=V[:,1]*100
    R=np.load('/home/claude/aj/regions_05AI.npz'); P=np.load('/home/claude/ag/protected_05AF.npz')
    tr=lab==names.index('trunk'); S=R['glute'].copy()
    S|=tr&(Z>88)&(Z<118)&(Yc>-36.0)&(np.abs(X)>sacral_half_cm)
    for s in 'LR':
        th=lab==names.index(f'thigh_{s}'); yc=np.median(V[th&(Z>zlo),1])
        S|=th&(Z>zlo)&(V[:,1]>yc)
    S&=~P['all']; S&=~R['torso']; S&=~((np.abs(X)<=sacral_half_cm)&(Z>100))
    Avg=D.adjacency(F,len(V)); c=(~S).astype(float)
    for _ in range(k): c=Avg@c
    m=np.ones(len(V)); m[S]=np.clip(gain*c[S],0,1); return m,S
