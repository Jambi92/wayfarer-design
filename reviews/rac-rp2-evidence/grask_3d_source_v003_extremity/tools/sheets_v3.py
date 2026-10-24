import numpy as np
from PIL import Image, ImageDraw, ImageFont
R='/tmp/claude-0/src3d/'; D=R+'v3/ev3/'; O=R+'v3/sheets/'
import os; os.makedirs(O,exist_ok=True)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26); Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
def crop(a):
    g=np.array(a.convert('L'),int); m=np.abs(g-np.median(g[:3]))>4; ys,xs=np.nonzero(m)
    return a.crop((max(xs.min()-8,0),max(ys.min()-8,0),min(xs.max()+8,a.width),min(ys.max()+8,a.height))) if len(xs) else a
def grid(rows,collabels,rowlabels,cell,title,out,foot=None):
    rows=[[im.resize((max(1,int(im.width*cell/im.height)),cell)) for im in r] for r in rows]
    cw=[max(r[i].width for r in rows if i<len(r)) for i in range(len(collabels))]
    W=220+sum(cw)+10*len(cw); H=90+len(rows)*(cell+12)+(50 if foot else 0); o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o); d.text((10,10),title,fill='black',font=F)
    x=220
    for i,l in enumerate(collabels): d.text((x+6,54),l,fill='black',font=Fs); x+=cw[i]+10
    for j,r in enumerate(rows):
        y=90+j*(cell+12); d.text((10,y+cell//2),rowlabels[j],fill='black',font=Fs); x=220
        for i,im in enumerate(r): o.paste(im,(x+(cw[i]-im.width)//2,y)); x+=cw[i]+10
    if foot: d.text((10,H-40),foot,fill='black',font=F)
    o.save(O+out,quality=90); print(out,o.size)
L=lambda n: Image.open(D+n+'.png').convert('RGB')
V=('front','left','back','q3','bq3')
grid([[crop(L('v2_b_'+k)) for k in V],[crop(L('v3_b_'+k)) for k in V]],['front','profile','back','3/4 front','3/4 back'],['source v002','source v003'],900,'A. Whole-body regression — v002 vs v003, identical cameras (body frozen; changes confined to hands, feet, eyes)','sheet_A_body_regression_v002_v003.jpg')
H=[('hand_right','palm'),('hand_left','dorsal'),('hand_q3','3/4'),('hand_back','outer / ulnar'),('thumb_q3r','thumb root'),('fside_front','finger side'),('knuck_left','knuckle close-up'),('ftip_left','fingertip close-up')]
grid([[L('v2_'+k) for k,_ in H],[L('v3_'+k) for k,_ in H]],[l for _,l in H],['v002','v003'],380,'B. Hands — v002 vs v003, identical close cameras (left hand)','sheet_B_hands_v002_v003.jpg')
Fo=[('foot_front','top / front'),('foot_left','side outer'),('foot_right','side inner'),('foot_q3','3/4'),('foot_bq3','heel'),('foot_below','sole'),('toe_front','toe close-up'),('toe_q3','toe 3/4'),('nail_top','nail-bed close-up')]
grid([[L('v2_'+k) for k,_ in Fo],[L('v3_'+k) for k,_ in Fo]],[l for _,l in Fo],['v002','v003'],360,'C. Feet — v002 vs v003, identical close cameras (left foot)','sheet_C_feet_v002_v003.jpg')
E=[('earL_left','left ear profile'),('earL_q3','left ear 3/4'),('earL_back','rear attachment'),('earR_right','right ear profile (L/R comparison)')]
grid([[L('v2_'+k) for k,_ in E],[L('v3_'+k) for k,_ in E]],[l for _,l in E],['v002','v003'],420,'D. Ear inspection — v002 vs v003 (no redesign; only generator poke-vertex cleanup, max 0.06 mm)','sheet_D_ears.jpg',foot='EARS PRESERVED — v002 anatomy intentional (helix/antihelix/concha/tragus/lobe; mirrored seam clean). Light differs L/R (studio light).')
Ey=[('face_front','face front'),('face_q3','face 3/4'),('face_left','profile'),('orb_front','orbit close front'),('orb_q3','orbit close 3/4')]
grid([[L('v2_'+k) for k,_ in Ey],[L('v3_'+k) for k,_ in Ey]],[l for _,l in Ey],['v002','v003'],420,'E. Eye / brow inspection — v002 vs v003','sheet_E_eye_brow.jpg',foot='EYE OPENING CORRECTED — GENERATOR COMPRESSION REMOVED (eyeball volume + lid seating restored; fissure kept narrow and stern)')
