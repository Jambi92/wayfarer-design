import sys
from PIL import Image
tags=sys.argv[1].split(',');views=sys.argv[2].split(',');out=sys.argv[3]
S=Image.new('RGB',(1400*len(tags),700*len(views)))
for i,v in enumerate(views):
    for j,t in enumerate(tags): S.paste(Image.open(f'r/{t}_{v}.png').convert('RGB'),(1400*j,700*i))
S.save(out,quality=88)
