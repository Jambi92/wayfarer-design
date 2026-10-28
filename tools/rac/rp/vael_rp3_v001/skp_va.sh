# skp_va.sh : Vael order Part A pelvis -- skeletal-envelope (lean: muscle 0, weight 0, same skeleton construction) builds + skeletal_proxy.py readings for
# VAL4, VALF178 and the 178 cm comparators (Marchfolk, frozen Fenn, frozen Aelari; c1 and c2), plus regen / native hm08 export of VALF178 (integrity).
W=/home/claude/wayfarer-design/tools/rac/w1; T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; BP=/home/claude/stc/bin/python3; cd ${VA_PA:-/tmp/claude-0/rt/va/partA}; mkdir -p lean skp
echo '{"muscle": 0.0, "weight": 0.0}' > lean.json
L(){ $BP $W/build_variant.py $2/$1_build.json lean.json lean $1-LEAN > skp/$1-LEAN.log 2>&1; python3 $W/skeletal_proxy.py $2 lean $1 skp > skp/$1_skp.log 2>&1; echo "SKP $1 $?"; }
L VAL4 ref & L VALF178 build & wait
L MFM178 cmp & L MFF178 cmp & wait
L FNM178 cmp & L FNF178 cmp & wait
L AEM178 cmp & L AEF178 cmp & wait
mkdir -p regen; $BP $T/regen.py build/VALF178_build.json build/VALF178_r6.npz regen > regen/regen.log 2>&1; $BP $T/native_export.py regen/VALF178_regen_source.blend regen/VALF178_native.npz > regen/native.log 2>&1
echo SKP_DONE
