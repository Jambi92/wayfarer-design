# run_fnfinal_eval.sh : order 6d2eadc §6-§13 -- final gates on the two Fenn RP3 production candidates (clean-rebuild folder $FN_FINAL).
#   production candidate = ear/build/<H>_E2_branch.npz (CF2 family realization outside the ear branch + ear branch topology v002, E2)
#   Standard v1 pipeline on the production candidate AND on its CF2 family realization (same sources; differs only inside the ear branch), so every
#   body gate is shown unchanged by consolidation: audit (integrity, density, loops, T-4), face rings, anatomy (T-1 / T-2 / T-3 / T-7, IoU), validator
#   D1 + D3 + D4 + D5 + D6, the Standard v1 18-pose deformation set (native / family / production), identity (family vs matched Marchfolk / Sagekin and
#   the other configuration), hidden-ear body + face (fenn_hidden_ear.py on the CF2 sources) and the CF2 hidden-ear facial evaluation (cf_eval.py).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; S=/home/claude/wayfarer-design/tools/rac/rp/sagekin_rp3_v001; FT=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001
BP=/home/claude/stc/bin/python3; RA=/home/claude/wayfarer-design/reviews/reference-assets/r6; PA=/tmp/claude-0/rt/fn/partA
WF=${FN_FINAL:-/tmp/claude-0/rt/fn/final}; cd $WF; mkdir -p audit anat val def he
one(){ H=$1; P=ear/build/${H}_E2_branch.npz; C=fam/${H}_fam.npz; N=src/${H}_native.npz; R=$RA/${H}_r6.npz
  $BP $T/audit.py $P $R audit/${H}_final_audit.json audit/${H}_final_loops.npz > audit/${H}_final.log 2>&1
  $BP $T/audit.py $N $R audit/${H}_native_audit.json audit/${H}_native_loops.npz > audit/${H}_native.log 2>&1
  python3 $T/face_rings.py $P audit/${H}_final_loops.npz lm/${H}_fam_landmarks.json audit/${H}_final_face.json >> audit/${H}_final.log 2>&1
  python3 $T/face_rings.py $C audit/${H}_fam_loops.npz lm/${H}_fam_landmarks.json audit/${H}_fam_face.json >> audit/${H}_fam.log 2>&1
  python3 $T/anatomy.py $R $P anat/${H}_final_anatomy.json >> audit/${H}_final.log 2>&1
  python3 $T/anatomy.py $R $C anat/${H}_fam_anatomy.json >> audit/${H}_fam.log 2>&1
  python3 $T/validator_v2.py $P val/${H}_final_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native $N > val/${H}_final.log 2>&1
  python3 $T/validator_v2.py $C val/${H}_fam_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native $N > val/${H}_fam.log 2>&1
  $BP $T/mf_deform.py $N $N def ${H}_native > def/${H}_native.log 2>&1
  $BP $T/mf_deform.py $N $C def ${H}_fam > def/${H}_fam.log 2>&1
  $BP $T/mf_deform.py $N $P def ${H}_final > def/${H}_final.log 2>&1
  echo "EVAL $H done"; }
[ "${SKIP_C:-0}" = 1 ] || { one FNL4-CF2 & one FNF181-CF2 & wait; }
# identity (family realization; == production outside the ear branch) vs matched-stature Marchfolk / Sagekin and the other configuration
python3 $S/sg_identity.py anat/FNL4-CF2_identity.json fam/FNL4-CF2_fam.npz audit/FNL4-CF2_fam_loops.npz src/FNL4-CF2_r6_regen.npz:FNL4-CF2 $PA/cmp/MFM181_r6.npz:MFM181 $PA/cmp/SGM181_r6.npz:SGM181 src/FNF181-CF2_r6_regen.npz:FNF181-CF2 > anat/identity.log 2>&1
python3 $S/sg_identity.py anat/FNF181-CF2_identity.json fam/FNF181-CF2_fam.npz audit/FNF181-CF2_fam_loops.npz src/FNF181-CF2_r6_regen.npz:FNF181-CF2 $PA/cmp/MFF181_r6.npz:MFF181 $PA/cmp/SGF181_r6.npz:SGF181 src/FNL4-CF2_r6_regen.npz:FNL4-CF2 >> anat/identity.log 2>&1
# hidden-ear body + face on the CF2 sources (W = the Fenn body workspace for the native topology / comparators)
FN_HE_OV=$WF/he FN_HE_C1=FNL4-CF2:$WF/src/FNL4-CF2_r6_regen.npz FN_HE_C2=FNF181-CF2:$WF/src/FNF181-CF2_r6_regen.npz python3 $FT/fenn_hidden_ear.py /tmp/claude-0/rt/fn he/FN_hidden_ear_identity_CF2.json > he/hidden_ear.log 2>&1
# CF2 hidden-ear facial evaluation (cf_eval.py) with the CF2 R-6 taken from this clean rebuild (CF1 / CF3 candidates from the reviewed workspace, unchanged)
mkdir -p he/W/cf/cand; ln -sfn $PA he/W/partA
for id in FNL4 FNF181; do for k in 1 2 3; do d=he/W/cf/cand/$id-CF$k; mkdir -p $d
  if [ $k = 2 ]; then ln -sf $WF/src/$id-CF2_r6_regen.npz $d/$id-CF2_r6.npz; else ln -sf /tmp/claude-0/rt/fn/cf/cand/$id-CF$k/$id-CF${k}_r6.npz $d/$id-CF${k}_r6.npz; fi; done; done
python3 $FT/cf_eval.py $WF/he/W he/CF_hidden_ear_eval_final.json > he/cf_eval.log 2>&1
echo FNFINAL_EVAL_DONE
