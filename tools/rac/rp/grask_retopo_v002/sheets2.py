# sheets2.py CMPDIR EVDIR OUTDIR : v002 density-study comparison sheets (visual + wire) and quad-quality / pole sheets
import sys, os
sys.argv=[sys.argv[0]]+sys.argv[1:]
from PIL import Image, ImageDraw, ImageFont
C,E,O=sys.argv[1],sys.argv[2],sys.argv[3]; os.makedirs(O,exist_ok=True)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20); FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',28)
def load(p,w):
    im=Image.open(p).convert('RGB'); h=int(im.height*w/im.width); return im.resize((w,h))
def sheet(name,title,rows,w=300,notes=None):
    ims=[[(load(p,w) if p and os.path.exists(p) else Image.new('RGB',(w,w),'white'),lab) for p,lab in r] for r in rows]
    H=80+sum(max(i.height for i,_ in r)+34 for r in ims)+(34*len(notes) if notes else 0); Wd=20+max(len(r) for r in ims)*(w+10)
    S=Image.new('RGB',(Wd,H),'white'); d=ImageDraw.Draw(S); d.text((20,20),title,fill='black',font=FB); y=80
    for r in ims:
        x=20
        for im,lab in r: d.text((x,y),lab,fill=(40,40,40),font=F); S.paste(im,(x,y+28)); x+=w+10
        y+=max(i.height for i,_ in r)+34
    for n in (notes or []): d.text((20,y),n,fill=(20,20,90),font=F); y+=34
    S.save(os.path.join(O,name)); print(name,S.size)
T=[('src','v005 source'),('v001','v001 (x3, 629k q)'),('x1','x1 (39k q)'),('x2','x2 raw (157k q)'),('v002','v002 selected')]
views=[('body','front'),('body','left'),('body','back'),('body','q3'),('head','front'),('head','left'),('shoulder','front'),('shoulder','q3'),('hand','left'),('hand','right'),('foot','top'),('foot','left')]
for part,(a,b) in (('1',(0,4)),('2',(4,8)),('3',(8,12))):
    sheet('S1_density_visual_%s.png'%part,'Density study - identical cameras: v005 / v001 / x1 / x2 / v002 (clay)',
      [[(os.path.join(C,'%s_%s_%s.png'%(t,g,v)),'%s  %s %s'%(lab,g,v)) for t,lab in T] for g,v in views[a:b]],w=300)
WT=[('cage','authored cage'),('x1','x1'),('x2','x2 raw'),('v002','v002 selected')]
sheet('S2_density_wire.png','Density study - wireframe: authored cage / x1 / x2 / v002',
  [[(os.path.join(C,'w_%s_%s.png'%(t,r)),'%s  %s'%(lab,r)) for t,lab in WT] for r in ('face','shoulder','hand','groin','knee','foot')],w=330)
