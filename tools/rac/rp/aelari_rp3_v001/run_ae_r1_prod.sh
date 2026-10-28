# run_ae_r1_prod.sh : order 0f6aba8 §12 -- production body-family candidates from the corrected sources (AEL1-R1 / AELF190-R1) on frozen MPFB v005:
# make_prod (production frame, hm08 map), freeze_check read-back (no save), then the parameterised manifest / sidecars (ae_manifest.py, AE_C1 / AE_C2).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; BP=/home/claude/stc/bin/python3; D=/home/claude/wayfarer-design/tools/rac/rp/aelari_rp3_v001
W=${AE_WORK:-/tmp/claude-0/rt/ae/r1}; E=${AE_EVI:?evidence dir}; cd $W; mkdir -p prod readback; : > prod_hashes.jsonl
ST="AELARI BODY-FAMILY DIAGNOSTIC CANDIDATE (order 0f6aba8 corrected body source) - carries the family human auricle; NOT final Aelari body; NOT frozen"
for x in "AEL1-R1 AE_M_REF_RP3_bodyfam_v002" "AELF190-R1 AE_F_REF_RP3_bodyfam_v002"; do set -- $x
  $BP $T/make_prod.py -- fam/$1_fam.npz lm/$1_fam_landmarks.json $2 prod "$ST" 2>/dev/null | grep '^{' >> prod_hashes.jsonl
  $BP $T/freeze_check.py -- prod/$2.blend fam/$1_fam.npz lm/$1_fam_landmarks.json readback/$2_readback.json > readback/$2.log 2>&1; done
ln -sf $W/partA_R1.json $W/partA/AELF190_reference_validation.json
AE_C1=AEL1-R1 AE_C2=AELF190-R1 AE_PROD_VER=v002 AE_ORDER_DOC='reviews/chatgpt-rac-rp3-aelari-body-source-correction-order.md (0f6aba8)' python3 $D/ae_manifest.py $W $E
echo AE_R1_PROD_DONE
