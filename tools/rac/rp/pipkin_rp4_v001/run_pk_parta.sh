# run_pk_parta.sh : RP4 Pipkin order (25f7ba0) §3 / §4 Part A -- full / lean rebuilds, skin measurements (run_candidate) and skeletal proxy for
# PK91 / PK-NAT / PK122 (accepted), PKF107-NAT (new c2 technical anchor), the route-matched Marchfolk comparators MF107 / MFF107 (sex-consistency only)
# and the NORMALIZED Marchfolk comparators MF-M-R / MF-F-R (the W2H comparator rule for Pipkin: ratios vs Marchfolk 173, never a same-height human).
W1=/home/claude/wayfarer-design/tools/rac/w1; RA=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; W=/tmp/claude-0/rt/pk
cd $W; mkdir -p full skp ref; echo '{}' > none.json; echo '{"muscle": 0.0, "weight": 0.0}' > lean.json
[ -f ref/MF-M-R_rest.npz ] || (cd $W1 && $BP build_variant.py $RA/MF-M-R_build.json $W/none.json $W/ref MF-M-R > $W/logs/ref.log 2>&1)
one(){ id=$1; bj=$2
  (cd $W1 && $BP build_variant.py $bj $W/none.json $W/full $id > $W/logs/full_$id.log 2>&1 && python3 run_candidate.py $W/full $id $W/ref/MF-M-R_rest.npz > $W/logs/fullm_$id.log 2>&1)
  (cd $W1 && $BP build_variant.py $bj $W/lean.json $W/full ${id}-LEAN > $W/logs/lean_$id.log 2>&1 && python3 skeletal_proxy.py $W/full $W/full $id $W/skp > $W/logs/skp_$id.log 2>&1)
  echo "A $id"; }
one PK-NAT $RA/PK-NAT_build.json & one PKF107-NAT $W/nat/PKF107-NAT_build.json & wait
one PK91-NAT $RA/PK91-NAT_build.json & one PK122-NAT $RA/PK122-NAT_build.json & wait
one MF107-NAT $W/nat/MF107-NAT_build.json & one MFF107-NAT $W/nat/MFF107-NAT_build.json & wait
one MF-M-R $RA/MF-M-R_build.json & one MF-F-R $RA/MF-F-R_build.json & wait
echo PK_PARTA_DONE
