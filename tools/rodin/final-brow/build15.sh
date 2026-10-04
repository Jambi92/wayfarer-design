set -e
L=/tmp/claude-0/rodin/c12/c12.log; G=/tmp/claude-0/rodin/g1; C=/tmp/claude-0/rodin/c12
cd $G
BROW_INT=5 CLOSURE=1 HEAD_SCALE=1.08 python3 g10.py 0.2 $C/hc1.npz -16,16,-34,28,161,203 > $C/hc1.log 2>&1; echo HC1 >> $L
CLOSURE=1 HEAD_SCALE=1.08 BROW_INT=4 python3 efield17.py e17_old.npy > e17o.log 2>&1
CLOSURE=1 HEAD_SCALE=1.08 BROW_INT=5 python3 efield17.py e17_new.npy > e17n.log 2>&1; echo EF17 >> $L
python3 assemble17.py > $C/asm17.log 2>&1; echo ASM17 >> $L
cd $C
python3 -c "
import numpy as np, igl
z=np.load('g15_body.npz'); V,F=igl.upsample(z['V'].astype(float),z['F'].astype(np.int64)); np.savez('g15up.npz',V=V.astype(np.float32),F=F.astype(np.int32))"
cd $G; HEAD_SCALE=1.08 python3 g7regs.py $C/g15up.npz $C/g15reg.npz > $C/reg.log 2>&1; echo REG >> $L
cd $C; python3 seedmap15.py > seedmap.log 2>&1; echo SEEDS >> $L
cd $G; SEEDS=$C/seeds15.npy python3 g7surfc.py $C/g15up.npz $C/g15reg.npz $C/g15_surf.npz > $C/surf.log 2>&1; echo SURF >> $L
cd $C; python3 snap15.py > snap.log 2>&1; echo SNAP >> $L
