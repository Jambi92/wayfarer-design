import sys; sys.path.insert(0,'/home/claude/an'); sys.path.insert(0,'/home/claude/al')
import numpy as np, scipy.sparse as sp, dryrun as D, predict_an as P, anmetrics as AM
from scipy.spatial import cKDTree
A=np.load('prep1/after_VF.npz'); V,F=A['V'],A['F']; Avg=D.adjacency(F,len(V)); M0=np.load('mask_ao.npy'); M=np.load('mask_ao_v2.npy')
W=np.load('vgroups.npz'); names=list(W['names']); lab=W['W'].argmax(1); ua=np.isin(lab,[names.index('upperarm_L'),names.index('upperarm_R')])
vf=sp.csr_matrix((np.ones(F.size),(F.ravel(),np.repeat(np.arange(len(F)),3))),shape=(len(V),len(F))); rv=P.ringang(V,F,vf)
for it in range(4):
    bad=[]
    for n in [190,230]:
        S=P.laplace_iter(V,Avg,M,n); rs=P.ringang(S,F,vf); bad+=list(np.flatnonzero(((rs>60)&(rv<=60))|((rs>90)&(rv<=90))))+list(D.flips(V,S,F))
    print(it,'bad',len(set(bad)),flush=True)
    if not bad: break
    d,_=cKDTree(V[F[np.array(sorted(set(bad)))]].mean(1)).query(V); d*=1000; bump=np.clip((25-d)/15,0,1); M[ua]=np.maximum(M[ua],bump[ua])
S=P.laplace_iter(V,Avg,M,190); r=AM.radius(S); print('UA',r['upperarm_L'],r['upperarm_R'],'bumped',(M>M0+1e-6).sum(),AM.cum(S)); np.save('mask_ao_v3.npy',M); np.savez('simAOv3.npz',V=S,F=F)
