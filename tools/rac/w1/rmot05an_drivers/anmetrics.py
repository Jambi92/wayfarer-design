import numpy as np
from scipy.spatial import cKDTree
B=np.load('/home/claude/al/out/after_VF.npz'); V0=B['V']
W=np.load('/home/claude/af/weights_05AE.npz'); names=[str(x) for x in W['names']]; o2n=np.load('/home/claude/af/old_to_new_05AE_to_05AF.npy'); lab=np.full(len(V0),-1); lab[o2n]=W['W'].argmax(1)
limb=np.isin(lab,[names.index(k) for k in names if k.split('_')[0] in ('upperarm','forearm','thigh','shin')])
SEG={f'{p}_{s}':lab==names.index(f'{p}_{s}') for p in ('upperarm','forearm','thigh','shin') for s in 'LR'}
AX={}
for k,m in SEG.items():
    C=V0[m]; mu=C.mean(0); _,_,vt=np.linalg.svd(C-mu,full_matrices=False); AX[k]=(mu,vt[0])
def radius(V):
    out={}
    for k,m in SEG.items():
        mu,ax=AX[k]; C=V[m]-mu; r=C-np.outer(C@ax,ax); C0=V0[m]-mu; r0=C0-np.outer(C0@ax,ax)
        out[k]=round(float((np.linalg.norm(r,axis=1).mean()/np.linalg.norm(r0,axis=1).mean()-1)*100),3)
    return out
JI={}
for s in 'LR':
    for a,b in [('upperarm','forearm'),('forearm','hand'),('thigh','shin'),('shin','foot')]:
        A=lab==names.index(f'{a}_{s}'); Bm=lab==names.index(f'{b}_{s}'); d,_=cKDTree(V0[Bm]).query(V0[A]); JI[f'{a}-{b}_{s}']=np.flatnonzero(A)[d<0.01]
def joints(V): return {k:round(float(np.linalg.norm(V[i].mean(0)-V0[i].mean(0))*1000),4) for k,i in JI.items()}
def cum(V):
    d=np.linalg.norm(V-V0,axis=1)*1000; m=limb&(d>0.01); return dict(median=round(float(np.median(d[m])),3),p95=round(float(np.percentile(d[m],95)),3),max=round(float(d[limb].max()),3),max_all=round(float(d.max()),3))
