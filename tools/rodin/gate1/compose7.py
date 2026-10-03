import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json, numpy as np
G='/tmp/claude-0/rodin/g1/'; O=G+'sheets7/'; A=json.load(open(G+'acct7.json')); T=" — DIAGNOSTIC / NOT FINAL"
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def pair(views,title,sub,out,tags=(('Pass 1\n(before)','E6'),('Pass 2\n(after)','E7')),cell=560):
    W=240+len(views)*(cell+16); top=100+30*len(sub); img=Image.new('RGB',(W,top+len(tags)*(cell+16)+20),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(30,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,62+30*i),s,font=F(20),fill=SUB)
    for r,(lab,tag) in enumerate(tags):
        y=top+r*(cell+16); d.multiline_text((20,y+cell//2-30),lab,font=F(24,True),fill=TXT,spacing=8)
        for c,(v,vl) in enumerate(views):
            x=240+c*(cell+16); img.paste(tile(G+'%s_%s.png'%(tag,v),cell),(x,y))
            if r==0: d.text((x+6,y-28),vl,font=F(19,True),fill=SUB)
    img.save(out,quality=88)
g=A['_global']
pair(VIEWS,"Gate 6 Pass 2 — whole body, Pass 1 vs Pass 2, identical cameras"+T,
 ["Pass 2: posterior pelvic volume rebuilt; proximal tail re-curved 20° (exact-length bend, not shortened); head +6 %% (scaled about the skull roof, height unchanged %.1f cm); skull refined; upper-arm/thigh bellies redistributed."%g['height'][0],
  "Depth grows %.1f → %.1f cm because the same-length tail now extends back as a counterbalance instead of hanging between the legs."%(g['depth_f'][1],g['depth_f'][0])],O+'g6p2_01_whole_body.jpg',cell=520)
pair([('pF','Front'),('pR','Rear'),('pP','Profile'),('pR34','Rear 3/4'),('pF34','Front 3/4'),('pLow','Low rear 3/4'),('pUnd','Underside')],
 "Gate 6 Pass 2 — pelvis / tail root"+T,
 ["Rebuilt VOLUME, not bands: one continuous sacral-caudal wedge (±17 cm at the sacrum → tail section by F −56), dorsally flattened, ventrally kept above the neutral pelvic floor; caudofemoral / iliocaudal masses from Pass 1 now sit on it.",
  "Tail root is materially wider than the free tail and tapers gradually into it. No buttock pair, no cleft, no crotch mass."],O+'g6p2_02_pelvis_tail_root.jpg',cell=470)
pair([('tailP','Tail profile'),('thF','Between the legs, front'),('front','Full front'),('rear34','Full rear 3/4')],
 "Gate 6 Pass 2 — proximal free-tail re-curve"+T,["Bend about the tail root (F −26, U 92): 0° at the root rising to 20° by ~30 cm, rigid beyond; length preserved exactly. The tail now reads as a counterbalance; it no longer hangs centrally between the legs."],O+'g6p2_03_tail_recurve.jpg',cell=560)
# head-scale comparison (whole-body composites, Pass 1 body)
names=[('front','Front'),('profile','Profile'),('front34','Front 3/4'),('up','Head on shoulders'),('upP','Head on shoulders, profile')]
cell=470; W=200+len(names)*(cell+16); img=Image.new('RGB',(W,160+3*(cell+16)),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Gate 6 Pass 2 — head-scale comparison in whole-body context: +0 % / +6 % / +9 %"+T,font=F(30,True),fill=TXT)
d.text((20,62),"Identical cameras. Scale about the skull roof, so standing height is unchanged and rostrum : cranium proportions are exact. +6 % adopted per directive; +9 % shown for comparison only.",font=F(20),fill=SUB)
d.text((20,92),"Diagnostic composites: Pass 1 body below U 155 + each head (small cut marks at the shoulders are the composite seam, not the model).",font=F(20),fill=SUB)
for r,(lab,sc) in enumerate((('+0 %','1.00'),('+6 %','1.06'),('+9 %','1.09'))):
    y=140+r*(cell+16); d.text((20,y+cell//2-14),lab,font=F(28,True),fill=TXT)
    for c,(v,vl) in enumerate(names):
        x=200+c*(cell+16); img.paste(tile(G+'HS%s_%s.png'%(sc,v),cell),(x,y))
        if r==0: d.text((x+6,y-26),vl,font=F(18,True),fill=SUB)
img.save(O+'g6p2_04_head_scale.jpg',quality=88)
pair([('hF','Front'),('hP','Profile'),('hR','Rear'),('hF34','Front 3/4'),('hR34','Rear 3/4'),('hT','Top'),('hU','Underside')],
 "Gate 6 Pass 2 — naked skull at +6 %"+T,["Stronger orbital-temporal organisation (temporal line, postorbital bar, deeper supratemporal fossa); sharper canthal / jugal / maxillary plane breaks; firmer occipital ridge and nuchal crest into the neck.",
 "Compact projecting rostrum kept; no frog domes, no horns/crests/display."],O+'g6p2_05_skull.jpg',cell=470)
pair([('shF','Shoulder front'),('shF34','Shoulder 3/4'),('shR34','Shoulder rear 3/4'),('thR34','Thigh rear 3/4'),('lP','Leg profile'),('lR','Legs rear')],
 "Gate 6 Pass 2 — shoulder / arm and hindlimb integration"+T,["Upper arm and thigh: 45–50 % mix toward a 3.5 cm low-pass of their own surface removes the biceps/triceps and quad-belly read, with a 2.5 mm outward offset so girth and strength are kept.",
 "Elbow, forearm, hand, knee, lower leg and foot unchanged."],O+'g6p2_06_limbs.jpg',cell=500)
# silhouette
cell=600; img=Image.new('RGB',(20+5*(cell+20),cell+230),(236,236,240)); d=ImageDraw.Draw(img)
d.text((20,16),"Gate 6 Pass 2 — silhouette comparison"+T,font=F(30,True),fill=(20,20,26))
d.text((20,62),"Dark: Pass 2. Red: Pass 1 only (removed). Blue: Pass 2 only (added).",font=F(20),fill=(60,60,70))
for i,(v,vl) in enumerate(VIEWS):
    a5=np.array(Image.open(G+'E6_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    a6=np.array(Image.open(G+'E7_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    rgb=np.full((cell,cell,3),236,np.uint8); rgb[a6]=(40,42,50); rgb[a5&~a6]=(220,60,50); rgb[a6&~a5]=(60,110,230)
    x=20+i*(cell+20); img.paste(Image.fromarray(rgb),(x,120)); d.text((x+6,92),vl,font=F(22,True),fill=(60,60,70))
img.save(O+'g6p2_07_silhouette.jpg',quality=90)
img=strip(G+'AC7',"Gate 6 Pass 2 accounting — deviation of every vertex from the Pass 1 surface",
 ["Green < 1 mm (unchanged), amber 1–5 mm, red > 5 mm (rebuilt / moved). Feet and lower legs unchanged; forearms and hands unchanged.",
  "Free tail moves as a rigid-length bend (median %.0f cm, tip %.0f cm). %d of %d vertices are exact Pass 1 copies."%(A['free tail (F < -45; re-curved)']['median_cm'],A['free tail (F < -45; re-curved)']['max_cm'],g['identical_copies'],g['verts'])],O+'g6p2_08_accounting.jpg')
cell=760; rowi=Image.new('RGB',(img.width,cell+40),BG)
for i,p in enumerate((G+'AC7_hF34.png',G+'AC7_pR34.png',G+'AC7_tailP.png')): rowi.paste(tile(p,cell),(20+i*(cell+20),20))
leg=Image.new('RGB',(img.width,80),BG); d=ImageDraw.Draw(leg); x=20
for lab,c in (("< 1 mm from Pass 1",COL["PRESERVE"]),("1–5 mm",COL["MODIFY"]),("> 5 mm",COL["REBUILD"])):
    d.rectangle((x,22,x+34,56),fill=c); d.text((x+46,26),lab,font=F(21,True),fill=TXT); x+=46+d.textlength(lab,font=F(21,True))+50
out=Image.new('RGB',(img.width,img.height+rowi.height+leg.height),BG); out.paste(img,(0,0)); out.paste(rowi,(0,img.height)); out.paste(leg,(0,img.height+rowi.height)); out.save(O+'g6p2_08_accounting.jpg',quality=88)
print('ok')
