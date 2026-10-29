# build_hv_partA.sh : Halvren central-anchor order (2026-10-29) Part A -- Halvren configuration-2 central anchor HVF178 (shared MPFB c2 route:
# MF-F-R base + exactly the HVC1 body targets, stature re-solved to 178 cm), a second independent full re-solve (determinism), the HVC1 rebuild from its
# committed record, and the matched-stature comparators at 178 cm not already built for Vael Part A: frozen Vael (VAL4-R1-VD2-VF2 / VALF178-R1-VD2-VF2,
# already 178 cm) and Skarn diagnostics (SK / SKF208 records re-solved to 178 cm, below the 183-229 cm Skarn envelope: diagnostic only).
# Marchfolk / Sagekin / frozen Fenn / frozen Aelari 178 cm comparators are the Vael Part A builds (same committed records; copied, not rebuilt).
# All measured with run_candidate.py and the common MF-M-R eye reference.
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; cd ${HV_PA:-/tmp/claude-0/rt/hv/partA}
b(){ $BP $W/build_variant.py $1 $2 $3 $4 > $3/$4.log 2>&1; python3 $W/run_candidate.py $3 $4 ref/MF-M-R_rest.npz >> $3/$4.log 2>&1; echo "BUILT $4 $?"; }
for n in MFM178 MFF178 SGM178 SGF178 FNM178 FNF178 AEM178 AEF178; do cp /tmp/claude-0/rt/va/partA/cmp/${n}_{build.json,meas.json,r6.npz,rest.npz} cmp/; done
b $RB/MF-F-R_build.json HVF178_overrides.json build HVF178 & b $RB/HVC1_build.json none.json ref HVC1 & wait
b $RB/MF-F-R_build.json HVF178_overrides.json build2 HVF178 & b $RB/VAL4-R1-VD2-VF2_build.json none.json cmp VAM178 & wait
b $RB/VALF178-R1-VD2-VF2_build.json none.json cmp VAF178 & b $RB/SK_build.json st178.json cmp SKM178 & wait
b $RB/SKF208_build.json st178.json cmp SKF178 & wait
echo HVPARTA_DONE
