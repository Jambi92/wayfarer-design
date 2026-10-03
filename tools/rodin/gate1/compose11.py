import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json, numpy as np
G='/tmp/claude-0/rodin/g1/'; O=G+'sheets11/'; A=json.load(open(G+'acct11.json')); T=" — GATE 7 CLOSURE"
import os; os.makedirs(O,exist_ok=True)
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def grid(views,title,sub,out,tags,cell=520,lw=240,fmt='%s_%s.png'):
    W=max(lw+len(views)*(cell+16),1400); top=100+30*len(sub); img=Image.new('RGB',(W,top+len(tags)*(cell+16)+20),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(30,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,62+30*i),s,font=F(20),fill=SUB)
    for r,(lab,tag) in enumerate(tags):
        y=top+r*(cell+16); d.multiline_text((20,y+cell//2-40),lab,font=F(22,True),fill=TXT,spacing=8)
        for c,(v,vl) in enumerate(views):
            x=lw+c*(cell+16); img.paste(tile(G+fmt%(tag,v),cell),(x,y))
            if r==0: d.text((x+6,y-28),vl,font=F(19,True),fill=SUB)
    img.save(out,quality=90)
grid(VIEWS,"Saurin Gate 7 closure — whole organism (identical cameras)"+T,
 ["Frozen Gate 6 base, Gate 7 diagnostic and Gate 7 closure. Closure changes only the surface relief (graded transitions, facial hierarchy, contact thickening);",
  "structure, proportions, tail and stance are the Gate 6 surface underneath in every row."],O+'c7_01_whole_organism.jpg',
 [('Gate 6\n(frozen)','E9'),('Gate 7\ndiagnostic','E10'),('Gate 7\nclosure','E11')],cell=440)
grid([('hF','Front'),('hP','Profile'),('hF34','Front 3/4'),('hR34','Rear 3/4')],"Saurin Gate 7 closure — head: cranial planes before microstructure"+T,
 ["Closure: expressive units finer/subtler (lids, mouth margin, jaw corner); roof, posterolateral and rostral units are flatter plates; relief is attenuated on sharp skull-plane edges",
  "(brow shelf, orbital rim, jugal, hinge) so the planes read first; the recessed tympanic (auricular) area is a smooth shallow recess with no rim. Skull unchanged; slit pupil + nictitating fold kept."],
 O+'c7_02_head.jpg',[('Gate 7\ndiagnostic','E10'),('Gate 7\nclosure','E11')],cell=560)
grid([('tv','Trunk → ventral'),('ax','Shoulder / axilla'),('ing','Lower trunk / inguinal'),('nh','Posterior neck → cranium'),('wh','Forearm / wrist → hand'),('af','Shin / ankle → foot'),('trc','Sacral base → tail root')],
 "Saurin Gate 7 closure — scale-family transitions"+T,
 ["Size, relief, elongation, plate-ness and imbrication now blend over ~2 cm on the body (~1 cm on head, hands, feet) and seeds follow the graded size field (variable-radius Poisson disk),",
  "so unit size grades across family boundaries with no border line, density step or texture island. Families stay distinct away from the boundaries."],
 O+'c7_03_transitions.jpg',[('Gate 7\ndiagnostic','E10'),('Gate 7\nclosure','E11')],cell=400,lw=200)
items=[('hD','Hand dorsal'),('hPal','Palm'),('hP34','Palm 3/4'),('hTip','Fingertips / claws')]; fitems=[('fD','Foot dorsal'),('fPl','Sole'),('fL','Foot lateral'),('f34','Foot 3/4')]
cell=420; img=Image.new('RGB',(220+8*(cell+12),150+2*(cell+40)),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin Gate 7 closure — hands and feet contact surfaces"+T,font=F(30,True),fill=TXT)
d.text((20,58),"Contact thickening raised slightly (pad relief 1.6 → 2.1 mm) at thenar/hypothenar/distal palm/digital and heel/metatarsal/digital load areas; still low swellings inside the fine contact scale field,",font=F(19),fill=SUB)
d.text((20,84),"not separate paw pads. Dorsal → joint → contact grading. Claw length and digit proportions unchanged; sole ground plane clamped (height unchanged). Foot views are an ankle crop.",font=F(19),fill=SUB)
for r,(lab,tg) in enumerate((('Diagnostic','D'),('Closure','C'))):
    y=140+r*(cell+40); d.text((20,y+cell//2),lab,font=F(22,True),fill=TXT)
    for i,(v,vl) in enumerate(items+fitems):
        x=220+i*(cell+12); p=G+('HA8%s_%s.png' if i<4 else 'FO8%s_%s.png')%(tg,v); img.paste(tile(p,cell),(x,y+28))
        if r==0: d.text((x+6,y),vl,font=F(19,True),fill=SUB)
img.save(O+'c7_04_hands_feet.jpg',quality=90)
VAR=[('baseline','Neutral naked\nbaseline\nCANONICAL'),('minimal_ridges','1. Minimal ridges\nnear-naked /\nminimal end'),('low_hornlets','2. Low hornlets\nACCEPTED\n(primary)'),('swept_paired','3. Swept-back\npaired ACCEPTED\n(primary)'),('crest','4. Crest\nRETAINED, low\n(2.43 cm ≤ 2.5)'),('mixed_asym','5. Mixed/asym.\nACCEPTED\n(primary)')]
grid([('hF','Front'),('hP','Profile'),('hF34','Front 3/4'),('hR34','Rear 3/4'),('hT','Top')],"Saurin Gate 7 closure — Cranial Keratin Display families (hair-analogue category)"+T,
 ["Identical frozen skull, camera and lighting; closure surface on every head. Attachments: 1 temporal line/parietal margin · 2 postorbital, squamosal corner, posterior parietal ·",
  "3 squamosal/temporal corner · 4 dorsal midline (crest lowered to 2.43 cm above the roof) · 5 posterior cranial margin + brow. None is required for a complete head; skull never reshaped.",
  "(Small isolated speck in Top view = crop-box fragment, not anatomy.)"],O+'c7_05_display_families.jpg',[(lab,v) for v,lab in VAR],cell=380,lw=250,fmt='DC_%s_%s.png')
cell=520; names=[('front','Front'),('rear34','Rear 3/4'),('hF34','Head'),('pR34','Tail root')]
img=Image.new('RGB',(20+4*(cell+16)+980,cell+330),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin Gate 7 — closure vs diagnostic change accounting"+T,font=F(30,True),fill=TXT)
d.text((20,62),"Colour = closure vs diagnostic vertex movement: dark < 0.2 mm, amber 0.2–0.6 mm, red > 0.6 mm (surface relief only; the Gate 6 base is identical under both).",font=F(20),fill=SUB)
for i,(v,vl) in enumerate(names):
    x=20+i*(cell+16); img.paste(tile(G+'AC11_%s.png'%v,cell),(x,130)); d.text((x+6,100),vl,font=F(19,True),fill=SUB)
x0=20+4*(cell+16)+10; y=110; f17=F(17)
d.text((x0,y),"Closure relief vs Gate 6 (mm): out / in / mean / rms     moved vs diag: median / p99",font=F(18,True),fill=TXT); y+=32
for k in A['closure_relief_vs_gate6']:
    if k.startswith('_'): continue
    v=A['closure_relief_vs_gate6'][k]; w=A['closure_vs_diagnostic'][k]
    d.text((x0,y),"%-30s %5.2f / %5.2f / %+6.3f / %5.3f      %5.2f / %5.2f"%(k[:30],v['out_max_mm'],v['in_max_mm'],v['mean_mm'],v['rms_mm'],w['median_mm'],w['p99_mm']),font=f17,fill=SUB); y+=26
a=A['closure_relief_vs_gate6']['_all']; w=A['closure_vs_diagnostic']['_all']; y+=8
d.text((x0,y),"ALL: out %.2f / in %.2f / mean %+.3f / rms %.3f mm; moved vs diag median %.2f, p99 %.2f mm"%(a['out_max_mm'],a['in_max_mm'],a['mean_mm'],a['rms_mm'],w['median_mm'],w['p99_mm']),font=F(18,True),fill=TXT); y+=34
g=A['transition_gradient_per_cm']
d.text((x0,y),"Size-field gradient (R change per cm, p99.9): diagnostic %.3f → closure %.3f"%(g['diagnostic_R']['p999'],g['closure_R']['p999']),font=F(18),fill=SUB); y+=28
d.text((x0,y),"Relief-field gradient (H change per cm, p99.9): diagnostic %.4f → closure %.4f"%(g['diagnostic_H']['p999'],g['closure_H']['p999']),font=F(18),fill=SUB); y+=28
e=A['_envelope_cm']
for k in ('height','width','depth'):
    d.text((x0,y),"%s: Gate 6 %.2f · diagnostic %.2f · closure %.2f cm"%(k,e[k]['gate6'],e[k]['diagnostic'],e[k]['closure']),font=F(18),fill=SUB); y+=26
img.save(O+'c7_06_accounting.jpg',quality=90)
cell=600; img=Image.new('RGB',(20+5*(cell+20),cell+230),(236,236,240)); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin Gate 7 closure — silhouette vs frozen Gate 6"+T,font=F(30,True),fill=(20,20,26))
sil=A['_silhouette_closure_vs_gate6']
d.text((20,62),"Dark: closure. Red: Gate 6 only. Blue: closure only. Changed outline pixels: "+", ".join("%s %.2f %%"%(k,v['pct']) for k,v in sil.items())+" (scale relief only).",font=F(20),fill=(60,60,70))
for i,(v,vl) in enumerate(VIEWS):
    a5=np.array(Image.open(G+'E9_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    a6=np.array(Image.open(G+'E11_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    rgb=np.full((cell,cell,3),236,np.uint8); rgb[a6]=(40,42,50); rgb[a5&~a6]=(220,60,50); rgb[a6&~a5]=(60,110,230)
    x=20+i*(cell+20); img.paste(Image.fromarray(rgb),(x,120)); d.text((x+6,92),vl,font=F(22,True),fill=(60,60,70))
img.save(O+'c7_07_silhouette.jpg',quality=90)
print('ok')
