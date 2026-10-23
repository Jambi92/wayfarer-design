import numpy as np, sys
from PIL import Image, ImageDraw, ImageFont
R='/tmp/claude-0/rp2/'; D=R+'fin4/'
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26); Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
def crop(a):
    g=np.array(a.convert('L'),int); m=np.abs(g-np.median(g[:3]))>4; ys,xs=np.nonzero(m)
    return a.crop((max(xs.min()-8,0),max(ys.min()-8,0),min(xs.max()+8,a.width),min(ys.max()+8,a.height))) if len(xs) else a
def grid(rows,collabels,rowlabels,cell,title,out):
    rows=[[im.resize((max(1,int(im.width*cell/im.height)),cell)) for im in r] for r in rows]
    cw=[max(r[i].width for r in rows) for i in range(len(collabels))]
    W=230+sum(cw)+10*len(cw); H=90+len(rows)*(cell+12); o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o); d.text((10,10),title,fill='black',font=F)
    x=230
    for i,l in enumerate(collabels): d.text((x+6,54),l,fill='black',font=Fs); x+=cw[i]+10
    for j,r in enumerate(rows):
        y=90+j*(cell+12); d.text((10,y+cell//2),rowlabels[j],fill='black',font=Fs); x=230
        for i,im in enumerate(r): o.paste(im,(x+(cw[i]-im.width)//2,y)); x+=cw[i]+10
    o.save(D+out,quality=90); print(out,o.size)
L=lambda n: Image.open(D+n).convert('RGB')
# A. target vs v004, matched displayed height (figure crown-to-sole)
T=Image.open(R+'v4/target.png').convert('RGB')
tf=T.crop((0,40,440,1410)); tp=T.crop((440,40,700,1410)); tq=T.crop((690,40,1086,1410))
v=[crop(Image.open(R+'v4/r_v004v_%s.png'%k).convert('RGB')) for k in ('front','left','q3r')]
grid([[tf,v[0],tp,v[1],tq,v[2]]],['target front','v004 front','target profile','v004 profile','target 3/4','v004 3/4'],['matched height'],1100,
     'A. Target image vs v004 neutral clay (silhouette and massing comparison; cameras differ, not a pixel match)','sheet_A_target_vs_v004.jpg')
rows2=['v003 (rejected)','v004']; ms=['v003','v004']
grid([[crop(L('b_%s_%s.png'%(m,k))) for k in ('front','left','back','q3')] for m in ms],['front','profile','back','three-quarter'],rows2,900,
     'B. v003 vs v004 whole body — identical cameras, neutral material','sheet_B_v003_vs_v004_body.jpg')
C=[('g','front','neck / shoulder front'),('c','front','chest / ribcage front'),('t','left','torso profile'),('p','front','pelvis / upper thigh'),
   ('a','front','arm / forearm'),('hn','left','hand back'),('hn','right','hand palm'),('k','front','thigh / knee / calf front'),('k','left','thigh / knee / calf profile'),('ft','left','foot side'),('ft','top','foot top')]
grid([[L('%s_%s_%s.png'%(p,m,k)) for p,k,_ in C] for m in ms],[l for _,_,l in C],rows2,330,'C. Body identity carriers — v003 vs v004, identical cameras','sheet_C_body_carriers.jpg')
Dh=[('h','front','head front'),('h','left','head profile'),('h','q3','head 3/4'),('f','front','brow / orbit'),('f','q3','brow / orbit 3/4'),('n','front','nose / midface'),('n','left','nose profile'),('j','left','jaw / chin profile'),('j','q3r','jaw 3/4'),('e','left','ear'),('e','q3','ear 3/4')]
grid([[L('%s_%s_%s.png'%(p,m,k)) for p,k,_ in Dh] for m in ms],[l for _,_,l in Dh],rows2,330,'D. Head — v003 vs v004, identical cameras','sheet_D_head.jpg')
grid([[crop(L('b_v004_%s.png'%k)) for k in ('front','left','back','q3')]],['front','profile','back','three-quarter'],['v004'],1100,
     'E. v004 nude neutral production presentation — chest, abdomen, hips, thighs, shoulders, arms and calves unobscured','sheet_E_presentation.jpg')
