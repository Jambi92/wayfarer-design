# skp_hv.sh : Halvren central-anchor order Part A / D pelvis -- skeletal-envelope (lean: muscle 0, weight 0, same skeleton construction) builds +
# skeletal_proxy.py readings for HVC1, HVF178 and the 178 cm Sagekin / Skarn comparators (Marchfolk / frozen Fenn / frozen Aelari from Vael Part A, frozen
# Vael from the Vael final rebuild -- same committed records, copied), plus regen / native hm08 export of HVF178 (integrity / regeneration identity).
W=/home/claude/wayfarer-design/tools/rac/w1; T=/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001; BP=/home/claude/stc/bin/python3; cd ${HV_PA:-/tmp/claude-0/rt/hv/partA}; mkdir -p lean skp regen
echo '{"muscle": 0.0, "weight": 0.0}' > lean.json
for n in MFM178 MFF178 FNM178 FNF178 AEM178 AEF178; do cp /tmp/claude-0/rt/va/partA/skp/${n}_skp.json skp/; done
cp /tmp/claude-0/rt/va/final/skp/VAL4-R1-VD2-VF2_skp.json skp/VAM178_skp.json; cp /tmp/claude-0/rt/va/final/skp/VALF178-R1-VD2-VF2_skp.json skp/VAF178_skp.json
L(){ $BP $W/build_variant.py $2/$1_build.json lean.json lean $1-LEAN > skp/$1-LEAN.log 2>&1; python3 $W/skeletal_proxy.py $2 lean $1 skp > skp/$1_skp.log 2>&1; echo "SKP $1 $?"; }
L HVC1 ref; L HVF178 build; L SGM178 cmp; L SGF178 cmp; L SKM178 cmp; L SKF178 cmp
$BP $T/regen.py build/HVF178_build.json build/HVF178_r6.npz regen > regen/regen.log 2>&1; $BP $T/native_export.py regen/HVF178_regen_source.blend regen/HVF178_native.npz > regen/native.log 2>&1
echo SKP_DONE
