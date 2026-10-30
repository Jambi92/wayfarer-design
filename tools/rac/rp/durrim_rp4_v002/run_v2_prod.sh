# run_v2_prod.sh : RP4 v002 production reference candidates DU_M_REF_RP4_v001 (c1, DU137C-NAT) / DU_F_REF_RP4_v001 (c2, DUF137C-NAT) on MPFB_COMPACT_BRANCH_v002
# (du_make_prod.py) + local Blender read-back (marchfolk freeze_check.py; opens without saving). NOT frozen.
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; D=/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002; BP=/home/claude/stc/bin/python3
W=/tmp/claude-0/rt/du/v2; cd $W; mkdir -p prod readback
ST="DURRIM RP4 PRODUCTION REFERENCE CANDIDATE (compact branch MPFB_COMPACT_BRANCH_v002, 2026-10-30) - NOT frozen; freeze only by author acceptance record"
for x in "DU137C-NAT DU_M_REF_RP4_v001" "DUF137C-NAT DU_F_REF_RP4_v001"; do set -- $x
  $BP $D/du_make_prod.py -- cb2/$1_cb2.npz lm/$1_cb2_landmarks.json $2 prod "$ST" > prod/$2.log 2>&1
  $BP $T/freeze_check.py -- prod/$2.blend cb2/$1_cb2.npz lm/$1_cb2_landmarks.json readback/$2_readback.json > readback/$2.log 2>&1
  echo "PROD $2 $(python3 -c "import json;d=json.load(open('readback/$2_readback.json'));print({k:d.get(k) for k in ('verts','faces','max_abs_diff_vs_candidate_m','faces_equal_candidate','components','boundary_edges','nonmanifold_edges','quads_pct','uv_layer')})")"; done
