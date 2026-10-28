# skp_ae.sh : order fd71f15 §5 pelvis -- skeletal-envelope (lean: muscle 0, weight 0, same skeleton construction) builds + skeletal_proxy.py readings
# for AEL1, AELF190 and the matched-stature Marchfolk / frozen-Fenn comparators (as Fenn order 57dc328 A4); plus regen / native export of AELF190.
W=/home/claude/wayfarer-design/tools/rac/w1; T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; BP=/home/claude/stc/bin/python3; cd /tmp/claude-0/rt/ae/partA; mkdir -p lean skp
echo '{"muscle": 0.0, "weight": 0.0}' > lean.json
L(){ $BP $W/build_variant.py $2/$1_build.json lean.json lean $1-LEAN > skp/$1-LEAN.log 2>&1; python3 $W/skeletal_proxy.py $2 lean $1 skp > skp/$1_skp.log 2>&1; echo "SKP $1 $?"; }
L AEL1 ref & L AELF190 build & wait
L MFM190 cmp & L MFF190 cmp & wait
L FNM190 cmp & L FNF190 cmp & wait
mkdir -p regen; $BP $T/regen.py build/AELF190_build.json build/AELF190_r6.npz regen > regen/regen.log 2>&1; $BP $T/native_export.py regen/AELF190_regen_source.blend regen/AELF190_native.npz > regen/native.log 2>&1
echo SKP_DONE
