# run_vafinal_prod.sh : Vael final consolidation (freeze order) §3 / §5 / §22 -- final production bodies VA_{M,F}_REF_RP3_v001 (fn_make_prod.py:
# production frame, UVMap, 'ear_branch' vertex group, branch-map / landmark / json sidecars) + local Blender read-back (freeze_check.py, no save).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; FT=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001; BP=/home/claude/stc/bin/python3
WF=${VA_FINAL:-/tmp/claude-0/rt/va/final}; cd $WF; mkdir -p prod readback_local
ST="VAEL RP3 FINAL PRODUCTION BODY (freeze order 2026-10-28) - freeze status is held by record: VAEL_RP3_FREEZE.json"
export RAC_COMPOSITION='Vael RP3: R1 + VD2 + VF2 body source with the VC2 face on MPFB Family Base v005 outside the ear branch + VA-E2 Vael ear geometry with RI3 root / concha integration on VAEL_EAR_BRANCH_TOPOLOGY_v002 (Vael-specific local cuff derivative of the Fenn / Aelari engineering topology)'
for x in "VAL4-R1-VD2-VF2 VA_M_REF_RP3_v001" "VALF178-R1-VD2-VF2 VA_F_REF_RP3_v001"; do set -- $x
  $BP $FT/fn_make_prod.py -- ear/RI3/build/$1_VA-E2-RI3_branch.npz fam/$1_fam.npz lm/$1_fam_landmarks.json $2 prod "$ST" > prod/$2.log 2>&1
  $BP $T/freeze_check.py -- prod/$2.blend ear/RI3/build/$1_VA-E2-RI3_branch.npz lm/$1_fam_landmarks.json readback_local/$2_readback.json > readback_local/$2.log 2>&1
  echo "PROD $2 $(python3 -c "import json;d=json.load(open('readback_local/$2_readback.json'));print(d['verts'],d['faces'],d['max_abs_diff_vs_candidate_m'],d['faces_equal_candidate'])")"; done
echo VAFINAL_PROD_DONE
