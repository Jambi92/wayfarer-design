# run_aefinal_eval.sh : Aelari final consolidation (order 2026-10-28) §6-§18 -- final gates on the two Aelari RP3 production candidates ($AE_FINAL).
#   production candidate = ear/build/<H>_AE-E2_branch.npz (R1 family realization outside the ear branch + AE-E2 on the reused Fenn v002 engineering topology)
#   Standard v1 pipeline on the production candidate AND its family realization: audit (integrity, density, loops), face rings, anatomy (unmasked anatomy.py
#   and the ear-excluded fn_final_anatomy.py), validator D1 + D3 + D4 + D5 + D6, 18-pose deformation (native / family / production), identity (sg_identity
#   vs matched Marchfolk / Sagekin / frozen Fenn / other configuration), body canon + skeletal-proxy pelvis (ae_partA.py on a partA layout of the committed
#   R1 records), metrics vs Fenn / MF (corr_matrix.py), hidden-ear body + face (ae_hidden_ear.py on the regenerated R1 sources).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; S=/home/claude/wayfarer-design/tools/rac/rp/sagekin_rp3_v001; FT=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001
D=/home/claude/wayfarer-design/tools/rac/rp/aelari_rp3_v001; BP=/home/claude/stc/bin/python3; RA=/home/claude/wayfarer-design/reviews/reference-assets; PA0=/tmp/claude-0/rt/ae/partA
EV=/home/claude/wayfarer-design/reviews/rac-rp3-evidence/aelari_rp3_correction; WF=${AE_FINAL:-/tmp/claude-0/rt/ae/final}; cd $WF; mkdir -p audit anat val def he
one(){ H=$1; P=ear/build/${H}_AE-E2_branch.npz; C=fam/${H}_fam.npz; N=src/${H}_native.npz; R=$RA/r6/${H}_r6.npz
  $BP $T/audit.py $P $R audit/${H}_final_audit.json audit/${H}_final_loops.npz > audit/${H}_final.log 2>&1
  $BP $T/audit.py $N $R audit/${H}_native_audit.json audit/${H}_native_loops.npz > audit/${H}_native.log 2>&1
  python3 $T/face_rings.py $P audit/${H}_final_loops.npz lm/${H}_fam_landmarks.json audit/${H}_final_face.json >> audit/${H}_final.log 2>&1
  python3 $T/face_rings.py $C audit/${H}_fam_loops.npz lm/${H}_fam_landmarks.json audit/${H}_fam_face.json >> audit/${H}_fam.log 2>&1
  python3 $T/anatomy.py $R $P anat/${H}_final_anatomy.json >> audit/${H}_final.log 2>&1
  python3 $FT/fn_final_anatomy.py $R $P anat/${H}_final_anatomy_earexcl.json >> audit/${H}_final.log 2>&1
  python3 $T/anatomy.py $R $C anat/${H}_fam_anatomy.json >> audit/${H}_fam.log 2>&1
  python3 $T/validator_v2.py $P val/${H}_final_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native $N > val/${H}_final.log 2>&1
  python3 $T/validator_v2.py $C val/${H}_fam_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native $N > val/${H}_fam.log 2>&1
  $BP $T/mf_deform.py $N $N def ${H}_native > def/${H}_native.log 2>&1
  $BP $T/mf_deform.py $N $C def ${H}_fam > def/${H}_fam.log 2>&1
  $BP $T/mf_deform.py $N $P def ${H}_final > def/${H}_final.log 2>&1
  echo "EVAL $H done"; }
[ "${SKIP_C:-0}" = 1 ] || { one AEL1-R1 & one AELF190-R1 & wait; }
# identity (family realization == production outside the ear branch) vs matched-stature Marchfolk / Sagekin / frozen Fenn and the other configuration
python3 $S/sg_identity.py anat/AEL1-R1_identity.json fam/AEL1-R1_fam.npz audit/AEL1-R1_fam_loops.npz src/AEL1-R1_r6_regen.npz:AEL1-R1 $PA0/cmp/MFM190_r6.npz:MFM190 $PA0/cmp/SGM190_r6.npz:SGM190 $PA0/cmp/FNM190_r6.npz:FNM190 src/AELF190-R1_r6_regen.npz:AELF190-R1 > anat/identity.log 2>&1
python3 $S/sg_identity.py anat/AELF190-R1_identity.json fam/AELF190-R1_fam.npz audit/AELF190-R1_fam_loops.npz src/AELF190-R1_r6_regen.npz:AELF190-R1 $PA0/cmp/MFF190_r6.npz:MFF190 $PA0/cmp/SGF190_r6.npz:SGF190 $PA0/cmp/FNF190_r6.npz:FNF190 src/AEL1-R1_r6_regen.npz:AEL1-R1 >> anat/identity.log 2>&1
# partA layout of the committed R1 records (body canon, configuration consistency, determinism, skeletal-proxy pelvis)
P=$WF/partA; mkdir -p $P/ref $P/build $P/build2 $P/skp; ln -sfn $PA0/cmp $P/cmp
ln -sf $RA/builds/AEL1-R1_meas.json $P/ref/AEL1_meas.json; ln -sf $RA/r6/AEL1-R1_r6.npz $P/ref/AEL1_r6.npz
for x in meas.json build.json; do ln -sf $RA/builds/AELF190-R1_$x $P/build/AELF190_$x; done; ln -sf $RA/r6/AELF190-R1_r6.npz $P/build/AELF190_r6.npz
ln -sf $EV/sources/AELF190-R1_second_resolve_build.json $P/build2/AELF190_build.json; ln -sf $WF/full/AELF190-R1_r6.npz $P/build2/AELF190_r6.npz
ln -sf $WF/skp/AEL1-R1_skp.json $P/skp/AEL1_skp.json; ln -sf $WF/skp/AELF190-R1_skp.json $P/skp/AELF190_skp.json; for n in MFM190 MFF190 FNM190 FNF190; do ln -sf $PA0/skp/${n}_skp.json $P/skp/; done
AE_ORDER=final-2026-10-28 python3 $D/ae_partA.py $WF anat/AE_final_canon_pelvis.json > anat/partA.log 2>&1
python3 $D/corr_matrix.py $WF anat/AE_final_metrics_vs_FN_MF.json > anat/metrics.log 2>&1
# hidden-ear body + face on the regenerated R1 sources (comparators from the reviewed partA at 190 cm)
mkdir -p he/src; for n in AEL1-R1 AELF190-R1; do ln -sf $WF/src/${n}_r6_regen.npz he/src/${n}_r6.npz; ln -sf $RA/builds/${n}_meas.json he/src/${n}_meas.json; done
AE_HE_OV=$WF/he AE_HE_C1=AEL1-R1:$WF/he/src/AEL1-R1 AE_HE_C2=AELF190-R1:$WF/he/src/AELF190-R1 python3 $D/ae_hidden_ear.py /tmp/claude-0/rt/ae he/AE_hidden_ear_identity_final.json > he/hidden_ear.log 2>&1
echo AEFINAL_EVAL_DONE
