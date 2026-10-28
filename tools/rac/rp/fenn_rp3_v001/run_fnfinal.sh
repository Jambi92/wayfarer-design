# run_fnfinal.sh : order 6d2eadc (Fenn final consolidation / freeze) -- clean rebuild from committed immutable inputs, stage A + B.
#   A. FNL4-CF2 / FNF181-CF2: regenerate the R-6 source from reviews/reference-assets/builds + r6 (regen.py proves geometry identity), native hm08 export,
#      propagate onto MPFB Family Base v005 (frozen blend + hm08 map) -> family realization; audit / landmarks / face rings / anatomy / validator on the family.
#   B. Fenn ear branch topology v002, E2, both configurations, from the committed cuff canon (read-only) -> branch realization + guard + audit + measure + probes.
# Work folder: $FN_FINAL (default /tmp/claude-0/rt/fn/final). Nothing here reads the review workspaces (/tmp/claude-0/rt/fn/cf, /tmp/claude-0/rt/fn/ear/*).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; F=/home/claude/wayfarer-design/tools/rac/rp/mpfb_family; FT=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001
BP=/home/claude/stc/bin/python3; B=/mnt/user-data/outputs/rp5; RA=/home/claude/wayfarer-design/reviews/reference-assets
WF=${FN_FINAL:-/tmp/claude-0/rt/fn/final}; mkdir -p $WF/{src,fam,audit,anat,lm,val}; cd $WF
one(){ id=$1
  $BP $T/regen.py $RA/builds/${id}_build.json $RA/r6/${id}_r6.npz src > src/regen_$id.log 2>&1
  $BP $T/native_export.py src/${id}_regen_source.blend src/${id}_native.npz > src/${id}_native.log 2>&1
  $BP $F/propagate.py $B/MF_M_REF_RP3_retopo_v005.blend $B/MF_M_REF_RP3_retopo_v005_hm08_map.npz src/${id}_native.npz fam/${id}_fam.npz > fam/${id}_prop.log 2>&1
  $BP $T/audit.py fam/${id}_fam.npz $RA/r6/${id}_r6.npz audit/${id}_fam_audit.json audit/${id}_fam_loops.npz > audit/${id}_fam.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $RA/r6/${id}_r6.npz fam/${id}_fam.npz lm/${id}_fam_landmarks.json >> audit/${id}_fam.log 2>&1
  echo "SRC $id done"; }
[ "${SKIP_A:-0}" = 1 ] || { one FNL4-CF2 & one FNF181-CF2 & wait; }
# B: ear branch v002 E2 (canon copied read-only from the committed topology record by run_earbranch_v002.sh)
EAR_CF=$WF EAR_WORK=$WF/ear bash $FT/run_earbranch_v002.sh > $WF/ear_run.log 2>&1
echo FNFINAL_AB_DONE
