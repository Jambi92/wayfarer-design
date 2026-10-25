# cmprender.sh MESH TAG OUTDIR : identical-camera comparison renders (body, head, shoulder, hand, foot)
P=/home/claude/stc/bin/python3; R=/tmp/claude-0/src3d/tools/rview2.py; M=$1; T=$2; O=$3
$P $R -- $M $O/${T}_body front,left,back,q3 - 1 - - 900 >/dev/null 2>&1
$P $R -- $M $O/${T}_head front,left - 1 0,2,201 13 700 >/dev/null 2>&1
$P $R -- $M $O/${T}_shoulder front,q3 - 1 18,-2,160 22 700 >/dev/null 2>&1
$P $R -- $M $O/${T}_hand left,right - 1 29,2,92 11 700 >/dev/null 2>&1
$P $R -- $M $O/${T}_foot top,left - 1 18,6,6 15 700 >/dev/null 2>&1
echo $T done
