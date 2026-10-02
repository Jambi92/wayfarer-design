set -e
cd /tmp/claude-0/rodin/g1
python3 stitch_mask.py
python3 g1.py 0.35 edit_mc.npz | tail -1
python3 assemble2.py | grep -v "loop "
python3 post.py
python3 -c "
import numpy as np; z=np.load('g1_body.npz'); np.savez('cur.npz',P=z['V'],f=z['F'],R=np.zeros(len(z['V']),int))"
VIEWS="rearC:180:5:0:-15:92:70;profC:90:0:0:-18:92:80;lowC:30:-35:0:0:88:70;frontC:0:0:0:0:92:60;hipL:250:5:-17:-3:98:40" NPZ=cur.npz TAG=$PWD/c2 python3 rclose.py 2>&1 | grep -E "RCLOSE"
python3 -c "
from PIL import Image
ims=[Image.open('/tmp/claude-0/rodin/g1/c2_%s.png'%n).convert('RGBA').resize((600,600)) for n in ('rearC','profC','lowC','frontC','hipL')]
o=Image.new('RGB',(3000,600),(40,42,48))
for i,im in enumerate(ims): o.paste(im,(i*600,0),im)
o.save('/tmp/claude-0/rodin/g1/dbg_close.jpg')"
