#!/bin/bash
# usage: check.sh TAG  (copies staged AC2 blend, gates, region disp, renders key comparisons)
cd /home/claude/aj; T=$1; mkdir -p $T
cp /mnt/user-data/uploads/RaceBodies/source/Gorrund-Neutral-C/05AJ/GO-05AJ_AC2.blend $T/GO-05AJ_AC2.blend; sha256sum $T/GO-05AJ_AC2.blend
bash /home/claude/ag/gates.sh $PWD/prep/after_VF.npz $PWD/$T/GO-05AJ_AC2.blend $PWD/$T/aj 2>&1 | grep -v "bbox\|height\|moved_z"
python3 -I - $T <<'PY'
import numpy as np, json, sys
T=sys.argv[1]
B=np.load('/home/claude/aj/prep/after_VF.npz')['V']; A=np.load(f'/home/claude/aj/{T}/aj_VF.npz')['V']; d=np.linalg.norm(A-B,axis=1)*1000
R=np.load('/home/claude/aj/regions_05AI.npz'); out={k:round(float(d[R[k]].max()),4) for k in R.files if R[k].size}
W=np.load('/home/claude/af/weights_05AE.npz'); names=[str(x) for x in W['names']]; o2n=np.load('/home/claude/af/old_to_new_05AE_to_05AF.npy'); lab=np.full(len(B),-1); lab[o2n]=W['W'].argmax(1)
for p in ['upperarm','forearm','thigh','shin']:
  m=np.isin(lab,[names.index(k) for k in names if k.startswith(p)]); mv=d[m]>0.01; out[p]=dict(moved=int(mv.sum()),max_mm=round(float(d[m].max()),3),p95_moved_mm=round(float(np.percentile(d[m][mv],95)),3))
print(out); json.dump(out,open(f'/home/claude/aj/{T}/region_disp.json','w'),indent=1)
PY
