# probe_corr.sh : order 0f6aba8 §4 -- bounded response probes on AEL1 (configuration 1; height macro held from the AEL1 record): thoracic set T1-T4
# (spine_03 / spine_02 Y bone scales) and leg set L1-L3 (thigh / calf Y bone scales); each measured with run_candidate.py (common MF-M-R eye reference).
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; cd /tmp/claude-0/rt/ae/corr/probe
b(){ $BP $W/build_variant.py $RB/AEL1_build.json $1.json . AEL1-$1 > AEL1-$1.log 2>&1; python3 $W/run_candidate.py . AEL1-$1 MF-M-R_rest.npz >> AEL1-$1.log 2>&1; echo "PROBE $1 $?"; }
for p in ${PROBES:-T1 T2 T3 T4 L1 L2 L3}; do b $p & [ $(jobs -r | wc -l) -ge 2 ] && wait -n; done; wait
echo PROBES_DONE
