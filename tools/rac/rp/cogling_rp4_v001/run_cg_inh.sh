# run_cg_inh.sh : RP4 Cogling order (9424c72) §7 / §9 -- DIAGNOSTIC inheritance test: the frozen Durrim MPFB_COMPACT_BRANCH_v002 and the frozen Pipkin
# MPFB_PIPKIN_COMPACT_BRANCH_v001 applied unchanged (their v005-face placements) to the Cogling v005 realizations, read with the authoritative validator
# v2 (D1+D3+D4+D5+D6) and audited; plus the size-consistent toe-probe diagnostic (§8) on the Cogling v005 bodies. Nothing here is a Cogling branch.
set -e
R=/home/claude/wayfarer-design; T=$R/tools/rac/rp/marchfolk_rp3_v001; D2=$R/tools/rac/rp/durrim_rp4_v002; P=$R/tools/rac/rp/pipkin_rp4_v001; C=$R/tools/rac/rp/cogling_rp4_v001
BP=/home/claude/stc/bin/python3; W=/tmp/claude-0/rt/cg; O=$W/inh; mkdir -p $O; cd $W
DU=$R/reviews/rac-rp4-evidence/durrim/v002/branch/MPFB_COMPACT_BRANCH_v002.json; PK=$R/reviews/rac-rp4-evidence/pipkin/branch/MPFB_PIPKIN_COMPACT_BRANCH_v001.json
one(){ id=$1
  python3 $D2/compact_branch_v002.py apply fam/${id}_fam.npz $DU $O/${id}_du2.npz > $O/${id}_du2.log 2>&1
  python3 $P/pk_branch_v001.py apply fam/${id}_fam.npz $PK $O/${id}_pk1.npz > $O/${id}_pk1.log 2>&1
  for b in du2 pk1; do
    python3 $T/validator_v2.py $O/${id}_$b.npz $O/${id}_${b}_validator.json --scale-ref 173.143 --d5 --d6-native src/${id}_native.npz > $O/${id}_${b}_val.log 2>&1
    $BP $T/audit.py $O/${id}_$b.npz $(case $id in CGF91-NAT) echo $W/nat/CGF91-NAT_r6.npz;; *) echo $R/reviews/reference-assets/r6/${id}_r6.npz;; esac) $O/${id}_${b}_audit.json $O/${id}_${b}_loops.npz > $O/${id}_${b}_audit.log 2>&1
  done; echo "INH $id"; }
one CGJ7 & one CGF91-NAT & wait
one CG76H-NAT & one CG107-NAT & wait
python3 $C/cg_toe_diag.py $O/cg_toe_station_diag.json fam/CG76H-NAT_fam.npz fam/CGJ7_fam.npz fam/CGF91-NAT_fam.npz fam/CG107-NAT_fam.npz > $O/toe_diag.log 2>&1
python3 $C/cg_inherit_sum.py $W $O/durrim_pipkin_branch_on_cogling.json
echo CG_INH_DONE
