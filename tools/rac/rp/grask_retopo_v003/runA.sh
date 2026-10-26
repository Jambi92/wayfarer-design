# runA.sh CAGE TAG : cage -> x2 fit -> quality chain (as run_v002) -> audits summary
set -e; cd /tmp/claude-0/rt; C=$1; T=$2; BP=/home/claude/stc/bin/python3
[ -f ${T}.npz ] || bash pipeL.sh $C.npz $T 2
python3 centfix.py $T.npz ${T}f.npz 1.0 | tail -1
bash recipe.sh ${T}f.npz ${T}fv | tail -2
python3 revsx.py ${T}f.npz ${T}fv.npz ${T}fw.npz | tail -1
python3 centfix.py ${T}fw.npz ${T}fx.npz 1.0 | tail -1
bash repairsafe.sh ${T}fx.npz ${T}K | tail -1
LDEV=0.06 bash repairall.sh ${T}K.npz ${T}n1 3 | tail -1
python3 revsx.py ${T}K.npz ${T}n1.npz ${T}n2.npz | tail -1
python3 centfix.py ${T}n2.npz ${T}M.npz 1.0 | tail -1
LDEV=0.1 LOFF=0.15 LIT=80 python3 lrepair.py ${T}M.npz ${T}o.npz 5 | tail -1
python3 foldfix.py ${T}o.npz ${T}of.npz | tail -1
python3 revsx.py ${T}M.npz ${T}of.npz ${T}N.npz | tail -1
python3 optfix.py ${T}N.npz ${T}O.npz | tail -1
python3 dev.py ${T}O.npz ${T}O_dev.json
python3 hardlist.py ${T}O.npz ${T}O_hard.json | tail -1
$BP /tmp/claude-0/rp2/sxq.py ${T}O.npz ${T}O_sx.npy | head -2
echo RUNADONE
