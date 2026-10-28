# skp_va2.sh ID... : Vael body / face source order §8 -- skeletal-envelope (lean: muscle 0, weight 0, same skeleton construction, as skp_va.sh) builds
# and skeletal_proxy.py readings for Vael source records in $VB_DIR/r1 (default /tmp/claude-0/rt/va2/vc2); comparators come from the Part A skp folder.
W=/home/claude/wayfarer-design/tools/rac/w1; BP=/home/claude/stc/bin/python3; D=${VB_DIR:-/tmp/claude-0/rt/va2/vc2}; S=${SKP_SRC:-r1}; cd $D; mkdir -p lean skp   # custom-deformation order: VB_DIR=/tmp/claude-0/rt/vd SKP_SRC=cand
echo '{"muscle": 0.0, "weight": 0.0}' > lean.json
L(){ $BP $W/build_variant.py $S/$1_build.json lean.json lean $1-LEAN > skp/$1-LEAN.log 2>&1; python3 $W/skeletal_proxy.py $S lean $1 skp > skp/$1_skp.log 2>&1; echo "SKP $1 $?"; }
for i in "$@"; do L $i & while [ $(jobs -r | wc -l) -ge 2 ]; do sleep 1; done; done; wait
echo SKP_DONE
