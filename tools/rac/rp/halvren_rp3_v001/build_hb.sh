# build_hb.sh TAG... : Halvren body / face source order -- source candidates: c1 = HVC1 record + c1_TAG overrides (id HVC1-TAG), c2 = MF-F-R base + c2_TAG
# (id HVF178-TAG); stature re-solved to 178 cm; measured with run_candidate.py (MF-M-R eye reference). Definitions: hv_defs.py.
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; D=${HB_DIR:-/tmp/claude-0/rt/hv/hb}
mkdir -p $D/cand; cd $D; python3 /home/claude/wayfarer-design/tools/rac/rp/halvren_rp3_v001/hv_defs.py $D "$@" > /dev/null
b(){ $BP $W/build_variant.py $1 $2 cand $3 > cand/$3.log 2>&1; python3 $W/run_candidate.py cand $3 /tmp/claude-0/rt/hv/partA/ref/MF-M-R_rest.npz >> cand/$3.log 2>&1; echo "BUILT $3 $?"; }
for t in "$@"; do b $RB/HVC1_build.json c1_$t.json HVC1-$t & b $RB/MF-F-R_build.json c2_$t.json HVF178-$t & wait; done
echo HB_DONE
