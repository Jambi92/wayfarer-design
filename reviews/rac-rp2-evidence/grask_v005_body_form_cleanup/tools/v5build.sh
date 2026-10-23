#!/bin/bash
# v5build.sh PARAMS TAG : build + ground + f32safe + both-diagonal self-intersection + standard renders
cd /tmp/claude-0/rp2; T=$2; P=/home/claude/stc/bin/python3
./tools/ident_full.sh $1 ${T}0 2>&1 | tail -1 && python3 tools/ground.py idc/${T}0.npz idc/${T}1.npz && python3 tools/f32safe.py idc/${T}1.npz idc/$T.npz | tail -1 && cp idc/joints_${T}0.json idc/joints_$T.json && cp cand_s3_S.npz idc/${T}_S.npz && cp cand_s3_SS.npz idc/${T}_SS.npz && rm -f idc/${T}0.npz idc/${T}1.npz idc/m_${T}*.npz
$P sxq.py idc/$T.npz /tmp/a_$T.npy | head -1
python3 -c "
import numpy as np; a=np.load('idc/$T.npz'); np.savez('/tmp/roll_$T.npz',V=a['V'],Q=a['Q'][:,[1,2,3,0]])"; $P sxq.py /tmp/roll_$T.npz /tmp/b_$T.npy | head -1
D=fin5; f=idc/$T.npz; n=$T
$P rview.py -- $f v4/r_$n front,left,q3r - 1 0,5,109 112 1000 >/dev/null 2>&1 &
$P rview.py -- $f $D/b_$n front,left,back,q3 - 1 0,5,109 112 1000 >/dev/null 2>&1 &
$P rview.py -- $f $D/th_$n front,q3 - 1 0,5,98 22 600 >/dev/null 2>&1 &
$P rview.py -- $f $D/tp_$n left - 1 10,3,98 22 600 >/dev/null 2>&1 &
$P rview.py -- $f $D/ch_$n front,q3 - 1 0,8,160 18 600 >/dev/null 2>&1 &
$P rview.py -- $f $D/bk_$n back,q3r - 1 0,0,145 26 600 >/dev/null 2>&1 &
$P rview.py -- $f $D/ar_$n front,q3 - 1 30,2,135 34 600 >/dev/null 2>&1 &
$P rview.py -- $f $D/fa_$n left - 1 30,2,128 22 600 >/dev/null 2>&1 &
$P rview.py -- $f $D/ab_$n left - 1 0,5,125 24 600 >/dev/null 2>&1 &
$P rview.py -- $f $D/hd_$n front,left,q3 - 1 0,8,198 24 600 >/dev/null 2>&1 &
wait
python3 v4/cmp_img.py $n
$P rview.py -- $f $D/tq_$n left,back,q3r - 1 0,-2,150 32 600 >/dev/null 2>&1 &
$P rview.py -- $f $D/bb_$n back,bq3,bq3r - 1 0,-4,145 30 600 >/dev/null 2>&1 &
$P rview.py -- $f $D/gl_$n left,bq3 - 1 4,-2,105 22 600 >/dev/null 2>&1 &
wait
$P rview.py -- $f $D/big_$n front,q3,left,bq3 - 1 0,2,128 52 900 >/dev/null 2>&1
