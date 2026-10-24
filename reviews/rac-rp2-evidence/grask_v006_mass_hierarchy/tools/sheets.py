import numpy as np
from PIL import Image, ImageDraw, ImageFont
R='/tmp/claude-0/rp2/'; D=R+'fin6/'; O=R+'fin6s/'
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
T=Image.open(R+'v4/target.png').convert('RGB'); tf=T.crop((0,40,440,1410)); tp=T.crop((440,40,700,1410)); tq=T.crop((690,40,1086,1410))
v=[crop(Image.open(R+'v4/r_v006_%s.png'%k).convert('RGB')) for k in ('front','left','q3r')]
grid([[tf,v[0],tp,v[1],tq,v[2]]],['target front','v006 front','target profile','v006 profile','target 3/4','v006 3/4'],['matched height'],1100,'A. Target image vs v006 neutral clay (mass-hierarchy comparison; cameras differ)','sheet_A_target_vs_v006.jpg')
ms=['v005','v006']; rl=['v005 (not accepted)','v006']
grid([[crop(L('b_%s_%s.png'%(m,k))) for k in ('front','left','back','q3')] for m in ms],['front','profile','back','three-quarter'],rl,900,'B. v005 vs v006 whole body — identical cameras, neutral material','sheet_B_v005_vs_v006_body.jpg')
C=[('hn','front','head/neck front'),('hn','left','head/neck profile'),('sc','front','shoulder/chest front'),('sc','q3','shoulder/chest 3/4'),('tp','left','torso profile'),('pv','front','pelvis front'),('pv','left','pelvis profile'),('th','front','thigh front'),('th','q3','thigh 3/4'),('cf','front','calf front'),('cf','left','calf profile'),('am','front','arm front'),('am','q3r','arm 3/4'),('ft','top','foot top'),('ft','left','foot profile')]
grid([[L('%s_%s_%s.png'%(p,m,k)) for p,k,_ in C] for m in ms],[l for _,_,l in C],rl,300,'C. Mass-hierarchy close-ups — v005 vs v006, identical cameras','sheet_C_mass_hierarchy_closeups.jpg')
sf=Image.open(R+'g6/silhouette_v006_front.png'); sp=Image.open(R+'g6/silhouette_v006_profile.png')
s5f=Image.open(R+'g6/silhouette_v005_front.png'); s5p=Image.open(R+'g6/silhouette_v005_profile.png')
grid([[s5f,s5p],[sf,sp]],['front (red = target only, blue = mesh only, grey = both)','profile (mirrored to face left; aligned at the calf)'],['v005 vs target','v006 vs target'],900,'D. Normalized silhouette study — target vs mesh at equal displayed height','sheet_D_silhouette_study.jpg')
