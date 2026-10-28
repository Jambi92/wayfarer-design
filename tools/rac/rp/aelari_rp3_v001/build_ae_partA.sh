# build_ae_partA.sh : order fd71f15 Part A -- Aelari configuration-2 central reference AELF190 (shared MPFB c2 route: MF-F-R base + the AEL1 targets /
# bone scales, stature re-solved to 190 cm), a second independent full re-solve (determinism), the AEL1 rebuild (rest for measurement) and the matched-
# stature diagnostic comparators at 190 cm (Marchfolk, Sagekin, frozen Fenn CF2; c1 and c2). All measured with run_candidate.py and the common MF-M-R eye reference.
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; cd /tmp/claude-0/rt/ae/partA
b(){ $BP $W/build_variant.py $1 $2 $3 $4 > $3/$4.log 2>&1; python3 $W/run_candidate.py $3 $4 ref/MF-M-R_rest.npz >> $3/$4.log 2>&1; echo "BUILT $4 $?"; }
b $RB/MF-F-R_build.json AELF190_overrides.json build AELF190 & b $RB/AEL1_build.json none.json ref AEL1 & wait
b $RB/MF-F-R_build.json AELF190_overrides.json build2 AELF190 & b $RB/MF-M-R_build.json st190.json cmp MFM190 & wait
b $RB/MF-F-R_build.json st190.json cmp MFF190 & b $RB/SG_build.json st190.json cmp SGM190 & wait
b $RB/SGF178_build.json st190.json cmp SGF190 & b $RB/FNL4-CF2_build.json st190.json cmp FNM190 & wait
b $RB/FNF181-CF2_build.json st190.json cmp FNF190 & wait
echo AEPARTA_DONE
