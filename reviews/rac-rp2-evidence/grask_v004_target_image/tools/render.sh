#!/bin/bash
P=/home/claude/stc/bin/python3; R=/tmp/claude-0/rp2; D=$R/fin4
for m in v003:$R/fin/v003.npz v004:$R/fin/v004.npz; do n=${m%%:*}; f=${m#*:}
 $P $R/rview.py -- $f $D/b_$n front,left,back,q3 - 1 0,5,109 112 1000 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/h_$n front,left,q3 - 1 0,8,202 18 700 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/e_$n left,q3 - 1 8.5,5,203 6.5 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/f_$n front,q3 - 1 0,14,201 7 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/n_$n left,front - 1 0,14,192 6 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/j_$n left,q3r - 1 4,9,192 8 600 >/dev/null 2>&1 &
 wait
 python3 $R/idc/sub.py $f $D/_h_$n.npz 23.5 44 -12 14 58 116; python3 $R/idc/sub.py $f $D/_f_$n.npz 0 25 -12 34 -1 11
 $P $R/rview.py -- $D/_h_$n.npz $D/hn_$n right,left - 1 31,1,89 21 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $D/_f_$n.npz $D/ft_$n top,left,q3 - 1 12,11,5 19 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/g_$n front - 1 0,5,176 28 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/c_$n front - 1 0,8,148 22 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/t_$n left - 1 0,5,140 34 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/p_$n front - 1 0,5,112 24 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/a_$n front - 1 29,2,135 36 600 >/dev/null 2>&1 &
 $P $R/rview.py -- $f $D/k_$n front,left - 1 12,3,52 42 600 >/dev/null 2>&1 &
 wait
done
