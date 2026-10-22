# finalrun.sh SIDE : all movement / grip tests on the final diagnostic rig (rig_c3)
cd /tmp/claude-0/hand; S=$1; RG=rig_c3; P=/home/claude/stc/bin/python3; G=tools/gripsolve.py
if [ $S = L ]; then DG="A_L17 A_L18 A_L19 A_L20 A_Lthumb"; IX=A_L20; CS=0.2; CM=thumb; else DG="A_R21 A_R22 A_R23 A_R24 A_Rthumb"; IX=A_R21; CS=0.1; CM=mid; fi
[ -f final/clench_${S}_out.json ] || $P $G -- $RG $S final/clench_$S.json final/clench_${S}_out.json > final/clench_$S.log 2>&1
for k in $DG; do [ -f final/bend_${k}_out.json ] || $P $G -- $RG $S grip/bend_$k.json final/bend_${k}_out.json > final/bend_$k.log 2>&1; done
$P $G -- $RG $S grip/open_$S.json final/open_${S}_out.json > final/open_$S.log 2>&1
$P -c "import json; d=json.load(open('final/open_${S}_out.json')); json.dump(d['angles'],open('final/open_${S}_angles.json','w'))"
$P tools/placefix.py -- $RG $S final/handle_fix_$S.json final/open_${S}_angles.json > final/placefix_$S.log 2>&1
$P - <<EOP
import json
s='$S'; T=json.load(open('grip/handle_%s.json'%s)); T['base_angles']=json.load(open('final/open_%s_angles.json'%s)); T['fixture']=json.load(open('final/handle_fix_%s.json'%s))
json.dump(T,open('final/handle_%s.json'%s,'w'),indent=1)
EOP
$P $G -- $RG $S final/handle_$S.json final/handle_${S}_out.json > final/handle_$S.log 2>&1
$P $G -- $RG $S grip/prepinch2_$S.json final/prepinch_${S}_out.json > final/prepinch_$S.log 2>&1
$P - <<EOP
import json
s='$S'; sc=$CS; ix='$IX'
d=json.load(open('final/prepinch_%s_out.json'%s)); T=json.load(open('grip/prepinch2_%s.json'%s)); a=d['angles']
for b,v in T['phases'][2]['targets'][ix].items(): a[b]=[(sc/0.4)*x for x in v]
json.dump(a,open('final/pp_%s.json'%s,'w'))
EOP
COINMODE=$CM $P tools/placecoin.py -- $RG $S final/pp_$S.json final/coin_fix_$S.json > final/placecoin_$S.log 2>&1
$P - <<EOP
import json
s='$S'; T=json.load(open('grip/pinch_%s.json'%s)); T['base_angles']=json.load(open('final/pp_%s.json'%s)); T['fixture']=json.load(open('final/coin_fix_%s.json'%s))
json.dump(T,open('final/pinch_%s.json'%s,'w'),indent=1)
EOP
$P $G -- $RG $S final/pinch_$S.json final/pinch_${S}_out.json > final/pinch_$S.log 2>&1
echo DONE > final/$S.done
