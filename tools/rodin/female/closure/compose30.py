import sys; sys.path.insert(0,'/tmp/claude-0/rodin/v4'); sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
import compose20 as C   # reuses tile / gtile / sheet helpers (runs pass-2 sheets into v4, harmless)
from PIL import Image
import json, os
D='/tmp/claude-0/rodin/v5/'; R=D+'R/'; C.O=D+'sheets30/'; os.makedirs(C.O,exist_ok=True)
C.T=T=" (CLOSURE PACKAGE)"
FS=json.load(open(D+'sweep3.json')); SG=json.load(open(D+'strain.json')); CL=json.load(open(D+'clamp.json')); TS=json.load(open(D+'torsosil.json'))
f=lambda r,c:R+'%s_%s.png'%(r,c); sheet=C.sheet
def m(k,key): return FS[k]['metrics'][key]
def dw(k): return m(k,'thorax_d_over_w')
def dl(k): return FS[k]['derived']['d_lean']
def rsi(k): return FS[k]['derived']['tail_RSI_n']
BV=[('Front','front'),('Profile','profile'),('Rear 3/4','rear34'),('Torso 3/4','tq')]
sheet("Saurin female — C1. male reference vs final reference female"+T,["Equal stature 187.9 cm, Balanced, reference composition. Final reference female = lower trunk +10 %, pelvic band +5.5 %, coelomic body wall (E) 2.0 cm,",
 "ventral fullness (B) 1.6 cm. Pass-1 female shown for comparison. No breasts, no hourglass, no hip flare; skull, limbs, tail identical."],
 [('Male /\nreference','m_ref'),('Pass-1 female\n(superseded)','p1'),('Final reference\nfemale','fref')],BV+[('Torso front','tf')],300,'v21_01_male_vs_final_reference.jpg',f,lw=200)
sheet("Saurin female — C2. male mean vs female sampling centre"+T,["The female sampling centre (trunk +7 %, pelvis +5.5 %, E 2.0 cm, B 1.6 cm) is the typical generated female; the +10 % reference is a valid individual above it."],
 [('Male mean','m_ref'),('Female\nsampling centre','fcen')],BV+[('Torso profile','tp'),('Torso front','tf')],270,'v21_02_male_mean_vs_female_centre.jpg',f,lw=180)
sheet("Saurin female — C3. female reference and sampling centre in isolation"+T,["Same cameras. The two differ only in lower-trunk length (+10 % vs +7 %)."],
 [('Final reference\nfemale (+10 %)','fref'),('Female sampling\ncentre (+7 %)','fcen')],BV+[('Torso profile','tp'),('Torso front','tf')],270,'v21_03_female_reference_and_centre.jpg',f,lw=180)
TV=[('Torso 3/4','sq'),('Torso profile','sp'),('Torso front','sf')]
TR=[('Male','m_ref'),('Female centre','fcen'),('Female reference','fref'),('Female ref,\nNarrow','fr_n'),('Female ref,\nfat high','fr_fhi')]
sheet("Saurin female — C4. torso close views (scaled surface)"+T,["E + B is one continuous shell-following field: ventral fullness crosses the midline, the body wall fills the sub-costal waist.",
 "No paired forms, no mammary read, no hourglass - the waist gets fuller, not narrower."],TR,TV,330,'v21_04_torso_close.jpg',f,lw=170)
PV=[('Rear 3/4','pR34'),('Profile','pP'),('Front','pF'),('Ventral (from below)','pV')]
sheet("Saurin female — C5. pelvis / sacrum / tail root"+T,["Pelvic band +5.5 %% = +%.1f cm external at the pelvis. No hip flare, no paired buttocks, no cleft; sacral platform, posterior mass and tail root unchanged."%(m('fref','pelvis_w')-m('m_ref','pelvis_w')),
 "Ventral pelvic field unchanged: no external sex anatomy is modelled."],[('Male','m_ref'),('Female centre','fcen'),('Female ref.','fref')],PV,330,'v21_05_pelvis_tail_root.jpg',f,lw=150)
s=SG['final_ref E2.0+B1.6']; c3=SG['C-level B3.0 + E2.0']; ft=SG['composition fat +1 (existing control, for scale)']
sheet("Saurin female — C6. scale-surface verification after deformation"+T,["Close views of the ventrolateral field where E + B act hardest. Edge stretch on the scaled surface (E+B only): 1st-99th pct %.3f-%.3f, max %.3f; flipped faces %d."%(s['edge_p01'],s['edge_p99'],s['edge_max'],s['flipped']),
 "C-level (3.0 cm): 99th pct %.3f, max %.3f, flipped %d. Speckle in the fat-high rows comes from the existing diagnostic fat tool (also on the male, last row; 99th pct %.3f), not from E + B."%(c3['edge_p99'],c3['edge_max'],c3['flipped'],ft['edge_p99'])],
 TR+[('Male, fat high\n(control: existing\nfat tool)','m_fhi')],[('Ventrolateral close','zS'),('Ventral close','zV')],420,'v21_06_scale_surface.jpg',f,lw=170)
FC=[('Narrow','fr_n'),('Balanced','fref'),('Broad','fr_b'),('Muscle low','fr_mlo'),('Muscle high','fr_mhi'),('Fat low','fr_flo'),('Fat high','fr_fhi')]
sheet("Saurin female — C7. frame / composition stress on the reference female"+T,["d/w (bound 0.80-1.00): "+', '.join('%s %.3f'%(l,dw(k)) for l,k in FC)+".",
 "E + B persist at fat low (not fat) and stay continuous at fat high (no hourglass, no mammary read). Fat is the generic fat control, unchanged."],
 [('Front','front'),('Profile','profile'),('Torso 3/4','tq')],FC,250,'v21_07_frame_composition.jpg',lambda r,c:R+'%s_%s.png'%(c,r),lw=110)
NT={
 'fr_h168':('PASS','168 cm: all proportions isometric'),'fr_h208':('PASS','208 cm: all proportions isometric'),
 'fr_t55':('PASS','55 %% tail, coupled base 0.83\nRSI %.2f, lean %+.1f deg'%(rsi('fr_t55'),dl('fr_t55'))),
 'fr_t78':('PASS','78 %% tail, coupled base 1.15\nRSI %.2f (<=1.20), lean %+.1f deg (<=3)\nnear both limits, as for the male'%(rsi('fr_t78'),dl('fr_t78'))),
 'fr_b80':('PASS','Broad + 80 %% tail, base 1.16\nRSI %.2f, lean %+.1f deg'%(rsi('fr_b80'),dl('fr_b80'))),
 'm_in':('PASS','male at the female sampling centre:\ngeometrically IDENTICAL to the\nfemale centre (overlap, not a preset)'),
 'fcen':('PASS','female sampling centre'),
 'm_mid':('PASS','ordinary male inside the female range\n(trunk +5, pelvis +3, E 1.0, B 0.8)'),
 'f_near':('PASS','female near the male mean\n(trunk +2, pelvis +1, E 0.5, B 0.4)'),
 'f_mean':('PASS','female at the male mean:\nidentical to the male reference'),
 'm_ref':('PASS','male mean'),
 'as_bm':('PASS','Broad + high-muscle female\n(d/w %.3f, RSI %.2f)'%(dw('as_bm'),rsi('as_bm'))),
 'as_nl':('PASS','Narrow + low-muscle female (d/w %.3f)'%dw('as_nl')),
 'fr_fhi':('PASS','high-fat female: d/w %.3f,\nno hourglass, no paired forms'%dw('fr_fhi')),
 'fr_flo':('PASS','low-fat female: E + B remain;\nnot a "reduced male"'),
 'as_mn':('PASS','Narrow male with the female-shifted\nvalues: valid (d/w %.3f), identical\nto the Narrow reference female'%dw('as_mn')),
 'cl_nC':('CONSTRAIN','Narrow + C 3.0 cm requested:\nd/w %.3f > 1.00'%dw('cl_nC')),
 'cl_nCk':('PASS','-> ventral fullness clamped to\n%.1f cm (d/w %.3f)'%(CL['Narrow'],dw('cl_nCk'))),
 'cl_nf':('CONSTRAIN','Narrow + fat high + B 1.6 requested:\nd/w %.3f > 1.00 (the centre value\nitself clamps on this combination)'%dw('cl_nf')),
 'cl_nfk':('PASS','-> ventral fullness clamped to\n%.1f cm (d/w %.3f)'%(CL['Narrow + fat high'],dw('cl_nfk'))),
 'cl_fC':('PASS','C 3.0 cm on fat high (Balanced):\nvalid individual (d/w %.3f)'%dw('cl_fC')),
 'cl_t16':('CONSTRAIN','trunk +16 % requested:\nclamped to the +10 % species bound'),
}
import textwrap
def lab(k): return '\n'.join(textwrap.wrap(FS[k]['label'],22))
def stress(keys,out,title,sub,cell=230):
    sheet(title,sub,[(lab(k),k) for k in keys],BV,cell,out,f,lw=260,notes={k:NT[k] for k in keys},nw=380)
stress(['fr_h168','fr_h208','fr_t55','fr_t78','fr_b80'],'v21_08_stature_tail.jpg',"Saurin female — C8. stature and tail extremes"+T,["Stature and tail rules are sex-neutral; existing tail coupling unchanged."])
stress(['m_ref','f_mean','f_near','m_mid','fcen','m_in'],'v21_09_overlap.jpg',"Saurin female — C9. overlap proof"+T,["Sex shifts distribution centres. Males occur inside the female-shifted range; females occur at and near the male mean."])
stress(['as_bm','as_nl','fr_fhi','fr_flo','as_mn','cl_nC','cl_nCk','cl_nf','cl_nfk','cl_fC','cl_t16'],'v21_10_anti_stereotype_clamps.jpg',"Saurin female — C10. anti-stereotype stress and every clamp invoked"+T,
 ["CONSTRAIN = the creator adapts the dependent value (ventral fullness, trunk) and the clamped result is shown on the next row."])
GV=[('Front ~64 px','front'),('Profile ~64 px','profile'),('Rear 3/4 ~64 px','rear34')]
def gfn(r,c):
    if c.startswith('s_'): return (lambda: C.gtile(R+'%s_%s.png'%(r,c[2:]),220,64,True),)
    return (lambda: C.gtile(R+'%s_%s.png'%(r,c),220,64),)
sheet("Saurin female — C11. gameplay distance (accounting only)"+T,["~64 px standing height. Recorded, not optimized: no anatomy was exaggerated for long-range readability.",
 "Front torso waist/shoulder: "+', '.join('%s %.3f'%(l,TS[k]['waist_sh']) for l,k in (('male',"m_ref"),('Pass-1','p1'),('centre','fcen'),('reference','fref')))+"."],
 [('Male','m_ref'),('Pass-1 female','p1'),('Female centre','fcen'),('Female ref.','fref')],GV+[('Front silhouette','s_front'),('Profile silhouette','s_profile')],220,'v21_11_gameplay_accounting.jpg',gfn,lw=180)
