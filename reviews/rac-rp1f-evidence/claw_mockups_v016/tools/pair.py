import sys,glob,os
from PIL import Image, ImageDraw, ImageFont
d=sys.argv[1]; la=sys.argv[2]; lb=sys.argv[3]; od=sys.argv[4]; os.makedirs(od,exist_ok=True)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',28)
for s in sorted(glob.glob(d+'/*_A.png')):
    n=os.path.basename(s)[:-6]; a=Image.open(s).convert('RGB'); b=Image.open(s[:-6]+'_B.png').convert('RGB'); W,H=a.size
    im=Image.new('RGB',(2*W+10,H+60),(30,30,34)); im.paste(a,(0,60)); im.paste(b,(W+10,60)); dr=ImageDraw.Draw(im)
    dr.text((20,14),la,fill=(230,230,230),font=f); dr.text((W+30,14),lb,fill=(255,200,120),font=f); dr.text((2*W-330,14),n,fill=(160,200,255),font=f)
    im.save(od+'/'+n+'.png')
