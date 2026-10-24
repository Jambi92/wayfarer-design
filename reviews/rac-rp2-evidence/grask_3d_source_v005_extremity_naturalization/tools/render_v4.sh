# render_v4.sh MESH TAG : v004 evidence renders (left hand, left foot) into v4/ev4/TAG_*
M=$1; T=$2; P=/home/claude/stc/bin/python3; RV=/tmp/claude-0/src3d/tools/rview2.py; C=/tmp/claude-0/src3d/tools/crop.py; O=/tmp/claude-0/src3d/v5/ev5; mkdir -p $O /tmp/cr
python3 $C $M /tmp/cr/${T}_h.npz "(x>18)&(z<108)&(z>60)" 1
python3 $C $M /tmp/cr/${T}_f.npz "(x>4)&(z<16)"
H=/tmp/cr/${T}_h.npz; F=/tmp/cr/${T}_f.npz
$P $RV -- $M $O/${T}_b front,left,back,q3,bq3 - 1 - - 1000 >/dev/null 2>&1 &
$P $RV -- $H $O/${T}_hand right,left,q3,back - 1 29,2,90 14 900 >/dev/null 2>&1 &
wait
$P $RV -- $H $O/${T}_thumbroot q3r - 1 26,5.5,94 6 900 >/dev/null 2>&1 &
$P $RV -- $H $O/${T}_thumbprof front - 1 25,5,93 7 900 >/dev/null 2>&1 &
$P $RV -- $H $O/${T}_index front - 1 28,7,84 7 900 >/dev/null 2>&1 &
$P $RV -- $H $O/${T}_middle back - 1 29,3,84 7 900 >/dev/null 2>&1 &
wait
$P $RV -- $H $O/${T}_mcp left - 1 32,2,89 5 900 >/dev/null 2>&1 &
$P $RV -- $H $O/${T}_pipdip left - 1 30,2,82.5 4.5 900 >/dev/null 2>&1 &
$P $RV -- $H $O/${T}_tip q3 - 1 26,3,79 3.2 900 >/dev/null 2>&1 &
$P $RV -- $H $O/${T}_nail left - 1 26.5,3,79.5 2.6 900 >/dev/null 2>&1 &
wait
$P $RV -- $H $O/${T}_web left - 1 32,2,86.5 4 900 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_foot front - 1 18,9,5 14 900 >/dev/null 2>&1 &
$P $RV -- $F $O/${T}_foot left,right,q3,bq3,below - 1 18,6,6 17 900 >/dev/null 2>&1 &
wait
$P $RV -- $M $O/${T}_fore q3 - 1 19,17,4 7 900 >/dev/null 2>&1 &
$P $RV -- $F $O/${T}_hallux q3r,top - 1 14,23,3 4.5 900 >/dev/null 2>&1 &
$P $RV -- $F $O/${T}_lesser front,top - 1 22.5,21,2.5 5 900 >/dev/null 2>&1 &
$P $RV -- $F $O/${T}_toeroot top - 1 20,16.5,4 5 900 >/dev/null 2>&1 &
wait
$P $RV -- $F $O/${T}_toenail top - 1 14,24.5,2.5 2.8 900 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_ground left - 1 18,16,3 12 900 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_head front,left,q3 - 1 0,6,202 16 900 >/dev/null 2>&1 &
wait
