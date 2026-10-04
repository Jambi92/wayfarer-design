set -e
L=/tmp/claude-0/rodin/c11/c11.log; G=/tmp/claude-0/rodin/g1; C=/tmp/claude-0/rodin/c11
cd $G
BROW_INT=4 CLOSURE=1 HEAD_SCALE=1.08 python3 g10.py 0.2 $C/hb5.npz -16,16,-34,28,161,203 > $C/hb5.log 2>&1; echo HB5 >> $L
CLOSURE=1 HEAD_SCALE=1.08 BROW_INT=3 python3 efield16.py e16_old.npy > e16o.log 2>&1
CLOSURE=1 HEAD_SCALE=1.08 BROW_INT=4 python3 efield16.py e16_new.npy > e16n.log 2>&1; echo EF16 >> $L
python3 assemble16.py > $C/asm16.log 2>&1; echo ASM16 >> $L
cd $C
python3 -c "
import numpy as np; z=np.load('g14a_body.npz'); np.savez('g14a.npz',V=z['V'],F=z['F'])"
SEAMZONE=forearm python3 fixslivers2.py g14a.npz g14b_body.npz > fixsl.log 2>&1; echo SLV >> $L
python3 tailfix2.py g14b_body.npz g14_body.npz > tail.log 2>&1; echo TAIL >> $L
python3 -c "
import numpy as np, igl
z=np.load('g14_body.npz'); V,F=igl.upsample(z['V'].astype(float),z['F'].astype(np.int64)); np.savez('g14up.npz',V=V.astype(np.float32),F=F.astype(np.int32))"
cd $G; HEAD_SCALE=1.08 python3 g7regs.py $C/g14up.npz $C/g14reg.npz > $C/reg.log 2>&1; echo REG >> $L
cd $C; python3 seedmap14.py > seedmap.log 2>&1; echo SEEDS >> $L
cd $G; SEEDS=$C/seeds14.npy python3 g7surfc.py $C/g14up.npz $C/g14reg.npz $C/g14_surf.npz > $C/surf.log 2>&1; echo SURF >> $L
