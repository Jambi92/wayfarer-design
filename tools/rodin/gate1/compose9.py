import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json, numpy as np
G='/tmp/claude-0/rodin/g1/'; O=G+'sheets9/'; A=json.load(open(G+'acct9.json')); T=" — GATE 6 CLOSURE VERIFICATION"
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def grid(views,title,sub,out,tags,cell=520,lw=240):
    W=lw+len(views)*(cell+16); top=100+30*len(sub); img=Image.new('RGB',(W,top+len(tags)*(cell+16)+20),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(30,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,62+30*i),s,font=F(20),fill=SUB)
    for r,(lab,tag) in enumerate(tags):
        y=top+r*(cell+16); d.multiline_text((20,y+cell//2-30),lab,font=F(24,True),fill=TXT,spacing=8)
        for c,(v,vl) in enumerate(views):
            x=lw+c*(cell+16); img.paste(tile(G+'%s_%s.png'%(tag,v),cell),(x,y))
            if r==0: d.text((x+6,y-28),vl,font=F(19,True),fill=SUB)
    img.save(out,quality=88)
TG=(('Pass 3\n(before)','E8'),('Closure\n(final)','E9')); g=A['_global']
grid(VIEWS,"Saurin Gate 6 — whole organism, Pass 3 vs closure"+T,
 ["Head frozen at +8 % (uniform, cranial-roof pivot). Posterior pelvis: caudofemoral mass redistributed into longer, lower directional slips; hip nub removed. Nothing else changed.",
  "Height %.2f cm, width %.2f cm, depth %.2f cm — identical to Pass 3."%(g['height'][0],g['width_x'][0],g['depth_f'][0])],O+'g6c_01_whole_organism.jpg',TG,cell=500)
grid([('pR','Rear'),('pP','Profile'),('pR34','Rear 3/4'),('pLow','Low rear 3/4'),('pUnd','Underside')],
 "Saurin Gate 6 — pelvis / tail root"+T,["Caudofemoral longus now two longer tensioned slips (dorsal + ventral) plus a flattened brevis, still running caudal base → posterior proximal femur; paired rounded rear masses reduced.",
 "Iliofemoral rim re-seated behind the hip-stabiliser origin; the measured hip nubs (±17, −14, 91.5) smoothed. Sacral volume, tail root taper, neutral pelvic floor unchanged."],O+'g6c_02_pelvis_tail_root.jpg',TG,cell=520)
grid([('hF','Front'),('hP','Profile'),('hF34','Front 3/4'),('hR34','Rear 3/4')],
 "Saurin Gate 6 — naked head, +6 % (Pass 3) vs +8 % (frozen)"+T,["Same Pass 3 skull; only the uniform scale changes (rostrum : cranium unchanged, skull top fixed). No horns, crests or display."],O+'g6c_03_head.jpg',TG,cell=560)
cell=600; img=Image.new('RGB',(20+5*(cell+20),cell+230),(236,236,240)); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin Gate 6 — silhouette, Pass 3 vs closure"+T,font=F(30,True),fill=(20,20,26))
d.text((20,62),"Dark: closure. Red: Pass 3 only. Blue: closure only. (Differences are confined to the head outline and are barely visible at this scale.)",font=F(20),fill=(60,60,70))
for i,(v,vl) in enumerate(VIEWS):
    a5=np.array(Image.open(G+'E8_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    a6=np.array(Image.open(G+'E9_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    rgb=np.full((cell,cell,3),236,np.uint8); rgb[a6]=(40,42,50); rgb[a5&~a6]=(220,60,50); rgb[a6&~a5]=(60,110,230)
    x=20+i*(cell+20); img.paste(Image.fromarray(rgb),(x,120)); d.text((x+6,92),vl,font=F(22,True),fill=(60,60,70))
img.save(O+'g6c_04_silhouette.jpg',quality=90)
e=A['EVERYTHING ELSE']; h=A['head-scale region (head + upper neck)']; p=A['posterior-pelvic closure region']
img=strip(G+'AC9',"Saurin Gate 6 closure accounting — deviation of every vertex from Pass 3",
 ["Everything outside the head-scale and posterior-pelvic regions: %d of %d vertices bit-identical, max change %.1f mm. Head region max %.1f mm; pelvic closure region max %.1f mm."%(e['identical'],e['verts'],e['max_mm'],h['max_mm'],p['max_mm']),
  "Green < 1 mm, amber 1–5 mm, red > 5 mm."],O+'g6c_05_accounting.jpg')
cell=760; rowi=Image.new('RGB',(img.width,cell+40),BG)
for i,pp in enumerate((G+'AC9_hF34.png',G+'AC9_pR34.png',G+'AC9_pLow.png')): rowi.paste(tile(pp,cell),(20+i*(cell+20),20))
leg=Image.new('RGB',(img.width,80),BG); d=ImageDraw.Draw(leg); x=20
for lab,c in (("< 1 mm from Pass 3",COL["PRESERVE"]),("1–5 mm",COL["MODIFY"]),("> 5 mm",COL["REBUILD"])):
    d.rectangle((x,22,x+34,56),fill=c); d.text((x+46,26),lab,font=F(21,True),fill=TXT); x+=46+d.textlength(lab,font=F(21,True))+50
out=Image.new('RGB',(img.width,img.height+rowi.height+leg.height),BG); out.paste(img,(0,0)); out.paste(rowi,(0,img.height)); out.paste(leg,(0,img.height+rowi.height)); out.save(O+'g6c_05_accounting.jpg',quality=88)
print('ok')
