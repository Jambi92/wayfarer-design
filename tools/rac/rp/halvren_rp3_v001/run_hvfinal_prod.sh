# run_hvfinal_prod.sh : Halvren final whole-character consolidation order §9 -- final production reference candidates HV_{M,F}_REF_RP3_v001 (hv_make_prod.py
# = fn_make_prod.py + the frozen TRI-HV1 face attribute / sidecar) + local Blender read-back (freeze_check.py, hv_tri_readback.py; no save).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; D=/home/claude/wayfarer-design/tools/rac/rp/halvren_rp3_v001; BP=/home/claude/stc/bin/python3
FZ=/home/claude/wayfarer-design/reviews/rac-rp3-evidence/halvren_rp3_final/baked; WF=${HV_FINAL:-/tmp/claude-0/rt/hv/final}; cd $WF; mkdir -p prod readback_local
ST="HALVREN RP3 FINAL PRODUCTION REFERENCE CANDIDATE (whole-character consolidation 2026-10-30) - NOT frozen; freeze status is held by record (HALVREN_RP3_FREEZE.json after author approval)"
export RAC_COMPOSITION='Halvren RP3: HB2 body + HF2 face + HP-B pelvis (HVC1 / HVF178 central anchors) on MPFB Family Base v005 outside the ear branch + HE2 HVEAR3 central ear with HR2 root on VAEL_EAR_BRANCH_TOPOLOGY_v002 + RI3 cuff canon (Halvren ear family, FINAL PRODUCTION FROZEN); TRI-HV1 production triangulation, LOD-HV1'
for x in "HVC1-HB2HF2-HPB HV_M_REF_RP3_v001 c1" "HVF178-HB2HF2-HPB HV_F_REF_RP3_v001 c2"; do set -- $x
  $BP $D/hv_make_prod.py -- ear/build/$1_HE2_branch.npz fam/$1_fam.npz lm/$1_fam_landmarks.json $2 prod "$ST" $FZ/HE2_$3_TRI-HV1.npz > prod/$2.log 2>&1
  $BP $T/freeze_check.py -- prod/$2.blend ear/build/$1_HE2_branch.npz lm/$1_fam_landmarks.json readback_local/$2_readback.json > readback_local/$2.log 2>&1
  $BP $D/hv_tri_readback.py -- prod/$2.blend prod/$2_TRI-HV1.npz readback_local/$2_tri_readback.json > readback_local/$2_tri.log 2>&1
  echo "PROD $2 $(python3 -c "import json;d=json.load(open('readback_local/$2_readback.json'));t=json.load(open('readback_local/$2_tri_readback.json'));print(d['verts'],d['faces'],d['max_abs_diff_vs_candidate_m'],d['faces_equal_candidate'],t['equals_sidecar_hash'])")"; done
echo HVFINAL_PROD_DONE
