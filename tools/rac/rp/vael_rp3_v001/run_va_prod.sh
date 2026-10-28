# run_va_prod.sh : Vael order Part B -- diagnostic body-family candidates VA_{M,F}_REF_RP3_bodyfam_v001 (make_prod.py, production frame, hm08 map),
# freeze_check read-back (no save), then the manifest / sidecars (va_manifest.py).
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; BP=/home/claude/stc/bin/python3; D=/home/claude/wayfarer-design/tools/rac/rp/vael_rp3_v001
W=${VA_WORK:-/tmp/claude-0/rt/va}; E=${VA_EVI:?evidence dir}; cd $W; mkdir -p prod readback; : > prod_hashes.jsonl
ST=${VA_STATUS:-"VAEL BODY-FAMILY DIAGNOSTIC CANDIDATE (Vael order 2026-10-28) - carries the family human auricle; NOT final Vael body; NOT frozen"}
C1=${VA_C1:-VAL4}; C2=${VA_C2:-VALF178}; V_=${VA_PROD_VER:-v001}   # body / face source order: VA_C1=VAL4-R1 VA_C2=VALF178-R1 VA_PROD_VER=v002
for x in "$C1 VA_M_REF_RP3_bodyfam_$V_" "$C2 VA_F_REF_RP3_bodyfam_$V_"; do set -- $x
  $BP $T/make_prod.py -- fam/$1_fam.npz lm/$1_fam_landmarks.json $2 prod "$ST" 2>/dev/null | grep '^{' >> prod_hashes.jsonl
  $BP $T/freeze_check.py -- prod/$2.blend fam/$1_fam.npz lm/$1_fam_landmarks.json readback/$2_readback.json > readback/$2.log 2>&1; done
VA_C1=$C1 VA_C2=$C2 VA_PROD_VER=$V_ python3 $D/va_manifest.py $W $E
echo VA_PROD_DONE
