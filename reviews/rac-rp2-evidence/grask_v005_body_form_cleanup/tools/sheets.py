import numpy as np
from PIL import Image, ImageDraw, ImageFont
R='/tmp/claude-0/rp2/'; D=R+'fin5/'; O=R+'fin5s/'
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26); Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
def crop(a):
    g=np.array(a.convert('L'),int); m=np.abs(g-np.median(g[:3]))>4; ys,xs=np.nonzero(m)
    return a.crop((max(xs.min()-8,0),max(ys.min()-8,0),min(xs.max()+8,a.width),min(ys.max()+8,a.height))) if len(xs) else a
def grid(rows,collabels,rowlabels,cell,title,out):
    rows=[[im.resize((max(1,int(im.width*cell/im.height)),cell)) for im in r] for r in rows]
    cw=[max(r[i].width for r in rows) for i in range(len(collabels))]
    W=200+sum(cw)+10*len(cw); H=90+len(rows)*(cell+12); o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o); d.text((10,10),title,fill='black',font=F)
    x=200
    for i,l in enumerate(collabels): d.text((x+6,54),l,fill='black',font=Fs); x+=cw[i]+10
    for j,r in enumerate(rows):
        y=90+j*(cell+12); d.text((10,y+cell//2),rowlabels[j],fill='black',font=Fs); x=200
        for i,im in enumerate(r): o.paste(im,(x+(cw[i]-im.width)//2,y)); x+=cw[i]+10
    o.save(O+out,quality=90); print(out,o.size)
L=lambda n: Image.open(D+n).convert('RGB')
ms=[('v004','v004'),('v5q','v005')]; rl=['v004 (not accepted)','v005']
grid([[crop(L('b_%s_%s.png'%(m,k))) for k in ('front','left','back','q3')] for m,_ in ms],['front','profile','back','three-quarter'],rl,900,'A. v004 vs v005 whole body — identical cameras, neutral material','sheet_A_v004_vs_v005_body.jpg')
T=Image.open(R+'v4/target.png').convert('RGB'); tf=T.crop((0,40,440,1410)); tp=T.crop((440,40,700,1410)); tq=T.crop((690,40,1086,1410))
v=[crop(Image.open(R+'v4/r_v5q_%s.png'%k).convert('RGB')) for k in ('front','left','q3r')]
grid([[tf,v[0],tp,v[1],tq,v[2]]],['target front','v005 front','target profile','v005 profile','target 3/4','v005 3/4'],['matched height'],1100,'B. Target image vs v005 neutral clay (shape-language comparison; cameras differ)','sheet_B_target_vs_v005.jpg')
C=[('th','front','upper thighs front'),('th','q3','upper thighs 3/4'),('tp','left','thigh profile'),('ch','front','chest front'),('ch','q3','chest 3/4'),('bb','back','mid-back'),('bb','bq3','back 3/4'),('am','front','upper arm front'),('am','q3r','upper arm 3/4'),('fa','left','forearm profile'),('ab','left','abdomen profile'),('gp','left','pelvis / glute profile')]
grid([[L('%s_%s_%s.png'%(p,m,k)) for p,k,_ in C] for m,_ in ms],[l for _,_,l in C],rl,330,'C. Mandatory close-ups — v004 vs v005, identical cameras','sheet_C_closeups.jpg')
Dh=[('hd','front','head front'),('hd','left','head profile'),('hd','q3','head 3/4'),('nk','front','neck / shoulder front'),('nk','left','neck / shoulder profile')]
grid([[L('%s_%s_%s.png'%(p,m,k)) for p,k,_ in Dh] for m,_ in ms],[l for _,_,l in Dh],rl,420,'D. Head / neck balance (head +5 % breadth/depth, +4 % height downward from the crown)','sheet_D_head_neck.jpg')
