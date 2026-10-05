import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import BG,PANEL,TXT,SUB,F
from PIL import Image, ImageDraw
import json, os
D='/tmp/claude-0/rodin/v3/'; R=D+'R/'; O=D+'sheets19/'; os.makedirs(O,exist_ok=True)
FS=json.load(open(D+'fsweep.json')); T=" (DIAGNOSTIC)"
RED=(235,110,100); YEL=(235,200,90); GRN=(120,200,120)
ST={'a1':('PASS','tallest Broad high-muscle female:\nall tail/balance/head rules hold'),'a2':('PASS','shortest Narrow male: valid'),
 'a5':('PASS','high fat on the female: same\nventral/flank/caudal pattern, no hourglass'),'a6':('PASS','low fat on the female: not a\n"reduced male" - same skeleton'),
 'a7m':('PASS','equal height & frame (180 cm)'),'a7f':('PASS','equal height & frame (180 cm):\ntrunk +1.8 cm is the only change'),
 'a8':('PASS','low-muscle high-fat Narrow male'),'a9':('PASS','female at the species trunk\nhard maximum (+10 %)'),
 'a10':('CONSTRAIN','sex shift may not extend the racial\nenvelope: clamped to +10 %'),'a11':('CONSTRAIN','pelvic width past the +7 % species\nbound: clamped'),
 'f_b80':('PASS','Broad female carries the 80 % tail\n(RSI 1.11, +2.6 deg)'),'f_t78':('PASS','78 % tail, coupled base'),'f_t55':('PASS','55 % tail, coupled base'),
 'm_ov':('PASS','male with trunk +6 % / pelvis +3 %:\ngeometrically IDENTICAL to the female ref'),'f_ov':('PASS','female at the male mean: identical\nto the male reference'),
 'fd_dsw':('PASS','female, swept-back pair'),'fd_dmx':('PASS','female, strong mixed/asymmetric'),'fd_dcr':('PASS','female, restrained crest 2.43 cm'),'fd_d13':('PASS','female, minimal ridges'),'fd_d00':('PASS','female, naked skull')}
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def sheet(title,sub,rows,cols,cell,out,fn,lw=230,notes=None):
    W=lw+len(cols)*(cell+12)+10+(360 if notes else 0); top=92+26*len(sub)+32
    img=Image.new('RGB',(max(W,1300),top+len(rows)*(cell+12)+20),BG); d=ImageDraw.Draw(img)
    d.text((20,14),title,font=F(28,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,56+26*i),s,font=F(18),fill=SUB)
    for c,(cl,ck) in enumerate(cols): d.text((lw+c*(cell+12)+4,top-26),cl,font=F(17,True),fill=SUB)
    for r,(rl,rk) in enumerate(rows):
        y=top+r*(cell+12); d.multiline_text((14,y+8),rl,font=F(17,True),fill=TXT,spacing=5)
        for c,(cl,ck) in enumerate(cols):
            p=fn(rk,ck)
            if p and os.path.exists(p): img.paste(tile(p,cell),(lw+c*(cell+12),y))
        if notes and rk in notes:
            st,txt=notes[rk]; col={'PASS':GRN,'CONSTRAIN':YEL,'FAIL':RED}.get(st,TXT)
            x0=lw+len(cols)*(cell+12)+6; d.text((x0,y+6),st,font=F(20,True),fill=col); d.multiline_text((x0,y+36),txt,font=F(14),fill=SUB,spacing=4)
    img.save(O+out,quality=88); print(out,img.size)
f=lambda r,c:R+'%s_%s.png'%(r,c)
BV=[('Front','front'),('Profile','profile'),('Rear 3/4','rear34'),('Torso 3/4','t34')]
sheet("Saurin female — 1. female reference"+T,["Same species, same frozen racial anatomy. Candidate low dimorphism: lower axial trunk +6 %, skeletal pelvic band +3 %, at equal stature,",
 "frame and composition; head and tail keep the reference absolute size / % H. No breasts, no hourglass, no human hip, no feminized face."],
 [('Female\nreference','f_ref')],BV+[('Head 3/4','hF34')],330,'v19_01_female_reference.jpg',f)
sheet("Saurin female — 2. male vs female, identical cameras"+T,["Equal stature (187.9 cm), Balanced frame, reference composition. The difference is deliberately small: individual variation is larger than the sex shift."],
 [('Male /\nreference','m_ref'),('Female\nreference','f_ref')],BV,380,'v19_02_male_vs_female.jpg',f)
sheet("Saurin female — 3. equal height / equal frame, and deliberate overlap"+T,["Rows 1-2: equal 180 cm, Balanced. Rows 3-4: a male at the female mean trunk/pelvis and a female at the male mean -",
 "the geometry is identical, which is the point: sex shifts a soft distribution, it is not a body preset."],
 [('Male 180 cm','a7m'),('Female 180 cm','a7f'),('Male, trunk +6 %\npelvis +3 %','m_ov'),('Female at the\nmale mean','f_ov')],BV,300,'v19_03_equal_and_overlap.jpg',f,notes={k:ST[k] for k in ('a7m','a7f','m_ov','f_ov')})
FC=[('Narrow','f_n'),('Balanced','f_ref'),('Broad','f_b'),('Muscle low','f_mlo'),('Muscle high','f_mhi'),('Fat low','f_flo'),('Fat high','f_fhi')]
sheet("Saurin female — 4. female frame / composition matrix"+T,["Frame and composition work on the female exactly as on the male (same maps, same rules). High fat = ventral/flank/graded-caudal volume, never an hourglass."],
 [('Front','front'),('Profile','profile'),('Torso 3/4','t34')],FC,250,'v19_04_female_frame_composition.jpg',lambda r,c:R+'%s_%s.png'%(c,r),lw=110)
PV=[('Rear 3/4','pR34'),('Profile','pP'),('Front','pF'),('Ventral (from below)','pV')]
sheet("Saurin female — 5. pelvis / sacrum / tail-root close views"+T,["Posterior mass and sacral-caudal load path unchanged; tail root identical. The +3 % pelvic band adds ~0.6 cm external width with no lateral hip flare,",
 "no buttock and no cleft. The ventral pelvic field is the same closed scale field in both sexes: no external primary-sex anatomy is modelled."],
 [('Male','m_ref'),('Female','f_ref'),('Female Narrow','f_n'),('Female Broad','f_b'),('Female fat high','f_fhi')],PV,300,'v19_05_pelvis_tail_root.jpg',f)
HV=[('Front','hF'),('Profile','hP'),('Front 3/4','hF34'),('Top','hT')]
sheet("Saurin female — 6. naked skull, male vs female"+T,["No first-pass skull dimorphism: the frozen naked skull is valid for both sexes and stays recognizably Saurin without displays."],
 [('Male','m_ref'),('Female','f_ref')],HV,360,'v19_06_naked_skull.jpg',f)
DV=[('Naked','fd_d00'),('Minimal ridges','fd_d13'),('Swept-back pair','fd_dsw'),('Mixed / asym.','fd_dmx'),('Restrained crest','fd_dcr')]
sheet("Saurin female — 7. cranial display family on the female"+T,["Full family available to both sexes with no incidence or size weighting (displays are not sex markers). Display heads joined to the female body at the neck (thin seam)."],
 DV,[('Body 3/4','front34'),('Head 3/4','hF34'),('Profile','hP')],300,'v19_07_female_displays.jpg',f,notes={k:ST[k] for _,k in DV})
TV=[('Profile','profile'),('Rear 3/4','rear34')]
sheet("Saurin female — 8. tail extremes on the female (existing coupling rules)"+T,["Tail rules are sex-neutral: same length envelope, same coupled base, same balance guard."],
 [('Tail 55 %','f_t55'),('Reference','f_ref'),('Tail 78 %','f_t78'),('Broad + 80 %','f_b80')],TV,360,'v19_08_female_tail.jpg',f,notes={k:ST[k] for k in ('f_t55','f_t78','f_b80')})
AS=['a1','a2','a5','a6','a8','a9','a10','a11']
lab={k:v['label'] for k,v in FS.items()}
sheet("Saurin female — 9. anti-stereotype stress matrix"+T,["Attempts to make sex act as a disguised preset. Displays on either sex: sheet 7 (female with strong displays) and the male reference (naked)."],
 [({'a1':'Female:\ntallest + Broad\n+ high muscle','a2':'Male:\nshortest + Narrow','a5':'Female:\nhigh fat','a6':'Female:\nlow fat','a8':'Male: low muscle\n+ high fat\n+ Narrow','a9':'Female:\ntrunk +10 %\n(species max)','a10':'Female:\ntrunk +16 %\n(requested)','a11':'Female:\npelvis +10 %\n(requested)'}[k],k) for k in AS],BV[:3],270,'v19_09_anti_stereotype.jpg',f,notes={k:ST[k] for k in AS})
