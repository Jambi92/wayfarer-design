import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json, os, numpy as np
D='/tmp/claude-0/rodin/c10/'; P9='/tmp/claude-0/rodin/p9/'; O=D+'sheets14/'; os.makedirs(O,exist_ok=True)
A=json.load(open(D+'acct13.json')); T=" — FINAL CLEANUP (DIAGNOSTIC)"
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def sheet(title,sub,rows,cols,cell,out,fn,lw=190,capfont=18):
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
BA=[('Polish\n(before)','B12'),('Cleanup\n(after)','B13')]
z=A['base_movement_by_zone']; fz=lambda k:"max %.1f / p99 %.1f mm"%(z[k]['max_mm'],z[k]['p99_mm'])
sheet("Saurin final cleanup — 1. whole organism, neutral, identical cameras"+T,
 ["Only local meso-scale corrections; envelope unchanged (h/w/d %.2f / %.2f / %.2f cm), silhouette unchanged at whole-body scale."%(A['envelope_cm']['height'][1],A['envelope_cm']['width'][1],A['envelope_cm']['depth'][1])],
 BA,[(l,v) for v,l in VIEWS],430,'c14_01_whole_organism.jpg',lambda r,c:D+'%s_%s.png'%(r,c))
items=[("2. chest / sternum",[('chest','Chest')],"Applied-looking Y/chevron strips and sternal bar lowered and broadened into the thoracic sheet ("+fz('sternum')+"); faint load-path relief kept, fine detail left for normal maps."),
 ("3. dorsal neck / upper thorax",[('back','Back'),('nape','Nape')],"Midline rod lowered progressively (more toward its lower end) and its flanking grooves filled, so it tapers into the dorsal spinal line ("+fz('dorsal_rod')+")."),
 ("4. shoulder and upper arm",[('shoulder','Shoulder top'),('arm','Upper arm')],"Acromial seam crease filleted into a graded fold ("+fz('shoulder')+"); lateral arm grooves softened and lengthened ("+fz('upper_arm')+")."),
 ("5. inguinal / hip",[('hip','Hip (rear 3/4)'),('ing','Inguinal (front)')],"Narrow thigh-pelvis creases filleted, residual hip fold removed ("+fz('inguinal_hip')+"); no groin, cleft or buttock anatomy created; pelvis-thigh-tail root unchanged in structure."),
 ("6. ankle / heel + defect repair",[('ankle','Ankle (side)'),('ankf','Ankle (front)'),('heel','Heel (rear)')],"The lump-with-step is on the FRONT of the ankle (mis-labelled 'heel' in the polish report): blended into the tendon line ("+fz('ankle_front')+"); heel/Achilles graded ("+fz('heel')+"); seam-ring slivers collapsed (dark speck gone)."),
 ("7. head-neck splice",[('nk','Neck'),('nkc','Neck close')],"Gate 6 head-patch seam band on the neck de-noised in place (Taubin, shape-preserving: "+fz('head-neck splice band')+"); scales carried, no ring or density jump."),
 ("8. postorbital / brow / jugal",[('pF34','Front 3/4'),('pP','Profile'),('poC','Postorbital close')],"Postorbital bar is now a sharp descending ridge that sweeps back into the jugal/quadrate line instead of ending as a peg (skull SDF, field-difference patch: "+fz('postorbital/brow patch')+"); brow integration kept."),
 ("9. tail confirmation",[('tprof','Profile'),('ttop','Top'),('tr34','Rear 3/4')],"Tail untouched: section areas identical to the accepted polish (max diff %.2f %%, volume %d = %d cm³)."%(A['tail_taper']['max_section_area_diff_pct'],A['tail_taper']['volume_s12_98_polish'],A['tail_taper']['volume_s12_98_cleanup']))]
for i,(t,cols,s) in enumerate(items):
    sheet("Saurin final cleanup — %s (neutral)"%t+T,[s],BA,[(l,v) for v,l in cols],460 if len(cols)<3 else 420,'c14_%02d_%s.jpg'%(i+2,t.split('. ')[1].split(' ')[0].replace('/','')),lambda r,c:D+'%s_%s.png'%(r,c))
VAR=[('baseline','Neutral naked'),('minimal_ridges','Minimal ridges'),('low_hornlets','Low hornlets'),('swept_paired','Swept-back\npaired'),('mixed_asym','Mixed / asym.'),('crest','Restrained\ncrest')]
sheet("Saurin final cleanup — 10. cranial display family on the polished skull"+T,
 ["All six rebuilt on the final skull (brow integration + postorbital sweep), identical cameras; last column = attachment close-up (rear-top 3/4).",
  "Structures are SDF-anchored on the skull surface and blended into it; the skull field outside each local box is identical to the naked head. Crest 2.43 cm above the roof."],
 [(l,v) for v,l in VAR],[('Front','hF'),('Profile','hP'),('Front 3/4','hF34'),('Rear 3/4','hR34'),('Top','hT'),('Attachment','att')],330,'c14_10_display_family.jpg',lambda r,c:D+'dv/DN_%s_%s.png'%(r,c),lw=210)
PK=[('P1_umber_mottled','P1'),('P2_slate_banded','P2'),('P7_bluegray_broken','P7'),('P9_green_mixed_asym','P9')]
sheet("Saurin final cleanup — 11. Gate 8 survives (pigmented, after)"+T,
 ["Same phenotype code and cameras on the cleaned geometry (fields rebuilt, scale cells carried). Pattern flow trunk → root → tail continuous; facial pattern follows the brow/postorbital planes."],
 [(n,k) for k,n in PK],[('Front 3/4','f34'),('Rear 3/4','r34'),('Head 3/4','hF34'),('Head profile','hP'),('Tail','tailP')],340,'c14_11_gate8_after.jpg',lambda r,c:D+'r8/A_%s_%s.png'%(r,c),lw=110)
sheet("Saurin final cleanup — 12. Regional Scale Architecture preservation"+T,
 ["Scale seeds carried from the polish surface (137,494 kept; 1,696 re-filled only where a base triangle was re-meshed). Family agreement: %.3f %% overall, %.3f %% on unmoved surface, %.2f %% on corrected surface."%(A['scale_family_agreement_pct_all'],A['scale_family_agreement_pct_unmoved_surface'],A['scale_family_agreement_pct_moved_surface'])],
 [('Polish','M12'),('Cleanup','M13')],[('Profile','profile'),('Head','hF34'),('Tail','tailP'),('Rear 3/4','rear34')],430,'c14_12_rsa.jpg',lambda r,c:(P9 if r=='M12' else D)+'%s_%s.png'%(r,c))
img=Image.new('RGB',(20+5*(430+14)+20,430+560),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin final cleanup — 13. geometry-change accounting"+T,font=F(30,True),fill=TXT)
d.text((20,58),"Colour = distance from the accepted polish surface (grey < 0.1 mm → yellow → red ≥ 10 mm). Movement is confined to the authorized zones and their feathered margins.",font=F(19),fill=SUB)
for i,(v,vl) in enumerate([('front34','Front 3/4'),('rear34','Rear 3/4'),('profile','Profile'),('hF34','Head'),('ankle','Ankle')]):
    x=20+i*444; img.paste(tile(D+'H13_%s.png'%v,430),(x,120)); d.text((x+4,96),vl,font=F(18,True),fill=SUB)
y=570; d.text((20,y),"%-28s %8s %9s %8s %8s %8s"%("zone (base mesh)","verts","median","p95","p99","max mm"),font=F(18,True),fill=TXT); y+=30
for k,v in z.items():
    d.text((20,y),"%-28s %8d %9.2f %8.2f %8.2f %8.2f"%(k,v['verts'],v['median_mm'],v['p95_mm'],v['p99_mm'],v['max_mm']),font=F(17),fill=SUB); y+=26
t=A['topology']; d.text((20,y+10),"Watertight: %d boundary edges, %d non-manifold, %d component(s); %d verts / %d faces."%(t['boundary_edges'],t['nonmanifold_edges'],t['components'] or 1,t['verts'],t['faces']),font=F(18,True),fill=TXT)
img.save(O+'c14_13_accounting.jpg',quality=90); print('c14_13')
