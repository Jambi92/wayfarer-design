# build_vf.sh TAG... : Vael elf-frame order §7 -- candidates VF1 / VF2 / VF3 = the accepted VD2 sources (VAL4-R1-VD2 c1, VALF178-R1-VD2 c2) + the elf-frame term
# VEF1 (clavicle span via the clavicle bone length + long-bone shaft gracility in tools/rac/w1/vael_body_field.py) at one vef_magnitude; VD field held at 1.0;
# height macro held; measured with run_candidate.py. Overrides ov_TAG.json in $VF_DIR (default /tmp/claude-0/rt/vf).
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; D=${VF_DIR:-/tmp/claude-0/rt/vf}; O=${VF_OUT:-cand}; cd $D; mkdir -p $O
b(){ $BP $W/build_variant.py $RB/$1_build.json ov_$2.json $O $1-$2 > $O/$1-$2.log 2>&1; [ -z "$NOMEAS" ] && python3 $W/run_candidate.py $O $1-$2 MF-M-R_rest.npz >> $O/$1-$2.log 2>&1; echo "BUILT $1-$2 $?"; }
for t in "$@"; do b VAL4-R1-VD2 $t & b VALF178-R1-VD2 $t & wait; done
echo VF_DONE
