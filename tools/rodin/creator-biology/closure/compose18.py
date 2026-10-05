import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import BG,PANEL,TXT,SUB,F
from PIL import Image, ImageDraw
import os, json
O='/tmp/claude-0/rodin/v2/sheets18/'; os.makedirs(O,exist_ok=True)
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def sheet(title,sub,rows,cols,cell,out,fn,lw=200):
    W=lw+len(cols)*(cell+12)+20; top=92+26*len(sub)+30
    img=Image.new('RGB',(max(W,1300),top+len(rows)*(cell+12)+20),BG); d=ImageDraw.Draw(img)
    d.text((20,14),title,font=F(28,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,56+26*i),s,font=F(18),fill=SUB)
    for c,(cl,ck) in enumerate(cols): d.text((lw+c*(cell+12)+4,top-26),cl,font=F(17,True),fill=SUB)
    for r,(rl,rk) in enumerate(rows):
        y=top+r*(cell+12); d.multiline_text((14,y+8),rl,font=F(17,True),fill=TXT,spacing=5)
        for c,(cl,ck) in enumerate(cols):
            p=fn(rk,ck)
            if os.path.exists(p): img.paste(tile(p,cell),(lw+c*(cell+12),y))
    img.save(O+out,quality=88); print(out,img.size)
C=json.load(open('claws.json'))
sheet("Saurin creator-biology closure — claw length diagnostic (DIAGNOSTIC)",
 ["Each claw stretched along its own axis from its base ring at reference curvature (derived; hands/feet not rebuilt).",
  "Foot-claw tip height above the ground: x0.8 %.2f, x1.0 %.2f, x1.15 %.2f, x1.3 %.2f cm  ->  tips reach the ground at ~+15 %%."%(C['k0.80']['foot_claw_min_u'],C['k1.00']['foot_claw_min_u'],C['k1.15']['foot_claw_min_u'],C['k1.30']['foot_claw_min_u']),
  "Grasp/footwear/glove compatibility cannot be validated without a grip pose and equipment: no numeric creator range canonized."],
 [('Length x0.80','080'),('Reference','100'),('Length x1.15','114'),('Length x1.30','130')],[('Foot side','fside'),('Foot 3/4','ftop'),('Hand','hfront'),('Fingertips','hside')],300,'v18_01_claw_length.jpg',lambda r,c:'CL_%s_%s.png'%(r,c))
sheet("Saurin creator-biology closure — orbital placement attempt (DIAGNOSTIC)",
 ["Each orbit moved with a smooth falloff in the skull frame: spacing -3 % / +3 %, vertical +0.25 / -0.25 cm.",
  "The falloff drags the brow rim and postorbital planes with the orbit instead of re-forming them, so the test cannot",
  "validate placement cleanly: orbital placement stays LOCKED, numeric tolerance OPEN."],
 [('Reference','ref'),('Spacing -3 %','sp_m3'),('Spacing +3 %','sp_p3'),('Up 0.25 cm','up'),('Down 0.25 cm','dn')],[('Front','hF'),('Front 3/4','hF34'),('Top','hT')],300,'v18_02_orbital_placement.jpg',lambda r,c:'OR_%s_%s.png'%(r,c))
