# Part B: unbranched MPFB Family Base v005 realizations of the Durrim sources (Standard v1 pipeline, as run_hvfinal.sh one(), no ear branch)
set -e
T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; F=/home/claude/wayfarer-design/tools/rac/rp/mpfb_family; S=/home/claude/wayfarer-design/tools/rac/rp/sagekin_rp3_v001
D=/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v001; BP=/home/claude/stc/bin/python3; B=/mnt/user-data/outputs/rp5; RA=/home/claude/wayfarer-design/reviews/reference-assets
W=/tmp/claude-0/rt/du; cd $W; mkdir -p src fam audit anat lm val def contact
one(){ id=$1; base=$2; bj=$3; R=$4
  [ -f src/${id}_regen_source.blend ] || $BP $D/du_regen.py $bj $R src > logs/regen_$id.log 2>&1
  $BP $T/native_export.py src/${id}_regen_source.blend src/${id}_native.npz > src/${id}_native.log 2>&1
  $BP $F/propagate.py $B/MF_M_REF_RP3_retopo_v005.blend $B/MF_M_REF_RP3_retopo_v005_hm08_map.npz src/${id}_native.npz fam/${id}_fam.npz > fam/${id}_prop.log 2>&1
  $BP $T/audit.py src/${id}_native.npz $R audit/${id}_native_audit.json audit/${id}_native_loops.npz > audit/${id}_native.log 2>&1
  $BP $T/audit.py fam/${id}_fam.npz $R audit/${id}_fam_audit.json audit/${id}_fam_loops.npz > audit/${id}_fam.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $R fam/${id}_fam.npz lm/${id}_fam_landmarks.json >> audit/${id}_fam.log 2>&1
  python3 $T/face_rings.py fam/${id}_fam.npz audit/${id}_fam_loops.npz lm/${id}_fam_landmarks.json audit/${id}_fam_face.json >> audit/${id}_fam.log 2>&1
  python3 $T/anatomy.py $R fam/${id}_fam.npz anat/${id}_fam_anatomy.json >> audit/${id}_fam.log 2>&1
  python3 $T/validator_v2.py fam/${id}_fam.npz val/${id}_fam_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz > val/${id}_fam.log 2>&1
  python3 $S/contact_prop.py contact/${id}_contact.json $id fam/${id}_fam.npz audit/${id}_fam_loops.npz src/${id}_native.npz audit/${id}_native_loops.npz \
          /tmp/claude-0/rt/v5/cand/${base}_v005.npz /tmp/claude-0/rt/v5/audit/${base}_v005_loops.npz > contact/${id}.log 2>&1
  $BP $T/mf_deform.py src/${id}_native.npz src/${id}_native.npz def ${id}_native > def/${id}_native.log 2>&1
  $BP $T/mf_deform.py src/${id}_native.npz fam/${id}_fam.npz def ${id}_fam > def/${id}_fam.log 2>&1
  echo "B $id"; }
one DU137C-NAT MF-M-R $RA/builds/DU137C-NAT_build.json $RA/r6/DU137C-NAT_r6.npz & one DUF137C-NAT MF-F-R $W/nat/DUF137C-NAT_build.json $W/nat/DUF137C-NAT_r6.npz & wait
one DU122C-NAT MF-M-R $RA/builds/DU122C-NAT_build.json $RA/r6/DU122C-NAT_r6.npz & one DU152C-NAT MF-M-R $RA/builds/DU152C-NAT_build.json $RA/r6/DU152C-NAT_r6.npz & wait
one MF152-NAT MF-M-R $W/nat/MF152-NAT_build.json $W/nat/MF152-NAT_r6.npz
echo PARTB_DONE
