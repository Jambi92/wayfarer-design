#!/bin/bash
# refine_loop.sh IN OUT PARAMS : run refine2 and grow contact protection until 0 self-intersections
cd /tmp/claude-0/src3d; IN=$1; OUT=$2; PJ=$3; K=$(python3 -c "import json;print(json.load(open('$PJ'))['keep'])")
python3 -c "import numpy as np; np.save('$K',np.zeros(len(np.load('$IN')['V'])))"
for it in 1 2 3 4 5 6 7 8; do
  python3 tools/refine2.py $IN $OUT $PJ >/tmp/rl.log
  PR=$(/home/claude/stc/bin/python3 /tmp/claude-0/rp2/sxq.py $OUT /tmp/np.npy 2>/dev/null | head -1 | awk '{print $2}')
  echo "iter $it pairs $PR"; [ "$PR" = "0" ] && break
  python3 - <<PY
import numpy as np
d=np.load('$OUT'); F=d['Q']; pr=np.load('/tmp/np.npy'); k=np.load('$K')
m=np.zeros(len(k)); m[np.unique(F[pr.ravel()])]=1
e=np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]
for _ in range(12):
    s=np.zeros(len(m)); np.maximum.at(s,e[:,0],m[e[:,1]]); np.maximum.at(s,e[:,1],m[e[:,0]]); m=np.maximum(m,s*0.9)
np.save('$K',np.maximum(k,np.clip(m*1.2,0,1)))
PY
done
cat /tmp/rl.log
