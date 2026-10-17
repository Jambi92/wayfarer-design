# incremental displacement vs previous checkpoint, joint-centre drift and dihedral counts vs the frozen 05AL baseline
import sys, json, numpy as np
from scipy.spatial import cKDTree
cur, prev, out = sys.argv[1:4]
B=np.load('/home/claude/al/out/after_VF.npz'); V0,F=B['V'],B['F']; V1=np.load(cur)['V']; VP=np.load(prev)['V']
W=np.load('/home/claude/af/weights_05AE.npz'); names=[str(x) for x in W['names']]; o2n=np.load('/home/claude/af/old_to_new_05AE_to_05AF.npy'); lab=np.full(len(V0),-1); lab[o2n]=W['W'].argmax(1)
limb=np.isin(lab,[names.index(k) for k in names if k.split('_')[0] in ('upperarm','forearm','thigh','shin')])
d=np.linalg.norm(V1-VP,axis=1)*1000; m=limb&(d>0.01)
R=dict(incremental=dict(moved=int(m.sum()),median=round(float(np.median(d[m])),3),p95=round(float(np.percentile(d[m],95)),3),max=round(float(d[limb].max()),3)) if m.any() else {})
jd={}
for s in 'LR':
    for a,b in [('upperarm','forearm'),('forearm','hand'),('thigh','shin'),('shin','foot')]:
        A=lab==names.index(f'{a}_{s}'); Bm=lab==names.index(f'{b}_{s}'); dd,_=cKDTree(V0[Bm]).query(V0[A]); idx=np.flatnonzero(A)[dd<0.01]
        jd[f'{a}-{b}_{s}']=round(float(np.linalg.norm(V1[idx].mean(0)-V0[idx].mean(0))*1000),4)
R['joint_centre_drift_mm']=jd
def fold(V):
    n=np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]]); n/=np.maximum(np.linalg.norm(n,axis=1),1e-30)[:,None]
    E=np.concatenate([np.sort(F[:,[0,1]],1),np.sort(F[:,[1,2]],1),np.sort(F[:,[2,0]],1)]); fid=np.tile(np.arange(len(F)),3)
    o=np.lexsort(E.T[::-1]); E,fid=E[o],fid[o]; s=(E[1:]==E[:-1]).all(1); a,b=fid[:-1][s],fid[1:][s]; return np.degrees(np.arccos(np.clip((n[a]*n[b]).sum(1),-1,1))), n
a0,n0=fold(V0); a1,n1=fold(V1); rot=np.degrees(np.arccos(np.clip((n0*n1).sum(1),-1,1)))
R['dihedral_gt60']=dict(base=int((a0>60).sum()),now=int((a1>60).sum())); R['faces_normal_rot_gt60_vs_base']=[int(x) for x in np.flatnonzero(rot>60)]
# limb circumference proxy: mean distance of limb verts to their segment centroid axis (mass preservation)
vol={}
for p in ['upperarm','forearm','thigh','shin']:
    for s in 'LR':
        mm=lab==names.index(f'{p}_{s}'); c0=V0[mm]; c1=V1[mm]
        def rad(C):
            mu=C.mean(0); u,sv,vt=np.linalg.svd(C-mu,full_matrices=False); ax=vt[0]; r=(C-mu)-np.outer((C-mu)@ax,ax); return np.linalg.norm(r,axis=1).mean()
        vol[f'{p}_{s}']=round(float((rad(c1)/rad(c0)-1)*100),3)
R['mean_radius_change_pct']=vol
json.dump(R,open(out,'w'),indent=1); print(json.dumps(R))
