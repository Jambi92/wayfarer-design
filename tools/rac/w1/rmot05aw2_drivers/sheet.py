import sys
from PIL import Image
tags=sys.argv[1].split(','); out=sys.argv[2]; views=sys.argv[3].split(',') if len(sys.argv)>3 else ['front_L','front_R','f34_L','f34_R','top_L','top_R']
ims=[[Image.open(f'/home/claude/aw1/r/{t}_{v}.png').convert('RGB') for t in tags] for v in views]
w,h=700,350; S=Image.new('RGB',(w*len(tags),h*len(views)))
for i,row in enumerate(ims):
    for j,im in enumerate(row): S.paste(im.resize((w,h)),(j*w,i*h))
S.save(out,quality=85)
