#!/bin/bash
# neutralize with automatic protection of contact regions until 0 self-intersections
cd /tmp/claude-0/src3d; IN=$1; OUT=$2; rm -f work/keep.npy
python3 -c "import numpy as np; n=len(np.load('$IN')['V']); np.save('work/keep.npy',np.zeros(n))"
for it in 1 2 3 4 5 6; do
  python3 tools/neutralize.py $IN $OUT "{\"keep\":\"work/keep.npy\",\"am_body\":0.3,\"af_body\":0.3,\"lam_med\":6.0}" | head -1
  PR=$(/home/claude/stc/bin/python3 /tmp/claude-0/rp2/sxq.py $OUT /tmp/np.npy 2>/dev/null | head -1 | awk '{print $2}')
  echo "iter $it pairs $PR"
  [ "$PR" = "0" ] && break
  python3 - <<PY
import numpy as np, sys
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); from cotfair import ss
d=np.load('$OUT'); F=d['Q']; pr=np.load('/tmp/np.npy'); k=np.load('work/keep.npy')
vs=np.unique(F[pr.ravel()]); m=np.zeros(len(k)); m[vs]=1
e=np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]
for _ in range(10):
    s=np.zeros(len(m)); np.maximum.at(s,e[:,0],m[e[:,1]]); np.maximum.at(s,e[:,1],m[e[:,0]]); m=np.maximum(m,s*0.9)
np.save('work/keep.npy',np.maximum(k,np.clip(m*1.2,0,1)))
PY
done
