# RM-OT-05AR posterior mask. Hard sets: free tail + immutable tail core (tail-junction vertices within CORE_MM of the tail
# interface), genital, perineal, head/hands/feet, 05AI torso, sacral strip, front thigh, lower thigh/knee and everything else outside
# the field. Field S = 05AI glute + trunk lateral/posterior hip (z 88-118 cm, y > -46 cm, |x| > 4 cm) + thigh above z 70 cm on the
# posterior + lateral side (angle test) + the tail-junction continuity ring. Mask = diffusion ramp inside S, then a graph Lipschitz
# limit: every edge satisfies M_v >= M_u - len_uv / R (R = 50 mm), so no transition anywhere is narrower than 50 mm (covers the
# >= 30 mm duplicate-seam rule and the >= 50 mm lateral / posterior-thigh rule).
import sys; sys.path[:0]=['/home/claude/aq','/home/claude/al']; import numpy as np, scipy.sparse as sp, dryrun as D
from scipy.spatial import cKDTree
def sets(V,F,lab,names,core_mm=8.0):
    P=np.load('/home/claude/ag/protected_05AF.npz'); n=len(V)
    A=sp.csr_matrix((np.ones(F.size*2),(np.r_[F[:,0],F[:,1],F[:,2],F[:,1],F[:,2],F[:,0]],np.r_[F[:,1],F[:,2],F[:,0],F[:,0],F[:,1],F[:,2]])),shape=(n,n))
    iface=P['tail']&((A@P['tail_junction'].astype(float))>0)
    d,_=cKDTree(V[iface]).query(V); core=P['tail']|(P['tail_junction']&(d*1000<=core_mm)); ring=P['tail_junction']&~core
    return dict(core=core,ring=ring,iface=iface,A=A)
def lipschitz(M,V,F,R=0.05,it=400):
    e=np.unique(np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1),axis=0); l=np.linalg.norm(V[e[:,0]]-V[e[:,1]],axis=1)/R
    M=M.copy()
    for _ in range(it):
        old=M.copy(); np.maximum.at(M,e[:,0],M[e[:,1]]-l); np.maximum.at(M,e[:,1],M[e[:,0]]-l)
        if np.abs(M-old).max()<1e-9: break
    return M
def build(V,F,lab,names,zlo=70.0,k=250,gain=2.0,R=0.05,core_mm=8.0,thigh_cos=-0.35,ytrunk=-46.0):
    z0=V[:,2].min(); Z=(V[:,2]-z0)*100; X=V[:,0]*100; Yc=V[:,1]*100
    Rg=np.load('/home/claude/aj/regions_05AI.npz'); P=np.load('/home/claude/ag/protected_05AF.npz'); s=sets(V,F,lab,names,core_mm)
    tr=lab==names.index('trunk'); S=Rg['glute'].copy()
    S|=tr&(Z>88)&(Z<118)&(Yc>ytrunk)&(np.abs(X)>4)
    for side,sg in (('L',1),('R',-1)):
        th=lab==names.index(f'thigh_{side}'); m=th&(Z>zlo); c=V[m].mean(0); _,_,vt=np.linalg.svd(V[m]-c,full_matrices=False); ax=vt[0]
        r=(V-c)-np.outer((V-c)@ax,ax); r/=np.maximum(np.linalg.norm(r,axis=1),1e-9)[:,None]
        post=r[:,1]; lat=sg*r[:,0]; S|=m&((post>thigh_cos)|(lat>0.5))   # posterior half + lateral side; front/medial stay hard
    S&=~(P['all']&~s['ring']); S&=~Rg['torso']; S&=~((np.abs(X)<=4)&(Z>100)); S|=s['ring']; S&=~s['core']
    Avg=D.adjacency(F,len(V)); c=(~S).astype(float)
    for _ in range(k): c=Avg@c
    m=np.ones(len(V)); m[S]=np.clip(gain*c[S],0,1); m=lipschitz(m,V,F,R); m[~S]=1.0
    return m,S,s
