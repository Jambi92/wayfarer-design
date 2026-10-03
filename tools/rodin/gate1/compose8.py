import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json, numpy as np
G='/tmp/claude-0/rodin/g1/'; O=G+'sheets8/'; A=json.load(open(G+'acct8.json')); T=" — DIAGNOSTIC / NOT FINAL"
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
P23=(('Pass 2\n(before)','E7'),('Pass 3\n(after)','E8')); g=A['_global']
grid(VIEWS+[('pLow','Low rear 3/4')],"Gate 6 Pass 3 — whole organism, Pass 2 vs Pass 3, identical cameras"+T,
 ["Tail: same length and rearward counterbalance; bend ramp lengthened (0° → 22° over ~62 cm) so root-to-tail curvature is continuous. Sacral volume narrowed (±17 → ±15 cm) and carried by iliosacral / caudofemoral / iliofemoral load paths.",
  "Naked skull refined (front view). Head +6 %% (control). Height %.1f cm, width %.1f cm unchanged; depth %.1f cm."%(g['height'][0],g['width_x'][0],g['depth_f'][0])],O+'g6p3_01_whole_organism.jpg',P23,cell=440)
grid([('pF','Front'),('pR','Rear'),('pP','Profile'),('pR34','Rear 3/4'),('pF34','Front 3/4'),('pLow','Low rear 3/4'),('pUnd','Underside'),('tailP','Tail profile')],
 "Gate 6 Pass 3 — pelvis / tail root"+T,
 ["The Pass 2 'shield' is now load-path architecture: iliosacral bands (ilium → sacrum → dorsal tail), caudofemoral longus (tail → posterior femur) and brevis, an iliofemoral rim onto the hip, and a low sacral/caudal neural-spine line.",
  "Narrower sacral station (±15 cm) — tail base still clearly wider than the free tail. No buttock pair, no cleft, no crotch mass. Tail curvature continuous (no kink)."],O+'g6p3_02_pelvis_tail_root.jpg',P23,cell=410)
grid([('hF','Front'),('hP','Profile'),('hF34','Front 3/4'),('hR34','Rear 3/4'),('hT','Top'),('hU','Underside'),('hR','Rear')],
 "Gate 6 Pass 3 — naked skull multi-view (at +6 %)"+T,
 ["Front: brow shelf overhangs the orbit laterally; postorbital bar and jugal flare outward (triangular orbital-temporal front read); slimmer rostral tip with dorsolateral nares; smaller premaxillary pad.",
  "Jugal arch now sweeps into the quadrate/hinge (its free end had read as an ear knob); auricular cup removed; flat temporal-plane cut removed; occiput lowered into the nuchal mass. Profile kept. No horns/crests/display."],O+'g6p3_03_skull.jpg',P23,cell=440)
# head-scale convergence (refined skull): +6 control = built body; +8/+9 = same body with the head region re-meshed at that scale
names=[('front','Front'),('profile','Profile'),('front34','Front 3/4'),('rear34','Rear 3/4'),('up','Head on thorax'),('upP','Head on thorax, profile')]
cell=430; W=200+len(names)*(cell+16); img=Image.new('RGB',(W,170+3*(cell+16)),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Gate 6 Pass 3 — head-scale convergence with the refined skull: +6 % / +8 % / +9 %"+T,font=F(30,True),fill=TXT)
d.text((20,62),"Identical cameras. Uniform scale about the cranial-roof pivot: standing height unchanged, rostrum : cranium unchanged, no independent snout scaling. No value is chosen here.",font=F(20),fill=SUB)
d.text((20,92),"+6 % row = the built Pass 3 mesh. +8 / +9 % rows = the same body with the head/neck above U 161 re-meshed at that scale (diagnostic splice above the shoulders).",font=F(20),fill=SUB)
for r,(lab,tag) in enumerate((('+6 %\n(control)','S106'),('+8 %','S108'),('+9 %','S109'))):
    y=150+r*(cell+16); d.multiline_text((20,y+cell//2-30),lab,font=F(26,True),fill=TXT,spacing=8)
    for c,(v,vl) in enumerate(names):
        x=200+c*(cell+16); img.paste(tile(G+'%s_%s.png'%(tag,v),cell),(x,y))
        if r==0: d.text((x+6,y-26),vl,font=F(18,True),fill=SUB)
img.save(O+'g6p3_04_head_scale.jpg',quality=88)
grid([('shF','Shoulder front'),('shF34','Shoulder 3/4'),('shR34','Shoulder rear 3/4'),('thR34','Thigh rear 3/4'),('lP','Leg profile'),('lR','Legs rear')],
 "Gate 6 Pass 3 — limbs (unchanged from Pass 2; integration check)"+T,["Pass 2 upper-arm / thigh redistribution kept. Caudofemoral paths now insert on the posterior proximal femur, tying thigh to tail."],O+'g6p3_05_limbs.jpg',P23,cell=440)
cell=600; img=Image.new('RGB',(20+5*(cell+20),cell+230),(236,236,240)); d=ImageDraw.Draw(img)
d.text((20,16),"Gate 6 Pass 3 — silhouette vs Pass 2"+T,font=F(30,True),fill=(20,20,26))
d.text((20,62),"Dark: Pass 3. Red: Pass 2 only (removed). Blue: Pass 3 only (added).",font=F(20),fill=(60,60,70))
for i,(v,vl) in enumerate(VIEWS):
    a5=np.array(Image.open(G+'E7_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    a6=np.array(Image.open(G+'E8_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    rgb=np.full((cell,cell,3),236,np.uint8); rgb[a6]=(40,42,50); rgb[a5&~a6]=(220,60,50); rgb[a6&~a5]=(60,110,230)
    x=20+i*(cell+20); img.paste(Image.fromarray(rgb),(x,120)); d.text((x+6,92),vl,font=F(22,True),fill=(60,60,70))
img.save(O+'g6p3_06_silhouette.jpg',quality=90)
img=strip(G+'AC8',"Gate 6 Pass 3 accounting — deviation of every vertex from the Pass 2 surface",
 ["Green < 1 mm, amber 1–5 mm, red > 5 mm. Feet, lower legs, forearms and hands unchanged.","%d of %d vertices are exact Pass 2 copies. Height %.2f cm (Pass 2 %.2f)."%(g['identical_copies'],g['verts'],g['height'][0],g['height'][1])],O+'g6p3_07_accounting.jpg')
cell=760; rowi=Image.new('RGB',(img.width,cell+40),BG)
for i,p in enumerate((G+'AC8_hF34.png',G+'AC8_pR34.png',G+'AC8_tailP.png')): rowi.paste(tile(p,cell),(20+i*(cell+20),20))
leg=Image.new('RGB',(img.width,80),BG); d=ImageDraw.Draw(leg); x=20
for lab,c in (("< 1 mm from Pass 2",COL["PRESERVE"]),("1–5 mm",COL["MODIFY"]),("> 5 mm",COL["REBUILD"])):
    d.rectangle((x,22,x+34,56),fill=c); d.text((x+46,26),lab,font=F(21,True),fill=TXT); x+=46+d.textlength(lab,font=F(21,True))+50
out=Image.new('RGB',(img.width,img.height+rowi.height+leg.height),BG); out.paste(img,(0,0)); out.paste(rowi,(0,img.height)); out.paste(leg,(0,img.height+rowi.height)); out.save(O+'g6p3_07_accounting.jpg',quality=88)
print('ok')
