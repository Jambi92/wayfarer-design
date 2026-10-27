R=/home/claude/wayfarer-design/reviews/reference-assets/builds; W=/home/claude/wayfarer-design/tools/rac/w1; BP=/home/claude/stc/bin/python3; cd /tmp/claude-0/rt/fn/cf
T="head-scale-vert-incr head-scale-horiz-decr head-scale-depth-decr head-back-scale-depth-incr head-oval head-invertedtriangular head-triangular head-diamond head-round forehead-nubian-decr forehead-nubian-incr forehead-trans-backward forehead-temple-decr LR:cheek-trans-up LR:cheek-bones-incr LR:cheek-volume-decr LR:cheek-inner-decr chin-width-decr chin-bones-decr chin-height-decr chin-prominent-decr chin-jaw-drop-decr chin-triangle neck-scale-horiz-decr"
run(){ t=$1; tag=$(echo $t | tr ':' '_'); echo "{\"targets\": {\"$t\": 0.5}}" > probe/$tag.json; $BP $W/build_variant.py $R/FNL4_build.json probe/$tag.json probe/$tag P > probe/$tag.log 2>&1; echo "PROBE $t $?"; }
set -- $T
while [ $# -gt 0 ]; do run $1 & if [ $# -gt 1 ]; then run $2 & fi; wait; shift; [ $# -gt 0 ] && shift; done
echo PROBEDONE
