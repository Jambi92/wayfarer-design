import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import BG,PANEL,TXT,SUB,F
from PIL import Image, ImageDraw
import numpy as np, json, os
D='/tmp/claude-0/rodin/v4/'; R=D+'R/'; O=D+'sheets20/'; os.makedirs(O,exist_ok=True)
T=" (DIAGNOSTIC / NOT FINAL)"
RED=(235,110,100); YEL=(235,200,90); GRN=(120,200,120)
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def gtile(p,cell,body_px=64,sil=False):
    im=Image.open(p).convert('RGBA'); a=np.array(im)[:,:,3]; ys,xs=np.where(a>20)
    y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max(); h=y1-y0; s=max(h,x1-x0)*1.08; cy=(y0+y1)/2; cx=(x0+x1)/2
    im=im.crop((int(cx-s/2),int(cy-s/2),int(cx+s/2),int(cy+s/2))); n=max(8,int(round(body_px*s/h)))
    sm=im.resize((n,n),Image.LANCZOS)
    if sil:
        arr=np.array(sm); arr[...,:3]=232; sm=Image.fromarray(arr)
    sm=sm.resize((cell,cell),Image.NEAREST); bg=Image.new('RGB',sm.size,PANEL); bg.paste(sm,(0,0),sm); return bg
def sheet(title,sub,rows,cols,cell,out,fn,lw=230,notes=None,tf=tile,nw=380):
    W=lw+len(cols)*(cell+12)+10+(nw if notes else 0); top=92+26*len(sub)+32
    img=Image.new('RGB',(max(W,1580),top+len(rows)*(cell+12)+20),BG); d=ImageDraw.Draw(img)
    d.text((20,14),title,font=F(28,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,56+26*i),s,font=F(18),fill=SUB)
    for c,(cl,ck) in enumerate(cols): d.text((lw+c*(cell+12)+4,top-26),cl,font=F(17,True),fill=SUB)
    for r,(rl,rk) in enumerate(rows):
        y=top+r*(cell+12); d.multiline_text((14,y+8),rl,font=F(17,True),fill=TXT,spacing=5)
        for c,(cl,ck) in enumerate(cols):
            p=fn(rk,ck)
            if isinstance(p,tuple): img.paste(p[0](*p[1:]),(lw+c*(cell+12),y))
            elif p and os.path.exists(p): img.paste(tf(p,cell),(lw+c*(cell+12),y))
        if notes and rk in notes:
            st,txt=notes[rk]; col={'PASS':GRN,'CONSTRAIN':YEL,'FAIL':RED}.get(st,TXT)
            x0=lw+len(cols)*(cell+12)+6; d.text((x0,y+6),st,font=F(20,True),fill=col); d.multiline_text((x0,y+36),txt,font=F(14),fill=SUB,spacing=4)
    img.save(O+out,quality=88); print(out,img.size)
f=lambda r,c:R+'%s_%s.png'%(r,c)
CAND=[('Male /\nreference','m_ref'),('A  structural\ntrunk +10 %\npelvis +5.5 %','A'),('B  A + ventral\nfullness, subtle\n(1.6 cm)','B'),('C  A + ventral\nfullness, strong\n(3.0 cm)','C'),
      ('D  A + paired\nbreasts 3.8 cm\nCOMPARISON ONLY\nnot canon','D'),('E  A + coelomic\nbody wall\n(additional)','E'),('E+B  body wall\n+ subtle ventral','E2')]
BV=[('Front','front'),('Profile','profile'),('Rear 3/4','rear34'),('Torso 3/4','tq')]
# 1. A/B/C/D(/E) identical cameras, columns = candidates
sheet("Saurin female Pass 2 — 1. candidates, identical cameras"+T,["Equal stature 187.9 cm, Balanced frame, reference composition, same skull/limbs/tail. Male reference in the first column.",
 "D is a comparison only and is NOT canon authorization for mammary anatomy (no nipples modelled). E / E+B is an additional non-mammalian candidate."],
 [(l,v) for l,v in BV],[('Male ref','m_ref'),('A structural','A'),('B subtle ventral','B'),('C strong ventral','C'),('D breasts (compar.)','D'),('E body wall','E'),('E+B','E2')],236,'v20_01_candidates_identical_cameras.jpg',lambda r,c:f(c,r),lw=110)
# 2. male vs each candidate, whole body rows
sheet("Saurin female Pass 2 — 2. male vs each candidate, whole body"+T,["Rows = candidates, columns = identical cameras."],
 CAND,BV[:3]+[('Torso profile','tp'),('Torso front','tf')],250,'v20_02_male_vs_each.jpg',f,lw=200)
# 3. structural isolation
ST1=[('Male /\nreference','m_ref'),('Pass-1 female\ntrunk +6 %\npelvis +3 %','p1'),('Trunk +10 %\nonly','a_tr'),('Pelvic band\n+5.5 % only','a_pv'),('A = trunk +10 %\n+ pelvis +5.5 %','A')]
sheet("Saurin female Pass 2 — 3. structural candidate in isolation (Q4, Q5)"+T,["Does the stronger trunk / pelvis tendency read on its own? Identical cameras, no soft-tissue change."],
 ST1,BV[:3]+[('Torso front','tf')],270,'v20_03_structural_isolation.jpg',f,lw=200)
# 4. torso close views (surface mesh, full scale detail)
TV=[('Torso 3/4','sq'),('Torso profile','sp'),('Torso front','sf')]
sheet("Saurin female Pass 2 — 4. torso close views (scaled surface)"+T,["Soft tissue is a smooth shell-following displacement: the ventral / transitional scale fields deform with it and keep their layout.",
 "D sits on the thoracic shell as two separate mounds; B/C/E stay continuous across the midline and fade into the flanks."],
 CAND,TV,340,'v20_04_torso_close.jpg',f,lw=200)
# 5. gameplay distance
GV=[('Front ~64 px','front'),('Profile ~64 px','profile'),('Rear 3/4 ~64 px','rear34')]
def gfn(r,c):
    if c.startswith('s_'): return (lambda: gtile(R+'%s_%s.png'%(r,c[2:]),220,64,True),)
    return (lambda: gtile(R+'%s_%s.png'%(r,c),220,64),)
sheet("Saurin female Pass 2 — 5. gameplay-distance readability"+T,["Each body downsampled to ~64 px standing height (a figure at roughly 25-30 m on a 1080p screen), shown enlarged without smoothing,",
 "then as flat silhouettes. Only proportion and silhouette survive at this size; surface detail does not."],
 CAND,GV+[('Front silhouette','s_front'),('Profile silhouette','s_profile')],220,'v20_05_gameplay_distance.jpg',gfn,lw=200)
# 6. pelvis / sacrum / tail root
PV=[('Rear 3/4','pR34'),('Profile','pP'),('Front','pF'),('Ventral (from below)','pV')]
sheet("Saurin female Pass 2 — 6. pelvis / sacrum / tail root, candidate A"+T,["Pelvic band +5.5 % is a skeletal/internal-capacity widening inside the +-7 % species bound: +1.1 cm external width at the pelvis,",
 "no lateral hip flare, no paired buttocks, no cleft; sacral platform, posterior mass and tail root identical. Ventral pelvic field unchanged (no external sex anatomy)."],
 [('Male','m_ref'),('A','A'),('C','C')],PV,330,'v20_06_pelvis_tail_root.jpg',f,lw=120)
# 7. overlap / anti-stereotype
FS=json.load(open(D+'sweep2.json'))
def dw(k): return FS[k]['metrics']['thorax_d_over_w']
NT={
 'c_n':('CONSTRAIN','Narrow + C: thoracic depth/width %.3f > 1.00.\nFullness counts against the thoracic\nshell bound: clamped to ~2.0 cm on Narrow.'%dw('c_n')),
 'c_bm':('PASS','Broad + high muscle + C: valid\n(d/w %.3f; tail RSI 0.83 >= 0.75)'%dw('c_bm')),
 'c_flo':('PASS','fat low + C: fullness is not fat;\nit stays when fat is minimal'),
 'c_fhi':('PASS','fat high + C: d/w %.3f; fat adds\nventral/flank/caudal volume, no hourglass'%dw('c_fhi')),
 'c_tall':('PASS','208 cm Broad high-muscle female'),
 'c_t80':('PASS','Broad + 80 %% tail: +%.1f deg (guard 3)'%FS['c_t80']['derived']['d_lean']),
 'c_t55':('PASS','55 % tail, coupled base'),
 'e_n':('PASS','Narrow + E+B: d/w %.3f'%dw('e_n')),
 'e_bm':('PASS','Broad + high muscle + E+B'),
 'e_flo':('PASS','fat low + E+B'),'e_fhi':('PASS','fat high + E+B: d/w %.3f'%dw('e_fhi')),
 'm_sn':('PASS','168 cm Narrow low-muscle male'),
 'm_ovB':('PASS','male with trunk +10 %, pelvis +5.5 %,\nfullness 1.6 cm: geometrically identical\nto female B (overlap, not a preset)'),
 'm_ovE':('PASS','male with half body-wall fullness\ninside the female range'),
 'f_lo':('PASS','female at the low end of every\ntendency = identical to the male mean'),
 'f_mid':('PASS','ordinary female individual:\ntrunk +4 %, pelvis +2 %, fullness 1.6 cm'),
 'c_over':('CONSTRAIN','fullness requested 4.5 cm: d/w %.3f\npasses, but above the 3.0 cm diagnostic\nceiling - clamp proposed'%dw('c_over')),
 'c_fhi_over':('CONSTRAIN','fat high + 4.5 cm fullness:\nd/w %.3f > 1.00 - clamped'%dw('c_fhi_over')),
 't16':('CONSTRAIN','female individual above a +10 % mean:\nclamped at the species bound. With the\nmean AT the bound, half the female\ndistribution clamps (see report).'),
}
def stress(keys,out,title,sub):
    sheet(title,sub,[(FS[k]['label'].replace(', ','\n',2),k) for k in keys],BV,230,out,f,lw=250,notes={k:NT[k] for k in keys},nw=400)
stress(['c_n','c_bm','c_flo','c_fhi','c_tall','c_t80','c_t55'],'v20_07_stress_C.jpg',"Saurin female Pass 2 — 7. frame / composition / tail stress on C"+T,
 ["Strongest ventral-fullness candidate (A + 3.0 cm). Frame, muscle, fat, stature and tail stay independent of sex."])
stress(['e_n','e_bm','e_flo','e_fhi','m_ovE','m_ovB','f_lo','f_mid','m_sn','c_over','c_fhi_over','t16'],'v20_08_stress_E_overlap.jpg',"Saurin female Pass 2 — 8. E+B stress, male/female overlap, ceilings"+T,
 ["Sex shifts soft distributions only: males can sit inside the female range and females at the male mean. Requests beyond a ceiling are CONSTRAINed."])
