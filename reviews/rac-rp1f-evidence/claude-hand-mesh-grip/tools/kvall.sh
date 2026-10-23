cd /tmp/claude-0/hand; P=/home/claude/stc/bin/python3
for s in $*; do
 if [ $s = L ]; then DG="A_L17 A_L18 A_L19 A_L20 A_Lthumb"; else DG="A_R21 A_R22 A_R23 A_R24 A_Rthumb"; fi
 for k in $DG; do [ -f f6/kv_bend_$k.json ] || $P tools/keyverify.py -- rig_c6 $s f6/bend_$k.json f6/bend_${k}_out.json f6/kv_bend_$k.json > f6/kv_bend_$k.log 2>&1; done
 for t in handle pinch; do [ -f f6/kv_${t}_$s.json ] || $P tools/keyverify.py -- rig_c6 $s f6/${t}_$s.json f6/${t}_${s}_out.json f6/kv_${t}_$s.json > f6/kv_${t}_$s.log 2>&1; done
done
echo KVDONE > f6/kv_$1.done
