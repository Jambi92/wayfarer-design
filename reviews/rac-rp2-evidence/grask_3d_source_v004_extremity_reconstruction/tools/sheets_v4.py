# sheets_v4.py : evidence sheets A-E for source v004 (v003 vs v004, identical cameras)
import json, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
R='/tmp/claude-0/src3d/v4/'; D=R+'ev4/'; O=R+'sheets/'; os.makedirs(O,exist_ok=True)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26); Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
def crop(a):
    g=np.array(a.convert('L'),int); m=np.abs(g-np.median(g[:3]))>4; ys,xs=np.nonzero(m)
    return a.crop((max(xs.min()-8,0),max(ys.min()-8,0),min(xs.max()+8,a.width),min(ys.max()+8,a.height))) if len(xs) else a
def grid(rows,collabels,rowlabels,cell,title,out,foot=None):
    rows=[[im.resize((max(1,int(im.width*cell/im.height)),cell)) for im in r] for r in rows]
    cw=[max(r[i].width for r in rows if i<len(r)) for i in range(len(collabels))]
    W=220+sum(cw)+10*len(cw); H=90+len(rows)*(cell+12)+(50*len(foot) if foot else 0); o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o); d.text((10,10),title,fill='black',font=F)
    x=220
    for i,l in enumerate(collabels): d.text((x+6,54),l,fill='black',font=Fs); x+=cw[i]+10
    for j,r in enumerate(rows):
        y=90+j*(cell+12); d.text((10,y+cell//2),rowlabels[j],fill='black',font=Fs); x=220
        for i,im in enumerate(r): o.paste(im,(x+(cw[i]-im.width)//2,y)); x+=cw[i]+10
    if foot:
        for k,t in enumerate(foot): d.text((10,H-50*len(foot)+10+50*k),t,fill='black',font=Fs)
    o.save(O+out,quality=90); print(out,o.size)
L=lambda n: Image.open(D+n+'.png').convert('RGB')
V=('front','left','back','q3','bq3')
grid([[crop(L('v3_b_'+k)) for k in V],[crop(L('v4_b_'+k)) for k in V]],['front','profile','back','3/4 front','3/4 back'],['source v003','source v004'],900,
 'A. Whole-body regression - v003 vs v004, identical cameras (only hands, fingers, feet, toes rebuilt)','sheet_A_body_v003_v004.jpg')
H=[('hand_right','palm'),('hand_left','dorsal'),('hand_q3','3/4'),('hand_back','outer / ulnar'),('thumbroot_q3r','thumb root'),('thumbprof_front','thumb profile'),('index_front','index side'),
   ('middle_back','middle side'),('mcp_left','MCP row'),('pipdip_left','PIP / DIP'),('tip_q3','fingertip'),('nail_left','fingernail'),('web_left','finger web')]
grid([[L('v3_'+k) for k,_ in H[:7]],[L('v4_'+k) for k,_ in H[:7]]],[l for _,l in H[:7]],['v003','v004'],400,'B1. Hands - v003 vs v004, identical cameras (left hand)','sheet_B1_hands_v003_v004.jpg')
grid([[L('v3_'+k) for k,_ in H[7:]],[L('v4_'+k) for k,_ in H[7:]]],[l for _,l in H[7:]],['v003','v004'],400,'B2. Hand close-ups - v003 vs v004, identical cameras (left hand)','sheet_B2_hand_closeups_v003_v004.jpg')
P=[('relaxed','source pose (relaxed)'),('open','opened flatter'),('fist','fist preview')]
grid([[crop(L('pose_%s_%s'%(q,v))) for v in ('top','front','below')] for q,_ in P],['dorsal','radial side','palmar'],[l for _,l in P],380,
 'B3. Functional sanity - same v004 hand anatomy re-posed (diagnostic SDF re-evaluation, not part of the source)','sheet_B3_hand_pose_check.jpg',
 foot=['Same digit lengths, radii, joints and nails; only joint flex angles changed. Digits open and close without collision or collapse.'])
Fo=[('foot_front','top / front'),('foot_left','outer'),('foot_right','inner'),('foot_q3','3/4'),('foot_bq3','heel'),('foot_below','sole')]
Fc=[('fore_q3','forefoot'),('hallux_q3r','hallux'),('hallux_top','hallux top'),('lesser_front','lesser toes'),('lesser_top','lesser top'),('toeroot_top','toe roots / webs'),('toenail_top','toenail'),('ground_left','ground contact')]
grid([[L('v3_'+k) for k,_ in Fo],[L('v4_'+k) for k,_ in Fo]],[l for _,l in Fo],['v003','v004'],420,'C1. Feet - v003 vs v004, identical cameras (left foot)','sheet_C1_feet_v003_v004.jpg')
grid([[L('v3_'+k) for k,_ in Fc],[L('v4_'+k) for k,_ in Fc]],[l for _,l in Fc],['v003','v004'],380,'C2. Foot close-ups - v003 vs v004, identical cameras','sheet_C2_foot_closeups_v003_v004.jpg')
st=json.load(open(R+'w/freeze_stats.json'))
Hd=[('head_front','face front'),('head_left','profile (ear)'),('head_q3','3/4')]
lines=['Freeze proof - closest-point distance v004 -> v003 surface (mm):']
for k in ('head_face','eyes','ears','torso_pelvis_back','arms_above_wrist','legs_above_forefoot','rest_all','hand_L','hand_R','foot_L','foot_R'):
    s=st[k]; lines.append('  %-22s verts %7d   max %7.3f   p95 %7.3f'%(k,s['v004_verts'],s['v004_to_v003_max_mm'],s['v004_to_v003_p95_mm']))
grid([[L('v3_'+k) for k,_ in Hd],[L('v4_'+k) for k,_ in Hd]],[l for _,l in Hd],['v003','v004'],520,'E. Freeze proof - head, face, eyes, ears unchanged (identical cameras) + regional movement','sheet_E_freeze_proof.jpg',foot=lines)
