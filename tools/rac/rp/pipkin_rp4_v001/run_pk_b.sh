# run_pk_b.sh [ID...] : RP4 Pipkin Phase A (order 25f7ba0 §5) -- unbranched MPFB Family Base v005 realizations of PK91 / PK-NAT / PK122 / PKF107 exactly as
# durrim_rp4_v002/run_ws.sh one() (propagate_core.py = Standard v1 step 2 from the committed v005 core; audit / landmarks / face rings / anatomy / validator v2
# D1+D3+D4+D5+D6 / contact vs the MF v005 base of the same configuration / density). No topology edits.
set -e
R=/home/claude/wayfarer-design; T=$R/tools/rac/rp/marchfolk_rp3_v001; S=$R/tools/rac/rp/sagekin_rp3_v001; D1=$R/tools/rac/rp/durrim_rp4_v001; D2=$R/tools/rac/rp/durrim_rp4_v002
BP=/home/claude/stc/bin/python3; RA=$R/reviews/reference-assets; MP=$R/reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/maps
CORE=$MP/MPFB_FAMILY_BASE_v005_core.npz; MAP=$MP/MPFB_FAMILY_BASE_v005_hm08_map.npz; W=/tmp/claude-0/rt/pk; V5=/tmp/claude-0/rt/v5; cd $W; mkdir -p src fam audit anat lm val contact dens logs
r6(){ case $1 in PKF107-NAT) echo $W/nat/PKF107-NAT_r6.npz;; *) echo $RA/r6/$1_r6.npz;; esac; }
one(){ id=$1; b=$2; R6=$(r6 $id)
  $BP $T/native_export.py src/${id}_regen_source.blend src/${id}_native.npz > src/${id}_native.log 2>&1
  python3 $D2/propagate_core.py $CORE $MAP src/${id}_native.npz fam/${id}_fam.npz > fam/${id}_prop.log 2>&1
  $BP $T/audit.py src/${id}_native.npz $R6 audit/${id}_native_audit.json audit/${id}_native_loops.npz > audit/${id}_native.log 2>&1
  $BP $T/audit.py fam/${id}_fam.npz $R6 audit/${id}_fam_audit.json audit/${id}_fam_loops.npz > audit/${id}_fam.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $R6 fam/${id}_fam.npz lm/${id}_fam_landmarks.json >> audit/${id}_fam.log 2>&1
  python3 $T/face_rings.py fam/${id}_fam.npz audit/${id}_fam_loops.npz lm/${id}_fam_landmarks.json audit/${id}_fam_face.json >> audit/${id}_fam.log 2>&1
  python3 $T/anatomy.py $R6 fam/${id}_fam.npz anat/${id}_fam_anatomy.json >> audit/${id}_fam.log 2>&1
  python3 $T/validator_v2.py fam/${id}_fam.npz val/${id}_fam_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz > val/${id}_fam.log 2>&1
  python3 $S/contact_prop.py contact/${id}_contact.json $id fam/${id}_fam.npz audit/${id}_fam_loops.npz src/${id}_native.npz audit/${id}_native_loops.npz \
          $V5/cand/${b}_v005.npz $V5/audit/${b}_v005_loops.npz > contact/${id}.log 2>&1
  python3 $D1/du_density.py fam/${id}_fam.npz audit/${id}_fam_loops.npz lm/${id}_fam_landmarks.json audit/${id}_fam_face.json val/${id}_fam_validator_v2_D1-D6.json dens/${id}_fam_density.json > logs/dens_$id.log 2>&1
  echo "B $id"; }
one PK-NAT MF-M-R & one PKF107-NAT MF-F-R & wait
one PK91-NAT MF-M-R & one PK122-NAT MF-M-R & wait
echo PK_B_DONE
