# hq_render.sh TAG... : look-dev renders of quick hands (hand frame) -> v5/w/HQ.jpg rows
cd /tmp/claude-0/src3d; P=/home/claude/stc/bin/python3
for t in "$@"; do
 $P tools/rview2.py -- v5/w/$t.npz v5/w/q_$t top,below,front,q3 - 1 13,1,-3 13 700 >/dev/null 2>&1
 $P tools/rview2.py -- v5/w/$t.npz v5/w/qz_$t front,q3 - 1 24,1.5,-5.5 3 700 >/dev/null 2>&1
done
python3 - "$@" <<'P'
import sys
from PIL import Image
R='/tmp/claude-0/src3d/v5/w/'; ts=sys.argv[1:]; s=400
vs=[('q_','top'),('q_','front'),('qz_','front'),('qz_','q3')]
c=Image.new('RGB',(s*len(vs),s*len(ts)))
for j,t in enumerate(ts):
  for i,(a,v) in enumerate(vs): c.paste(Image.open(R+a+t+'_'+v+'.png').convert('RGB').resize((s,s)),(i*s,j*s))
c.save(R+'HQ.jpg',quality=88)
P
