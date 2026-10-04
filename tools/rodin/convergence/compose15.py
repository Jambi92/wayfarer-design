import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json, os, numpy as np
D='/tmp/claude-0/rodin/c11/'; C10='/tmp/claude-0/rodin/c10/'; O=D+'sheets15/'; os.makedirs(O,exist_ok=True)
A=json.load(open(D+'acct14.json')); T=" — CONVERGENCE (DIAGNOSTIC)"
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def sheet(title,sub,rows,cols,cell,out,fn,lw=190,capfont=18):
    W=lw+len(cols)*(cell+14)+10; top=96+28*len(sub)+34; img=Image.new('RGB',(max(W,1400),top+len(rows)*(cell+14)+20),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(30,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,60+28*i),s,font=F(19),fill=SUB)
    for c,(cl,ck) in enumerate(cols): d.text((lw+c*(cell+14)+4,top-28),cl,font=F(capfont,True),fill=SUB)
    for r,(rl,rk) in enumerate(rows):
        y=top+r*(cell+14); d.multiline_text((16,y+cell//2-30),rl,font=F(20,True),fill=TXT,spacing=6)
        for c,(cl,ck) in enumerate(cols):
            p=fn(rk,ck)
            if p and os.path.exists(p): img.paste(tile(p,cell),(lw+c*(cell+14),y))
    img.save(O+out,quality=90); print(out,img.size)
BA=[('Cleanup\n(before)','Y13'),('Convergence\n(after)','Y14')]; f=lambda r,c:D+'%s_%s.png'%(r,c)
sil=A['silhouette_changed_pct']; e=A['envelope_cm']
sheet("Saurin convergence — 1. whole organism, neutral, identical five cameras"+T,
 ["Changed: orbital/postorbital planes, tail mass distribution, structural scale order, forearm seam. Height/width/depth %.2f/%.2f/%.2f cm (before %.2f/%.2f/%.2f)."%(e['height'][1],e['width'][1],e['depth'][1],e['height'][0],e['width'][0],e['depth'][0]),
  "Silhouette pixels changed: "+", ".join("%s %.2f %%"%(k,v) for k,v in sil.items())+" (tail mid-section + scale relief)."],BA,[(l,v) for v,l in VIEWS],430,'v15_01_whole_organism.jpg',f)
sheet("Saurin convergence — 2. orbital integration (neutral, identical cameras)"+T,
 ["The round postorbital column (and the knob where it met the brow crest) is replaced by a raised PLANE-CHANGE ridge: a crisp edge with a broad base drawn on the lateral skull from the brow,",
  "behind the orbit, down and back along the jugal toward the quadrate. Brow crest tapers further toward its rear; lateral shelf and orbital-temporal platform flattened. Eye, aperture, rostrum, jaw, +8 % scale unchanged."],
 BA,[('Front','hF'),('Profile','hP'),('Front 3/4','hF34'),('Rear 3/4','hR34'),('Top','hT'),('Orbit close','oC'),('Orbit close profile','oP')],330,'v15_02_orbital.jpg',f,capfont=16)
sheet("Saurin convergence — 3. orbital curvature diagnostic (base, no scales)"+T,
 ["Mean curvature on the anatomical base: red = convex, blue = concave. Before: a closed red blob behind/above the orbit (boss). After: long red EDGE lines (plane changes)",
  "running brow → postorbital → jugal, with neutral planes between them; no isolated convex island."],
 [('Before','K13'),('After','K14')],[('Front 3/4','hF34'),('Profile','hP'),('Orbit close','oC'),('Top','hT')],400,'v15_03_orbital_curvature.jpg',f)
sheet("Saurin convergence — 4. tail before / after (neutral, identical cameras)"+T,
 ["Mass now sheds continuously from pelvis to tip: intermediate mass carried farther distally, no 'thick root + thin appendage'. Root, tip, length, path unchanged (tip shift %.2f cm)."%A['tail_tip_shift_cm']],
 BA,[('Profile','tprof'),('Top','ttop'),('Rear 3/4','tr34'),('Tail profile','tailP')],430,'v15_04_tail.jpg',f)
# 5 taper graph
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s0=np.load(D+'sl13.npy'); s1=np.load(D+'sl14.npy'); ok=~np.isnan(s0[:,1])&~np.isnan(s1[:,1])
fig,ax=plt.subplots(1,3,figsize=(21,6),dpi=110); fig.patch.set_facecolor('#1b1b20')
for x in ax: x.set_facecolor('#24242a'); x.tick_params(colors='#ccc'); [q.set_color('#666') for q in x.spines.values()]; x.grid(color='#3a3a44')
xn0=(s0[ok,0])/98.0
ax[0].plot(s0[ok,0]/98,s0[ok,1],color='#e07a5f',lw=2.2,label='cleanup (before)'); ax[0].plot(s1[ok,0]/98,s1[ok,1],color='#81b29a',lw=2.2,label='convergence (after)')
ax[0].set_title('Cross-sectional area vs normalized length (0 = tip, 1 = root s=98 cm)',color='w',fontsize=11); ax[0].set_ylabel('cm²',color='#ccc'); ax[0].legend(facecolor='#2a2a30',labelcolor='w')
ax[1].plot(s0[ok,0]/98,np.sqrt(s0[ok,1]/np.pi),color='#e07a5f',lw=2.2); ax[1].plot(s1[ok,0]/98,np.sqrt(s1[ok,1]/np.pi),color='#81b29a',lw=2.2); ax[1].set_title('Equivalent radius',color='w'); ax[1].set_ylabel('cm',color='#ccc')
from scipy.ndimage import uniform_filter1d
r0=np.gradient(s0[ok,1],s0[ok,0]); r1=np.gradient(s1[ok,1],s1[ok,0])
ax[2].plot(s0[ok,0]/98,uniform_filter1d(r0,5),color='#e07a5f',lw=2); ax[2].plot(s1[ok,0]/98,uniform_filter1d(r1,5),color='#81b29a',lw=2); ax[2].set_title('Area-loss rate dA/ds (cm²/cm)',color='w')
for x in ax: x.axvspan(98/98,1.12,color='#555',alpha=0.35); x.axvspan(0,12/98,color='#555',alpha=0.35); x.set_xlabel('normalized length from tip',color='#ccc')
plt.tight_layout(); plt.savefig(D+'taper14.png',facecolor=fig.get_facecolor()); plt.close()
g=Image.open(D+'taper14.png').convert('RGB'); img=Image.new('RGB',(g.width+40,g.height+520),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin convergence — 5. normalized tail cross-section / taper comparison"+T,font=F(30,True),fill=TXT)
t=A['tail']; d.text((20,58),"True planar sections perpendicular to the fixed axis. Root (s ≥ 98 cm) and terminal tip (s ≤ 12 cm) unchanged; loss rate prescribed: slow at the tip, long even plateau, gently rising into the root.",font=F(18),fill=SUB)
img.paste(g,(20,100)); y=110+g.height
d.text((20,y),"99th-pct area-loss rate: %.1f → %.1f cm²/cm   |   volume s12–98: %d → %d cm³   |   root area s=100: %.0f → %.0f cm²   |   tip area s=8: %.1f → %.1f cm²"%(t['peak_dAds_before'],t['peak_dAds_after'],t['volume_s12_98_before'],t['volume_s12_98_after'],t['root_area_s100_before'],t['root_area_s100_after'],t['tip_area_s8_before'],t['tip_area_s8_after']),font=F(19,True),fill=TXT); y+=40
d.text((20,y),"normalized position (tip→root)   "+"  ".join("%4.1f"%r['norm_from_tip'] for r in A['tail_table']),font=F(18,True),fill=SUB); y+=30
d.text((20,y),"area before (cm²)                     "+"  ".join("%5.0f"%r['area_before'] for r in A['tail_table']),font=F(18),fill=SUB); y+=28
d.text((20,y),"area after  (cm²)                     "+"  ".join("%5.0f"%r['area_after'] for r in A['tail_table']),font=F(18),fill=SUB)
img.save(O+'v15_05_tail_taper.jpg',quality=92); print('v15_05')
sz=A['structural_scale_size_cm']
sheet("Saurin convergence — 6. structural scale hierarchy, whole body"+T,
 ["Two orders: fine/flexible fields (median spacing %.2f cm) everywhere that bends, expresses or contacts; a larger structural/scute order (median %.2f → %.2f cm, up to %.1f cm)"%(sz['fine_p50'],sz['structural_p50_before'],sz['structural_p50_after'],sz['structural_p99_after']),
  "on cranium, nape, upper dorsal thorax, dorsal forearm, dorsal shin and dorsal tail. Bottom row: scale-size map (blue fine → orange/red large)."],
 [('Neutral','Y14'),('Scale size','SZ14')],[('Profile','profile'),('Rear 3/4','rear34'),('Head','hF34'),('Tail','tailP')],430,'v15_06_scale_hierarchy.jpg',f)
sheet("Saurin convergence — 7/8. head, nape and dorsal-thorax scale hierarchy"+T,
 ["Cranial plates follow the brow → temporal → jugal flow; fine expressive units stay around the eye aperture, lids and mouth margin; nape and upper back carry the larger order, grading into the fine neck and flank fields."],
 BA,[('Head','hd'),('Head 3/4','hF34'),('Nape','nape'),('Dorsal thorax','back')],430,'v15_07_head_dorsal_scales.jpg',f)
sheet("Saurin convergence — 9. tail scale-size gradient"+T,
 ["Structural scales ~3.6 cm at the root shrink smoothly to ~1 cm distally (smoothed size field, random Poisson layout: no rows, no belt); the gradient follows the corrected taper rather than faking it."],
 BA,[('Whole tail','tailP'),('Tail close','tsc'),('Top','ttop'),('Rear 3/4','tr34')],430,'v15_08_tail_scales.jpg',f)
sheet("Saurin convergence — 10. articulation zones stay fine"+T,
 ["Large scales do not enter flexion fields: elbow, knee, axilla, wrist, throat and the eyelids keep the fine articulation/expressive units."],
 [('After','Y14')],[('Elbow','elbow'),('Knee','knee'),('Axilla','axilla'),('Wrist','wrist'),('Throat','throat'),('Eyelids','oC')],360,'v15_09_articulation.jpg',f)
VAR=[('baseline','Neutral naked'),('minimal_ridges','Minimal ridges'),('low_hornlets','Low hornlets'),('swept_paired','Swept-back\npaired'),('mixed_asym','Mixed / asym.'),('crest','Restrained\ncrest')]
sheet("Saurin convergence — 11/12. neutral naked skull + display family on the final skull"+T,
 ["Row 1 is the neutral naked skull after all surface work (passes the orbital tests on its own). All six rebuilt on the converged skull with identical cameras; displays do not repair the skull."],
 [(l,v) for v,l in VAR],[('Front','hF'),('Profile','hP'),('Front 3/4','hF34'),('Rear 3/4','hR34'),('Top','hT'),('Attachment','att')],320,'v15_10_display_family.jpg',lambda r,c:D+'dv/DN_%s_%s.png'%(r,c),lw=200)
sheet("Saurin convergence — 13. swept-back display attachment before / after"+T,
 ["Base radius 1.30 → 0.98 and the root now starts ~1.7 cm further forward lying along the cranial surface (no bulb/socket); tip position and length unchanged."],
 [('Before','C'),('After','N')],[('Profile','hP'),('Rear 3/4','hR34'),('Attachment','att'),('Top','hT')],400,'v15_11_swept_attachment.jpg',lambda r,c:(C10 if r=='C' else D)+'dv/DN_swept_paired_%s.png'%c)
sheet("Saurin convergence — 14. forearm seam repair"+T,
 ["Old forearm zip ring (u ≈ 110): sliver/folded triangles collapsed link-safely",
  "and the narrow band smoothed (%s); watertight and manifold. Scale field carried across the repaired band."%("max %.2f mm"%A['base_movement_by_zone'].get('forearm seam repair',{'max_mm':0})['max_mm'])],
 BA,[('Forearm seam','fa')],520,'v15_12_forearm_seam.jpg',f)
PK=[('P1_umber_mottled','P1'),('P2_slate_banded','P2'),('P7_bluegray_broken','P7'),('P9_green_mixed_asym','P9')]
sheet("Saurin convergence — 15. Gate 8 phenotype survival"+T,
 ["Same phenotype code, cameras and lights on the converged geometry and scale hierarchy (fields rebuilt). Tail pattern flow continuous; facial pattern follows the new orbital planes."],
 [(n,k) for k,n in PK],[('Front 3/4','f34'),('Rear 3/4','r34'),('Head 3/4','hF34'),('Head profile','hP'),('Tail','tailP')],330,'v15_13_gate8.jpg',lambda r,c:D+'r8/A_%s_%s.png'%(r,c),lw=110)
sheet("Saurin convergence — 16. Regional Scale Architecture map before / after"+T,
 ["Family identities unchanged (agreement %.2f %%); the structural family now carries the second, larger order inside it."%A['scale_family_agreement_pct']],
 [('Before','M13'),('After','M14')],[('Profile','profile'),('Head','hF34'),('Tail','tailP'),('Rear 3/4','rear34')],430,'v15_14_rsa_map.jpg',lambda r,c:(C10 if r=='M13' else D)+'%s_%s.png'%(r,c))
z=A['base_movement_by_zone']; img=Image.new('RGB',(20+5*(430+14)+20,430+520),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin convergence — 17. geometry-change accounting and silhouette"+T,font=F(30,True),fill=TXT)
d.text((20,58),"Colour = distance from the cleanup surface (grey < 0.1 mm → yellow → red ≥ 12 mm; includes the new scute relief).",font=F(19),fill=SUB)
for i,(v,vl) in enumerate([('front34','Front 3/4'),('rear34','Rear 3/4'),('profile','Profile'),('hF34','Head'),('fa','Forearm seam')]):
    x=20+i*444; img.paste(tile(D+'H14_%s.png'%v,430),(x,120)); d.text((x+4,96),vl,font=F(18,True),fill=SUB)
y=570; d.text((20,y),"%-30s %8s %9s %8s %8s %8s"%("zone (base mesh)","verts","median","p95","p99","max mm"),font=F(18,True),fill=TXT); y+=30
for k,v in z.items(): d.text((20,y),"%-30s %8d %9.2f %8.2f %8.2f %8.2f"%(k,v['verts'],v['median_mm'],v['p95_mm'],v['p99_mm'],v['max_mm']),font=F(17),fill=SUB); y+=26
t=A['topology']; d.text((20,y+10),"Watertight: %d boundary, %d non-manifold, %s component(s). Silhouette changed: "%(t['boundary_edges'],t['nonmanifold_edges'],t['components'])+", ".join("%s %.2f%%"%(k,v) for k,v in sil.items()),font=F(18,True),fill=TXT)
img.save(O+'v15_15_accounting.jpg',quality=90); print('v15_15')
