# finalaudit.sh BLEND ORIGIN.json CAGE TAG : full audit of the EXACT exported blend (read back, translation undone)
set -e; cd /tmp/claude-0/rt; B=$1; O=$2; C=$3; T=$4; BP=/home/claude/stc/bin/python3
$BP rbnpz.py -- $B $O $T.npz | tail -1
python3 gate.py $T.npz ${T}_gate.json > /dev/null; python3 techx.py $T.npz ${T}_techx.json
python3 dev.py $T.npz ${T}_dev.json
$BP /tmp/claude-0/rp2/sxq.py $T.npz ${T}_sx.npy | head -1 > ${T}_sx.txt; cat ${T}_sx.txt
python3 folds.py $T.npz > ${T}_folds.txt 2>/dev/null; python3 flipchk.py $T.npz >> ${T}_folds.txt; cat ${T}_folds.txt
python3 hardlist.py $T.npz ${T}_hard.json | tail -1
LEVEL=2 python3 tagloops.py $C.npz $T.npz ${T}_loops.json | tail -1
timeout 3000 python3 loopaudit.py $T.npz ${T}_loops_audit.json | tail -1
python3 lm.py $T.npz ${T}_lm.json | tail -1; python3 lmdrift.py lm_src_v2.json ${T}_lm.json ${T}_lmdrift.json
python3 identity.py $T.npz ${T}_identity.json | tail -1; python3 iou.py $T.npz ${T}_iou.json | tail -1
python3 symm.py $T.npz ${T}_symmetry.json > /dev/null; python3 origin.py $T.npz ${T}_lm.json lm_src_v2.json ${T}_origin_check.json
echo FINALAUDITDONE
