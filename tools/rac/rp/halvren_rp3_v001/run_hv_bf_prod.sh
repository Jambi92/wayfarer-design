# run_hv_bf_prod.sh : Halvren body / face source order -- diagnostic production blends of the recommended central pair HB2 + HF2 on frozen v005
# (HV_M_REF_RP3_bodyfam_v002 from HVC1-HB2HF2, HV_F_REF_RP3_bodyfam_v002 from HVF178-HB2HF2): make_prod.py (production frame, hm08 map) + freeze_check read-back.
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; BP=/home/claude/stc/bin/python3; W=/tmp/claude-0/rt/hv; E=$W/hbe; O=$W/hbprod; mkdir -p $O/prod $O/readback; : > $O/prod_hashes.jsonl
ST="HALVREN BODY x FACE SOURCE CANDIDATE HB2 + HF2 (Halvren body / face source order 2026-10-29) - pelvis held, family human auricle (non-final ear); NOT accepted; NOT frozen"
for x in "HVC1-HB2HF2 HV_M_REF_RP3_bodyfam_v002" "HVF178-HB2HF2 HV_F_REF_RP3_bodyfam_v002"; do set -- $x
  $BP $T/make_prod.py -- $E/fam/$1_fam.npz $E/lm/$1_fam_landmarks.json $2 $O/prod "$ST" 2>/dev/null | grep '^{' >> $O/prod_hashes.jsonl
  $BP $T/freeze_check.py -- $O/prod/$2.blend $E/fam/$1_fam.npz $E/lm/$1_fam_landmarks.json $O/readback/$2_readback.json > $O/readback/$2.log 2>&1; done
echo HVBF_PROD_DONE
