# RM-OT-05AS mask: 05AR field widened toward the front/lateral thigh and hip, variable graph-Lipschitz feather
# (R = 80 mm on edges touching the lateral-hip / thigh transition zone, 50 mm elsewhere), 05AR tail core/ring distance ramp
# (1.0 to 22 mm from the root core, smoothstep to 0 over 60 mm), duplicate-position seams pinned to 1.0.
import sys; sys.path[:0]=['/home/claude/ar','/home/claude/aq','/home/claude/al']; import numpy as np, aqmetrics as Q, armask as AR, dryrun as D
from scipy.spatial import cKDTree
V=Q.V0; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; lab=Q.lab; names=Q.names
St=np.load('/home/claude/ar/sets.npz'); P=np.load('/home/claude/ag/protected_05AF.npz'); dup=np.load('/home/claude/ar/dup.npy'); Rg=np.load('/home/claude/aj/regions_05AI.npz')
E=np.unique(np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1),axis=0); L=np.linalg.norm(V[E[:,0]]-V[E[:,1]],axis=1)
def lip(M,zone,R1=0.08,R0=0.05,it=600):
    r=np.where(zone[E[:,0]]|zone[E[:,1]],R1,R0); l=L/r; M=M.copy()
    for _ in range(it):
        o=M.copy(); np.maximum.at(M,E[:,0],M[E[:,1]]-l); np.maximum.at(M,E[:,1],M[E[:,0]]-l)
        if np.abs(M-o).max()<1e-9: break
    return M
def build(ytrunk=-44.0,thigh_cos=-0.35,lat_min=0.5,zlo=70.0,k=250,gain=2.0,D0=0.022,W=0.06,csm=40,extra=None):
    z0=V[:,2].min(); Z=(V[:,2]-z0)*100; X=V[:,0]*100; Yc=V[:,1]*100
    tr=lab==names.index('trunk'); S=Rg['glute'].copy(); S|=tr&(Z>88)&(Z<118)&(Yc>ytrunk)&(np.abs(X)>4)
    thz=np.zeros(len(V),bool)
    for side,sg in (('L',1),('R',-1)):
        th=lab==names.index(f'thigh_{side}'); m=th&(Z>zlo); c=V[m].mean(0); _,_,vt=np.linalg.svd(V[m]-c,full_matrices=False); ax=vt[0]
        r=(V-c)-np.outer((V-c)@ax,ax); r/=np.maximum(np.linalg.norm(r,axis=1),1e-9)[:,None]
        S|=m&((r[:,1]>thigh_cos)|(sg*r[:,0]>lat_min)); thz|=th
    S&=~(P['all']&~St['ring']); S&=~Rg['torso']; S&=~((np.abs(X)<=4)&(Z>100)); S|=St['ring']; S&=~St['core']
    Avg=D.adjacency(F,len(V)); c=(~S).astype(float)
    for _ in range(k): c=Avg@c
    M=np.ones(len(V)); M[S]=np.clip(gain*c[S],0,1)
    rootcore=St['core']&~P['tail']; dc,_=cKDTree(V[rootcore]).query(V); t=np.clip((dc-D0)/W,0,1); M=np.maximum(M,1-(3*t**2-2*t**3))
    zone=thz|(tr&(np.abs(X)>14))   # lateral hip + whole thigh transition zone -> 80 mm feather
    M[dup]=1.0; M=lip(M,zone); M[~S]=1.0; M[dup]=1.0
    # C1 pass: relax the mask itself (hard vertices held at 1.0) so the ramp meets 1.0 tangentially instead of with a slope kink
    hard=(~S)|dup|St['core']|(dc<=D0)
    for _ in range(csm):
        M=np.where(hard,1.0,Avg@M)
    if extra is not None: M=np.maximum(M,np.where(S,extra,1.0))
    M=np.maximum(M,lip(M,zone)); M[hard]=1.0
    return M,S,zone
if __name__=='__main__':
    kw=eval('dict('+(sys.argv[2] if len(sys.argv)>2 else '')+')'); M,S,zone=build(**kw); np.save(sys.argv[1],M); np.savez('as_sets.npz',S=S,zone=zone)
    j=np.abs(M[E[:,0]]-M[E[:,1]])/L; z=zone[E[:,0]]|zone[E[:,1]]
    print('S',S.sum(),'M<1',(M<1).sum(),'M<0.5',(M<0.5).sum(),'max slope zone (per 80mm)',(j[z]*0.08).max().round(3),'elsewhere (per 50mm)',(j[~z]*0.05).max().round(3),'ring min',M[St['ring']].min().round(3),'core min',M[St['core']].min(),'dup min',M[dup].min())
