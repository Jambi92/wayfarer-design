# Gate 8 measured safeguards for every library phenotype and every rejection control.
import sys, json, numpy as np; sys.path.insert(0,'/tmp/claude-0/rodin/g8'); sys.path.insert(0,'/tmp/claude-0/rodin/g1')
import g8pheno as GP, g7geo as G
from g8lib import PH
Fd=dict(np.load('fld_body.npz')); V=np.load('/tmp/claude-0/rodin/g1/g7up.npz')['V'].astype(float); x,f,u=V.T
FAM=Fd['FAM']; scaly=(FAM!=6)&(FAM!=7); TH=Fd['TH']; LW=Fd['LW']; S=Fd['S']
AX=np.load('axis.npy'); S_root=0.5*int(np.argmax(AX[:,1]>-27))
def srgb(c): return np.where(c<=0.0031308,12.92*c,1.055*np.power(np.clip(c,0,1),1/2.4)-0.055)
def lum(c): return c@np.array([0.2126,0.7152,0.0722])
jp=[np.array(A[k]) for A in G.ARM.values() for k in ('E','W')]+[np.array(L[k]) for L in G.LEG.values() for k in ('K','A')]
nearj=np.zeros(len(V),bool)
for p in jp: nearj|=np.linalg.norm(V-p,axis=1)<6.0
limb=(Fd['LID']>0)&~nearj
head=(u>170)&(np.abs(x)<12)&(f>-14)&((f>-5)|(u>177)); body=(u>100)&(u<160)&(LW<0.2)&scaly
dors=(np.cos(TH)>0.6)&(LW<0.2)&(u>95)&(u<165)&scaly; vent=(np.cos(TH)<-0.6)&(LW<0.2)&(u>100)&(u<165)&scaly
pre=(S>S_root-12)&(S<S_root)&(LW<0.2)&scaly; post=(S>S_root)&(S<S_root+12)&(LW<0.2)&scaly
CV=Fd['CELLV']
def metrics(ph,ov={}):
    C,M=GP.phenotype(Fd,V,ph); s=srgb(C)
    if ov.get('flat') is not None: s[:]=ov['flat']; C=GP.lin(np.array(ov['flat']))[None,:].repeat(len(V),0)
    rough=M[:,0].copy()
    if ov.get('rough') is not None: rough[:]=ov['rough']
    mx=s.max(1); mn=s.min(1); sat=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
    L=lum(C)
    # ventral boundary sharpness: max luminance step between neighbouring stations of theta (binned) on the trunk
    tb=np.clip(((TH[body]+np.pi)/(2*np.pi)*48).astype(int),0,47); lb=np.bincount(tb,L[body],48)/np.maximum(np.bincount(tb,minlength=48),1)
    step=float(np.max(np.abs(np.diff(np.r_[lb,lb[:1]])))/max(lb.mean(),1e-6))
    # cell-to-cell contrast on the face vs the trunk (face noise)
    cl=lambda m: float(np.std(L[m][np.unique(CV[m],return_index=True)[1]])/max(L[m].mean(),1e-6))
    return dict(rough_scaly_min=round(float(rough[scaly].min()),3),rough_scaly_median=round(float(np.median(rough[scaly])),3),
        rough_keratin_median=round(float(np.median(rough[FAM==6])),3),sat_p99=round(float(np.percentile(sat[scaly],99)),3),
        metallic=ov.get('metallic',0.0),emission=0.0,
        ventral_to_dorsal_luminance=round(float(L[vent].mean()/max(L[dors].mean(),1e-6)),2),
        ventral_boundary_max_step=round(step,3),
        joint_ring_index=round(float(L[nearj].mean()/max(L[limb].mean(),1e-6)),3),
        face_cell_contrast=round(cl(head&scaly),3),trunk_cell_contrast=round(cl(body),3),
        tail_root_luminance_jump=round(float(abs(L[post].mean()-L[pre].mean())/max(L[pre].mean(),1e-6)),3),
        tail_root_pattern_var_ratio=round(float((L[post].std()+1e-6)/(L[pre].std()+1e-6)),2))
out={k:metrics(v) for k,v in PH.items()}
P1=PH['P1_umber_mottled']
fails={'wet_plastic':(dict(P1,pattern='uniform',contrast=0),dict(flat=(0.16,0.42,0.17),rough=0.06)),'metallic':(P1,dict(metallic=1.0,rough=0.25)),
 'pale_belly':(dict(P1,fail='pale_belly'),{}),'paint_mask':(dict(P1,fail='paint_mask'),{}),'joint_rings':(dict(P1,pattern='uniform',contrast=0.95,fail='joint_rings'),{}),
 'face_noise':(dict(P1,fail='face_noise'),{}),'tail_seam':(dict(P1,pattern='uniform',fail='tail_seam'),{}),
 'dragon':(dict(P1,pattern='uniform',primary=(0.62,0.06,0.04),secondary=(0.3,0.02,0.02),belly=(0.95,0.72,0.18),fail='dragon'),dict(metallic=0.35,rough=0.15))}
out['_REJECT']={k:metrics(a,b) for k,(a,b) in fails.items()}
json.dump(out,open('acct12.json','w'),indent=1); print(json.dumps(out,indent=0)[:4000])
