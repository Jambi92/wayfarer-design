import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json, os, numpy as np
D='/tmp/claude-0/rodin/p9/'; G8='/tmp/claude-0/rodin/g8/r/'; R8=D+'r8/'; O=D+'sheets13/'; os.makedirs(O,exist_ok=True)
A=json.load(open(D+'acct_p9.json')); TP=json.load(open(D+'taper.json')); T=" — POLISH (DIAGNOSTIC / NOT FINAL)"
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def sheet(title,sub,rows,cols,cell,out,fn,lw=200,capfont=18):
    W=lw+len(cols)*(cell+14)+10; top=96+28*len(sub)+34; img=Image.new('RGB',(max(W,1300),top+len(rows)*(cell+14)+20),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(30,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,60+28*i),s,font=F(19),fill=SUB)
    for c,(cl,ck) in enumerate(cols): d.text((lw+c*(cell+14)+4,top-28),cl,font=F(capfont,True),fill=SUB)
    for r,(rl,rk) in enumerate(rows):
        y=top+r*(cell+14); d.multiline_text((16,y+cell//2-30),rl,font=F(20,True),fill=TXT,spacing=6)
        for c,(cl,ck) in enumerate(cols):
            p=fn(rk,ck)
            if p and os.path.exists(p): img.paste(tile(p,cell),(lw+c*(cell+14),y))
    img.save(O+out,quality=90); print(out,img.size)
BA=[('Gate 8 /\ncurrent','N7'),('Polish','N12')]
# 1 tail before/after
sheet("Saurin polish — 1. tail taper before / after (neutral material, identical cameras)"+T,
 ["Proximal/mid-tail volume redistributed longitudinally (same volume s=12–98 cm: %.0f → %.0f cm³, %+.2f %%); per-direction outline smoothed along the axis, so the dorsal knob and ventral pinch at f≈−65 are gone."%(TP['volume_s12_98_cm3'][0],TP['volume_s12_98_cm3'][1],TP['volume_change_pct']),
  "Root (sacral base, caudofemoral slips) and terminal taper untouched; tail path and tip identical (tip shift %.1f cm)."%TP['tail_tip_shift_cm']],
 BA,[('Profile','tprof'),('Tail profile','tailP'),('Top (dorsal)','ttop'),('Dorsal oblique','dorsT'),('Rear 3/4','tr34'),('Root rear 3/4','trc')],400,'p9_01_tail_before_after.jpg',lambda r,c:D+'%s_%s.png'%(r,c))
# 2 taper graph + silhouettes
g=Image.open(D+'taper_graph.png').convert('RGB'); cell=420
img=Image.new('RGB',(max(g.width,3*(cell+16)+40)+40,g.height+cell+260),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin polish — 2. tail taper measurement"+T,font=F(30,True),fill=TXT)
d.text((20,58),"True planar cross-sections perpendicular to the anatomical axis, sacral base → tip. Gate 8: area jumps 120 → 300 cm² over ~15 cm (s 55–70) then plateaus = bulb. Polish: one monotone, smooth taper.",font=F(19),fill=SUB)
img.paste(g,(20,100)); y=110+g.height
nums=["max dA/ds (taper-rate spike): %.1f → %.1f cm²/cm"%(TP['max_dA_ds_gate6'],TP['max_dA_ds_polish']),"volume s12–98: %+.2f %%   root r_eq at s=100: %.2f → %.2f cm"%(TP['volume_change_pct'],TP['root_req_s100_gate6'],TP['root_req_s100_polish']),
      "tail tip: identical (shift %.1f cm) → length/path preserved;  largest vertex move %.1f cm (bulb zone)"%(TP['tail_tip_shift_cm'],TP['tail_max_move_cm'])]
for i,s in enumerate(nums): d.text((20,y+8+28*i),s,font=F(20,True),fill=TXT)
y+=110
for i,(v,vl) in enumerate([('tprof','Profile silhouette'),('ttop','Top silhouette'),('dorsT','Dorsal oblique silhouette')]):
    a5=np.array(Image.open(D+'N7_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127; a6=np.array(Image.open(D+'N12_%s.png'%v).convert('RGBA').resize((cell,cell)))[...,3]>127
    rgb=np.full((cell,cell,3),236,np.uint8); rgb[a6]=(40,42,50); rgb[a5&~a6]=(220,60,50); rgb[a6&~a5]=(60,110,230)
    x=20+i*(cell+16); img.paste(Image.fromarray(rgb),(x,y+30)); d.text((x+4,y+4),vl+'  (red = Gate 8 only, blue = polish only)',font=F(16,True),fill=SUB)
img.save(O+'p9_02_tail_taper_graph.jpg',quality=92); print('p9_02')
# 3 brow
sheet("Saurin polish — 3. supraorbital / brow-shelf integration (neutral material)"+T,
 ["Sharp crest kept (tapering ridge, 0.60 → 0.40 cm); broad low root web into the frontal roof and a lateral web filling the concave crease under the ridge; the ridge now dissolves into the",
  "temporal line instead of ending as a slab; postorbital bar tapers into the brow with a filleted root (no L-corner). Skull proportions, rostrum, jaw, +8 % scale unchanged. Brow-patch scales re-seeded."],
 BA,[('Front','hF'),('Profile','hP'),('Front 3/4','hF34'),('Rear 3/4','hR34'),('Top','hT'),('Brow close 3/4','bF34'),('Brow close profile','bP')],380,'p9_03_brow_before_after.jpg',lambda r,c:D+'%s_%s.png'%(r,c))
# 4 whole neutral
sheet("Saurin polish — 4. whole organism, neutral, identical cameras"+T,
 ["Only the tail taper and brow changed. Height %.2f → %.2f cm, width %.2f → %.2f, depth %.2f → %.2f."%(A['envelope_cm']['height'][0],A['envelope_cm']['height'][1],A['envelope_cm']['width'][0],A['envelope_cm']['width'][1],A['envelope_cm']['depth'][0],A['envelope_cm']['depth'][1])],
 BA,[(l,v) for v,l in VIEWS],440,'p9_04_whole_neutral.jpg',lambda r,c:D+'%s_%s.png'%(r,c))
# 5 pigmented whole
PK=[('P1_umber_mottled','P1'),('P2_slate_banded','P2'),('P7_bluegray_broken','P7'),('P9_green_mixed_asym','P9')]
cols=[(n+' f3/4',k+'|f34') for k,n in PK]+[(n+' r3/4',k+'|r34') for k,n in PK]
sheet("Saurin polish — 5. representative pigmented whole body (Gate 8 model, unchanged)"+T,
 ["Same Gate 8 phenotypes, same cameras and lights, re-evaluated on the corrected geometry (fields rebuilt; scale cells carried from Gate 7)."],
 [('Gate 8','b'),('Polish','a')],cols,330,'p9_05_pigmented_whole.jpg',lambda r,c:(G8 if r=='b' else R8)+'A_%s_%s.png'%tuple(c.split('|')),capfont=15,lw=120)
cols=[(n+' front 3/4',k+'|hF34') for k,n in PK]+[(n+' profile',k+'|hP') for k,n in PK]
sheet("Saurin polish — 6. representative pigmented head"+T,
 ["Facial pattern logic unchanged (damped, plane-following); brow ridge reads as part of the skull in every phenotype."],
 [('Gate 8','b'),('Polish','a')],cols,330,'p9_06_pigmented_head.jpg',lambda r,c:(G8 if r=='b' else R8)+'A_%s_%s.png'%tuple(c.split('|')),capfont=15,lw=120)
# 7 pattern flow
cols=[('banding · tail profile','B_banded|tailP'),('banding · root','B_banded|trc'),('axial · tail profile','B_axial|tailP'),('axial · root','B_axial|trc')]
sheet("Saurin polish — 7. pattern flow over the corrected tail"+T,
 ["Bands and stripes still run trunk → sacral base → root → free tail with no restart; band period now shortens smoothly with the smoother girth curve (no crowding at the old bulb)."],
 [('Gate 8','b'),('Polish','a')],cols+[('P2 tail','A_P2_slate_banded|tailP'),('P7 tail','A_P7_bluegray_broken|tailP')],400,'p9_07_pattern_flow.jpg',
 lambda r,c:((G8 if r=='b' else R8)+'%s_%s.png'%tuple(c.split('|'))) if not (r=='b' and c.startswith('A_')) else None,lw=120)
# 8 RSA
ag=A['scale_family_agreement_pct']
sheet("Saurin polish — 8. Regional Scale Architecture preservation"+T,
 ["Scale seeds carried from the Gate 7 closure (135,248 of 138,497 kept; 4,156 new only inside the re-meshed brow patch). Family agreement with Gate 7: head %.1f %%, tail %.1f %%, everywhere else %.2f %%."%(ag['head (brow surgery box)'],ag['tail (s<98, f<-26)'],ag['everything else']),
  "Outside the brow patch and the tail the surface is identical to Gate 7 (max 0.00 mm). Tail scales are the same scales, carried with the taper (re-projection)."],
 [('Gate 7 /\nGate 8','M7'),('Polish','M12')],[('Profile','profile'),('Head','hF34'),('Tail','tailP'),('Rear 3/4','rear34')],440,'p9_08_rsa_preservation.jpg',lambda r,c:D+'%s_%s.png'%(r,c))
# 9 heat map
b=A['base_geometry_change_vs_gate6_closed']
img=Image.new('RGB',(20+5*(440+14)+20,440+330),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin polish — 9. geometry-change accounting"+T,font=F(30,True),fill=TXT)
d.text((20,58),"Colour = distance from the Gate 7 closure surface: grey < 0.1 mm, then yellow → red up to 15 mm+. Only the tail taper zone and the brow patch change.",font=F(19),fill=SUB)
for i,(v,vl) in enumerate([('front34','Front 3/4'),('profile','Profile'),('rear34','Rear 3/4'),('hF34','Head'),('tailP','Tail')]):
    x=20+i*454; img.paste(tile(D+'H12_%s.png'%v,440),(x,120)); d.text((x+4,96),vl,font=F(18,True),fill=SUB)
y=580
for k,v in b.items():
    d.text((20,y),"%-26s base verts %7d | median %.2f mm | p99 %.2f mm | max %.2f mm | moved >0.1 mm: %d"%(k,v['verts'],v['median_mm'],v['p99_mm'],v['max_mm'],v['changed_gt_0p1mm']),font=F(19,True),fill=TXT); y+=32
d.text((20,y+6),"Base mesh: %d → %d verts (brow patch re-meshed); identical copies of Gate 6 vertices: %d. Envelope unchanged (h/w/d)."%(A['base_mesh']['gate6_verts'],A['base_mesh']['polish_verts'],A['base_mesh']['identical_copies']),font=F(18),fill=SUB)
img.save(O+'p9_09_change_accounting.jpg',quality=90); print('p9_09')
# 11 grown-not-assembled findings
FD=[('chest','1. Sternal strips'),('back','2. Dorsal neck/thoracic rod'),('shoulder','3. Shoulder crease'),('arm','4. Upper-arm path bands'),('hip','5. Inguinal creases + hip fold'),('ankle','6. Heel/Achilles lump'),('neckhead','7. Head–neck splice band'),('postorb','8. Postorbital peg')]
cell=360; img=Image.new('RGB',(20+4*(cell+14),140+2*(cell+50)),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin polish — 11. 'grown, not assembled' findings (documented, NOT changed)"+T,font=F(28,True),fill=TXT)
d.text((20,58),"Neutral base geometry after the polish. Each tile is a location that still reads as attached/strip/step; details and suggested fixes in the report. Author decision required before any change.",font=F(18),fill=SUB)
for i,(v,l) in enumerate(FD):
    x=20+(i%4)*(cell+14); y=110+(i//4)*(cell+50); d.text((x+4,y),l,font=F(18,True),fill=TXT); img.paste(tile(D+'SV12_%s.png'%v,cell),(x,y+28))
img.save(O+'p9_11_grown_findings.jpg',quality=90); print('p9_11')
# 10 4K detail-ceiling audit sheet
cell=430; img=Image.new('RGB',(2000,1420),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin polish — 10. 4K detail-ceiling audit (what the diagnostic mesh is NOT yet)"+T,font=F(28,True),fill=TXT)
d.text((20,56),"Current diagnostic: ~4.5 M-vertex displaced surface, 0.9 mm edges, procedural vertex colour. Production should carry detail in layers, not in ever-denser base geometry.",font=F(18),fill=SUB)
tiers=[(R8+'A_P1_umber_mottled_f34.png','1. Normal gameplay distance','body ~300–700 px tall at 4K: silhouette, value pattern,\nscale-field breakup in normal + roughness maps. Base mesh\n~60–120 k tris + LODs; no scale geometry.'),
       (R8+'A_P1_umber_mottled_hF34.png','2. Dialogue / cinematic','head ~1200–1800 px: planes in base mesh; scales as\ndisplacement/normal (4K maps head, 4K body tiles);\nroughness micro-variation; eye shader with refraction.'),
       (G8+'C_eye_P1_m0_eyec.png','3. Extreme facial / hand close-up','eye or hand fills frame: per-scale edge irregularity,\ninterscale tissue, lid folds, cornea/iris parallax,\nkeratin growth lines need 8K-equivalent texel density\n(UDIM) + tessellated displacement or a hero sculpt.')]
for i,(p,t,s) in enumerate(tiers):
    x=20+i*(cell+230)//1; x=20+i*650; d.text((x,96),t,font=F(20,True),fill=TXT); img.paste(tile(p,cell),(x,126)); d.multiline_text((x,126+cell+8),s,font=F(16),fill=SUB,spacing=4)
rows=[("Feature","Base geometry","Sculpt / disp.","Normal map","Rough/spec","Albedo","SSS/transm.","Eye / keratin mat."),
("Major planes, brow, tail taper","YES (this pass)","—","—","—","—","—","—"),
("Scale field (size/family)","no","YES (16-bit disp)","YES","per-family","pattern only","—","—"),
("Individual scale-edge irregularity","no","YES (hero sculpt/procedural)","YES","edge wear","subtle","—","—"),
("Interscale tissue","no","YES (groove depth)","YES","rougher, paler","paler","thin-skin SSS","—"),
("Scale height/shape variation","no","YES","YES","—","—","—","—"),
("Articulation folds/compression","primary folds only","YES (+ correctives)","YES","—","—","—","—"),
("Facial microstructure","no","YES (head UDIMs)","YES","YES","YES","lids/lips-margin SSS","—"),
("Eyelid / socket transitions","lid thickness, aperture","YES","YES","moist margin","—","YES","—"),
("Cornea / iris / membrane","separate eye meshes","—","iris relief","cornea gloss","iris maps","membrane","YES: refraction"),
("Keratin growth / wear","horn/claw form","growth ridges","YES","YES (0.3–0.45)","banding","tip translucency","YES"),
("Claw / digit transitions","nail-bed fold geometry","YES","YES","—","—","—","YES"),
("Contact surfaces","pad volume (done)","fine tubercles","YES","matte 0.7–0.8","paler","—","—"),
("Roughness breakup","no","—","—","YES (tileable detail)","—","—","—")]
cw=[330,240,250,140,170,150,170,250]; y=700; x0=20
for r,row in enumerate(rows):
    x=x0
    for c,txt in enumerate(row):
        d.text((x,y),txt,font=F(16,r==0),fill=TXT if r==0 else SUB); x+=cw[c]
    y+=40 if r==0 else 34
d.text((20,y+14),"Current gaps (diagnostic ceiling): eye is a single surface (no cornea/iris separation, membrane is shading-only); scales are Voronoi-regular; no interscale micro-texture;",font=F(17,True),fill=TXT)
d.text((20,y+42),"no lid/claw fold geometry; vertex colour (≈1 sample/0.9 mm) instead of UDIM maps; head-neck splice band still visible in close-up (finding 7).",font=F(17,True),fill=TXT)
img.save(O+'p9_10_4k_detail_audit.jpg',quality=90); print('p9_10')
