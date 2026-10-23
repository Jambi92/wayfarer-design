# mkrig.sh MESHTAG RIGDIR : rebuild the diagnostic rig on tf/MESHTAG.npz with the new thumb keratin labels
cd /tmp/claude-0/hand; t=$1; R=$2; P=/home/claude/stc/bin/python3; mkdir -p $R
$P - <<EOP
import numpy as np,pickle,json
RD=pickle.load(open('rig_c3/rig_data.pkl','rb')); z=np.load('tf/$t.npz'); V=z['V']*np.array([1,-1,1])
d=json.load(open('digits_c3.json')); ko={}
for s in 'LR':
    vid=RD[s]['vid']; own=RD[s]['own']; ko['clear_%s'%s]=vid[own==4]; kk=vid[np.load('tf/${t}_ker_%s.npy'%s)]; ko['set_%s'%s]=kk
    k='A_%sthumb'%s; j2=np.array(RD[s]['joints'][k]['j2']); old=np.array(d[k]['claw_tip']); ea=(old-j2)/np.linalg.norm(old-j2)
    kv=V[kk]; ap=kv[np.argmax((kv-j2)@ea)]; d[k]['claw_tip']=ap.tolist(); print(s,'new thumb apex',np.round(ap,2),'keratin',len(kk))
np.savez('$R/kero.npz',**ko); json.dump(d,open('digits.json','w'),indent=1); json.dump(d,open('$R/digits.json','w'),indent=1)
EOP
$P tools/skel2.py tf/$t.npz $R/skel.json > $R/skel.log 2>&1
TD0=1.8 TW=1.2 KER_OVR=$R/kero.npz $P tools/rig.py -- tf/$t.npz $R/skel.json $R > $R/rig.log 2>&1
$P -c "import sys;sys.path.insert(0,'tools');import fastpose;fastpose.export_rig('$R')" >> $R/rig.log 2>&1
$P tools/spreadsign.py -- $R >> $R/rig.log 2>&1
echo RIGDONE >> $R/rig.log
