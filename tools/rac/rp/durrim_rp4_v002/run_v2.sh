# run_v2.sh BRANCH_DEF.json ID [ID...] : RP4 v002 per-body gate pipeline (order 8080f9f §7 / §10-§12) on the compact v002 realization of each body.
# Needs the run_ws.sh workspace (src natives, fam v005 realizations + audit loops). Outputs under $W/v2/{cb2,audit,lm,anat,val,contact,dens,def}.
#   apply (compact_branch_v002) -> audit (integrity / T-4 / poles / S7) -> landmarks (T-6) -> face rings -> anatomy (T-1/T-2/T-3/T-7) -> validator v2 (D1+D3+D4+D5+D6)
#   -> contact classes vs the same body's unbranched v005 realization -> density (v005 / v002 side by side) -> deformation (18 poses; native and v005 run by run_ws.sh def).
set -e
R=/home/claude/wayfarer-design; T=$R/tools/rac/rp/marchfolk_rp3_v001; S=$R/tools/rac/rp/sagekin_rp3_v001; D1=$R/tools/rac/rp/durrim_rp4_v001; D=$R/tools/rac/rp/durrim_rp4_v002
BP=/home/claude/stc/bin/python3; RA=$R/reviews/reference-assets; PA=$R/reviews/rac-rp4-evidence/durrim/partA; W=/tmp/claude-0/rt/du; O=$W/v2
DEF=$1; shift; mkdir -p $O/{cb2,audit,lm,anat,val,contact,dens,def,logs}
r6(){ case $1 in DUF137C-NAT) echo $PA/DUF137C-NAT_r6.npz;; MF152-NAT) echo $W/src/MF152-NAT_r6_first.npz;; *) echo $RA/r6/$1_r6.npz;; esac; }
one(){ id=$1; R6=$(r6 $id); cd $W
  python3 $D/compact_branch_v002.py apply fam/${id}_fam.npz $DEF $O/cb2/${id}_cb2.npz > $O/logs/${id}_apply.log 2>&1
  $BP $T/audit.py $O/cb2/${id}_cb2.npz $R6 $O/audit/${id}_cb2_audit.json $O/audit/${id}_cb2_loops.npz > $O/logs/${id}_audit.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $R6 $O/cb2/${id}_cb2.npz $O/lm/${id}_cb2_landmarks.json >> $O/logs/${id}_audit.log 2>&1
  python3 $T/face_rings.py $O/cb2/${id}_cb2.npz $O/audit/${id}_cb2_loops.npz $O/lm/${id}_cb2_landmarks.json $O/audit/${id}_cb2_face.json >> $O/logs/${id}_audit.log 2>&1
  python3 $T/anatomy.py $R6 $O/cb2/${id}_cb2.npz $O/anat/${id}_cb2_anatomy.json >> $O/logs/${id}_audit.log 2>&1
  python3 $T/validator_v2.py $O/cb2/${id}_cb2.npz $O/val/${id}_cb2_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz > $O/logs/${id}_val.log 2>&1
  python3 $S/contact_prop.py $O/contact/${id}_cb2_contact.json $id $O/cb2/${id}_cb2.npz $O/audit/${id}_cb2_loops.npz src/${id}_native.npz audit/${id}_native_loops.npz \
          fam/${id}_fam.npz audit/${id}_fam_loops.npz > $O/logs/${id}_contact.log 2>&1
  for k in fam cb2; do
    if [ $k = fam ]; then M=fam/${id}_fam.npz; L=audit/${id}_fam_loops.npz; LM=lm/${id}_fam_landmarks.json; FC=audit/${id}_fam_face.json; VA=val/${id}_fam_validator_v2_D1-D6.json
    else M=$O/cb2/${id}_cb2.npz; L=$O/audit/${id}_cb2_loops.npz; LM=$O/lm/${id}_cb2_landmarks.json; FC=$O/audit/${id}_cb2_face.json; VA=$O/val/${id}_cb2_validator_v2_D1-D6.json; fi
    python3 $D1/du_density.py $M $L $LM $FC $VA $O/dens/${id}_${k}_density.json > $O/logs/${id}_dens_$k.log 2>&1
  done
  echo "V2 $id"; }
deform(){ id=$1; cd $W; $BP $T/mf_deform.py src/${id}_native.npz $O/cb2/${id}_cb2.npz $O/def ${id}_cb2 > $O/logs/${id}_def.log 2>&1; echo "DEF2 $id"; }
case "$1" in
  def) shift; for id in "$@"; do deform $id; done ;;
  *) for id in "$@"; do one $id; done ;;
esac
