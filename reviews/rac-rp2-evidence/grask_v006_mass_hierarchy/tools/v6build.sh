#!/bin/bash
# v6build.sh PARAMS TAG : build + ground + f32safe + head-joint update + self-intersection (both diagonals) + renders
cd /tmp/claude-0/rp2; T=$2; P=/home/claude/stc/bin/python3
./tools/ident_full.sh $1 ${T}0 2>&1 | tail -1 && python3 tools/ground.py idc/${T}0.npz idc/${T}1.npz && python3 tools/f32safe.py idc/${T}1.npz idc/$T.npz | tail -1 && cp idc/joints_${T}0.json idc/joints_$T.json && cp cand_s3_S.npz idc/${T}_S.npz && cp cand_s3_SS.npz idc/${T}_SS.npz && rm -f idc/${T}0*.npz idc/${T}1.npz idc/joints_${T}0.json
python3 - <<PY
import json,numpy as np
p=json.load(open('$1')); J=json.load(open('idc/joints_$T.json')); V=np.load('idc/$T.npz')['V']
if p.get('head_scale'):
    sxy,sz=p['head_scale']; top=V[:,2].max()
    h=np.array(J['head'][0]); h2=h.copy(); h2[1]=h[1]*sxy; h2[2]=top+(h[2]-top)*sz
    J['head'][0]=h2.tolist(); J['neck_01'][1]=h2.tolist()
    json.dump(J,open('idc/joints_$T.json','w'))
    print('head joint',h.round(2),'->',h2.round(2))
PY
$P sxq.py idc/$T.npz /tmp/a_$T.npy | head -1
python3 -c "
import numpy as np; a=np.load('idc/$T.npz'); np.savez('/tmp/roll_$T.npz',V=a['V'],Q=a['Q'][:,[1,2,3,0]])"; $P sxq.py /tmp/roll_$T.npz /tmp/b_$T.npy | head -1; rm -f /tmp/roll_$T.npz
D=fin6; mkdir -p $D; f=idc/$T.npz; n=$T
$P rview.py -- $f v4/r_$n front,left,q3r - 1 0,5,109 112 1000 >/dev/null 2>&1 &
$P rview.py -- $f $D/b_$n front,left,back,q3 - 1 0,5,109 112 1000 >/dev/null 2>&1 &
$P rview.py -- $f $D/big_$n front,q3,left,bq3 - 1 0,2,128 52 900 >/dev/null 2>&1 &
wait
python3 v4/cmp_img.py $n
