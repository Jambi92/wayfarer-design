import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json, numpy as np
G='/tmp/claude-0/rodin/g1/'; O=G+'sheets6/'; A=json.load(open(G+'acct6.json')); T=" — DIAGNOSTIC / NOT FINAL"
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def row(items,title,sub,out,cell=700):
    W=20+len(items)*(cell+20); top=100+30*len(sub); img=Image.new('RGB',(W,top+cell+30),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(30,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,62+30*i),s,font=F(20),fill=SUB)
    for i,(p,lab) in enumerate(items):
        x=20+i*(cell+20); img.paste(tile(p,cell),(x,top)); d.text((x+6,top-30),lab,font=F(21,True),fill=SUB)
    img.save(out,quality=90)
E=lambda v: G+'E6_%s.png'%v
strip(G+'E6',"Saurin Gate 6 — whole-organism anatomical integration (on accepted Gate 5)"+T,
 ["Head: TS6.3 naked-skull refinement rebuilt through the accepted Gate 3/3A seating. Body: regional low-pass of the Gate 5 surface removes procedural grooves, lumps, rims and debris; structure rebuilt on top.",
  "Pelvis/tail root rebuilt as a sacral-caudal platform with broad caudofemoral and iliocaudal masses. Height, width, depth, stance, tail, feet, hands unchanged."],O+'g6_01_five_views.jpg')
row([(E('hF'),'Front'),(E('hP'),'Profile'),(E('hR'),'Rear'),(E('hF34'),'Front 3/4'),(E('hR34'),'Rear 3/4'),(E('hT'),'Top')],
 "Gate 6 — head five-view close (TS6.3 naked skull)"+T,
 ["Frog eye-domes removed: interorbital roof joins brow, orbits and rostrum. Midline knife-edge removed. Premaxillary boss, low nasal ridges, slit nares in a raised narial rim, maxillary swelling + antorbital fossa.",
  "Orbital-temporal platform, supratemporal fossa, tucked jaw adductor, deeper posterior mandible, closed jaws with one oral line, rounded mandible underside, occipital bosses + short nuchal crest. No horns/crests/display."],O+'g6_02_head.jpg',cell=560)
row([(E('nP'),'Profile'),(E('nF34'),'Front 3/4'),(E('nR34'),'Rear 3/4'),(E('nR'),'Rear')],
 "Gate 6 — head / neck / thorax"+T,["Skull seated through the Gate 3A cervical system (rebuilt around the new skull, not re-designed). Neck scratch texture relaxed; occipital crest runs into the nuchal mass.",
 "Jaw base flows into the throat sheet and chest shield; no collar, hose or pedestal."],O+'g6_03_head_neck_thorax.jpg')
row([(E('shF'),'Front'),(E('shL'),'Lateral'),(E('shF34'),'Front 3/4'),(E('shR34'),'Rear 3/4')],
 "Gate 6 — shoulder / arm integration"+T,["Gate 5 shoulder root kept (arm grows from the thoracic/scapular mass). Shoulder-top crack and posterior armpit creases relaxed into the thoracic shell.",
 "Elbow, forearm and hand architecture unchanged from Gate 5."],O+'g6_04_shoulder_arm.jpg')
row([(E('tF'),'Front'),(E('tF34'),'Front 3/4'),(E('tP'),'Profile'),(E('tR'),'Rear')],
 "Gate 6 — torso"+T,["Gate 2A map preserved (keel/chest shield, pectoral fan, costal arches, ventral shield, long obliques). Procedural grooves/striations relaxed ~65 %; the scalloped lower ventral-shield crown removed.",
 "Rear: parallel lumbar channels beside the tail root filled. No pec plates, rectus blocks, linea alba or navel."],O+'g6_05_torso.jpg')
row([(E('pF'),'Front'),(E('pP'),'Profile'),(E('pR'),'Rear'),(E('pF34'),'Front 3/4'),(E('pR34'),'Rear 3/4')],
 "Gate 6 — pelvis / tail root"+T,["Pelvis rebuilt from the low-pass of its own surface: no buttock hemispheres, cleft or crotch lump. Neutral pelvic floor runs straight into the tail's ventral surface (no external genital form).",
 "Load paths: transverse sacral platform, iliocaudal bands (ilium → tail), broad caudofemoral masses (tail → posterior femur) that fill the tail/thigh crease, ischiocaudal (ventral), lateral hip stabiliser."],O+'g6_06_pelvis_tail_root.jpg',cell=600)
row([(E('lF'),'Front'),(E('lP'),'Profile'),(E('lR'),'Rear'),(E('lR34'),'Rear 3/4'),(E('ft'),'Foot 3/4')],
 "Gate 6 — hindlimb / foot integration"+T,["Gate 4 load paths and plantigrade foot kept (feet vertex-identical). Patellar-like knee lumps, the right posterior knee ball and both calf balls deflated so the calf lengthens into the leg.",
 "Inner-thigh shards and the old hand-contact patch on the outer thigh smoothed."],O+'g6_07_hindlimb_foot.jpg',cell=600)
row([(E('fwF'),'Forearm front'),(E('fwL'),'Forearm lateral'),(E('wrL'),'Wrist close'),(E('hnd'),'Hand 3/4')],
 "Gate 6 — forearm / wrist / hand"+T,["Gate 5 forelimb architecture unchanged: flexor/extensor systems → carpal block → metacarpal palm → digits → claws; opposable thumb. No wrist stalk."],O+'g6_08_forearm_wrist_hand.jpg')
row([(E('hU'),'Underside'),(E('hU2'),'Low front 3/4')],
 "Gate 6 — jaw / throat underside"+T,["Jaws closed into one skull with a single oral line; mandible underside rounded (no flat plate or lip edge) and rolling into the throat; intermandibular groove; no pouch or dewlap."],O+'g6_09_jaw_throat.jpg',cell=760)
row([(E('pLow'),'Low rear 3/4'),(E('pLow2'),'From below, rear'),(E('pUnd'),'From below, front')],
 "Gate 6 — pelvic / caudal origin from below"+T,["The tail's ventral surface continues forward into the neutral pelvic floor; caudofemoral masses meet the posterior thighs."],O+'g6_10_pelvic_underside.jpg',cell=760)
# 11 comparison
views=[('front','Full front'),('profile','Full profile'),('rear34','Full rear 3/4'),('hF34','Head 3/4'),('hP','Head profile'),('tF','Torso'),('pR34','Tail root'),('lR','Legs rear')]
cell=430; W=230+len(views)*(cell+16); img=Image.new('RGB',(W,130+2*(cell+16)),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Gate 5 vs Gate 6 — identical cameras"+T,font=F(30,True),fill=TXT); d.text((20,62),"Same orthographic cameras on both meshes.",font=F(20),fill=SUB)
for r,(lab,tag) in enumerate((("Gate 5\n(before)",'F5'),("Gate 6\n(after)",'E6'))):
    y=120+r*(cell+16); d.multiline_text((20,y+cell//2-30),lab,font=F(24,True),fill=TXT,spacing=8)
    for c,(v,vl) in enumerate(views):
        x=230+c*(cell+16); img.paste(tile(G+'%s_%s.png'%(tag,v),cell),(x,y))
        if r==0: d.text((x+6,y-26),vl,font=F(18,True),fill=SUB)
img.save(O+'g6_11_gate5_vs_gate6.jpg',quality=88)
# 12 silhouette
cell=600; img=Image.new('RGB',(20+5*(cell+20),cell+230),(236,236,240)); d=ImageDraw.Draw(img)
d.text((20,16),"Gate 6 — whole-organism silhouette (no surface detail)"+T,font=F(30,True),fill=(20,20,26))
d.text((20,62),"Dark: Gate 6 silhouette. Red: Gate 5 only (removed). Blue: Gate 6 only (added). Five established cameras.",font=F(20),fill=(60,60,70))
for i,(v,vl) in enumerate(VIEWS):
    a5=np.array(Image.open(G+'F5_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    a6=np.array(Image.open(G+'E6_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    rgb=np.full((cell,cell,3),236,np.uint8); rgb[a6]=(40,42,50); rgb[a5&~a6]=(220,60,50); rgb[a6&~a5]=(60,110,230)
    x=20+i*(cell+20); img.paste(Image.fromarray(rgb),(x,120)); d.text((x+6,92),vl,font=F(22,True),fill=(60,60,70))
img.save(O+'g6_12_silhouette.jpg',quality=90)
# 13 accounting
g=A['_global']
img=strip(G+'AC6',"Gate 6 accounting — deviation of every vertex from the Gate 5 surface",
 ["Green < 1 mm (unchanged), amber 1–5 mm (relaxed), red > 5 mm (rebuilt). Free tail and feet unchanged (≤ 1 mm). Height %.1f cm (Gate 5 %.1f); width and depth unchanged."%(g['height'][0],g['height'][1]),
  "Seams fall only where the field is unchanged (free tail, feet, outer arms). %d of %d vertices are exact Gate 5 copies."%(g['identical_copies'],g['verts'])],O+'g6_13_accounting.jpg')
cell=760; rowi=Image.new('RGB',(img.width,cell+40),BG)
for i,p in enumerate((G+'AC6_hF34.png',G+'AC6_pR34.png',G+'AC6_lR.png')): rowi.paste(tile(p,cell),(20+i*(cell+20),20))
leg=Image.new('RGB',(img.width,80),BG); d=ImageDraw.Draw(leg); x=20
for lab,c in (("< 1 mm from Gate 5",COL["PRESERVE"]),("1–5 mm",COL["MODIFY"]),("> 5 mm (rebuilt)",COL["REBUILD"])):
    d.rectangle((x,22,x+34,56),fill=c); d.text((x+46,26),lab,font=F(21,True),fill=TXT); x+=46+d.textlength(lab,font=F(21,True))+50
out=Image.new('RGB',(img.width,img.height+rowi.height+leg.height),BG); out.paste(img,(0,0)); out.paste(rowi,(0,img.height)); out.paste(leg,(0,img.height+rowi.height)); out.save(O+'g6_13_accounting.jpg',quality=88)
print('ok')
