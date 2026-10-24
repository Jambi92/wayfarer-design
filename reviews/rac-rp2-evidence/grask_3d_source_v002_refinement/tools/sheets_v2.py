import numpy as np
from PIL import Image, ImageDraw, ImageFont
R='/tmp/claude-0/src3d/'; D=R+'v2/ev/'; O=R+'v2/sheets/'
import os; os.makedirs(O,exist_ok=True)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26); Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
def crop(a):
    g=np.array(a.convert('L'),int); m=np.abs(g-np.median(g[:3]))>4; ys,xs=np.nonzero(m)
    return a.crop((max(xs.min()-8,0),max(ys.min()-8,0),min(xs.max()+8,a.width),min(ys.max()+8,a.height))) if len(xs) else a
def grid(rows,collabels,rowlabels,cell,title,out):
    rows=[[im.resize((max(1,int(im.width*cell/im.height)),cell)) for im in r] for r in rows]
    cw=[max(r[i].width for r in rows if i<len(r)) for i in range(len(collabels))]
    W=220+sum(cw)+10*len(cw); H=90+len(rows)*(cell+12); o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o); d.text((10,10),title,fill='black',font=F)
    x=220
    for i,l in enumerate(collabels): d.text((x+6,54),l,fill='black',font=Fs); x+=cw[i]+10
    for j,r in enumerate(rows):
        y=90+j*(cell+12); d.text((10,y+cell//2),rowlabels[j],fill='black',font=Fs); x=220
        for i,im in enumerate(r): o.paste(im,(x+(cw[i]-im.width)//2,y)); x+=cw[i]+10
    o.save(O+out,quality=90); print(out,o.size)
L=lambda n: Image.open(D+n+'.png').convert('RGB')
grid([[crop(L('v2_b_'+k)) for k in ('front','left','back','q3','q3r','bq3')]],['front','left profile','back','three-quarter front L','three-quarter front R','three-quarter back'],['source v002'],1000,'A. Grask 3D anatomical source v002 — neutral clay turnaround, 218 cm','sheet_A_v002_turnaround.jpg')
T=Image.open(R+'in/turnaround.png').convert('RGB'); figs=[T.crop((0,40,440,1410)),T.crop((440,40,700,1410)),T.crop((690,40,1086,1410))]
v=[crop(L('v2_b_'+k)) for k in ('front','left','q3r')]; row=[]
for t,m in zip(figs,v): row+=[t,m]
grid([row],['target front','v002 front','target profile','v002 profile','target 3/4','v002 3/4'],['matched height'],1100,'B. Target turnaround vs 3D anatomical source v002 (neutral clay)','sheet_B_target_vs_v002.jpg')
C1=[('face_front','face front'),('face_left','face profile'),('face_q3','face 3/4'),('ear_left','ear profile'),('ear_q3','ear 3/4'),('ear_back','ear from behind')]
grid([[L('v2_'+k) for k,_ in C1]],[l for _,l in C1],['v002'],420,'C1. Face and ears (left ear = mirrored copy of the anatomically complete right ear)','sheet_C1_face_ears.jpg')
CH=[('hand_right','palm / front'),('hand_left','dorsal / back'),('hand_back','outer (ulnar)'),('hand_q3','3/4'),('thumb_q3r','thumb root close-up'),('thumb_front','thumb root front')]
CF=[('ffront_front','front'),('foot_left','side (outer)'),('foot_right','side (inner)'),('foot_q3','3/4'),('foot_bq3','heel'),('foot_below','sole'),('toe_front','toe close-up'),('toe_q3r','toe close-up 3/4')]
grid([[L('v2_'+k) for k,_ in CH]],[l for _,l in CH],['hand'],380,'C2a. Hands (left hand shown; isolated for clear views)','sheet_C2a_hands.jpg')
grid([[L('v2_'+k) for k,_ in CF]],[l for _,l in CF],['foot'],340,'C2b. Feet (left foot shown; isolated for clear views)','sheet_C2b_feet.jpg')
C3=[('neck_front','neck/shoulders'),('neck_q3','neck/shoulders 3/4'),('chest_front','chest/ribcage front'),('tprof_left','torso profile'),('uback_back','upper back'),('uback_bq3','back 3/4'),('pelv_front','pelvis front'),('pelv_left','pelvis profile'),('pelv_bq3','glute 3/4'),('thigh_q3','upper thigh'),('calf_front','calf/ankle front'),('calf_left','calf/ankle profile')]
grid([[L('v2_'+k) for k,_ in C3]],[l for _,l in C3],['v002'],330,'C3. Body detail','sheet_C3_body_details.jpg')
grid([[crop(L('v1_b_'+k)) for k in ('front','left','back','q3')],[crop(L('v2_b_'+k)) for k in ('front','left','back','q3')]],['front','profile','back','three-quarter'],['source v001','source v002'],900,'D. v001 vs v002 — identical cameras','sheet_D_v001_vs_v002.jpg')
ks=['face_front','face_q3','ear_left','hand_left','hand_q3','foot_q3','foot_left','tprof_left','uback_back','pelv_left','pelv_bq3']
grid([[L('v1_'+k) for k in ks],[L('v2_'+k) for k in ks]],['face','face 3/4','ear (left)','hand dorsal','hand 3/4','foot 3/4','foot side','torso profile','upper back','pelvis profile','glute 3/4'],['v001','v002'],320,'D2. v001 vs v002 — refinement close-ups, identical cameras','sheet_D2_v001_vs_v002_details.jpg')
