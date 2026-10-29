# va_final_collect.sh : copy the Vael final consolidation records from the clean-rebuild folder into the committed evidence folder (no blends / meshes).
set -e
WF=${VA_FINAL:-/tmp/claude-0/rt/va/final}; R=/home/claude/wayfarer-design; EV=$R/reviews/rac-rp3-evidence/vael_rp3_final
mkdir -p $EV/{anatomy,audit,deformation,ear/probes,hidden_ear,gates,pelvis,production,readback,rebuild,sheets,validator,diagnostics}
H="VAL4-R1-VD2-VF2 VALF178-R1-VD2-VF2"
cp $WF/VAEL_FINAL_gates.json $WF/VAEL_FINAL_deformation_summary.json $WF/VAEL_RP3_freeze_readback.json $EV/
for f in $WF/VAEL_RP3_FREEZE.json $WF/VAEL_RP3_FREEZE_CANDIDATE.json; do [ -f $f ] && cp $f $EV/; done
for h in $H; do
  cp $WF/anat/${h}_fam_anatomy.json $WF/anat/${h}_final_anatomy.json $WF/anat/${h}_final_anatomy_earexcl.json $EV/anatomy/
  cp $WF/audit/${h}_fam_audit.json $WF/audit/${h}_fam_face.json $WF/audit/${h}_final_audit.json $WF/audit/${h}_final_face.json $WF/audit/${h}_native_audit.json $EV/audit/
  cp $WF/def/deform_${h}_fam.json $WF/def/deform_${h}_final.json $WF/def/deform_${h}_native.json $EV/deformation/
  for k in audit/${h}_VA-E2-RI3_audit.json build/${h}_VA-E2-RI3_branch.json deform/${h}_VA-E2-RI3_deform.json build/${h}_VA-E2-RI3_deform_guard_log.json meas/${h}_VA-E2-RI3_measure.json; do cp $WF/ear/RI3/$k $EV/ear/; done
  cp $WF/val/${h}_fam_validator_v2_D1-D6.json $WF/val/${h}_final_validator_v2_D1-D6.json $EV/validator/
  cp $WF/src/${h}_regen_check.json $WF/contact/${h}_contact.json $EV/rebuild/
  cp $WF/skp/${h}_skp.json $EV/pelvis/ 2>/dev/null || true
done
cp $WF/anat/VAEL_unmasked_anatomy_localisation.json $EV/anatomy/
cp $WF/ear/RI3/canon_branch_topology.json $EV/ear/
for d in $WF/ear/RI3/probe/*/; do n=$(basename $d); mkdir -p $EV/ear/probes/$n; cp $d/audit.json $d/measure.json $EV/ear/probes/$n/; done
cp $WF/he/VA_hidden_ear_identity_final.json $EV/hidden_ear/
cp $WF/gates/VA_final_eval_c1.json $WF/gates/VA_final_eval_c2.json $WF/gates/VA_final_expression_sanity.json $EV/gates/
cp $WF/gates/VA_final_pelvis.json $EV/pelvis/
for n in VA_M_REF_RP3_v001 VA_F_REF_RP3_v001; do cp $WF/prod/$n.json $WF/prod/${n}_landmarks.json $EV/production/; cp $WF/readback/${n}_FREEZE_readback.json $WF/readback_local/${n}_readback.json $EV/readback/; done
(cd /mnt/user-data/uploads/RaceBodies/production/Vael/RP3 && sha256sum VA_*_REF_RP3_v001*) > $EV/production/pc_readback_sha256.txt
cp $WF/diag_earw/deform_rigidear.json $EV/diagnostics/deform_VAL4-R1-VD2-VF2_rigid_head_ear_weights.json
cp $WF/sheets/*.jpg $WF/sheets/*.csv $EV/sheets/
{ echo "# Vael RP3 final consolidation 2026-10-28: immutable inputs and sources (sha256)"
  cd $R; sha256sum /mnt/user-data/outputs/rp5/MF_M_REF_RP3_retopo_v005.blend /mnt/user-data/outputs/rp5/MF_M_REF_RP3_retopo_v005_hm08_map.npz \
    reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/MPFB_FAMILY_BASE_v005_FREEZE.json reviews/rac-rp3-evidence/fenn_rp3_freeze/FENN_RP3_FREEZE.json reviews/rac-rp3-evidence/aelari_rp3_freeze/AELARI_RP3_FREEZE.json \
    reviews/reference-assets/r6/VAL4-R1-VD2-VF2_r6.npz reviews/reference-assets/r6/VALF178-R1-VD2-VF2_r6.npz reviews/reference-assets/builds/VAL4-R1-VD2-VF2_build.json reviews/reference-assets/builds/VALF178-R1-VD2-VF2_build.json \
    reviews/rac-rp3-evidence/vael_rp3_ear_root_integration/topology/* reviews/rac-rp3-evidence/vael_rp3_ear_root_integration/mapping/* reviews/rac-rp3-evidence/vael_rp3_elf_frame/VF_definitions.json \
    reviews/rac-rp3-evidence/vael_rp3_custom_deformation/VD_definitions.json reviews/rac-rp3-evidence/vael_rp3_source/vb_vc_definitions/iter2_3/VC_definitions_final.json; } > $EV/immutable_and_source_hashes.txt
du -sh $EV; echo COLLECT_DONE
