set -e
cd /tmp/claude-0/rodin/g1
CLOSURE=1 HEAD_SCALE=1.08 BROW_INT=2 python3 efield14.py e14_new.npy > e14n.log 2>&1; echo EFN >> /tmp/claude-0/rodin/p9/p9.log
python3 assemble14.py > /tmp/claude-0/rodin/p9/asm14.log 2>&1; echo ASM >> /tmp/claude-0/rodin/p9/p9.log
cd /tmp/claude-0/rodin/p9
python3 tailfix.py /tmp/claude-0/rodin/g1/g11_body.npz g12_body.npz > tailfix.log 2>&1; echo TAIL >> p9.log
python3 -c "
import numpy as np, igl
z=np.load('g12_body.npz'); V,F=igl.upsample(z['V'].astype(float),z['F'].astype(np.int64)); np.savez('g12up.npz',V=V.astype(np.float32),F=F.astype(np.int32)); print(len(V))" > up.log 2>&1; echo UP >> p9.log
cd /tmp/claude-0/rodin/g1
HEAD_SCALE=1.08 python3 g7regc.py /tmp/claude-0/rodin/p9/g12up.npz /tmp/claude-0/rodin/p9/g12reg.npz > /tmp/claude-0/rodin/p9/reg.log 2>&1; echo REG >> /tmp/claude-0/rodin/p9/p9.log
python3 g7surfc.py /tmp/claude-0/rodin/p9/g12up.npz /tmp/claude-0/rodin/p9/g12reg.npz /tmp/claude-0/rodin/p9/g12_surf.npz > /tmp/claude-0/rodin/p9/surf.log 2>&1; echo SURF >> /tmp/claude-0/rodin/p9/p9.log
