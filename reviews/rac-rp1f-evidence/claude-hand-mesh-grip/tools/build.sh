# build.sh TAG : assemble + bounded collision-free repair (both hands) + gates
set -x
cd /tmp/claude-0/hand; T=$1; mkdir -p $T
P=/home/claude/stc/bin/python3; FX=/home/claude/stc/rp1e/fixall.py
$P tools/stage4_assemble.py $T/asm.npz > $T/asm.log 2>&1
SRC=r107a.npz REG=33,-50,98,16 timeout 3500 $P $FX -- $T/asm.npz $T/f1.npz 40 0.3 0.6 > $T/f1.log 2>&1
SRC=r107a.npz REG=33,-50,98,16 timeout 3500 $P $FX -- $T/f1.npz $T/f2.npz 40 0.0 0.5 > $T/f2.log 2>&1
SRC=r107a.npz REG=-32,-42,97,16 timeout 3500 $P $FX -- $T/f2.npz $T/f3.npz 40 0.3 0.6 > $T/f3.log 2>&1
SRC=r107a.npz REG=-32,-42,97,16 timeout 3500 $P $FX -- $T/f3.npz $T/f4.npz 40 0.0 0.5 > $T/f4.log 2>&1
$P - <<EOP
import numpy as np
a=np.load('$T/asm.npz'); b=np.load('$T/f4.npz')
np.savez_compressed('$T/prod.npz',V=b['V'],Q=b['Q'],F=b['F'],old2new=a['old2new'],prot=a['prot'])
EOP
$P tools/twoway.py $T/prod.npz $T/prod_tw.npz -38.97,-42.43,98.84,1.6 30 > $T/tw.log 2>&1 && mv $T/prod_tw.npz $T/prod.npz
$P tools/gate_topo.py $T/prod.npz $T/topo.json > $T/topo.log 2>&1
$P tools/sx.py $T/prod.npz $T/sx_pairs.npy > $T/sx.log 2>&1
$P tools/gate_dev.py $T/prod.npz $T/dev.json > $T/dev.log 2>&1
echo BUILD_DONE > $T/done
