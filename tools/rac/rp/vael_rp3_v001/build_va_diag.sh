# build_va_diag.sh : Vael order Part A diagnostics for the VA-P2a / VA-P6 decision -- Vael at the Aelari reference stature (VAL4 / VALF178 design at 190 cm)
# and the ORIGINAL Aelari sources (AEL1 / AELF190, before the 0f6aba8 R1 correction) at 178 cm, measured as Part A.
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; cd ${VA_PA:-/tmp/claude-0/rt/va/partA}
b(){ $BP $W/build_variant.py $1 $2 $3 $4 > $3/$4.log 2>&1; python3 $W/run_candidate.py $3 $4 ref/MF-M-R_rest.npz >> $3/$4.log 2>&1; echo "BUILT $4 $?"; }
b $RB/VAL4_build.json st190.json diag VAM190 & b $RB/MF-F-R_build.json VALF190_overrides.json diag VAF190 & wait
b $RB/AEL1_build.json st178.json diag AEL1orig178 & b $RB/AELF190_build.json st178.json diag AELF190orig178 & wait
echo VADIAG_DONE
