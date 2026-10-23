#!/bin/bash
# ident_full.sh PARAMS.json TAG : complete identity-correction build -> idc/TAG.npz (+_S/_SS) and joints
set -e; cd /tmp/claude-0/rp2
python3 tools/ident_make2.py $1 idc/m_$2.npz
python3 -c "
import sys; sys.path.insert(0,'/tmp/claude-0/rp2/tools'); import numpy as np
from ident_apply import SS
P=np.load('idc/m_$2.npz'); W=np.load('weights_body.npz'); ew=SS()@W['ears']
np.save('idc/trm_$2.npy',P['fair_mask']*(1-0.8*np.clip(ew/0.5,0,1)))"
python3 tools/tan_relax.py idc/m_$2.npz idc/t_$2.npz idc/trm_$2.npy 12
python3 tools/ident_finish.py idc/t_$2.npz idc/$2.npz
cp cand_s3_S.npz idc/$2_S.npz; cp cand_s3_SS.npz idc/$2_SS.npz
python3 -c "
import sys,json; sys.path.insert(0,'/tmp/claude-0/rp2/tools'); import ident_body as B
json.dump(B.new_joints(json.load(open('$1'))['body']),open('idc/joints_$2.json','w'))"
echo FULL_DONE $2
