cd /tmp/claude-0/rodin/g1
python3 -c "
import numpy as np, igl
z=np.load('hv_crest_c.npz'); V,F=igl.upsample(z['v'].astype(float),z['f'].astype(np.int64),1); np.savez('hvu_crest_c.npz',V=V.astype(np.float32),F=F.astype(np.int32))"
for V in baseline minimal_ridges low_hornlets swept_paired crest mixed_asym; do
  DV=$V; U=$V; [ "$V" = baseline ] && DV=""; [ "$V" = crest ] && U=crest_c
  DISPLAY_VARIANT=$DV HEAD_SCALE=1.08 python3 g7regc.py hvu_$U.npz hvrc_$V.npz > hvc_$V.log 2>&1
  python3 g7surfc.py hvu_$U.npz hvrc_$V.npz hvsc_$V.npz >> hvc_$V.log 2>&1
  python3 -c "
import numpy as np; z=np.load('hvsc_$V.npz'); np.savez('hvcc_$V.npz',P=z['V'],f=z['F'],R=np.zeros(len(z['V']),np.int8))"
  VIEWS="hF:0:3:0:8:182:30;hP:90:0:0:2:182:34;hF34:40:12:0:6:183:32;hR34:145:15:0:-2:183:32;hT:0:89:0:2:184:34" NPZ=hvcc_$V.npz TAG=$PWD/DC_$V RES=900 python3 rclose.py >> hvc_$V.log 2>&1
  echo VCDONE $V >> c7.log
done
