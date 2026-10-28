# build_vb.sh TAG... : Vael body / face source order §6 -- body-source candidates VB*: c1 = VAL4 record + c1_TAG overrides, c2 = MF-F-R base + c2_TAG
# (the full VAL4 Vael cfg with the identical VB changes; the VALF178 route); stature re-solved to 178 cm; measured with run_candidate.py (MF-M-R eye ref).
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; D=${VB_DIR:-/tmp/claude-0/rt/va2/vb}; cd $D; mkdir -p cand
b(){ $BP $W/build_variant.py $1 $2 cand $3 > cand/$3.log 2>&1; python3 $W/run_candidate.py cand $3 ../MF-M-R_rest.npz >> cand/$3.log 2>&1; echo "BUILT $3 $?"; }
for t in "$@"; do b $RB/VAL4_build.json c1_$t.json VAL4-$t & b $RB/MF-F-R_build.json c2_$t.json VALF178-$t & wait; done
echo VB_DONE
