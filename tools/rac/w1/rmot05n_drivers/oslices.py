import numpy as np, sys
from PIL import Image, ImageDraw
# oslices.py occ.npz out.png zlist [scale]: occupancy slices, anterior (+Y) up, +X right, 10cm grid
d=np.load(sys.argv[1]); O=d['O']; lo=d['lo']; h=float(d['h']); zl=[float(z) for z in sys.argv[3].split(',')]; sc=int(sys.argv[4]) if len(sys.argv)>4 else 2
tiles=[]
for z in zl:
    k=int(round((z-lo[2])/h)); s=O[:,:,k].astype(np.uint8)*200
    im=s.T[::-1]; I=Image.fromarray(im).convert('RGB').resize((im.shape[1]*sc,im.shape[0]*sc),Image.NEAREST); dr=ImageDraw.Draw(I)
    for g in range(-60,61,10):
        px=(g-lo[0])/h*sc; dr.line([(px,0),(px,I.size[1])],fill=(60,60,120) if g else (150,60,60))
        py=I.size[1]-(g-lo[1])/h*sc; dr.line([(0,py),(I.size[0],py)],fill=(60,60,120) if g else (150,60,60))
    dr.text((4,4),'z=%g'%z,fill=(255,255,0)); tiles.append(I)
n=len(tiles); c=min(n,int(sys.argv[5]) if len(sys.argv)>5 else 4); r=(n+c-1)//c; w,hh=tiles[0].size; S=Image.new('RGB',(w*c,hh*r),(40,40,40))
for i,t in enumerate(tiles): S.paste(t,((i%c)*w,(i//c)*hh))
S.save(sys.argv[2])
