R=/home/claude/wayfarer-design/reviews/reference-assets/builds; W=/home/claude/wayfarer-design/tools/rac/w1; BP=/home/claude/stc/bin/python3; cd /tmp/claude-0/rt/fn/cf
run(){ $BP $W/build_variant.py $1 cand/$2_overrides.json cand/$3 $3 > cand/$3.log 2>&1; echo "BUILT $3 $?"; }
run $R/FNL4_build.json CF1 FNL4-CF1 & run $R/FNL4_build.json CF2 FNL4-CF2 & wait
run $R/FNL4_build.json CF3 FNL4-CF3 & run $R/FNF181_build.json CF1 FNF181-CF1 & wait
run $R/FNF181_build.json CF2 FNF181-CF2 & run $R/FNF181_build.json CF3 FNF181-CF3 & wait
echo CFBUILDDONE
