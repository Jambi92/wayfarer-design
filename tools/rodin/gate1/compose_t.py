import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
G='/tmp/claude-0/rodin/g1/'; O=G+'sheets_t/'
strip(G+'tfull',"Saurin Gate 2 — torso anatomical translation on the accepted Gate 1 body — DIAGNOSTIC / NOT FINAL",
 ["Torso only. Locked and identical: Gate 1 pelvis/sacrum/tail root, B2 free tail, head, neck, arms/hands, thighs, lower legs, feet.",
  "Removed: human pectoral plates + under-pec shelf, rectus six-pack ladder, linea alba groove, navel. Built: keeled chest shield, pectoral fan, ventral shield, costal arches, oblique load paths."],
 O+'t2_01_five_views.jpg')
def row(items,title,sub,out,cell=900):
    W=20+len(items)*(cell+20); img=Image.new('RGB',(W,cell+190),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(30,True),fill=TXT); d.text((20,62),sub,font=F(20),fill=SUB)
    for i,(p,lab) in enumerate(items):
        im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im)
        x=20+i*(cell+20); img.paste(bg,(x,150)); d.text((x+6,114),lab,font=F(22,True),fill=SUB)
    img.save(out,quality=90)
row([(G+'T2_tF.png',"Close front torso"),(G+'T2_tF34.png',"Close front 3/4 torso"),(G+'T2_tP.png',"Close profile torso"),(G+'T2_tL.png',"Close front 3/4 (other side)")],
 "Gate 2 — close torso checks — DIAGNOSTIC",
 "Silhouette and thoracic depth are B1's (low-pass of B1's own surface, 1.5 mm recession). Organization is new: keel + chest shield + pectoral fan; ventral shield; costal arches; long obliques.",
 O+'t2_02_close_torso.jpg',cell=860)
views=[("tF","Close front"),("tF34","Close front 3/4"),("tP","Close profile")]
rows=[("Untouched\nRodin B1",'T0'),("Accepted\nGate 1\n(before)",'T1'),("Gate 2\n(after)",'T2')]
cell=760; W=260+len(views)*(cell+20); img=Image.new('RGB',(W,140+len(rows)*(cell+20)),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Gate 2 before/after — untouched B1 / accepted Gate 1 / Gate 2, identical cameras",font=F(30,True),fill=TXT)
d.text((20,62),"Gate 1 did not touch the torso, so rows 1 and 2 match above the lower trunk; row 1 is the anti-regression reference.",font=F(20),fill=SUB)
for r,(lab,tag) in enumerate(rows):
    y=120+r*(cell+20); d.multiline_text((20,y+cell//2-50),lab,font=F(24,True),fill=TXT,spacing=8)
    for c,(v,vl) in enumerate(views):
        im=Image.open(G+'%s_%s.png'%(tag,v)).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im)
        x=260+c*(cell+20); img.paste(bg,(x,y))
        if r==0: d.text((x+6,y-30),vl,font=F(20,True),fill=SUB)
img.save(O+'t2_03_before_after.jpg',quality=88)
cell=640; img=Image.new('RGB',(20+4*(cell+20),cell+170),BG); d=ImageDraw.Draw(img); d.text((20,16),"Gate 2 before/after — full body",font=F(30,True),fill=TXT); k=0
for v,vl in (("front","Front"),("front34","Front 3/4")):
    for t,tl in (("rfull","Gate 1 (before)"),("tfull","Gate 2 (after)")):
        im=Image.open(G+'%s_%s.png'%(t,v)).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im)
        x=20+k*(cell+20); img.paste(bg,(x,130)); d.text((x+6,96),"%s — %s"%(vl,tl),font=F(21,True),fill=SUB); k+=1
img.save(O+'t2_04_before_after_full.jpg',quality=88)
img=strip(G+'tacct',"Gate 2 accounting — what changed relative to the accepted Gate 1 mesh",["Colours are provenance relative to the Gate 1 refinement (e751973)."],O+'t2_05_accounting.jpg')
items=[G+'tacctc_tF.png',G+'tacctc_tF34.png',G+'tacctc_tP.png']; cell=760; rowi=Image.new('RGB',(img.width,cell+40),BG)
for i,p in enumerate(items):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); rowi.paste(bg,(20+i*(cell+20),20))
leg=Image.new('RGB',(img.width,80),BG); d=ImageDraw.Draw(leg); x=20
for lab,c in (("Unchanged from Gate 1 (identical vertices)",COL["PRESERVE"]),("Copied, relaxed ≤0.9 cm at the new seam",COL["MODIFY"]),("Re-surfaced in Gate 2",COL["REBUILD"])):
    d.rectangle((x,22,x+34,56),fill=c); d.text((x+46,26),lab,font=F(21,True),fill=TXT); x+=46+d.textlength(lab,font=F(21,True))+50
out=Image.new('RGB',(img.width,img.height+rowi.height+leg.height),BG); out.paste(img,(0,0)); out.paste(rowi,(0,img.height)); out.paste(leg,(0,img.height+rowi.height)); out.save(O+'t2_05_accounting.jpg',quality=88)
print('ok')
