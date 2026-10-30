# run_hvfinal_eval.sh : Halvren final whole-character consolidation order §4-§8 -- final gates on the two Halvren RP3 production candidates ($HV_FINAL)
# (as vael_rp3_v001/run_vafinal_eval.sh):
#   production candidate = ear/build/<H>_HE2_branch.npz (HB2 + HF2 + HP-B family realization outside the ear branch + HE2 HVEAR3 / HR2)
#   Standard v1 pipeline on the candidate: audit (integrity, density, loops), face rings, anatomy (unmasked anatomy.py + ear-excluded fn_final_anatomy.py),
#   validator D1 + D3 + D4 + D5 + D6, 18-pose deformation; Halvren gates on the rebuilt sources (full record rebuild = committed r6): run_candidate
#   measurement (= committed _meas.json), hv_eval.py (body / face / ears-excluded identity, scalar-blend firewall, anti-beauty; = accepted HPB_eval),
#   hv_hidden_ear.py (hidden-ear / neutral body + face vs MF / SG / SK / FN / AE / VA at 178 cm), cf_expr.py (expression sanity).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; FT=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001; D=/home/claude/wayfarer-design/tools/rac/rp/halvren_rp3_v001
BP=/home/claude/stc/bin/python3; RA=/home/claude/wayfarer-design/reviews/reference-assets; WF=${HV_FINAL:-/tmp/claude-0/rt/hv/final}; cd $WF; mkdir -p audit anat val def he gates
one(){ H=$1; P=ear/build/${H}_HE2_branch.npz; N=src/${H}_native.npz; R=$RA/r6/${H}_r6.npz
  $BP $T/audit.py $P $R audit/${H}_final_audit.json audit/${H}_final_loops.npz > audit/${H}_final.log 2>&1
  python3 $T/face_rings.py $P audit/${H}_final_loops.npz lm/${H}_fam_landmarks.json audit/${H}_final_face.json >> audit/${H}_final.log 2>&1
  python3 $T/anatomy.py $R $P anat/${H}_final_anatomy.json >> audit/${H}_final.log 2>&1
  python3 $FT/fn_final_anatomy.py $R $P anat/${H}_final_anatomy_earexcl.json >> audit/${H}_final.log 2>&1
  python3 $T/validator_v2.py $P val/${H}_final_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native $N > val/${H}_final.log 2>&1
  $BP $T/mf_deform.py $N $P def ${H}_final > def/${H}_final.log 2>&1
  echo "EVAL $H done"; }
[ "${SKIP_C:-0}" = 1 ] || { one HVC1-HB2HF2-HPB & one HVF178-HB2HF2-HPB & wait; }
for H in HVC1-HB2HF2-HPB HVF178-HB2HF2-HPB; do python3 /home/claude/wayfarer-design/tools/rac/w1/run_candidate.py full $H /tmp/claude-0/rt/hv/partA/ref/MF-M-R_rest.npz > full/${H}_meas.log 2>&1; done
python3 $D/hv_eval.py gates/HV_final_eval_c1.json c1 HB2HF2-HPB:$WF/full/HVC1-HB2HF2-HPB > gates/eval_c1.log 2>&1
python3 $D/hv_eval.py gates/HV_final_eval_c2.json c2 HB2HF2-HPB:$WF/full/HVF178-HB2HF2-HPB > gates/eval_c2.log 2>&1
HV_HE_OV=$WF/he HV_HE_C1=HVC1-HB2HF2-HPB:$WF/full/HVC1-HB2HF2-HPB HV_HE_C2=HVF178-HB2HF2-HPB:$WF/full/HVF178-HB2HF2-HPB python3 $D/hv_hidden_ear.py /tmp/claude-0/rt/hv he/HV_hidden_ear_identity_final.json > he/hidden_ear.log 2>&1
$BP $FT/cf_expr.py -- $WF gates/HV_final_expression_sanity.json HVC1-HB2HF2-HPB:$RA/r6/HVC1-HB2HF2-HPB_r6.npz:fam/HVC1-HB2HF2-HPB_fam.npz HVF178-HB2HF2-HPB:$RA/r6/HVF178-HB2HF2-HPB_r6.npz:fam/HVF178-HB2HF2-HPB_fam.npz > gates/expr.log 2>&1
echo HVFINAL_EVAL_DONE
