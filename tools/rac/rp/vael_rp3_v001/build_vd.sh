# build_vd.sh TAG... : Vael custom body-deformation order §7 -- candidates VD1 / VD2 / VD3 = the accepted R1 sources (VAL4-R1 c1, VALF178-R1 c2) + the
# deterministic Vael body field (tools/rac/w1/vael_body_field.py, applied by arm_lib.build from cfg["vael_field"]) at one magnitude; height macro held
# (skeleton identical to R1); measured with run_candidate.py. Overrides ov_TAG.json live in $VD_DIR (default /tmp/claude-0/rt/vd).
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; D=${VD_DIR:-/tmp/claude-0/rt/vd}; cd $D; mkdir -p cand
b(){ $BP $W/build_variant.py $RB/$1_build.json ov_$2.json cand $1-$2 > cand/$1-$2.log 2>&1; python3 $W/run_candidate.py cand $1-$2 MF-M-R_rest.npz >> cand/$1-$2.log 2>&1; echo "BUILT $1-$2 $?"; }
for t in "$@"; do b VAL4-R1 $t & b VALF178-R1 $t & wait; done
echo VD_DONE
