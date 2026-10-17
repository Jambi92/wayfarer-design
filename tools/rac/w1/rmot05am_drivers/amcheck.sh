#!/bin/bash
# usage: akcheck.sh STAGED_BLEND TAG  -> gates (vs 05AJ preflight baseline) + limb displacement envelope
cd /home/claude/am; T=$2; mkdir -p $T; cp "$1" $T/; B=$T/$(basename "$1"); sha256sum $B
bash /home/claude/ag/gates.sh /home/claude/al/out/after_VF.npz $PWD/$B $PWD/$T/ak 2>&1 | grep -v "bbox\|moved_z"
python3 -I - $T <<'PY'
import numpy as np, json, sys
T=sys.argv[1]
B=np.load('/home/claude/al/out/after_VF.npz')['V']; A=np.load(f'/home/claude/am/{T}/ak_VF.npz')['V']; d=np.linalg.norm(A-B,axis=1)*1000
R=np.load('/home/claude/aj/regions_05AI.npz'); out={k:round(float(d[R[k]].max()),4) for k in R.files if R[k].size}
W=np.load('/home/claude/af/weights_05AE.npz'); names=[str(x) for x in W['names']]; o2n=np.load('/home/claude/af/old_to_new_05AE_to_05AF.npy'); lab=np.full(len(B),-1); lab[o2n]=W['W'].argmax(1)
limb=np.isin(lab,[names.index(k) for k in names if k.split('_')[0] in ('upperarm','forearm','thigh','shin')]); mv=limb&(d>0.01)
out['limb_all']=dict(moved=int(mv.sum()),median=round(float(np.median(d[mv])),3),p95=round(float(np.percentile(d[mv],95)),3),max=round(float(d[limb].max()),3))
for p in ['upperarm','forearm','thigh','shin']:
  m=np.isin(lab,[names.index(k) for k in names if k.startswith(p)]); m2=m&(d>0.01); out[p]=dict(moved=int(m2.sum()),median=round(float(np.median(d[m2])),3) if m2.any() else 0,p95=round(float(np.percentile(d[m2],95)),3) if m2.any() else 0,max=round(float(d[m].max()),3))
print(json.dumps(out)); json.dump(out,open(f'/home/claude/am/{T}/region_disp.json','w'),indent=1)
PY
