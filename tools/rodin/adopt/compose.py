import numpy as np, math
from PIL import Image, ImageDraw, ImageFont
F=lambda n,b=False: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"%("-Bold" if b else ""),n)
BG=(28,28,32); PANEL=(38,40,46); TXT=(235,235,240); SUB=(170,180,200)
COL={"PRESERVE":(84,178,107),"MODIFY":(245,184,51),"REBUILD":(230,82,61),"REPLACE":(84,135,245)}
VIEWS=[("front","Front"),("profile","Profile"),("rear","Rear"),("front34","Front 3/4"),("rear34","Rear 3/4")]
def strip(tag, title, lines, out, labels=None, cell=760, legend=False):
    ims=[Image.open("%s_%s.png"%(tag,v)).convert("RGBA").resize((cell,cell),Image.LANCZOS) for v,_ in VIEWS]
    top=150+30*len(lines); W=cell*5+20*6; Hh=top+cell+(110 if legend else 30)
    img=Image.new("RGB",(W,Hh),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(32,True),fill=TXT)
    for i,l in enumerate(lines): d.text((20,66+30*i),l,font=F(20),fill=SUB)
    for i,(im,(v,lab)) in enumerate(zip(ims,VIEWS)):
        x=20+i*(cell+20); bg=Image.new("RGB",im.size,PANEL); bg.paste(im,(0,0),im); img.paste(bg,(x,top))
        d.text((x+8,top-34),lab,font=F(24,True),fill=SUB)
        if labels:
            for num,(px,py) in labels.get(v,{}).items():
                X,Y=x+px*cell,top+py*cell; r=17
                d.ellipse((X-r,Y-r,X+r,Y+r),fill=(20,20,24),outline=(255,255,255),width=2)
                tw=d.textlength(str(num),font=F(18,True)); d.text((X-tw/2,Y-11),str(num),font=F(18,True),fill=(255,255,255))
    if legend:
        x=20; y=top+cell+30
        for k,c in COL.items():
            d.rectangle((x,y,x+34,y+34),fill=c); d.text((x+46,y+4),k,font=F(24,True),fill=TXT); x+=300
    img.save(out,quality=90); return img
