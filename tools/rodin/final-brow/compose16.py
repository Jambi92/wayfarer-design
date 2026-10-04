import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json, os
D='/tmp/claude-0/rodin/c12/'; C11='/tmp/claude-0/rodin/c11/'; O=D+'sheets16/'; os.makedirs(O,exist_ok=True)
A=json.load(open(D+'acct15.json')); T=" — FINAL BROW/ORBIT (DIAGNOSTIC)"
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def sheet(title,sub,rows,cols,cell,out,fn,lw=190,capfont=18,extra=None):
    W=lw+len(cols)*(cell+14)+10; top=96+28*len(sub)+34; H=top+len(rows)*(cell+14)+20+(28*len(extra)+20 if extra else 0)
    img=Image.new('RGB',(max(W,1400),H),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(30,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,60+28*i),s,font=F(19),fill=SUB)
    for c,(cl,ck) in enumerate(cols): d.text((lw+c*(cell+14)+4,top-28),cl,font=F(capfont,True),fill=SUB)
    for r,(rl,rk) in enumerate(rows):
        y=top+r*(cell+14); d.multiline_text((16,y+cell//2-30),rl,font=F(20,True),fill=TXT,spacing=6)
        for c,(cl,ck) in enumerate(cols):
            p=fn(rk,ck)
            if p and os.path.exists(p): img.paste(tile(p,cell),(lw+c*(cell+14),y))
    if extra:
        y=top+len(rows)*(cell+14)+10
        for i,(s,b) in enumerate(extra): d.text((20,y+28*i),s,font=F(19,b),fill=TXT if b else SUB)
    img.save(O+out,quality=90); print(out,img.size)
def pth(r,c):
    for base in (D,C11):
        p=base+'%s_%s.png'%(r,c)
        if os.path.exists(p) and (r.endswith('15') or base==C11 or r.startswith('DN')): return p
    return D+'%s_%s.png'%(r,c)
BA=[('Convergence\n(before)','Y14'),('Final\n(after)','Y15')]
ORB=[('Front','hF'),('Profile','hP'),('Front 3/4','hF34'),('Rear 3/4','hR34'),('Top','hT'),('Orbit close','oC'),('Orbit close profile','oP')]
sheet("Saurin — 1. brow/orbit before vs after (scaled surface, identical cameras)"+T,
 ["Supraorbital edge kept crisp over the eye; behind the orbit the lateral brow/platform edge turns progressively into an inclined plane, so the rear brow dissolves into the",
  "temporal/postorbital planes instead of running on as one long projecting bar. Postorbital ridge now fades to zero below the brow: no T-junction, no vertical notch."],
 BA,ORB,330,'v16_01_brow_orbit.jpg',pth,capfont=16)
sheet("Saurin — 2. base mesh, no scales: mean-curvature diagnostic"+T,
 ["Red = convex, blue = concave, on the anatomical base (scales off). Before: one continuous red brow-shelf edge from the orbit to the back of the skull with a blue undercut and a",
  "concave pocket where the postorbital ridge met it. After: the crisp red edge stops behind the orbit and widens into a soft inclined band; no undercut, no pocket, no convex island."],
 [('Before','K14'),('After','K15')],ORB,330,'v16_02_curvature_base.jpg',lambda r,c:D+'%s_%s.png'%(r,c),capfont=16)
sheet("Saurin — 3. final scaled head, neutral naked skull"+T,
 ["Naked skull after the micro-correction with the regenerated scale surface. Fine expressive field kept around the eye; structural cranial scutes follow the corrected planes."],
 [('Scaled head','Y15')],[('Profile','hP'),('Front','hF'),('Front 3/4','hF34'),('Top','hT')],420,'v16_03_scaled_head.jpg',lambda r,c:D+'Y15_%s.png'%c)
sheet("Saurin — 3b. Regional Scale Architecture map before / after"+T,
 ["Scale-family assignment on the regenerated surface: agreement %.3f %% overall, %.3f %% outside the head. Only the re-surfaced brow patch was locally re-seeded."%(A['scale_family_agreement_pct'],A['scale_family_agreement_outside_head_pct'])],
 [('Before','M14'),('After','M15')],[('Front 3/4','hF34'),('Profile','hP')],520,'v16_03b_rsa_map.jpg',lambda r,c:D+'%s_%s.png'%(r,c))
DV=[('Neutral\nnaked','baseline'),('Low\nhornlets','low_hornlets'),('Swept-back\npaired','swept_paired'),('Mixed /\nasym.','mixed_asym'),('Restrained\ncrest','crest')]
sheet("Saurin — 4. display survival on the corrected skull"+T,
 ["Same display parameters as the accepted convergence (crest 2.43 cm, corrected swept-back base).","Each is SDF-anchored on the new skull surface: re-seated only, none redesigned."],
 DV,[('Front','hF'),('Profile','hP'),('Front 3/4','hF34'),('Top','hT'),('Attachment','att')],300,'v16_04_display_survival.jpg',lambda r,c:D+'dv/DN_%s_%s.png'%(r,c),lw=170)
e=A['envelope_cm']; sil=A['silhouette_changed']
sheet("Saurin — 5. whole organism, identical five cameras"+T,
 ["Height/width/depth %.2f/%.2f/%.2f cm (before %.2f/%.2f/%.2f). Silhouette pixels changed: "%(e['height'][1],e['width'][1],e['depth'][1],e['height'][0],e['width'][0],e['depth'][0])
  +", ".join("%s %d"%(k,v['pixels']) for k,v in sil.items())+"."],
 BA,[('Front','front'),('Profile','profile'),('Rear','rear'),('Front 3/4','front34'),('Rear 3/4','rear34')],400,'v16_05_whole_organism.jpg',pth)
bm=A['base_movement']['brow/postorbital zone']; tb=A['tail_bit_identity']; tp=A['topology']
ex=[("Base mesh, brow/postorbital zone: %d verts, median %.2f mm, p95 %.2f, p99 %.2f, max %.2f mm."%(bm['verts'],bm['median_mm'],bm['p95_mm'],bm['p99_mm'],bm['max_mm']),True),
    ("Outside the zone: %d verts, max movement %.4f mm (exact)."%(A['base_movement']['outside zone']['verts'],A['base_movement']['outside zone']['max_mm_exact']),True),
    ("Watertight/manifold: %d boundary, %d non-manifold edges, %d component; %d verts / %d faces."%(tp['boundary_edges'],tp['nonmanifold_edges'],tp['components'],tp['verts'],tp['faces']),False),
    ("Tail: %d/%d base verts bit-identical; scaled surface tail bit-identical: %s."%(tb['bit_identical'],tb['base_tail_verts'],'YES' if tb['surface_tail_bit_identical'] else 'NO'),True),
    ("Silhouette changed: "+", ".join("%s %.3f %%"%(k,v['pct']) for k,v in sil.items())+".   RSA agreement %.3f %%."%A['scale_family_agreement_pct'],False)]
sheet("Saurin — 6. change accounting"+T,
 ["Colour = distance from the accepted convergence surface (grey < 0.1 mm → yellow → red ≥ 8 mm)."],
 [('Heat','H15')],[('Front 3/4 head','hF34'),('Profile head','hP'),('Orbit close','oC'),('Whole body','front34')],400,'v16_06_accounting.jpg',lambda r,c:D+'H15_%s.png'%c,extra=ex)
