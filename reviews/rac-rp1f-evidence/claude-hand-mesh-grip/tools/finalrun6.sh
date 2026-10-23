# finalrun6.sh SIDE : all movement / grip tests on rig_c6 with soft-tissue correctives + natural-contact stops
cd /tmp/claude-0/hand; S=$1; RG=rig_c6; P=/home/claude/stc/bin/python3; G=tools/gripsolve2.py; O=f6
if [ $S = L ]; then DG="A_L17 A_L18 A_L19 A_L20"; IX=A_L20; CS=0.2; CM=thumb; else DG="A_R21 A_R22 A_R23 A_R24"; IX=A_R21; CS=0.1; CM=mid; fi
for k in $DG; do $P th/addc.py grip/bend_$k.json $O/bend_$k.json "stop_targets={\"$k\": [\"palm\"]}"; $P $G -- $RG $S $O/bend_$k.json $O/bend_${k}_out.json > $O/bend_$k.log 2>&1; done
k=A_${S}thumb; $P th/addc.py grip/bend2_$k.json $O/bend_$k.json "stop_new_contact=[\"$k\"]"; $P $G -- $RG $S $O/bend_$k.json $O/bend_${k}_out.json > $O/bend_$k.log 2>&1
$P th/addc.py grip/open_$S.json $O/open_$S.json; $P $G -- $RG $S $O/open_$S.json $O/open_${S}_out.json > $O/open_$S.log 2>&1
$P -c "import json; d=json.load(open('$O/open_${S}_out.json')); json.dump(d['angles'],open('$O/open_${S}_angles.json','w'))"
$P tools/placefix.py -- $RG $S $O/handle_fix_$S.json $O/open_${S}_angles.json > $O/placefix_$S.log 2>&1
$P - <<EOP
import json
s='$S'; T=json.load(open('grip/handle_%s.json'%s)); T['base_angles']=json.load(open('$O/open_%s_angles.json'%s)); T['fixture']=json.load(open('$O/handle_fix_%s.json'%s))
json.dump(T,open('$O/handle_%s.json'%s,'w'),indent=1)
EOP
$P th/addc.py $O/handle_$S.json $O/handle_$S.json; $P $G -- $RG $S $O/handle_$S.json $O/handle_${S}_out.json > $O/handle_$S.log 2>&1
$P th/addc.py grip/prepinch2_$S.json $O/prepinch_$S.json; $P $G -- $RG $S $O/prepinch_$S.json $O/prepinch_${S}_out.json > $O/prepinch_$S.log 2>&1
$P - <<EOP
import json
s='$S'; sc=$CS; ix='$IX'
d=json.load(open('$O/prepinch_%s_out.json'%s)); T=json.load(open('grip/prepinch2_%s.json'%s)); a=d['angles']
for b,v in T['phases'][2]['targets'][ix].items(): a[b]=[(sc/0.4)*x for x in v]
json.dump(a,open('$O/pp_%s.json'%s,'w'))
EOP
COINMODE=$CM $P tools/placecoin.py -- $RG $S $O/pp_$S.json $O/coin_fix_$S.json > $O/placecoin_$S.log 2>&1
$P - <<EOP
import json
s='$S'; T=json.load(open('grip/pinch_%s.json'%s)); T['base_angles']=json.load(open('$O/pp_%s.json'%s)); T['fixture']=json.load(open('$O/coin_fix_%s.json'%s))
json.dump(T,open('$O/pinch_%s.json'%s,'w'),indent=1)
EOP
$P th/addc.py $O/pinch_$S.json $O/pinch_$S.json; $P $G -- $RG $S $O/pinch_$S.json $O/pinch_${S}_out.json > $O/pinch_$S.log 2>&1
echo DONE > $O/$S.done
