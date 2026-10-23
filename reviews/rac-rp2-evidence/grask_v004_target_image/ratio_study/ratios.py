# ratios.py MESH.npz JOINTS.json [...] : order section 12 visual-calibration ratios.
# The same silhouette measurements are taken on the target image and on each mesh, at anatomical stations:
# target stations are read by hand from the gridded target image (pixel rows); mesh stations come from the mesh joints.
import sys, json, numpy as np
sys.path.insert(0,'/tmp/claude-0/rp2/v4'); from prof import runs
from ourprof import sil
from PIL import Image
R='/tmp/claude-0/rp2/'
# target pixel rows (front figure x 0-440, profile figure x 440-700), read from v4/grid_top.png, grid_bot.png, arm_zoom.png
TGT=dict(crown=68,sole=1380,chin=228,acromion=275,elbow=510,wrist=735,fingertip=900,hip=640,knee=940,ankle=1300,temple=110,pcrown=71,psole=1376)
def T_masks():
    a=np.asarray(Image.open(R+'v4/target.png').convert('RGB')).astype(int); m=np.abs(a-np.array([192,190,190])).sum(2)>40
    F=np.zeros_like(m); F[:,0:440]=m[:,0:440]; P=np.zeros_like(m); P[:,440:700]=m[:,440:700]
    t=lambda y:(y-TGT['crown'])/(TGT['sole']-TGT['crown'])
    st={k:t(v) for k,v in TGT.items() if k not in('crown','sole','pcrown','psole')}
    return F,TGT['crown'],TGT['sole'],220,P,TGT['pcrown'],TGT['psole'],st
def M_masks(f,jf):
    D=np.load(f); V=D['V']; J=json.load(open(jf)); top=V[:,2].max(); bot=V[:,2].min(); t=lambda z:(top-z)/(top-bot)
    out=[]
    for view in ('front','left'):
        m,ppc=sil(V,D['Q'],view); H=m.shape[0]; out+= [m,int(H-(top+2)*ppc),int(H-(bot+2)*ppc)]+([int(60*ppc)] if view=='front' else [])
    hand=V[(np.abs(V[:,0]-J['hand_l'][0][0])<12)&(V[:,0]>15)&(V[:,2]<J['hand_l'][0][2])]
    # chin: lowest midline point of the face in front of the neck
    mid=np.abs(V[:,0])<0.5; face=V[mid&(V[:,1]>J['head'][0][1]+4)&(V[:,2]>J['neck_01'][0][2])&(V[:,2]<J['head'][0][2]+8)]
    sel=face[face[:,1]>np.percentile(face[:,1],60)]; chin=sel[:,2].min()
    st=dict(chin=t(chin),acromion=t(J['upperarm_l'][0][2]),elbow=t(J['lowerarm_l'][0][2]),wrist=t(J['hand_l'][0][2]),fingertip=t(J['middle_03_l'][1][2]-1.0),
            hip=t(J['thigh_l'][0][2]),knee=t(J['calf_l'][0][2]),ankle=t(J['foot_l'][0][2]),temple=(TGT['temple']-TGT['crown'])/(TGT['sole']-TGT['crown']))
    return out+[st]
def measure(F,c,s,cx,P,pc,ps,st):
    H=s-c; row=lambda t: runs(F[int(c+t*H)]); G=lambda a,b: np.arange(a,b,0.0025)
    def center(t):
        rs=[r for r in row(t) if r[0]<=cx<=r[1]]; return (rs[0][1]-rs[0][0])/H if rs else 0
    def full(t):
        rs=row(t); return (rs[-1][1]-rs[0][0])/H if rs else 0
    def arm(t):                     # image-left arm, only where it is separated from the trunk
        rs=row(t); return (rs[0][1]-rs[0][0])/H if len(rs)>=3 and rs[0][1]<cx-10 else np.nan
    def leg(t):
        rs=[r for r in row(t) if r[1]<cx+3]; return (rs[-1][1]-rs[-1][0])/H if rs else np.nan
    nmax=lambda f,a,b: np.nanmax([f(t) for t in G(a,b)])
    shoulder=nmax(full,st['acromion'],st['acromion']+0.06)
    rib=center(0.34); waist=min(center(t) for t in G(0.38,0.47)); pelvis=max(center(t) for t in G(0.47,0.54))
    head_w=full(st['temple']); neck=min(center(t) for t in G(st['chin']+0.005,st['acromion']))
    ua=nmax(arm,st['acromion']+0.06,st['elbow']); fa=nmax(arm,st['elbow'],st['wrist'])
    th=leg(st['hip']+0.7*(st['knee']-st['hip'])); ca=nmax(leg,st['knee'],st['ankle'])
    PH=ps-pc; foot=max((runs(P[y])[-1][1]-runs(P[y])[0][0]) for y in range(int(pc+0.975*PH),ps) if runs(P[y]))/PH
    return dict(shoulder_width_over_height=shoulder, ribcage_width_over_height=rib, waist_over_shoulder=waist/shoulder, pelvis_over_shoulder=pelvis/shoulder,
        hand_length_over_forearm_length=(st['fingertip']-st['wrist'])/(st['wrist']-st['elbow']), foot_length_over_height=foot,
        head_height_over_height=st['chin'], neck_width_over_head_width=neck/head_w,
        upperarm_thickness_over_arm_length=ua/(st['fingertip']-st['acromion']), forearm_thickness_over_forearm_length=fa/(st['wrist']-st['elbow']),
        thigh_thickness_over_leg_length=th/(1-st['hip']), calf_thickness_over_lower_leg_length=ca/(st['ankle']-st['knee']), _stations_t=st)
res={'target':measure(*T_masks())}
a=sys.argv[1:]
for f,j in zip(a[::2],a[1::2]): res[f.split('/')[-1][:-4]]=measure(*M_masks(f,j))
json.dump(res,open(R+'v4/ratios.json','w'),indent=1,default=float)
ks=[k for k in res['target'] if not k.startswith('_')]; names=list(res)
print('| ratio | '+' | '.join(names)+' | v004 / target |'); print('|---|'+'---|'*(len(names)+1))
for k in ks: print('| %s | '%k+' | '.join('%.3f'%res[n][k] for n in names)+' | %.2f |'%(res[names[-1]][k]/res['target'][k]))
for n in names: print(n,{k:round(float(v),3) for k,v in res[n]['_stations_t'].items()})
