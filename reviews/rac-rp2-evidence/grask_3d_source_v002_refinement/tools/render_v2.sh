# render_v2.sh MESH TAG : evidence renders into v2/ev/TAG_*
M=$1; T=$2; P=/home/claude/stc/bin/python3; RV=/tmp/claude-0/src3d/tools/rview2.py; C=/tmp/claude-0/src3d/tools/crop.py; O=/tmp/claude-0/src3d/v2/ev; mkdir -p $O /tmp/cr
python3 $C $M /tmp/cr/${T}_hand.npz "(x>18)&(z<108)&(z>60)" 1
python3 $C $M /tmp/cr/${T}_foot.npz "(x>4)&(z<16)" 1
python3 $C $M /tmp/cr/${T}_trunk.npz "(np.abs(x)<19.5)|(z>140)" 1
python3 $C $M /tmp/cr/${T}_leg.npz "(x>2)&(z<60)" 1
$P $RV -- $M $O/${T}_b front,left,back,q3,q3r,bq3 - 1 - - 1000 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_face front,left,q3 - 1 0,6,200 15 700 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_ear left,q3,back - 1 9.5,0,204 6.5 700 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_hand.npz $O/${T}_hand right,left,back,q3,front - 1 29,2,91 14 700 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_hand.npz $O/${T}_thumb q3r,front - 1 26.5,5,93 7 700 >/dev/null 2>&1 &
wait
$P $RV -- /tmp/cr/${T}_foot.npz $O/${T}_foot top,left,right,q3,bq3,below - 1 18,6,6 17 700 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_foot.npz $O/${T}_toe front,q3r - 1 18,20,3 7 700 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_neck front,q3 - 1 0,2,180 22 700 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_chest front - 1 0,6,155 26 700 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_trunk.npz $O/${T}_tprof left - 1 0,0,145 40 700 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_uback back,bq3 - 1 0,0,162 28 700 >/dev/null 2>&1 &
wait
$P $RV -- $M $O/${T}_pelv front - 1 0,2,105 24 700 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_trunk.npz $O/${T}_pelv left,bq3 - 1 0,0,105 24 700 >/dev/null 2>&1 &
$P $RV -- $M $O/${T}_thigh q3 - 1 8,4,92 22 700 >/dev/null 2>&1 &
$P $RV -- /tmp/cr/${T}_leg.npz $O/${T}_calf front,left - 1 15,2,28 24 700 >/dev/null 2>&1 &
wait
