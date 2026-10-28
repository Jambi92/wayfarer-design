# build_corr.sh TAG... : order 0f6aba8 -- corrected Aelari source candidates: c1 = AEL1 record + corr overrides (bone scales spine_03 / thigh / calf,
# stature 190 re-solved); c2 = MF-F-R base + the identical corrected Aelari cfg (the accepted AELF190 route). Measured with run_candidate.py.
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; cd /tmp/claude-0/rt/ae/corr; mkdir -p cand
b(){ $BP $W/build_variant.py $1 $2 cand $3 > cand/$3.log 2>&1; python3 $W/run_candidate.py cand $3 probe/MF-M-R_rest.npz >> cand/$3.log 2>&1; echo "BUILT $3 $?"; }
for t in "$@"; do b $RB/AEL1_build.json c1_$t.json AEL1-$t & b $RB/MF-F-R_build.json c2_$t.json AELF190-$t & wait; done
echo CORR_DONE
