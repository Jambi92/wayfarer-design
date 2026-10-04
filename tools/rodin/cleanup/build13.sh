set -e
L=/tmp/claude-0/rodin/c10/c10.log
while ! grep -q EF15O $L; do sleep 20; done
cd /tmp/claude-0/rodin/g1
CLOSURE=1 HEAD_SCALE=1.08 BROW_INT=3 python3 efield15.py e15_new.npy > e15n.log 2>&1; echo EF15N >> $L
python3 assemble15.py > /tmp/claude-0/rodin/c10/asm15.log 2>&1; echo ASM15 >> $L
cd /tmp/claude-0/rodin/c10
python3 -c "
import numpy as np; z=np.load('g13a_body.npz'); np.savez('g13a.npz',V=z['V'],F=z['F'])"
python3 fixslivers.py g13a.npz g13b_body.npz > fixsl.log 2>&1; echo SLV >> $L
python3 seamdist13.py > sd.log 2>&1
python3 cleanup_ops.py g13b_body.npz g13_body.npz neckseam13.npy > ops.log 2>&1; echo OPS >> $L
python3 -c "
import numpy as np, igl
z=np.load('g13_body.npz'); V,F=igl.upsample(z['V'].astype(float),z['F'].astype(np.int64)); np.savez('g13up.npz',V=V.astype(np.float32),F=F.astype(np.int32))"
cd /tmp/claude-0/rodin/g1
HEAD_SCALE=1.08 python3 g7regc.py /tmp/claude-0/rodin/c10/g13up.npz /tmp/claude-0/rodin/c10/g13reg.npz > /tmp/claude-0/rodin/c10/reg.log 2>&1; echo REG >> $L
cd /tmp/claude-0/rodin/c10; python3 seedmap13.py > seedmap.log 2>&1; echo SEEDS >> $L
cd /tmp/claude-0/rodin/g1
SEEDS=/tmp/claude-0/rodin/c10/seeds13.npy python3 g7surfc.py /tmp/claude-0/rodin/c10/g13up.npz /tmp/claude-0/rodin/c10/g13reg.npz /tmp/claude-0/rodin/c10/g13_surf.npz > /tmp/claude-0/rodin/c10/surf.log 2>&1; echo SURF >> $L
