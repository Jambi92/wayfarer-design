# evidence.sh PROD SRC OUTDIR : raw renders for sheets A-G
P=/home/claude/stc/bin/python3; R=/tmp/claude-0/src3d/tools/rview2.py; PROD=$1; SRC=$2; O=$3; cd /tmp/claude-0/rt
mkdir -p $O
for t in prod src; do M=$PROD; [ $t = src ] && M=$SRC
  $P $R -- $M $O/A_$t front,left,back,q3,right - 1 - - 1100 >/dev/null 2>&1
  $P $R -- $M $O/B_$t front,left,q3,right,q3r - 1 0,2,201 13 900 >/dev/null 2>&1
  $P $R -- $M $O/C_$t front,back,q3,left,bq3 - 1 0,-3,150 42 1000 >/dev/null 2>&1
  $P $R -- $M $O/D_$t left,right,front,back,q3 - 1 29,2,92 11 900 >/dev/null 2>&1
  $P $R -- $M $O/Dr_$t left,right,front,back,q3r - 1 -29,2,92 11 900 >/dev/null 2>&1
  $P $R -- $M $O/E_$t top,left,right,front,below - 1 18,6,6 15 900 >/dev/null 2>&1
  $P $R -- $M $O/Er_$t top,left,right,front,below - 1 -18,6,6 15 900 >/dev/null 2>&1
done
# wireframes (production)
python3 wireh.py $PROD $O/Bw_front.png "(z>186)&(f>-2)" 0,5 plain 220
python3 wireh.py $PROD $O/Bw_left.png "(z>186)&(x>-2)" 90,5 plain 220
python3 wireh.py $PROD $O/Bw_ear.png "(z>194)&(z<212)&(x>5)&(f>-7)&(f<5)" 90,5 plain 220
python3 wireh.py $PROD $O/Cw_shoulder.png "(x>8)&(z>140)&(z<190)" 30,10 plain 200
python3 wireh.py $PROD $O/Cw_axilla.png "(x>12)&(z>140)&(z<170)" 0,-25 plain 200
python3 wireh.py $PROD $O/Cw_pelvis.png "(z>95)&(z<130)" 0,5 plain 200
python3 wireh.py $PROD $O/Cw_glute.png "(z>95)&(z<130)" 180,5 plain 200
python3 wireh.py $PROD $O/Dw_dorsal.png "handpart&(x>0)" 90,0 plain 220
python3 wireh.py $PROD $O/Dw_palmar.png "handpart&(x>0)" -90,0 plain 220
python3 wireh.py $PROD $O/Dw_thumb.png "handpart&(x>0)" 0,0 plain 220
python3 wireh.py $PROD $O/Ew_top.png "(x>6)&(z<12)&(f>-12)" 0,70 plain 220
python3 wireh.py $PROD $O/Ew_lat.png "(x>6)&(z<12)" 90,5 plain 220
python3 wireh.py $PROD $O/Ew_med.png "(x>6)&(z<12)" -90,5 plain 220
python3 wireh.py $PROD $O/Ew_sole.png "(x>6)&(z<12)" 0,-80 plain 220
echo EVDONE
# G: deviation heat maps (mm, 0..1.5)
TAG=$(basename $PROD .npz)
python3 -c "
import numpy as np; z=np.load('$PROD'); d=np.load('/tmp/claude-0/rt/${TAG}_dps.npy'); np.save('$O/_dps_v.npy',d[:len(z['V'])])"
$P $R -- $SRC $O/G_src front,back,left /tmp/claude-0/rt/${TAG}_dsp.npy 1.5 - - 900 >/dev/null 2>&1
$P $R -- $PROD $O/G_prod front,back,left $O/_dps_v.npy 1.5 - - 900 >/dev/null 2>&1
$P $R -- $SRC $O/Gh_src front /tmp/claude-0/rt/${TAG}_dsp.npy 1.5 0,2,201 13 900 >/dev/null 2>&1
echo GDONE
