# ident_stations.py : relationship readings E3 / v001 / candidate (cm)
import sys, json, numpy as np
sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from ident_apply import SS
R='/tmp/claude-0/rp2/'
W=np.load(R+'weights_body.npz'); S=SS()
J0=json.loads(str(np.load(R+'GR5DE3_r6.npz')['joints']))
def read(V, ear_w, hand_w, foot_w, J):
    st=V[:,2].max()-V[:,2].min()
    mid=np.abs(V[:,0])<0.4
    chin=V[mid&(V[:,1]>12)&(V[:,2]>175)&(V[:,2]<200),2].min()
    crown=V[:,2].max()
    el=V[(ear_w>0.5)&(V[:,0]>0)]; ear_len=el[:,2].max()-el[:,2].min(); ear_out=el[:,0].max()
    h=V[(hand_w>0.5)&(V[:,0]>0)]; wr=np.array(J['hand_l'][0]); hand_len=wr[2]-h[:,2].min()
    f=V[(foot_w>0.5)&(V[:,0]>0)]; foot_len=f[:,1].max()-f[:,1].min(); foot_br=f[:,0].max()-f[:,0].min()
    sh=V[(V[:,2]>150)&(V[:,2]<185)]; biacrom=sh[:,0].max()-sh[:,0].min()
    tr=V[(V[:,2]>128)&(V[:,2]<132)&(np.abs(V[:,0])<17)]
    fore=np.linalg.norm(np.array(J['lowerarm_l'][1])-np.array(J['lowerarm_l'][0])); shank=np.linalg.norm(np.array(J['calf_l'][1])-np.array(J['calf_l'][0]))
    return dict(stature=st, head_height_crown_to_menton=crown-chin, head_to_stature=(crown-chin)/st, ear_length=ear_len, ear_lateral_extent=ear_out,
                hand_length_wrist_to_tip=hand_len, hand_to_forearm=hand_len/fore, foot_length=foot_len, foot_breadth=foot_br, foot_to_shank=foot_len/shank,
                shoulder_span_150_185=biacrom, trunk_width_130=tr[:,0].max()-tr[:,0].min(), trunk_depth_130=tr[:,1].max()-tr[:,1].min())
ew=S@W['ears']; hw=S@(W['hand_l']+W['fingers_l']); fw=S@(W['foot_l']+W['ball_l'])
E=np.load(R+'e3_body.npz')['V']
res={'E3':read(E,W['ears'],W['hand_l']+W['fingers_l'],W['foot_l']+W['ball_l'],J0),'v001':read(np.load(R+'cand_v001b.npz')['V'],ew,hw,fw,J0)}
for c,j in zip(sys.argv[1::2],sys.argv[2::2]):
    res[c.split('/')[-1][:-4]]=read(np.load(c)['V'],ew,hw,fw,json.load(open(j)))
json.dump(res,open(R+'idc/stations_ident.json','w'),indent=1)
for k in res['E3']: print('%-30s'%k, *['%9.3f'%res[m][k] for m in res])
