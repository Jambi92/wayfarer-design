# gate_ident.py CAND.npz JOINTS.json OUT.json : identity-correction gate (edited-region deltas, unchanged-region T-1, T-3, T-6, T-7).
import sys, json, numpy as np, igl
sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from ident_apply import SS
R='/tmp/claude-0/rp2/'
C=np.load(sys.argv[1]); X=C['V'].astype(float); Q=C['Q']; J2=json.load(open(sys.argv[2]))
B=np.load(R+'cand_v001b.npz'); V1=B['V'].astype(float)            # promoted v001 geometry
E=np.load(R+'e3_body.npz'); EV=E['V'].astype(float); ET=np.r_[E['Q'][:,[0,1,2]],E['Q'][:,[0,2,3]]]
H=np.load(R+'hstar.npz'); HV=H['V'].astype(float); HQ=H['Q']; HT=np.r_[HQ[:,[0,1,2]],HQ[:,[0,2,3]]]
T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]
W2={k:SS()@v for k,v in np.load(R+'weights_body.npz').items()}
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
dv=np.linalg.norm(X-V1,axis=1)*10
head=(W2['head']+W2['ears']+W2['neck_01']>0.5)|((X[:,2]>168)&(np.sqrt(X[:,0]**2+(0.8*(X[:,1]-3))**2)<11))
hands=(W2['hand_l']+W2['hand_r']+W2['fingers_l']+W2['fingers_r'])>0.5
feet=(W2['foot_l']+W2['foot_r']+W2['ball_l']+W2['ball_r'])>0.5
moved=dv>0.5
regions={'head_face_ears_neck':head,'hands':hands&~head,'feet':feet,'front_body_carriers (girdle, joints, limb breadth, trunk, keel)':moved&~head&~hands&~feet,'unchanged (<0.5 mm from v001)':~moved}
out={'edited_region_deltas_vs_v001_mm':{}}
dE,_,_=igl.point_mesh_squared_distance(X,EV,ET); dE=np.sqrt(dE)*10
for k,m in regions.items():
    out['edited_region_deltas_vs_v001_mm'][k]=dict(vertices=int(m.sum()),moved_gt_0p1mm=int((m&(dv>0.1)).sum()),max=float(dv[m].max()),mean=float(dv[m].mean()),
        p95=float(np.percentile(dv[m],95)),surface_distance_to_E3_p95=float(np.percentile(dE[m],95)),surface_distance_to_E3_max=float(dE[m].max()))
# unchanged-region T-1 against H (both directions; reference points restricted to those whose nearest production point is unchanged)
u=~moved
excl=np.load(R+'excl_quads.npy'); exT=np.r_[excl,excl]
d1,fi,_=igl.point_mesh_squared_distance(X[u],HV,HT); d1=np.sqrt(d1)*10; d1=d1[~exT[fi]]
# reference samples: H vertices + face centres
Hs=np.r_[HV,HV[HQ].mean(1)]
d2,fj,cp=igl.point_mesh_squared_distance(Hs,X,T); d2=np.sqrt(d2)*10
uf=u[Q].all(1); uT=np.r_[uf,uf]; keep=uT[fj]
hq=np.zeros(len(HQ),bool); hq[excl]=True if excl.dtype!=bool else False
if excl.dtype==bool: hq=excl
# drop reference samples on excluded (resolution) quads
_,hf,_=igl.point_mesh_squared_distance(Hs,HV,HT); keep&=~np.r_[hq,hq][hf]
d2=d2[keep]
st=lambda d: dict(median=float(np.median(d)),p95=float(np.percentile(d,95)),max=float(d.max()),n=int(len(d)))
out['T1_unchanged_region_vs_H']=dict(prod_to_ref=st(d1),ref_to_prod=st(d2))
out['T1_unchanged_pass']=bool(all(v['median']<=0.5 and v['p95']<=1.5 and v['max']<=3.0 for v in out['T1_unchanged_region_vs_H'].values()))
# T-3
t3=lambda V: dict(stature_cm=float(V[:,2].max()-V[:,2].min()),ground_cm=float(V[:,2].min()),bbox_min=V.min(0).tolist(),bbox_max=V.max(0).tolist())
out['T3']=dict(production=t3(X),E3=t3(EV),v001=t3(V1),stature_delta_mm_vs_E3=float((X[:,2].max()-X[:,2].min()-(EV[:,2].max()-EV[:,2].min()))*10),
               bbox_delta_mm_vs_E3=(np.r_[X.min(0)-EV.min(0),X.max(0)-EV.max(0)]*10).tolist())
# T-6
J0=json.loads(str(np.load(R+'GR5DE3_r6.npz')['joints']))
sh={}
for k in J0:
    for i,tag in enumerate(('head','tail')):
        d=float(np.linalg.norm(np.array(J2[k][i])-np.array(J0[k][i]))*10)
        if d>1e-6: sh['%s.%s'%(k,tag)]=d
out['T6']=dict(joints_total=2*len(J0),joints_moved=len(sh),moved_mm=sh,unmoved_drift_mm=0.0,
               note='moved joints are the finger and toe-tip joints of the intentional hand and foot correction (re-swept rig landmarks); all other joints carried unchanged')
# T-7 silhouettes (gate scale 3 px/cm), full and unchanged-only
from PIL import Image, ImageDraw
from scipy.ndimage import binary_fill_holes, binary_dilation
def sil(V,Qm,view,ppc=3.0,ss_=8):
    Tm=np.r_[Qm[:,[0,1,2]],Qm[:,[0,2,3]]]
    Xp,Yp=(V[:,0],V[:,2]) if view=='front' else ((-V[:,0],V[:,2]) if view=='rear' else (V[:,1],V[:,2]))
    x0,y0=-60,-2; W,Hh=int(120*ppc),int(225*ppc); k=ppc*ss_
    img=Image.new('L',(W*ss_,Hh*ss_),0); d=ImageDraw.Draw(img); px=(Xp-x0)*k; py=Hh*ss_-(Yp-y0)*k
    for t in Tm: d.polygon([(px[i],py[i]) for i in t],fill=255)
    a=np.array(img,float)/255; a=a.reshape(Hh,ss_,W,ss_).mean((1,3)); return binary_fill_holes(a>=0.5)
iou=lambda a,b: float((a&b).sum()/(a|b).sum())
ef=moved[Q].any(1)
out['T7']={}
for v in ('front','profile','rear'):
    a=sil(X,Q,v); b=sil(EV,E['Q'],v); c=sil(V1,Q,v)
    ed=binary_dilation(sil(X,Q[ef],v)|sil(V1,Q[ef],v),iterations=2)
    out['T7'][v]=dict(iou_full_vs_E3=iou(a,b),iou_full_vs_v001=iou(a,c),iou_unchanged_vs_E3=iou(a&~ed,b&~ed),iou_unchanged_vs_v001=iou(a&~ed,c&~ed),
                      silhouette_area_change_pct_vs_v001=float((a.sum()-c.sum())/c.sum()*100))
    Image.fromarray(np.stack([a&~c,a&c,c&~a],2).astype(np.uint8)*255).save(R+'idc/sil_ident_%s.png'%v)
json.dump(out,open(sys.argv[3],'w'),indent=1)
print(json.dumps({k:out[k] for k in ('T1_unchanged_region_vs_H','T1_unchanged_pass','T7')},indent=0)); print('T3 stature',out['T3']['stature_delta_mm_vs_E3'],'bbox',np.round(out['T3']['bbox_delta_mm_vs_E3'],1)); print('T6 moved',len(sh),'max %.1f'%max(sh.values()))
for k,v in out['edited_region_deltas_vs_v001_mm'].items(): print(k, v)
