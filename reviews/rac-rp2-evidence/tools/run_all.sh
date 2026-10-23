#!/bin/bash
# run_all.sh CROTCH_VARIANT OUTTAG : full RP2 production build from the adjudicated target
set -e
cd /tmp/claude-0/rp2; P=/home/claude/stc/bin/python3; V=$1; T=$2
cp sstar_p_$V.npz sstar_p.npz
python3 - <<'EOP'
import sys; sys.path.insert(0,'/tmp/claude-0/rp2/tools'); sys.path.insert(0,'/tmp/claude-0/rp2'); import numpy as np
from hidden import hidden_quads; from crotch_region import region
b=np.load('/tmp/claude-0/rp2/sstar_p.npz'); V=b['V']; Q=b['Q']; m=b['mir']; o2n=b['o2n']; n=len(V)
Wb=dict(np.load('/tmp/claude-0/rp2/weights_body.npz')); n2o=-np.ones(n,int); n2o[o2n[o2n>=0]]=np.where(o2n>=0)[0]
arm=np.zeros(n)
for k in ('upperarm_l','lowerarm_l','hand_l','fingers_l','upperarm_r','lowerarm_r','hand_r','fingers_r'): arm[n2o>=0]+=Wb[k][n2o[n2o>=0]]
np.save('/tmp/claude-0/rp2/arm_p.npy',arm)
h,s,ht=hidden_quads(V,Q); C=V[Q].mean(1); seed=h&(C[:,0]>6)
if seed.sum()==0 and len(Q)==len(np.load('/tmp/claude-0/rp2/hq_s.npy')): seed=np.load('/tmp/claude-0/rp2/hq_s.npy')&(C[:,0]>6)
R=region(V,Q,m,seed,2); R&=(C[:,0]>0); np.save('/tmp/claude-0/rp2/axR_2.npy',R); print('axilla region quads',R.sum())
EOP
CSM=3 python3 tools/axilla_patch.py 16 2
$P tools/untangle.py -- sstar_pp.npz sstar_ppu0.npz 0.01 80 2>&1 | tail -1
$P tools/untangle_sub.py -- sstar_ppu0.npz sstar_ppu.npz 0.005 100 2>&1 | tail -1
python3 -c "
import sys; sys.path.insert(0,'tools'); import numpy as np
from subdiv import subdivide_levels
b=np.load('sstar_ppu.npz'); Q,n,S,m=subdivide_levels(b['Q'],len(b['V']),2,b['mir']); np.savez('lin_ppu.npz',V=S@b['V'],Q=Q)"
python3 tools/clearance2.py lin_ppu.npz clr.npy
python3 tools/build7.py c_$T.npz 60 0.2 0.5
python3 tools/fair3.py c_$T.npz f_$T.npz 400 1.0 2.0 8 | tail -1
cp c_${T}_S.npz f_${T}_S.npz; cp c_${T}_SS.npz f_${T}_SS.npz
RINGS=${RINGS:-4} SEAMFREE=1 python3 tools/patch_relax.py f_$T.npz g_$T.npz ${PRIT:-150}
cp c_${T}_S.npz g_${T}_S.npz; cp c_${T}_SS.npz g_${T}_SS.npz
$P tools/untangle.py -- g_$T.npz cand_$T.npz 0.003 200 2>&1 | tail -1
cp c_${T}_S.npz cand_${T}_S.npz; cp c_${T}_SS.npz cand_${T}_SS.npz
echo BUILD_DONE $T
