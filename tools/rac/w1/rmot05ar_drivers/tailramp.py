# 05AR v5: the continuity ring is driven by a smooth function of distance to the immutable root core (junction part of the core),
# not by membership in the irregular 05AF tail-junction set, so the ramp outline follows the round root, not the jagged set border.
import sys; sys.path[:0]=['/home/claude/ar','/home/claude/aq']; import numpy as np, aqmetrics as Q, armask as AR
from scipy.spatial import cKDTree
V=Q.V0; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; St=np.load('sets.npz'); S=St['S']; P=np.load('/home/claude/ag/protected_05AF.npz'); dup=np.load('dup.npy')
rootcore=St['core']&~P['tail']; dcore,_=cKDTree(V[rootcore]).query(V)
def make(base,Rt,W=0.06):
    t=np.clip((dcore-Rt)/W,0,1); ramp=1-(3*t**2-2*t**3)   # 1 out to Rt from the root core, smoothstep to 0 over W
    M=np.maximum(base,ramp); M[dup]=1.0; M=AR.lipschitz(M,V,F,0.05); M[~S]=1.0; return M
if __name__=='__main__':
    import aqsim as A
    base=np.load('mask_ar0.npy'); base[dup]=1.0; base=AR.lipschitz(base,V,F,0.05); base[~S]=1.0
    for Rt in [float(x) for x in sys.argv[1].split(',')]:
        M=make(base,Rt); res,Sv=A.flags2(V,F,M,-0.007919,[200]); dr=np.linalg.norm(Sv-V,axis=1)*1000
        print('D0',Rt,{k:len(v) for k,v in res[200].items()},'ring max',dr[St['ring']].max().round(3),'core',dr[St['core']].max(),'depth',Q.profile_depth(Sv),flush=True)
        np.save(f'mask_t{int(Rt*1000)}.npy',M)
