import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json, numpy as np
G='/tmp/claude-0/rodin/g1/'; O=G+'sheets10/'; A=json.load(open(G+'acct10.json')); T=" — DIAGNOSTIC / NOT FINAL"
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def grid(views,title,sub,out,tags,cell=520,lw=240,fmt='%s_%s.png'):
    W=lw+len(views)*(cell+16); top=100+30*len(sub); img=Image.new('RGB',(W,top+len(tags)*(cell+16)+20),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(30,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,62+30*i),s,font=F(20),fill=SUB)
    for r,(lab,tag) in enumerate(tags):
        y=top+r*(cell+16); d.multiline_text((20,y+cell//2-30),lab,font=F(22,True),fill=TXT,spacing=8)
        for c,(v,vl) in enumerate(views):
            x=lw+c*(cell+16); img.paste(tile(G+fmt%(tag,v),cell),(x,y))
            if r==0: d.text((x+6,y-28),vl,font=F(19,True),fill=SUB)
    img.save(out,quality=90)
GT=(('Gate 6\n(frozen)','E9'),('Gate 7','E10'))
grid(VIEWS+[('mid1','Mid front 3/4'),('mid2','Mid rear 3/4')],"Saurin Gate 7 — whole organism: regional scale architecture on the frozen Gate 6 body"+T,
 ["Scales are a normal displacement only (relief ≤ 1.5 mm, zero mean): structural fields on the dorsal trunk/tail/cranium/shins/forearms, transitional fields at every flexion boundary,",
  "fine expressive fields on the face, a broad transverse ventral field (no continuous belly scutes), fine palmar/plantar contact fields with pad thickening, smooth keratin claws. No pigment."],O+'g7_01_whole_organism.jpg',GT,cell=430)
grid([('hF','Front'),('hP','Profile'),('hF34','Front 3/4'),('hR34','Rear 3/4'),('eye','Eye close')],"Saurin Gate 7 — head close-ups (neutral naked baseline, frozen +8 % skull)"+T,
 ["Structural units on the cranial roof / posterolateral cranium and rostral dorsum; fine expressive field over lids, mouth margin, cheek, jaw corner and throat; scale flow runs rostral → caudal.",
  "Eye: vertically elliptical (slit) pupil and a resting nictitating-membrane fold at the rostral canthus — biological anatomy, no emissive treatment. Skull geometry unchanged (Gate 6 row)."],O+'g7_02_head.jpg',GT,cell=520)
VAR=[('baseline','Neutral naked\nbaseline'),('minimal_ridges','1. Minimal\ncranial ridges'),('low_hornlets','2. Low\nhornlets'),('swept_paired','3. Swept-back\npaired'),('crest','4. Crest-\ndominant'),('mixed_asym','5. Mixed /\nasymmetric')]
grid([('hF','Front'),('hP','Profile'),('hF34','Front 3/4'),('hR34','Rear 3/4'),('hT','Top')],"Saurin Gate 7 — Cranial Keratin Display comparison: identical frozen skull, camera and lighting"+T,
 ["Every structure is anchored ON the skull surface at a §101 attachment region and blended into it (smooth keratin, no scales); the skull underneath is never reshaped.",
  "1 parietal/temporal-line ridges · 2 postorbital, squamosal and posterior parietal hornlets · 3 squamosal-corner swept-back pair",
  "4 dorsal-midline crest + low side ridges · 5 posterior pair (left ~15 % shorter) + unequal brow hornlets.  (Small isolated speck in Top view = crop-box fragment, not anatomy.)"],
 O+'g7_03_display_comparison.jpg',[(lab,v) for v,lab in VAR],cell=380,lw=230,fmt='DV_%s_%s.png')
# scale-field map
names=[('front','Front'),('profile','Profile'),('rear','Rear'),('rear34','Rear 3/4'),('hF34','Head'),('nk','Neck'),('pR34','Tail root'),('hnd','Hand'),('ft','Foot')]
cell=420; W=20+len(names)*(cell+12); img=Image.new('RGB',(W,cell+260),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin Gate 7 — scale-field map (Regional Scale Architecture)"+T,font=F(30,True),fill=TXT)
d.text((20,62),"Regions follow mobility, load, abrasion and expression (spec §79–84, §106A); boundaries are smoothed so unit size grades across them rather than switching.",font=F(20),fill=SUB)
for i,(v,vl) in enumerate(names):
    x=20+i*(cell+12); img.paste(tile(G+'MP_%s.png'%v,cell),(x,120)); d.text((x+6,94),vl,font=F(19,True),fill=SUB)
PAL=[('Protective structural',(204,115,64)),('Transitional articulation',(242,204,77)),('Fine expressive',(140,89,191)),('Ventral (transverse)',(89,166,217)),('Palmar/plantar contact',(102,191,115)),('Claw keratin',(51,51,56)),('Eye',(242,242,242))]
x=20; y=cell+150
for lab,c in PAL:
    d.rectangle((x,y,x+30,y+30),fill=c); d.text((x+40,y+3),lab,font=F(20,True),fill=TXT); x+=40+d.textlength(lab,font=F(20,True))+40
img.save(O+'g7_04_scale_field_map.jpg',quality=90)
grid([('pR','Rear'),('pP','Profile'),('pR34','Rear 3/4'),('pLow','Low rear 3/4'),('tailC','Tail root → free tail')],"Saurin Gate 7 — tail-root surface continuity"+T,
 ["Dorsal structural units continue pelvis → sacral base → tail without a seam or separate 'tail texture'; a transitional articulation band sits on the caudofemoral/root flexion zone,",
  "and the tail underside carries the ventral transverse field. Gate 6 sacral volume, caudofemoral slips and root taper unchanged underneath."],O+'g7_05_tail_root.jpg',GT,cell=480)
# hands / feet
items=[('HA7_hD','Hand dorsal'),('HA7_hPal','Hand palmar'),('HA7_h34','Hand palmar 3/4'),('HA7_hClaw','Fingertips / claws'),('FO7_fD','Foot dorsal'),('FO7_fPl','Sole (plantar)'),('FO7_fL','Foot lateral'),('FO7_f34','Foot 3/4')]
cell=470; W=20+4*(cell+16); img=Image.new('RGB',(W,140+2*(cell+50)),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin Gate 7 — hands and feet: contact surfaces, pads, claws"+T,font=F(30,True),fill=TXT)
d.text((20,58),"Dorsal: small structural scales. Palm/sole: fine flexible contact scales with localized pad thickening (thenar, hypothenar, distal palm, digital;",font=F(19),fill=SUB)
d.text((20,84),"heel, metatarsal band, digital) — not paw pads. Claws: smooth keratin from the terminal phalanx. Foot views are a crop at the ankle (open rim = crop edge).",font=F(19),fill=SUB)
for i,(p,l) in enumerate(items):
    x=20+(i%4)*(cell+16); y=130+(i//4)*(cell+50); img.paste(tile(G+p+'.png',cell),(x,y+30)); d.text((x+6,y),l,font=F(20,True),fill=SUB)
img.save(O+'g7_06_hands_feet.jpg',quality=90)
cell=600; img=Image.new('RGB',(20+5*(cell+20),cell+230),(236,236,240)); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin Gate 7 — silhouette: Gate 6 frozen vs Gate 7"+T,font=F(30,True),fill=(20,20,26))
sil=A['_silhouette_vs_gate6']
d.text((20,62),"Dark: Gate 7. Red: Gate 6 only. Blue: Gate 7 only. Changed outline pixels: "+", ".join("%s %.2f %%"%(k,v['pct']) for k,v in sil.items())+" (scale relief only).",font=F(20),fill=(60,60,70))
for i,(v,vl) in enumerate(VIEWS):
    a5=np.array(Image.open(G+'E9_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    a6=np.array(Image.open(G+'E10_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    rgb=np.full((cell,cell,3),236,np.uint8); rgb[a6]=(40,42,50); rgb[a5&~a6]=(220,60,50); rgb[a6&~a5]=(60,110,230)
    x=20+i*(cell+20); img.paste(Image.fromarray(rgb),(x,120)); d.text((x+6,92),vl,font=F(22,True),fill=(60,60,70))
img.save(O+'g7_07_silhouette.jpg',quality=90)
# accounting
cell=560; names=[('front','Front'),('rear34','Rear 3/4'),('hF34','Head'),('pR34','Tail root')]
img=Image.new('RGB',(20+4*(cell+16)+900,cell+240),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin Gate 7 — change accounting vs the frozen Gate 6 surface"+T,font=F(30,True),fill=TXT)
d.text((20,62),"Colour = |normal displacement|: dark < 0.3 mm, amber 0.3–0.8 mm, red > 0.8 mm. Displacement is along the surface normal only; no region is inflated or shrunk.",font=F(20),fill=SUB)
for i,(v,vl) in enumerate(names):
    x=20+i*(cell+16); img.paste(tile(G+'AC10_%s.png'%v,cell),(x,130)); d.text((x+6,100),vl,font=F(19,True),fill=SUB)
x0=20+4*(cell+16)+10; y=130; d.text((x0,y),"Region   out-max / in-max / mean / rms (mm)",font=F(19,True),fill=TXT); y+=34
for k,v in A.items():
    if k.startswith('_'): continue
    d.text((x0,y),"%-34s %5.2f / %5.2f / %+6.3f / %5.3f"%(k[:34],v['out_max_mm'],v['in_max_mm'],v['mean_mm'],v['rms_mm']),font=F(17),fill=SUB); y+=28
a=A['_all']; e=A['_envelope']; y+=10
d.text((x0,y),"ALL: out %.2f / in %.2f / mean %+.3f / rms %.3f mm"%(a['out_max_mm'],a['in_max_mm'],a['mean_mm'],a['rms_mm']),font=F(19,True),fill=TXT); y+=34
d.text((x0,y),"Height %.2f (Gate 6 %.2f)  width %.2f (%.2f)  depth %.2f (%.2f) cm"%(e['height'][0],e['height'][1],e['width'][0],e['width'][1],e['depth'][0],e['depth'][1]),font=F(18),fill=SUB)
img.save(O+'g7_08_accounting.jpg',quality=90)
print('ok')
