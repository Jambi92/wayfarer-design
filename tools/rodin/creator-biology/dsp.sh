while [ ! -f /tmp/claude-0/rodin/v1/sweep.json ]; do sleep 20; done
cd /tmp/claude-0/rodin/g1; D=/tmp/claude-0/rodin/v1/dv
run() { ID=$1; DV=$2; shift 2
  [ -f $D/DN_${ID}_hR34.png ] && return
  env "$@" DISPLAY_VARIANT=$DV BROW_INT=5 CLOSURE=1 HEAD_SCALE=1.08 python3 g10v.py 0.2 $D/hv_$ID.npz -16,16,-34,28,161,203 > $D/hv_$ID.log 2>&1
  python3 -c "
import numpy as np, igl
z=np.load('$D/hv_$ID.npz'); V,F=igl.upsample(z['v'].astype(float),z['f'].astype(np.int64),1); np.savez('$D/hvu_$ID.npz',V=V.astype(np.float32),F=F.astype(np.int32))"
  env "$@" DISPLAY_VARIANT=$DV BROW_INT=5 HEAD_SCALE=1.08 python3 g7regsv.py $D/hvu_$ID.npz $D/hvr_$ID.npz >> $D/hv_$ID.log 2>&1
  python3 g7surfc.py $D/hvu_$ID.npz $D/hvr_$ID.npz $D/hvs_$ID.npz >> $D/hv_$ID.log 2>&1
  python3 -c "
import numpy as np; z=np.load('$D/hvs_$ID.npz'); np.savez('$D/hvc_$ID.npz',P=z['V'],f=z['F'])"
  VIEWS="hF:0:3:0:8:182:30;hP:90:0:0:2:182:34;hF34:40:12:0:6:183:32;hT:0:89:0:2:184:34;att:120:35:3:-4:186:16;hR34:145:15:0:-4:181:36" NPZ=$D/hvc_$ID.npz TAG=$D/DN_$ID RES=700 python3 rclose.py >> $D/hv_$ID.log 2>&1
  echo DSP $ID >> $D/dsp.log
}
run d00 ""
run d13 minimal_ridges
run d01 low_hornlets DSP_COUNT=1
run dlh low_hornlets
run d02 low_hornlets DSP_LEN=1.5
run d03 low_hornlets DSP_LEN=0.7 DSP_BASE=0.85
run d04 low_hornlets DSP_LEN=1.5 DSP_BASE=0.7
run dsw swept_paired
run d05 swept_paired DSP_LEN=0.75
run d06 swept_paired DSP_LEN=1.25
run d07 swept_paired DSP_SWEEP=10
run d08 swept_paired DSP_SWEEP=-12
run d09 swept_paired DSP_LEN=1.25 DSP_BASE=0.8
run dmx mixed_asym
run d10 mixed_asym DSP_ASYM=0.70
run dcr crest
run d11 crest CREST_H=1.6
run d12 crest CREST_H=3.0
echo DSP_ALL >> $D/dsp.log
