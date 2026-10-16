import sys, json, numpy as np
sys.argv=['x']
src=open('/home/claude/wayfarer-design/tools/rac/w1/rmot05ac_drivers/ac1_checks.py').read().split('b, a, pp')[0]; exec(src)
U='/mnt/user-data/uploads/RaceBodies/source/Gorrund-Neutral-C'
VB,FB,_=load_glb(U+'/05AB1/GO-05AB1_macro_corrected_clean.glb'); VA,FA,_=load_glb(U+'/05AC/GO-05AC_AC1.glb')
kB,ivB=np.unique(np.round(VB,6),axis=0,return_inverse=True); ivB=ivB.ravel(); WB=ivB[FB]
# corner positions after
CA=VA[FA].reshape(-1,3); gid=WB.ravel()
order=np.argsort(gid); g=gid[order]; P=CA[order]
starts=np.r_[0,np.flatnonzero(np.diff(g))+1]; ends=np.r_[starts[1:],len(g)]
mn=np.minimum.reduceat(P,starts,axis=0); mx=np.maximum.reduceat(P,starts,axis=0)
spread=np.linalg.norm(mx-mn,axis=1)*1000  # mm
print('welded B groups',len(starts),'groups with corner spread >0.01mm',int((spread>0.01).sum()),'>0.1mm',int((spread>0.1).sum()),'>1mm',int((spread>1).sum()),'max mm',round(float(spread.max()),3))
# glTF split counts: how many distinct GLB vertices per welded group before
cntB=np.bincount(ivB); print('baseline GLB verts per welded position: max',cntB.max(),'groups with >1',int((cntB>1).sum()))
bad=spread>0.01; X=kB[bad]; Z=np.c_[X[:,0],-X[:,2],X[:,1]]*100
if bad.any(): print('opened seam bbox cm zup',np.round(Z.min(0),1),np.round(Z.max(0),1))
np.save('seam_spread_mm.npy',spread)
# flips relative to opened seams
n=lambda V: np.cross(V[:,1]-V[:,0],V[:,2]-V[:,0])
TB=VB[FB]; TA=VA[FA]; nb=n(TB); na=n(TA)
lb=np.linalg.norm(nb,axis=1); la=np.linalg.norm(na,axis=1)
dot=(nb*na).sum(1)/np.maximum(lb*la,1e-30)
flip=dot<0; degen=la<1e-14
seamface=bad[WB].any(1)
print('flipped',int(flip.sum()),'of which on opened-seam faces',int((flip&seamface).sum()))
print('degenerate after',int(degen.sum()),'of which on opened-seam faces',int((degen&seamface).sum()))
fl=flip&~seamface
if fl.any():
    c=TA[fl].mean(1); c=np.c_[c[:,0],-c[:,2],c[:,1]]*100; print('non-seam flips bbox',np.round(c.min(0),1),np.round(c.max(0),1))
json.dump(dict(opened_positions=int(bad.sum()),gt_0_1mm=int((spread>0.1).sum()),gt_1mm=int((spread>1).sum()),max_gap_mm=round(float(spread.max()),3),flipped=int(flip.sum()),flipped_on_opened_seams=int((flip&seamface).sum()),degenerate_after=int(degen.sum()),degenerate_on_opened_seams=int((degen&seamface).sum())),open('seam_report.json','w'),indent=1)
