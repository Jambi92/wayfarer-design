# cmpwire.sh MESH TAG OUTDIR : wire crops for the density comparison (face, shoulder, hand, groin, knee, foot)
M=$1; T=$2; O=$3; cd /tmp/claude-0/rt
python3 wireh.py $M $O/w_${T}_face.png "(z>186)&(f>-2)" 0,5 plain 160
python3 wireh.py $M $O/w_${T}_shoulder.png "(x>8)&(z>140)&(z<190)" 30,10 plain 160
python3 wireh.py $M $O/w_${T}_hand.png "(x>22)&(z>75)&(z<105)" 90,0 plain 160
python3 wireh.py $M $O/w_${T}_groin.png "(z>95)&(z<130)&(f>-6)" 0,5 plain 160
python3 wireh.py $M $O/w_${T}_knee.png "(x>0)&(z>55)&(z<90)" 20,5 plain 160
python3 wireh.py $M $O/w_${T}_foot.png "(x>6)&(z<12)&(f>-12)" 0,70 plain 160
echo $T wires
