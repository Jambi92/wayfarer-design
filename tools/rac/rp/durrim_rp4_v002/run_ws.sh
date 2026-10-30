# run_ws.sh : RP4 v002 workspace rebuild (cloud). Regenerates the Durrim sources + MF152 comparator and MF-M-R / MF-F-R bases, then the
# unbranched MPFB Family Base v005 realizations exactly as durrim_rp4_v001/run_b.sh one(), with propagate_core.py (faces/UVs from the committed
# v005 core) in place of propagate.py (needs the PC production .blend). Usage: bash run_ws.sh [ID...]   (default: all)
set -e
R=/home/claude/wayfarer-design; T=$R/tools/rac/rp/marchfolk_rp3_v001; S=$R/tools/rac/rp/sagekin_rp3_v001
D1=$R/tools/rac/rp/durrim_rp4_v001; D=$R/tools/rac/rp/durrim_rp4_v002; BP=/home/claude/stc/bin/python3
RA=$R/reviews/reference-assets; PA=$R/reviews/rac-rp4-evidence/durrim/partA; MP=$R/reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/maps
CORE=$MP/MPFB_FAMILY_BASE_v005_core.npz; MAP=$MP/MPFB_FAMILY_BASE_v005_hm08_map.npz
W=/tmp/claude-0/rt/du; V5=/tmp/claude-0/rt/v5; mkdir -p $W/{logs,src,fam,audit,anat,lm,val,def,contact} $V5/{src,cand,audit}
regen(){ id=$1; bj=$2; cr=$3; out=$4
  if [ ! -f $out/${id}_regen_source.blend ]; then
    if [ -z "$cr" ]; then  # no committed R-6: build once, then regenerate against the first build (determinism proof)
      $BP $D1/du_regen.py $bj $RA/r6/MF-M-R_r6.npz $out > $W/logs/regen0_$id.log 2>&1 || true
      cp $out/${id}_r6_regen.npz $out/${id}_r6_first.npz; cr=$out/${id}_r6_first.npz; rm -f $out/${id}_regen_source.blend
    fi
    $BP $D1/du_regen.py $bj $cr $out > $W/logs/regen_$id.log 2>&1
  fi
  $BP $T/native_export.py $out/${id}_regen_source.blend $out/${id}_native.npz > $out/${id}_native.log 2>&1; }
base(){ id=$1; bj=$2; cr=$3   # MF-M-R / MF-F-R v005 realizations for contact_prop
  regen $id $bj $cr $V5/src
  python3 $D/propagate_core.py $CORE $MAP $V5/src/${id}_native.npz $V5/cand/${id}_v005.npz > $V5/cand/${id}_prop.log 2>&1
  $BP $T/audit.py $V5/cand/${id}_v005.npz $cr $V5/audit/${id}_v005_audit.json $V5/audit/${id}_v005_loops.npz > $V5/audit/${id}.log 2>&1
  echo "BASE $id"; }
one(){ id=$1; b=$2; bj=$3; R6=$4; cd $W
  regen $id $bj "$R6" src; [ -n "$R6" ] || R6=src/${id}_r6_first.npz
  python3 $D/propagate_core.py $CORE $MAP src/${id}_native.npz fam/${id}_fam.npz > fam/${id}_prop.log 2>&1
  $BP $T/audit.py src/${id}_native.npz $R6 audit/${id}_native_audit.json audit/${id}_native_loops.npz > audit/${id}_native.log 2>&1
  $BP $T/audit.py fam/${id}_fam.npz $R6 audit/${id}_fam_audit.json audit/${id}_fam_loops.npz > audit/${id}_fam.log 2>&1
  python3 $T/landmarks.py src/${id}_native.npz $R6 fam/${id}_fam.npz lm/${id}_fam_landmarks.json >> audit/${id}_fam.log 2>&1
  python3 $T/face_rings.py fam/${id}_fam.npz audit/${id}_fam_loops.npz lm/${id}_fam_landmarks.json audit/${id}_fam_face.json >> audit/${id}_fam.log 2>&1
  python3 $T/anatomy.py $R6 fam/${id}_fam.npz anat/${id}_fam_anatomy.json >> audit/${id}_fam.log 2>&1
  python3 $T/validator_v2.py fam/${id}_fam.npz val/${id}_fam_validator_v2_D1-D6.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz > val/${id}_fam.log 2>&1
  python3 $S/contact_prop.py contact/${id}_contact.json $id fam/${id}_fam.npz audit/${id}_fam_loops.npz src/${id}_native.npz audit/${id}_native_loops.npz \
          $V5/cand/${b}_v005.npz $V5/audit/${b}_v005_loops.npz > contact/${id}.log 2>&1
  echo "WS $id"; }
deform(){ id=$1; cd $W
  $BP $T/mf_deform.py src/${id}_native.npz src/${id}_native.npz def ${id}_native > def/${id}_native.log 2>&1
  $BP $T/mf_deform.py src/${id}_native.npz fam/${id}_fam.npz def ${id}_fam > def/${id}_fam.log 2>&1; echo "DEF $id"; }
case "${1:-all}" in
 bases) base MF-M-R $RA/builds/MF-M-R_build.json $RA/r6/MF-M-R_r6.npz & base MF-F-R $RA/builds/MF-F-R_build.json $RA/r6/MF-F-R_r6.npz & wait ;;
 du)  one DU137C-NAT MF-M-R $RA/builds/DU137C-NAT_build.json $RA/r6/DU137C-NAT_r6.npz & one DUF137C-NAT MF-F-R $PA/DUF137C-NAT_build.json $PA/DUF137C-NAT_r6.npz & wait
      one DU122C-NAT MF-M-R $RA/builds/DU122C-NAT_build.json $RA/r6/DU122C-NAT_r6.npz & one DU152C-NAT MF-M-R $RA/builds/DU152C-NAT_build.json $RA/r6/DU152C-NAT_r6.npz & wait
      one MF152-NAT MF-M-R $PA/MF152-NAT_build.json "" ;;
 def) for id in ${@:2}; do deform $id; done ;;
esac
