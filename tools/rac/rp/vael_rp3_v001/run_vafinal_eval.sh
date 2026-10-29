# run_vafinal_eval.sh : Vael final consolidation / freeze order §6-§20 -- final gates on the two Vael RP3 production candidates ($VA_FINAL).
#   production candidate = ear/RI3/build/<H>_VA-E2-RI3_branch.npz (VF2 family realization outside the ear branch + VA-E2-RI3 on VAEL_EAR_BRANCH_TOPOLOGY_v002)
#   Standard v1 pipeline on the production candidate: audit (integrity, density, loops), face rings, anatomy (unmasked anatomy.py and the ear-excluded
#   fn_final_anatomy.py), validator D1 + D3 + D4 + D5 + D6, 18-pose deformation; Vael gates on the rebuilt sources (full record rebuild = committed r6):
#   va2_eval.py (body canon 20 rows, body systems vs humans, face systems 6, elf face rows 9), va2_pelvis.py (skeletal-proxy pelvis 9 / 9),
#   va_hidden_ear.py (hidden-ear / neutral-complexion body + face vs Marchfolk / Sagekin / frozen Fenn / frozen Aelari at 178 cm), cf_expr.py (expressions).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; FT=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001; D=/home/claude/wayfarer-design/tools/rac/rp/vael_rp3_v001
BP=/home/claude/stc/bin/python3; RA=/home/claude/wayfarer-design/reviews/reference-assets; WF=${VA_FINAL:-/tmp/claude-0/rt/va/final}; cd $WF; mkdir -p audit anat val def he gates
one(){ H=$1; P=ear/RI3/build/${H}_VA-E2-RI3_branch.npz; N=src/${H}_native.npz; R=$RA/r6/${H}_r6.npz
  $BP $T/audit.py $P $R audit/${H}_final_audit.json audit/${H}_final_loops.npz > audit/${H}_final.log 2>&1
  python3 $T/face_rings.py $P audit/${H}_final_loops.npz lm/${H}_fam_landmarks.json audit/${H}_final_face.json >> audit/${H}_final.log 2>&1
  python3 $T/anatomy.py $R $P anat/${H}_final_anatomy.json >> audit/${H}_final.log 2>&1
  python3 $FT/fn_final_anatomy.py $R $P anat/${H}_final_anatomy_earexcl.json >> audit/${H}_final.log 2>&1
  python3 $T/validator_v2.py $P val/${H}_final_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native $N > val/${H}_final.log 2>&1
  $BP $T/mf_deform.py $N $P def ${H}_final > def/${H}_final.log 2>&1
  echo "EVAL $H done"; }
[ "${SKIP_C:-0}" = 1 ] || { one VAL4-R1-VD2-VF2; one VALF178-R1-VD2-VF2; }
# measurement record of the full record rebuild (run_candidate.py, as build_vf.sh; must equal the committed _meas.json)
for H in VAL4-R1-VD2-VF2 VALF178-R1-VD2-VF2; do python3 /home/claude/wayfarer-design/tools/rac/w1/run_candidate.py full $H /tmp/claude-0/rt/vf/MF-M-R_rest.npz > full/${H}_meas.log 2>&1; done
# Vael canon / systems / face (rebuilt sources; comparators at 178 cm from the Vael Part A workspace)
python3 $D/va2_eval.py gates/VA_final_eval_c1.json c1 VF2:$WF/full/VAL4-R1-VD2-VF2 > gates/eval_c1.log 2>&1
python3 $D/va2_eval.py gates/VA_final_eval_c2.json c2 VF2:$WF/full/VALF178-R1-VD2-VF2 > gates/eval_c2.log 2>&1
python3 $D/va2_pelvis.py gates/VA_final_pelvis.json skp VAL4-R1-VD2-VF2 VALF178-R1-VD2-VF2 > gates/pelvis.log 2>&1
VA_HE_OV=$WF/he VA_HE_C1=VAL4-R1-VD2-VF2:$WF/full/VAL4-R1-VD2-VF2 VA_HE_C2=VALF178-R1-VD2-VF2:$WF/full/VALF178-R1-VD2-VF2 python3 $D/va_hidden_ear.py /tmp/claude-0/rt/va he/VA_hidden_ear_identity_final.json > he/hidden_ear.log 2>&1
$BP $FT/cf_expr.py -- $WF gates/VA_final_expression_sanity.json VAL4-R1-VD2-VF2:$RA/r6/VAL4-R1-VD2-VF2_r6.npz:fam/VAL4-R1-VD2-VF2_fam.npz VALF178-R1-VD2-VF2:$RA/r6/VALF178-R1-VD2-VF2_r6.npz:fam/VALF178-R1-VD2-VF2_fam.npz > gates/expr.log 2>&1
echo VAFINAL_EVAL_DONE
