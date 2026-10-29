# run_vafinal.sh : Vael final consolidation / freeze order (chatgpt-rac-rp3-vael-final-consolidation-freeze-order.md) §4 -- clean rebuild from committed
# immutable inputs only, stages A + B.
#   A. VAL4-R1-VD2-VF2 / VALF178-R1-VD2-VF2: regenerate the R-6 source from reviews/reference-assets/builds + r6 (regen.py proves geometry identity), full
#      record rebuild (build_variant, no overrides; must equal the committed r6), native hm08 export, propagate onto MPFB Family Base v005 (frozen blend +
#      hm08 map) -> family realization; audit / landmarks / face rings / anatomy / validator / contact / 18-pose deformation of the family realization
#      (the Standard v1 run_aeeval.sh steps); lean skeletal-envelope build + skeletal proxy (pelvis gate).
#   B. VA-E2-RI3 on VAEL_EAR_BRANCH_TOPOLOGY_v002 (committed VAEL_EAR_CUFF_CANON_v001 read-only), both configurations, deformation-aware guard, audit /
#      measure / blend, and the twelve RI3 shape probes on configuration 1 (run_va_ri.sh).
# Work folder: $VA_FINAL (default /tmp/claude-0/rt/va/final). Nothing here reads the review workspaces.
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; F=/home/claude/wayfarer-design/tools/rac/rp/mpfb_family; S=/home/claude/wayfarer-design/tools/rac/rp/sagekin_rp3_v001
D=/home/claude/wayfarer-design/tools/rac/rp/vael_rp3_v001; W1=/home/claude/wayfarer-design/tools/rac/w1; BP=/home/claude/stc/bin/python3; B=/mnt/user-data/outputs/rp5
RA=/home/claude/wayfarer-design/reviews/reference-assets
WF=${VA_FINAL:-/tmp/claude-0/rt/va/final}; mkdir -p $WF/{src,fam,audit,anat,lm,val,def,contact,skp,lean,full}; cd $WF
echo '{"muscle": 0.0, "weight": 0.0}' > lean.json; echo '{}' > none.json
one(){ id=$1; base=$2; R=$RA/r6/${id}_r6.npz
  $BP $T/regen.py $RA/builds/${id}_build.json $R src > src/regen_$id.log 2>&1
  $BP $W1/build_variant.py $RA/builds/${id}_build.json none.json full $id > full/$id.log 2>&1
  $BP $T/native_export.py src/${id}_regen_source.blend src/${id}_native.npz > src/${id}_native.log 2>&1
  $BP $F/propagate.py $B/MF_M_REF_RP3_retopo_v005.blend $B/MF_M_REF_RP3_retopo_v005_hm08_map.npz src/${id}_native.npz fam/${id}_fam.npz > fam/${id}_prop.log 2>&1
  $BP $T/audit.py src/${id}_native.npz $R audit/${id}_native_audit.json audit/${id}_native_loops.npz > audit/${id}_native.log 2>&1
  $BP $T/audit.py fam/${id}_fam.npz $R audit/${id}_fam_audit.json audit/${id}_fam_loops.npz > audit/${id}_fam.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $R fam/${id}_fam.npz lm/${id}_fam_landmarks.json >> audit/${id}_fam.log 2>&1
  python3 $T/face_rings.py fam/${id}_fam.npz audit/${id}_fam_loops.npz lm/${id}_fam_landmarks.json audit/${id}_fam_face.json >> audit/${id}_fam.log 2>&1
  python3 $T/anatomy.py $R fam/${id}_fam.npz anat/${id}_fam_anatomy.json >> audit/${id}_fam.log 2>&1
  python3 $T/validator_v2.py fam/${id}_fam.npz val/${id}_fam_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz > val/${id}_fam.log 2>&1
  python3 $S/contact_prop.py contact/${id}_contact.json $id fam/${id}_fam.npz audit/${id}_fam_loops.npz src/${id}_native.npz audit/${id}_native_loops.npz \
          /tmp/claude-0/rt/v5/cand/${base}_v005.npz /tmp/claude-0/rt/v5/audit/${base}_v005_loops.npz > contact/${id}.log 2>&1
  $BP $T/mf_deform.py src/${id}_native.npz src/${id}_native.npz def ${id}_native > def/${id}_native.log 2>&1
  $BP $T/mf_deform.py src/${id}_native.npz fam/${id}_fam.npz def ${id}_fam > def/${id}_fam.log 2>&1
  $BP $W1/build_variant.py $RA/builds/${id}_build.json lean.json lean ${id}-LEAN > skp/${id}-LEAN.log 2>&1
  python3 $W1/skeletal_proxy.py full lean $id skp > skp/${id}_skp.log 2>&1
  echo "SRC $id done"; }
[ "${SKIP_A:-0}" = 1 ] || { one VAL4-R1-VD2-VF2 MF-M-R & one VALF178-R1-VD2-VF2 MF-F-R & wait; }
VA_RI_WORK=$WF/ear VA_CF=$WF VA_RI_LIST=RI3 VA_RI_SEL=RI3 bash $D/run_va_ri.sh > $WF/ear_run.log 2>&1
echo VAFINAL_AB_DONE
