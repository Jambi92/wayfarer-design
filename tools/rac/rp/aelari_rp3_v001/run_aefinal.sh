# run_aefinal.sh : order (Aelari final consolidation / freeze, 2026-10-28) -- clean rebuild from committed immutable inputs, stage A + B.
#   A. AEL1-R1 / AELF190-R1: regenerate the R-6 source from reviews/reference-assets/builds + r6 (regen.py proves geometry identity), native hm08 export,
#      propagate onto MPFB Family Base v005 (frozen blend + hm08 map) -> family realization; audit / landmarks; lean build + skeletal proxy (pelvis gate).
#   B. AE-E2 on the reused Fenn ear topology v002 (engineering topology only; committed cuff canon read-only), both configurations, deformation-aware
#      guard, audit / measure, and the ten AE-E2 shape probes on configuration 1 (run_ae_ear.sh).
# Work folder: $AE_FINAL (default /tmp/claude-0/rt/ae/final). Nothing here reads the review workspaces.
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; F=/home/claude/wayfarer-design/tools/rac/rp/mpfb_family; D=/home/claude/wayfarer-design/tools/rac/rp/aelari_rp3_v001
W1=/home/claude/wayfarer-design/tools/rac/w1; BP=/home/claude/stc/bin/python3; B=/mnt/user-data/outputs/rp5; RA=/home/claude/wayfarer-design/reviews/reference-assets
WF=${AE_FINAL:-/tmp/claude-0/rt/ae/final}; mkdir -p $WF/{src,fam,audit,anat,lm,val,skp,lean,full}; cd $WF; echo '{"muscle": 0.0, "weight": 0.0}' > lean.json; echo '{}' > none.json
one(){ id=$1
  $BP $T/regen.py $RA/builds/${id}_build.json $RA/r6/${id}_r6.npz src > src/regen_$id.log 2>&1
  $BP $T/native_export.py src/${id}_regen_source.blend src/${id}_native.npz > src/${id}_native.log 2>&1
  $BP $F/propagate.py $B/MF_M_REF_RP3_retopo_v005.blend $B/MF_M_REF_RP3_retopo_v005_hm08_map.npz src/${id}_native.npz fam/${id}_fam.npz > fam/${id}_prop.log 2>&1
  $BP $T/audit.py fam/${id}_fam.npz $RA/r6/${id}_r6.npz audit/${id}_fam_audit.json audit/${id}_fam_loops.npz > audit/${id}_fam.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $RA/r6/${id}_r6.npz fam/${id}_fam.npz lm/${id}_fam_landmarks.json >> audit/${id}_fam.log 2>&1
  # skeletal proxy (pelvis gate): full rebuild from the committed record (no overrides; must equal the committed r6) + lean envelope build
  $BP $W1/build_variant.py $RA/builds/${id}_build.json none.json full $id > skp/${id}-FULL.log 2>&1
  $BP $W1/build_variant.py $RA/builds/${id}_build.json lean.json lean ${id}-LEAN > skp/${id}-LEAN.log 2>&1
  python3 $W1/skeletal_proxy.py full lean $id skp > skp/${id}_skp.log 2>&1
  echo "SRC $id done"; }
[ "${SKIP_A:-0}" = 1 ] || { one AEL1-R1 & one AELF190-R1 & wait; }
AE_EAR_WORK=$WF/ear AE_CF=$WF AE_H1=AEL1-R1 AE_H2=AELF190-R1 AE_EAR_CANDS=AE-E2 AE_EAR_VER=final_check bash $D/run_ae_ear.sh > $WF/ear_run.log 2>&1
echo AEFINAL_AB_DONE
