import numpy as np
from PIL import Image, ImageDraw, ImageFont
R='/tmp/claude-0/src3d/'; D=R+'fin/'; O=R+'sheets/'
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
grid([[crop(L('b_'+k)) for k in ('front','left','back','q3')]+[crop(L('b_q3r_q3r')),crop(L('b_bq3'))]],['front','left profile','back','three-quarter front (L)','three-quarter front (R)','three-quarter back'],['source v001'],1000,'A. Grask 3D anatomical source v001 — neutral clay, 218 cm','sheet_A_source_views.jpg')
T=Image.open('/tmp/claude-0/src3d/in/turnaround.png').convert('RGB'); W_,H_=T.size
# split the turnaround into its three figures by column gaps
g=np.array(T.convert('L'),int); bg=np.median(g[:5]); col=(np.abs(g-bg)>18).sum(0); occ=col>5
runs=[]; i=0
while i<len(occ):
    if occ[i]:
        j=i
        while j<len(occ) and occ[j]: j+=1
        if j-i>40: runs.append((i,j))
        i=j
    else: i+=1
figs=[T.crop((0,40,440,1410)),T.crop((440,40,700,1410)),T.crop((690,40,1086,1410))]
print('turnaround figures',runs[:3])
v=[crop(L('r_'+k)) for k in ('front','left','q3r')]
row=[]
for t,m in zip(figs,v): row+= [t,m]
grid([row],['target front','source front','target profile','source profile','target 3/4','source 3/4'][:len(row)],['matched height'],1100,'B. Target turnaround vs 3D anatomical source (neutral clay; generated from the same turnaround)','sheet_B_target_vs_source.jpg')
C1=[('face_front','face front'),('face_left','face profile'),('face_q3','face 3/4'),('ear_left','ear'),('ear_q3','ear 3/4'),('ear_back','ear from behind')]
C2=[('hand_front','hand front'),('hand_q3','hand 3/4'),('hand_left','hand outer'),('hand_back','hand back view'),('foot_front','foot front'),('foot_left','foot side'),('foot_q3','foot 3/4'),('foot_bq3','heel 3/4'),('foot_below','sole')]
C3=[('neck_front','neck/shoulders front'),('neck_q3','neck/shoulders 3/4'),('neck_left','neck profile'),('chest_front','chest/ribcage front'),('chest_q3','chest 3/4'),('pelvis_front','pelvis/thigh front'),('pelvis_left','pelvis profile'),('pelvis_bq3','pelvis back 3/4'),('pelvis_back','pelvis back'),('calf_front','calf/ankle front'),('calf_left','calf/ankle profile')]
grid([[L(k) for k,_ in C1]],[l for _,l in C1],['head'],420,'C1. Detail — face and ears','sheet_C1_face_ears.jpg')
grid([[L(k) for k,_ in C2]],[l for _,l in C2],['extremities'],360,'C2. Detail — hands and feet','sheet_C2_hands_feet.jpg')
grid([[L(k) for k,_ in C3]],[l for _,l in C3],['body'],330,'C3. Detail — neck/shoulders, chest, pelvis/thigh (reconstructed under the loincloth), calf/ankle','sheet_C3_body_details.jpg')
grid([[crop(L('v006_'+k)) for k in ('front','left','q3')],[crop(L('b_'+k)) for k in ('front','left','q3')]],['front','profile','three-quarter'],['v006 (superseded)','3D source v001'],900,'D. Historical comparison — v006 production morphology vs the new 3D anatomical source','sheet_D_v006_vs_source.jpg')
