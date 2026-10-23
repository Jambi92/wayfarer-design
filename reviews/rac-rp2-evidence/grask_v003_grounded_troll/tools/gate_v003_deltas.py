# gate_v003_deltas.py V003.npz OUT.json MASKS.npz : delta accounting of v003 against v001 and v002 per region mask
import sys, json, numpy as np
sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from ident_apply import SS
R='/tmp/claude-0/rp2/'
X=np.load(sys.argv[1])['V'].astype(float); Q=np.load(sys.argv[1])['Q']
V1=np.load(R+'cand_v001b.npz')['V'].astype(float); V2=np.load(R+'fin/v002.npz')['V'].astype(float)
W={k:SS()@v for k,v in np.load(R+'weights_body.npz').items()}; g=lambda *ks: sum(W[k] for k in ks)
ears=W['ears']>0.5
head=(g('head','ears')>0.5)&~ears
neck=((g('neck_01','clavicle_l','clavicle_r')>0.5)|((X[:,2]>168)&(np.abs(X[:,0])<16)&~(g('upperarm_l','upperarm_r')>0.5)))&~head&~ears
hands=g('hand_l','hand_r','fingers_l','fingers_r')>0.5
feet=g('foot_l','foot_r','ball_l','ball_r')>0.5
torso=(g('spine_01','spine_02','spine_03','pelvis')>0.5)&~neck&~head&~ears
limbs=~(ears|head|neck|hands|feet|torso)
M=dict(head_face=head,ears=ears,neck_girdle=neck,torso=torso,hands=hands,feet=feet,joint_structure_limbs=limbs)
np.savez_compressed(sys.argv[3],**M,displacement_from_v001_mm=(np.linalg.norm(X-V1,axis=1)*10).astype(np.float32),displacement_from_v002_mm=(np.linalg.norm(X-V2,axis=1)*10).astype(np.float32))
out={}
d21=np.linalg.norm(V2-V1,axis=1)*10
for k,m in M.items():
    r={}
    for nm,B in (('vs_v001',V1),('vs_v002',V2)):
        d=np.linalg.norm(X-B,axis=1)*10
        r[nm]=dict(vertices=int(m.sum()),moved_gt_0p5mm=int((m&(d>0.5)).sum()),mean_mm=float(d[m].mean()),max_mm=float(d[m].max()))
    # fraction of the v001->v002 change retained (projection of v003-v001 onto v002-v001)
    a=(X-V1)[m]; b=(V2-V1)[m]; den=(b*b).sum()
    r['retained_fraction_of_v002_change']=float((a*b).sum()/den) if den>0 else None
    r['closer_to']='v001' if r['vs_v001']['mean_mm']<r['vs_v002']['mean_mm'] else 'v002'
    out[k]=r
t3=lambda V: dict(stature_cm=float(V[:,2].max()-V[:,2].min()),bbox_min=V.min(0).tolist(),bbox_max=V.max(0).tolist())
out['T3']=dict(v003=t3(X),v001=t3(V1),v002=t3(V2),stature_delta_mm_vs_v001=float(((X[:,2].max()-X[:,2].min())-(V1[:,2].max()-V1[:,2].min()))*10),
               stature_delta_mm_vs_v002=float(((X[:,2].max()-X[:,2].min())-(V2[:,2].max()-V2[:,2].min()))*10),
               bbox_delta_mm_vs_v001=(np.r_[X.min(0)-V1.min(0),X.max(0)-V1.max(0)]*10).tolist(),bbox_delta_mm_vs_v002=(np.r_[X.min(0)-V2.min(0),X.max(0)-V2.max(0)]*10).tolist())
exec(open(R+'tools/gate_ident.py').read().split('# T-7 silhouettes')[1].split("ef=moved")[0].replace('iou=lambda','iou=lambda') if False else '')
from PIL import Image, ImageDraw
from scipy.ndimage import binary_fill_holes
def sil(V,Qm,view,ppc=3.0,ss_=8):
    Tm=np.r_[Qm[:,[0,1,2]],Qm[:,[0,2,3]]]
    Xp,Yp=(V[:,0],V[:,2]) if view=='front' else ((-V[:,0],V[:,2]) if view=='rear' else (V[:,1],V[:,2]))
    x0,y0=-60,-2; Wd,Hh=int(120*ppc),int(225*ppc); k=ppc*ss_
    img=Image.new('L',(Wd*ss_,Hh*ss_),0); d=ImageDraw.Draw(img); px=(Xp-x0)*k; py=Hh*ss_-(Yp-y0)*k
    for t in Tm: d.polygon([(px[i],py[i]) for i in t],fill=255)
    a=np.array(img,float)/255; a=a.reshape(Hh,ss_,Wd,ss_).mean((1,3)); return binary_fill_holes(a>=0.5)
iou=lambda a,b: float((a&b).sum()/(a|b).sum())
out['silhouette']={}
for v in ('front','profile','rear'):
    a=sil(X,Q,v); b1=sil(V1,Q,v); b2=sil(V2,Q,v)
    out['silhouette'][v]=dict(iou_vs_v001=iou(a,b1),iou_vs_v002=iou(a,b2),area_change_pct_vs_v001=float((a.sum()-b1.sum())/b1.sum()*100),area_change_pct_vs_v002=float((a.sum()-b2.sum())/b2.sum()*100))
json.dump(out,open(sys.argv[2],'w'),indent=1)
for k in M: print('%-22s'%k, 'v001 mean %.1f max %.1f | v002 mean %.1f max %.1f | retained %.2f | closer %s'%(out[k]['vs_v001']['mean_mm'],out[k]['vs_v001']['max_mm'],out[k]['vs_v002']['mean_mm'],out[k]['vs_v002']['max_mm'],out[k]['retained_fraction_of_v002_change'] or 0,out[k]['closer_to']))
print(json.dumps(out['T3'],indent=0)[:600]); print(out['silhouette'])
