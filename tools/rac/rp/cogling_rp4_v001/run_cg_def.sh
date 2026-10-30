# run_cg_def.sh MODE TAGDIR ID... : RP4 Cogling deformation (order 9424c72 §18) with marchfolk_rp3_v001/mf_deform.py (source rig + source MPFB weights carried
# through the body's linear map, plain LBS from R-6).  MODE: native | fam | cb (Cogling branch realization in /tmp/claude-0/rt/cg/<TAGDIR>/cb).
# Central c1 / c2 (CGJ7, CGF91-NAT): the full 18-pose family suite. Bounds (CG76H-NAT, CG107-NAT): the §18 key poses (ONLY_POSES).
R=/home/claude/wayfarer-design; T=$R/tools/rac/rp/marchfolk_rp3_v001; BP=/home/claude/stc/bin/python3; W=/tmp/claude-0/rt/cg; cd $W
KEY=shoulder_abd90_l,shoulder_flex90_l,elbow_130_l,wrist_flex60_l,wrist_ext60_l,fist_l,thumb_opposition_l,hip_flex90_l,knee_140_l,ankle_dorsi20_l,toe_flex30_l,toe_ext30_l,trunk_twist30,neck_flex30,neck_rot45
MODE=$1; TD=$2; shift 2
for id in "$@"; do
  case $MODE in native) C=src/${id}_native.npz; O=def; TAG=${id}_native;; fam) C=fam/${id}_fam.npz; O=def; TAG=${id}_fam;; cb) C=$TD/cb/${id}_cgb.npz; O=$TD/def; TAG=${id}_cgb;; esac
  case $id in CG76H-NAT|CG107-NAT) export ONLY_POSES=$KEY;; *) unset ONLY_POSES;; esac
  mkdir -p $O; $BP $T/mf_deform.py src/${id}_native.npz $C $O $TAG > $O/${TAG}.log 2>&1; echo "CGDEF $TAG"
done
