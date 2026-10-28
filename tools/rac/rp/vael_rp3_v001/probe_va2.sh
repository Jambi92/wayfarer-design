# probe_va2.sh : Vael body / face source order (2026-10-28) §6 / §9 -- bounded single-control probes on the VAL4 record (configuration 1; height macro held):
# body probes pB_* (bone scales / MPFB body targets) and face probes pF_* (MPFB head / face targets). Each: build_variant + run_candidate (MF-M-R eye ref).
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; cd ${VA2:-/tmp/claude-0/rt/va2}; mkdir -p probe
mk(){ echo "$2" > probe/$1.json; }
mk pB_depth '{"targets": {"torso-scale-depth-incr": 0.30}}'
mk pB_napew '{"targets": {"measure-napetowaist-dist-decr": 0.3}}'
mk pB_sp02 '{"bone_scales": {"spine_02": [1, 0.97, 1]}}'
mk pB_sp01 '{"bone_scales": {"spine_01": [1, 0.97, 1]}}'
mk pB_pelY '{"bone_scales": {"pelvis": [1.02, 1.03, 1.03]}}'
mk pB_thigh '{"bone_scales": {"LR:thigh": [1, 0.97849, 1]}}'
mk pB_calf '{"bone_scales": {"LR:calf": [1, 1.01951, 1]}}'
mk pB_fing '{"targets": {"LR:hand-fingers-length-incr": 0.3}}'
mk pB_fdist '{"targets": {"LR:hand-fingers-distance-incr": 0.45}}'
mk pB_fdiam '{"targets": {"LR:hand-fingers-diameter-incr": 0.3}}'
mk pB_neckc '{"targets": {"measure-neck-circ-incr": 0.3}}'
mk pB_neckh '{"targets": {"neck-scale-horiz-incr": 0.3}}'
mk pB_wrist '{"targets": {"measure-wrist-circ-decr": 0.15}}'
mk pB_ankle '{"targets": {"measure-ankle-circ-decr": null}}'
mk pB_hipd '{"targets": {"hip-scale-depth-incr": 0.3}}'
mk pB_footv '{"targets": {"LR:foot-scale-vert-incr": 0.3}}'
for t in head-scale-vert-incr head-oval head-back-scale-depth-incr head-scale-depth-decr head-scale-horiz-incr forehead-scale-vert-incr forehead-trans-backward forehead-temple-decr chin-height-decr \
         LR:cheek-volume-incr LR:cheek-trans-up LR:cheek-inner-incr nose-scale-depth-incr nose-trans-forward eyebrows-trans-forward eyebrows-trans-down LR:eye-trans-out \
         chin-width-incr chin-bones-incr chin-prominent-incr chin-jaw-drop-incr head-square head-diamond mouth-trans-up; do mk pF_$(echo $t | tr ':' '_') "{\"targets\": {\"$t\": 0.5}}"; done
mk pF_LR_cheek-bones-incr '{"targets": {"LR:cheek-bones-incr": 0.7}}'
mk pF_LR_eye-scale-incr '{"targets": {"LR:eye-scale-incr": 0.45}}'
b(){ $BP $W/build_variant.py $RB/VAL4_build.json probe/$1.json probe $1 > probe/$1.log 2>&1; python3 $W/run_candidate.py probe $1 MF-M-R_rest.npz >> probe/$1.log 2>&1; echo "PROBE $1 $?"; }
for f in ${PROBES:-$(ls probe/*.json | xargs -n1 basename | sed 's/.json//')}; do [ -f probe/${f}_meas.json ] && continue; b $f & [ $(jobs -r | wc -l) -ge 2 ] && wait -n; done; wait
echo PROBE_DONE
