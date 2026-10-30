# run_pk_v1.sh DEF.json ID... | def ID... : RP4 Pipkin per-body gates on MPFB_PIPKIN_COMPACT_BRANCH_v001 (as durrim_rp4_v002/run_v2.sh): apply -> audit -> landmarks -> face rings ->
# anatomy -> validator v2 (D1+D3+D4+D5+D6) -> contact vs the body's v005 realization -> density (v005 / branch). Outputs /tmp/claude-0/rt/pk/v1/.
set -e
R=/home/claude/wayfarer-design; T=$R/tools/rac/rp/marchfolk_rp3_v001; S=$R/tools/rac/rp/sagekin_rp3_v001; D1=$R/tools/rac/rp/durrim_rp4_v001; P=$R/tools/rac/rp/pipkin_rp4_v001
BP=/home/claude/stc/bin/python3; RA=$R/reviews/reference-assets; W=/tmp/claude-0/rt/pk; O=$W/v1; mkdir -p $O/{cb,audit,lm,anat,val,contact,dens,def,logs}
r6(){ case $1 in PKF107-NAT) echo $W/nat/PKF107-NAT_r6.npz;; *) echo $RA/r6/$1_r6.npz;; esac; }
one(){ id=$1; R6=$(r6 $id); cd $W
  python3 $P/pk_branch_v001.py apply fam/${id}_fam.npz $DEF $O/cb/${id}_pkb.npz > $O/logs/${id}_apply.log 2>&1
  $BP $T/audit.py $O/cb/${id}_pkb.npz $R6 $O/audit/${id}_pkb_audit.json $O/audit/${id}_pkb_loops.npz > $O/logs/${id}_audit.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $R6 $O/cb/${id}_pkb.npz $O/lm/${id}_pkb_landmarks.json >> $O/logs/${id}_audit.log 2>&1
  python3 $T/face_rings.py $O/cb/${id}_pkb.npz $O/audit/${id}_pkb_loops.npz $O/lm/${id}_pkb_landmarks.json $O/audit/${id}_pkb_face.json >> $O/logs/${id}_audit.log 2>&1
  python3 $T/anatomy.py $R6 $O/cb/${id}_pkb.npz $O/anat/${id}_pkb_anatomy.json >> $O/logs/${id}_audit.log 2>&1
  python3 $T/validator_v2.py $O/cb/${id}_pkb.npz $O/val/${id}_pkb_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz > $O/logs/${id}_val.log 2>&1
  python3 $S/contact_prop.py $O/contact/${id}_pkb_contact.json $id $O/cb/${id}_pkb.npz $O/audit/${id}_pkb_loops.npz src/${id}_native.npz audit/${id}_native_loops.npz \
          fam/${id}_fam.npz audit/${id}_fam_loops.npz > $O/logs/${id}_contact.log 2>&1
  python3 $D1/du_density.py $O/cb/${id}_pkb.npz $O/audit/${id}_pkb_loops.npz $O/lm/${id}_pkb_landmarks.json $O/audit/${id}_pkb_face.json $O/val/${id}_pkb_validator_v2_D1-D6.json $O/dens/${id}_pkb_density.json > $O/logs/${id}_dens.log 2>&1
  echo "PKV1 $id"; }
deform(){ id=$1; cd $W; $BP $T/mf_deform.py src/${id}_native.npz $O/cb/${id}_pkb.npz $O/def ${id}_pkb > $O/logs/${id}_def.log 2>&1; echo "PKDEF $id"; }
if [ "$1" = def ]; then shift; for id in "$@"; do deform $id; done; else DEF=$1; shift; for id in "$@"; do one $id; done; fi
