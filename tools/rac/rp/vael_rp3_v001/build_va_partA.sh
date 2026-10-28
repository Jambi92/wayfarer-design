# build_va_partA.sh : Vael order (2026-10-28) Part A -- Vael configuration-2 central reference VALF178 (shared MPFB c2 route: MF-F-R base + exactly the VAL4
# targets / bone scales, stature re-solved to 178 cm), a second independent full re-solve (determinism), the VAL4 rebuild (rest for measurement) and the
# matched-stature comparators at 178 cm: Marchfolk, Sagekin, frozen Fenn (FNL4-CF2 / FNF181-CF2 records) and frozen Aelari (AEL1-R1 / AELF190-R1 records),
# c1 and c2. All measured with run_candidate.py and the common MF-M-R eye reference.
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; cd ${VA_PA:-/tmp/claude-0/rt/va/partA}
b(){ $BP $W/build_variant.py $1 $2 $3 $4 > $3/$4.log 2>&1; python3 $W/run_candidate.py $3 $4 ref/MF-M-R_rest.npz >> $3/$4.log 2>&1; echo "BUILT $4 $?"; }
b $RB/MF-F-R_build.json VALF178_overrides.json build VALF178 & b $RB/VAL4_build.json none.json ref VAL4 & wait
b $RB/MF-F-R_build.json VALF178_overrides.json build2 VALF178 & b $RB/MF-M-R_build.json st178.json cmp MFM178 & wait
b $RB/MF-F-R_build.json st178.json cmp MFF178 & b $RB/SG_build.json st178.json cmp SGM178 & wait
b $RB/SGF178_build.json st178.json cmp SGF178 & b $RB/FNL4-CF2_build.json st178.json cmp FNM178 & wait
b $RB/FNF181-CF2_build.json st178.json cmp FNF178 & b $RB/AEL1-R1_build.json st178.json cmp AEM178 & wait
b $RB/AELF190-R1_build.json st178.json cmp AEF178 & wait
echo VAPARTA_DONE
