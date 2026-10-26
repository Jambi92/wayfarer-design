# repairall.sh IN OUT ROUNDS : iterated local sliver repair (patch smoothing on-surface, then bounded off-surface <=0.8 mm)
set -e; cd /tmp/claude-0/rt; I=$1; O=$2; R=${3:-4}; cp $I ${O}_w.npz; prev=999999
for r in $(seq 1 $R); do
  for cfg in "0 30 6" "0 50 9" "0.04 40 6" "0.06 60 8" "0.08 80 10" "0.08 40 5"; do set -- $cfg
    LOFF=$1 LIT=$2 python3 lrepair.py ${O}_w.npz ${O}_t.npz $3 > ${O}_t.log; mv ${O}_t.npz ${O}_w.npz; tail -1 ${O}_t.log
  done
  h=$(tail -1 ${O}_t.log | awk '{print $NF}'); [ "$h" -ge "$prev" ] && break; prev=$h
done
mv ${O}_w.npz ${O}.npz; rm -f ${O}_t.log
