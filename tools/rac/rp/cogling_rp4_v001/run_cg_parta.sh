# run_cg_parta.sh : RP4 Cogling order (9424c72) §3 / §4 Part A -- exact regeneration of the accepted Cogling sources CGJ7 / CG76H-NAT / CG107-NAT
# (du_regen.py, recorded route), the new configuration-2 central technical anchor CGF91-NAT (native short-adult route, CGJ7 targets / bone scales /
# girth beta / CGJ7 head factor on the MPFB configuration-2 base macro; cg_native_c2.py) + its determinism rebuild, the route-matched 91 cm Marchfolk comparators MF91 / MFF91
# (sex-consistency only), the DIAGNOSTIC equal-height Pipkin c2 comparator PKF91-NAT (PKF107 route at 91 cm; §4B rows only), the normalized Marchfolk comparators MF-M-R / MF-F-R, and the accepted COG-BODY-11 toddler proxy CHILD1 (76 cm, ~1.5 y;
# diagnostic only). Full / lean rebuilds, skin measurements (run_candidate) and skeletal proxy for every body.
W1=/home/claude/wayfarer-design/tools/rac/w1; RA=/home/claude/wayfarer-design/reviews/reference-assets; D=/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v001; C=/home/claude/wayfarer-design/tools/rac/rp/cogling_rp4_v001
BP=/home/claude/stc/bin/python3; W=/tmp/claude-0/rt/cg; cd $W
for id in CGJ7 CG76H-NAT; do [ -f src/${id}_regen_check.json ] || $BP $D/du_regen.py $RA/builds/${id}_build.json $RA/r6/${id}_r6.npz src > logs/regen_$id.log 2>&1 & done; wait
[ -f src/CG107-NAT_regen_check.json ] || $BP $D/du_regen.py $RA/builds/CG107-NAT_build.json $RA/r6/CG107-NAT_r6.npz src > logs/regen_CG107-NAT.log 2>&1 &
[ -f nat/CGF91-NAT_build.json ] || $BP $C/cg_native_c2.py $W/nat/CGF91.cfg.json $W/nat > $W/logs/nat_CGF91.log 2>&1 &
wait
for n in MF91 MFF91 PKF91; do [ -f nat/$n-NAT_build.json ] || (cd $W1 && $BP native_short.py $W/nat/$n.cfg.json $W/nat > $W/logs/nat_$n.log 2>&1) & done; wait
[ -f src/CGF91-NAT_regen_check.json ] || $BP $D/du_regen.py $W/nat/CGF91-NAT_build.json $W/nat/CGF91-NAT_r6.npz src > logs/regen_CGF91-NAT.log 2>&1
cp $W/../pk/ref/MF-M-R_rest.npz ref/ 2>/dev/null
one(){ id=$1; bj=$2
  [ -f $W/full/${id}_meas.json ] && [ -f $W/skp/${id}_skp.json ] && { echo "A $id (cached)"; return; }
  (cd $W1 && $BP build_variant.py $bj $W/none.json $W/full $id > $W/logs/full_$id.log 2>&1 && python3 run_candidate.py $W/full $id $W/ref/MF-M-R_rest.npz > $W/logs/fullm_$id.log 2>&1)
  (cd $W1 && $BP build_variant.py $bj $W/lean.json $W/full ${id}-LEAN > $W/logs/lean_$id.log 2>&1 && python3 skeletal_proxy.py $W/full $W/full $id $W/skp > $W/logs/skp_$id.log 2>&1)
  echo "A $id"; }
one CGJ7 $RA/builds/CGJ7_build.json & one CGF91-NAT $W/nat/CGF91-NAT_build.json & wait
one CG76H-NAT $RA/builds/CG76H-NAT_build.json & one CG107-NAT $RA/builds/CG107-NAT_build.json & wait
one MF91-NAT $W/nat/MF91-NAT_build.json & one MFF91-NAT $W/nat/MFF91-NAT_build.json & wait
one PKF91-NAT $W/nat/PKF91-NAT_build.json
one MF-M-R $RA/builds/MF-M-R_build.json & one MF-F-R $RA/builds/MF-F-R_build.json & wait
[ -f $W/skp/CHILD1_skp.json ] || (cd $W1 && $BP build_variant.py $RA/builds/MF-M-R_build.json $W/child/c1.json $W/child CHILD1 > $W/logs/child1.log 2>&1 && python3 run_candidate.py $W/child CHILD1 $W/ref/MF-M-R_rest.npz > $W/logs/child1m.log 2>&1
 $BP build_variant.py $W/child/CHILD1_build.json $W/lean.json $W/child CHILD1-LEAN > $W/logs/child1l.log 2>&1 && python3 skeletal_proxy.py $W/child $W/child CHILD1 $W/skp > $W/logs/skp_CHILD1.log 2>&1)
echo CG_PARTA_DONE
