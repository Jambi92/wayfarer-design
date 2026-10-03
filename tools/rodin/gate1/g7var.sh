cd /tmp/claude-0/rodin/g1
for V in baseline minimal_ridges low_hornlets swept_paired crest mixed_asym; do
  DV=$V; [ "$V" = baseline ] && DV=""
  DISPLAY_VARIANT=$DV CLOSURE=1 HEAD_SCALE=1.08 python3 g10.py 0.2 hv_$V.npz -16,16,-34,28,161,203 > hv_$V.log 2>&1
  python3 -c "
import numpy as np, igl
z=np.load('hv_$V.npz'); V,F=igl.upsample(z['v'].astype(float),z['f'].astype(np.int64),1); np.savez('hvu_$V.npz',V=V.astype(np.float32),F=F.astype(np.int32))"
  DISPLAY_VARIANT=$DV HEAD_SCALE=1.08 python3 g7reg.py hvu_$V.npz hvr_$V.npz >> hv_$V.log 2>&1
  python3 g7surf.py hvu_$V.npz hvr_$V.npz hvs_$V.npz >> hv_$V.log 2>&1
  python3 -c "
import numpy as np; z=np.load('hvs_$V.npz'); np.savez('hvc_$V.npz',P=z['V'],f=z['F'],R=np.zeros(len(z['V']),int))"
  VIEWS="hF:0:3:0:8:182:30;hP:90:0:0:2:182:34;hF34:40:12:0:6:183:32;hR34:145:15:0:-2:183:32;hT:0:89:0:2:184:34" NPZ=hvc_$V.npz TAG=$PWD/DV_$V RES=900 python3 rclose.py >> hv_$V.log 2>&1
  echo VDONE $V >> hv_all.log
done
