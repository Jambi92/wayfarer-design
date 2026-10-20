#!/bin/bash
cd /tmp/claude-0/rp1f; IN=$1; OUT=$2
for N in A_L17 A_L18 A_L19 A_L20 A_Lthumb A_R21 A_R22 A_R23 A_R24 A_Rthumb; do
  python3 clawsdf.py $IN hand_sdf.json $N tg_$N.npz | tail -1
  T=$(python3 -c "import json;print(','.join(map(str,json.load(open('hand_frames.json'))['$N']['T'])))")
  PC=$(python3 -c "import json,numpy as np;d=json.load(open('hand_sdf.json'))['$N'];f=json.load(open('hand_frames.json'))['$N'];T=np.array(f['T']);C=np.array(f['C']);e=(T-C)/np.linalg.norm(T-C);print(','.join(map(str,(T-d['c0back']*e).round(4))))")
  PR=$(python3 -c "import json;print(json.load(open('hand_sdf.json'))['$N']['projR'])")
  R=$(python3 -c "import json,numpy as np;d=json.load(open('hand_frames.json'))['$N'];print(round(max(0.9,1.35*np.linalg.norm(np.array(d['T'])-np.array(d['C']))+0.6),2))")
  timeout 900 /home/claude/stc/bin/python3 projn.py -- tg_${N}_erased.npz tg_$N.npz cur_$N.npz $PC $PR 8 2>&1 | tail -1
  IN=cur_$N.npz
done
cp $IN $OUT; echo DONE
