#!/bin/bash
P=/home/claude/stc/bin/python3; R=/tmp/claude-0/rp2; D=$R/fin6
for m in "$@"; do n=${m%%:*}; f=${m#*:}
 $P $R/rview.py -- $f $D/b_$n front,left,back,q3 - 1 0,5,109 112 1000 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/hn_$n front,left - 1 0,6,190 26 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/sc_$n front,q3 - 1 0,6,165 26 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/tp_$n left - 1 0,2,145 36 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/pv_$n front,left - 1 0,2,108 22 600 >/dev/null 2>&1 &
 wait
 $P $R/rview.py -- $f $D/th_$n front,q3 - 1 0,4,92 24 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/cf_$n front,left - 1 0,3,45 26 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/am_$n front,q3r - 1 -30,2,140 32 600 >/dev/null 2>&1 &
 python3 $R/idc/sub.py $f $D/_f_$n.npz 0 25 -12 34 -1 11
 $P $R/rview.py -- $D/_f_$n.npz $D/ft_$n top,left - 1 12,11,5 19 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/hd_$n front,left,q3 - 1 0,8,198 24 600 >/dev/null 2>&1 &
 wait
done
