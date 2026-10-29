# run_hv_prod.sh : Halvren central-anchor order Part B -- diagnostic body-family candidates HV_{M,F}_REF_RP3_bodyfam_v001 (make_prod.py, production frame,
# hm08 map), freeze_check read-back (no save), then the manifest / sidecars (hv_manifest.py).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; BP=/home/claude/stc/bin/python3; D=/home/claude/wayfarer-design/tools/rac/rp/halvren_rp3_v001
W=${HV_WORK:-/tmp/claude-0/rt/hv}; E=${HV_EVI:?evidence dir}; cd $W; mkdir -p prod readback; : > prod_hashes.jsonl
ST="HALVREN BODY-FAMILY DIAGNOSTIC CANDIDATE (Halvren central-anchor order 2026-10-29) - carries the family human auricle; NOT final Halvren anatomy; NOT frozen"
for x in "HVC1 HV_M_REF_RP3_bodyfam_v001" "HVF178 HV_F_REF_RP3_bodyfam_v001"; do set -- $x
  $BP $T/make_prod.py -- fam/$1_fam.npz lm/$1_fam_landmarks.json $2 prod "$ST" 2>/dev/null | grep '^{' >> prod_hashes.jsonl
  $BP $T/freeze_check.py -- prod/$2.blend fam/$1_fam.npz lm/$1_fam_landmarks.json readback/$2_readback.json > readback/$2.log 2>&1; done
python3 $D/hv_manifest.py $W $E
echo HV_PROD_DONE
