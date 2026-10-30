# Part A: equal-height Marchfolk comparators (native route), full / lean rebuilds, measurements, skeletal proxy for every Part A body
W1=/home/claude/wayfarer-design/tools/rac/w1; RA=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; W=/tmp/claude-0/rt/du; cd $W; mkdir -p full skp
for n in MF137 MFF137; do (cd $W1 && $BP native_short.py $W/nat/$n.cfg.json $W/nat > $W/logs/nat_$n.log 2>&1) & done; wait
one(){ id=$1; bj=$2
  (cd $W1 && $BP build_variant.py $bj $W/none.json $W/full $id > $W/logs/full_$id.log 2>&1 && python3 run_candidate.py $W/full $id /tmp/claude-0/rt/hv/partA/ref/MF-M-R_rest.npz > $W/logs/fullm_$id.log 2>&1)
  (cd $W1 && $BP build_variant.py $bj $W/lean.json $W/full ${id}-LEAN > $W/logs/lean_$id.log 2>&1 && python3 skeletal_proxy.py $W/full $W/full $id $W/skp > $W/logs/skp_$id.log 2>&1)
  echo "A $id"; }
one DU137C-NAT $RA/DU137C-NAT_build.json & one DU122C-NAT $RA/DU122C-NAT_build.json & one DU152C-NAT $RA/DU152C-NAT_build.json & wait
one DUF137C-NAT $W/nat/DUF137C-NAT_build.json & one MF137-NAT $W/nat/MF137-NAT_build.json & one MFF137-NAT $W/nat/MFF137-NAT_build.json & wait
one MF152-NAT $W/nat/MF152-NAT_build.json & one MFF152-NAT $W/nat/MFF152-NAT_build.json & wait
echo PARTA_DONE
