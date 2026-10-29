# run_hveval.sh ID... : Halvren body / face source order §18 -- v005 family propagation of source candidates (records in $HV_SRC = the candidate build folder:
# <ID>_build.json + <ID>_r6.npz), Standard v1 pipeline as aelari_rp3_v001/run_aeeval.sh: regen from the record (geometry identity), native hm08 export,
# propagate onto frozen MPFB Family Base v005 (no topology change), audit, landmarks, face rings, anatomy, validator D1 + D3 + D4 + D5 + D6, contact class,
# 18-pose deformation (native + family). c1 ids (HVC1-*) use the MF-M-R v005 contact baseline, c2 ids (HVF178-*) MF-F-R. Two at a time.
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; F=/home/claude/wayfarer-design/tools/rac/rp/mpfb_family; S=/home/claude/wayfarer-design/tools/rac/rp/sagekin_rp3_v001
BP=/home/claude/stc/bin/python3; B=/mnt/user-data/outputs/rp5; SRC=${HV_SRC:-/tmp/claude-0/rt/hv/hb/cand}
W=${HV_WORK:-/tmp/claude-0/rt/hv/hbe}; mkdir -p $W; cd $W; mkdir -p src fam audit anat lm val def contact
one(){ id=$1; R=$SRC/${id}_r6.npz; case $id in HVC1*) base=MF-M-R;; *) base=MF-F-R;; esac
  $BP $T/regen.py $SRC/${id}_build.json $R src > src/regen_$id.log 2>&1
  $BP $T/native_export.py src/${id}_regen_source.blend src/${id}_native.npz > src/${id}_native.log 2>&1; rm -f src/${id}_regen_source.blend
  $BP $F/propagate.py $B/MF_M_REF_RP3_retopo_v005.blend $B/MF_M_REF_RP3_retopo_v005_hm08_map.npz src/${id}_native.npz fam/${id}_fam.npz > fam/${id}_prop.log 2>&1
  $BP $T/audit.py src/${id}_native.npz $R audit/${id}_native_audit.json audit/${id}_native_loops.npz > audit/${id}_native.log 2>&1
  $BP $T/audit.py fam/${id}_fam.npz $R audit/${id}_fam_audit.json audit/${id}_fam_loops.npz > audit/${id}_fam.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $R fam/${id}_fam.npz lm/${id}_fam_landmarks.json >> audit/${id}_fam.log 2>&1
  python3 $T/face_rings.py fam/${id}_fam.npz audit/${id}_fam_loops.npz lm/${id}_fam_landmarks.json audit/${id}_fam_face.json >> audit/${id}_fam.log 2>&1
  python3 $T/anatomy.py $R fam/${id}_fam.npz anat/${id}_fam_anatomy.json >> audit/${id}_fam.log 2>&1
  python3 $T/validator_v2.py fam/${id}_fam.npz val/${id}_fam_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz > val/${id}.log 2>&1
  python3 $S/contact_prop.py contact/${id}_contact.json $id fam/${id}_fam.npz audit/${id}_fam_loops.npz src/${id}_native.npz audit/${id}_native_loops.npz \
          /tmp/claude-0/rt/v5/cand/${base}_v005.npz /tmp/claude-0/rt/v5/audit/${base}_v005_loops.npz > contact/${id}.log 2>&1
  $BP $T/mf_deform.py src/${id}_native.npz src/${id}_native.npz def ${id}_native > def/${id}_native.log 2>&1
  $BP $T/mf_deform.py src/${id}_native.npz fam/${id}_fam.npz def ${id}_fam > def/${id}_fam.log 2>&1
  rm -f def/*_${id}_native.npz
  echo "HVEVAL $id done"; }
set -- "$@"
while [ $# -gt 0 ]; do one $1 & if [ $# -gt 1 ]; then one $2 & fi; wait; shift; [ $# -gt 0 ] && shift; done
echo HVEVAL_DONE
