# render_v3.sh MESH TAG : v003 evidence renders into v3/ev3/TAG_*
M=$1; T=$2; P=/home/claude/stc/bin/python3; RV=/tmp/claude-0/src3d/tools/rview2.py; C=/tmp/claude-0/src3d/tools/crop.py; O=/tmp/claude-0/src3d/v3/ev3; mkdir -p $O /tmp/cr
python3 $C $M /tmp/cr/${T}_hand.npz "(x>18)&(z<108)&(z>60)" 1
python3 $C $M /tmp/cr/${T}_foot.npz "(x>4)&(z<16)"
$P $RV -- $M $O/${T}_b front,left,back,q3,bq3 - 1 - - 1000 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_hand.npz $O/${T}_hand right,left,q3,back - 1 29,2,90 13 800 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_hand.npz $O/${T}_thumb q3r - 1 25.5,6,90 6 800 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_hand.npz $O/${T}_fside front - 1 26,2,83 8 800 >/dev/null 2>&1 &
wait
$P $RV -- /tmp/cr/${T}_hand.npz $O/${T}_knuck left,q3 - 1 30.5,2,87 5.5 800 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_hand.npz $O/${T}_ftip left - 1 26.5,2,80.5 3.5 800 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_foot front - 1 18,8,5 15 800 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_foot.npz $O/${T}_foot left,right,q3,bq3,below - 1 18,6,6 17 800 >/dev/null 2>&1 &
wait
$P $RV -- /tmp/cr/${T}_foot.npz $O/${T}_toe front,q3 - 1 19,22,2.5 7 800 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_foot.npz $O/${T}_nail top - 1 17,23,2.5 5 800 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_earL left,q3,back - 1 9.5,0,204 6 800 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_earR right - 1 -9.5,0,204 6 800 >/dev/null 2>&1 &
wait
$P $RV -- $M $O/${T}_face front,q3,left - 1 0,6,200 15 800 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_orb front,q3 - 1 3.4,8,203.8 3.2 800 >/dev/null 2>&1 &
wait
