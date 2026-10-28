# run_aefinal_prod.sh : Aelari final consolidation (order 2026-10-28) §2 / §5 / §21 -- final production bodies AE_{M,F}_REF_RP3_v001 (fn_make_prod.py:
# production frame, UVMap, 'ear_branch' vertex group, branch-map / landmark / json sidecars) + local Blender read-back (freeze_check.py, no save).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; FT=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001; BP=/home/claude/stc/bin/python3
WF=${AE_FINAL:-/tmp/claude-0/rt/ae/final}; cd $WF; mkdir -p prod readback_local
ST="AELARI RP3 FINAL PRODUCTION BODY (order 2026-10-28 final consolidation) - freeze status is held by record: AELARI_RP3_FREEZE.json"
export RAC_COMPOSITION='Aelari RP3: R1 corrected body source on MPFB Family Base v005 outside the ear branch + AE-E2 Aelari ear geometry on the reused Fenn ear topology v002 (engineering topology only)'
for x in "AEL1-R1 AE_M_REF_RP3_v001" "AELF190-R1 AE_F_REF_RP3_v001"; do set -- $x
  $BP $FT/fn_make_prod.py -- ear/build/$1_AE-E2_branch.npz fam/$1_fam.npz lm/$1_fam_landmarks.json $2 prod "$ST" > prod/$2.log 2>&1
  $BP $T/freeze_check.py -- prod/$2.blend ear/build/$1_AE-E2_branch.npz lm/$1_fam_landmarks.json readback_local/$2_readback.json > readback_local/$2.log 2>&1
  echo "PROD $2 $(python3 -c "import json;d=json.load(open('readback_local/$2_readback.json'));print(d['verts'],d['faces'],d['max_abs_diff_vs_candidate_m'],d['faces_equal_candidate'])")"; done
echo AEFINAL_PROD_DONE
