# gate_v005_deltas.py V005.npz OUT.json MASKS.npz : v004 -> v005 delta accounting per order section 21 region mask
import sys, json, numpy as np
sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from ident_apply import SS
R='/tmp/claude-0/rp2/'
X=np.load(sys.argv[1])['V'].astype(float); Q=np.load(sys.argv[1])['Q']; V4=np.load(R+'fin/v004.npz')['V'].astype(float)
W={k:SS()@v for k,v in np.load(R+'weights_body.npz').items()}; g=lambda *ks: sum(W[k] for k in ks)
z=V4[:,2]; f=V4[:,1]; ears=W['ears']>0.5
head_neck=(g('head','ears','neck_01')>0.5)
upper_arms=g('upperarm_l','upperarm_r')>0.5
forearms=g('lowerarm_l','lowerarm_r')>0.5
hands=g('hand_l','hand_r','fingers_l','fingers_r')>0.5
feet=g('foot_l','foot_r','ball_l','ball_r')>0.5
thighs=g('thigh_l','thigh_r')>0.5
calves=g('calf_l','calf_r')>0.5
trunk=(g('spine_01','spine_02','spine_03','pelvis','clavicle_l','clavicle_r')>0.5)&~head_neck&~upper_arms
chest=trunk&(f>2.5)&(z>142)
abdomen=trunk&(f>2.5)&(z>108)&(z<=142)
back=trunk&(f<=2.5)&(z>118)
pelvis_glutes=trunk&~chest&~abdomen&~back
M=dict(thighs=thighs,back=back,chest=chest,upper_arms=upper_arms,forearms=forearms,abdomen=abdomen,pelvis_glutes=pelvis_glutes,head_neck=head_neck,calves=calves,hands=hands,feet=feet)
d=np.linalg.norm(X-V4,axis=1)*10
np.savez_compressed(sys.argv[3],**M,displacement_from_v004_mm=d.astype(np.float32))
out={}
anym=np.zeros(len(X),bool)
for k,m in M.items():
    anym|=m; out[k]=dict(vertices=int(m.sum()),moved_gt_0p5mm=int((m&(d>0.5)).sum()),mean_mm=float(d[m].mean()),max_mm=float(d[m].max()))
o=~anym; out['outside_all_masks']=dict(vertices=int(o.sum()),moved_gt_0p5mm=int((o&(d>0.5)).sum()),max_mm=float(d[o].max()) if o.any() else 0.0)
out['all']=dict(moved_gt_0p5mm=int((d>0.5).sum()),mean_mm=float(d.mean()),max_mm=float(d.max()))
st=lambda V: float(V[:,2].max()-V[:,2].min())
out['stature_cm']=dict(v004=st(V4),v005=st(X),delta_mm=(st(X)-st(V4))*10)
out['bbox_delta_mm']=dict(min=((X.min(0)-V4.min(0))*10).tolist(),max=((X.max(0)-V4.max(0))*10).tolist())
json.dump(out,open(sys.argv[2],'w'),indent=1)
for k,v in out.items(): print(k,v)
