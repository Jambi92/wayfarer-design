# run_cg_v1.sh DEF.json ID... : RP4 Cogling per-body gates on MPFB_COGLING_COMPACT_BRANCH_v001 (copy of pipkin_rp4_v001/run_pk_v1.sh): apply -> audit -> landmarks (cg_landmarks.py) -> face rings ->
# anatomy -> validator v2 (D1+D3+D4+D5+D6) -> contact vs the body v005 realization -> density. Outputs /tmp/claude-0/rt/cg/v1/ (deformation: run_cg_def.sh cb).
set -e
R=/home/claude/wayfarer-design; T=$R/tools/rac/rp/marchfolk_rp3_v001; S=$R/tools/rac/rp/sagekin_rp3_v001; D1=$R/tools/rac/rp/durrim_rp4_v001; P=$R/tools/rac/rp/cogling_rp4_v001
BP=/home/claude/stc/bin/python3; RA=$R/reviews/reference-assets; W=/tmp/claude-0/rt/cg; O=${OUTDIR:-$W/v1}; mkdir -p $O/{cb,audit,lm,anat,val,contact,dens,def,logs}
r6(){ case $1 in CGF91-NAT) echo $W/nat/CGF91-NAT_r6.npz;; *) echo $RA/r6/$1_r6.npz;; esac; }
one(){ id=$1; R6=$(r6 $id); cd $W
  python3 $P/cg_branch_v001.py apply fam/${id}_fam.npz $DEF $O/cb/${id}_cgb.npz > $O/logs/${id}_apply.log 2>&1
  $BP $T/audit.py $O/cb/${id}_cgb.npz $R6 $O/audit/${id}_cgb_audit.json $O/audit/${id}_cgb_loops.npz > $O/logs/${id}_audit.log 2>&1
  python3 $P/cg_landmarks.py src/${id}_native.npz $R6 $O/cb/${id}_cgb.npz $O/lm/${id}_cgb_landmarks.json >> $O/logs/${id}_audit.log 2>&1
  python3 $T/face_rings.py $O/cb/${id}_cgb.npz $O/audit/${id}_cgb_loops.npz $O/lm/${id}_cgb_landmarks.json $O/audit/${id}_cgb_face.json >> $O/logs/${id}_audit.log 2>&1
  python3 $T/anatomy.py $R6 $O/cb/${id}_cgb.npz $O/anat/${id}_cgb_anatomy.json >> $O/logs/${id}_audit.log 2>&1
  python3 $T/validator_v2.py $O/cb/${id}_cgb.npz $O/val/${id}_cgb_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz > $O/logs/${id}_val.log 2>&1
  python3 $S/contact_prop.py $O/contact/${id}_cgb_contact.json $id $O/cb/${id}_cgb.npz $O/audit/${id}_cgb_loops.npz src/${id}_native.npz audit/${id}_native_loops.npz \
          fam/${id}_fam.npz audit/${id}_fam_loops.npz > $O/logs/${id}_contact.log 2>&1
  python3 $D1/du_density.py $O/cb/${id}_cgb.npz $O/audit/${id}_cgb_loops.npz $O/lm/${id}_cgb_landmarks.json $O/audit/${id}_cgb_face.json $O/val/${id}_cgb_validator_v2_D1-D6.json $O/dens/${id}_cgb_density.json > $O/logs/${id}_dens.log 2>&1
  echo "CGV1 $id"; }
DEF=$1; shift; for id in "$@"; do one $id; done
