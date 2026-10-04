while ! grep -q "^SNAP" /tmp/claude-0/rodin/c12/c12.log; do sleep 20; done
cd /tmp/claude-0/rodin/g1; D=/tmp/claude-0/rodin/c12/dv
for V in baseline low_hornlets swept_paired mixed_asym crest; do
  DV=$V; [ "$V" = baseline ] && DV=""
  DISPLAY_VARIANT=$DV BROW_INT=5 CLOSURE=1 HEAD_SCALE=1.08 python3 g10.py 0.2 $D/hv_$V.npz -16,16,-34,28,161,203 > $D/hv_$V.log 2>&1
  python3 -c "
import numpy as np, igl
z=np.load('$D/hv_$V.npz'); V,F=igl.upsample(z['v'].astype(float),z['f'].astype(np.int64),1); np.savez('$D/hvu_$V.npz',V=V.astype(np.float32),F=F.astype(np.int32))"
  DISPLAY_VARIANT=$DV BROW_INT=5 HEAD_SCALE=1.08 python3 g7regs.py $D/hvu_$V.npz $D/hvr_$V.npz >> $D/hv_$V.log 2>&1
  python3 g7surfc.py $D/hvu_$V.npz $D/hvr_$V.npz $D/hvs_$V.npz >> $D/hv_$V.log 2>&1
  python3 -c "
import numpy as np; z=np.load('$D/hvs_$V.npz'); np.savez('$D/hvc_$V.npz',P=z['V'],f=z['F'],R=np.zeros(len(z['V']),np.int8))"
  VIEWS="hF:0:3:0:8:182:30;hP:90:0:0:2:182:34;hF34:40:12:0:6:183:32;hR34:145:15:0:-2:183:32;hT:0:89:0:2:184:34;att:120:35:3:-4:186:16" NPZ=$D/hvc_$V.npz TAG=$D/DN_$V RES=900 python3 rclose.py >> $D/hv_$V.log 2>&1
  echo DV15 $V >> /tmp/claude-0/rodin/c12/c12.log
done
