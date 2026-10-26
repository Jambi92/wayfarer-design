# repairsafe.sh IN OUT : guarded on-surface sliver repair (no off-surface) + undo near any new self-intersection
set -e; cd /tmp/claude-0/rt; I=$1; O=$2; cp $I ${O}_w.npz
for cfg in "30 6" "50 9" "40 5" "60 8" "30 6" "50 10"; do set -- $cfg
  LOFF=0 LIT=$1 python3 lrepair.py ${O}_w.npz ${O}_t.npz $2 | tail -1; mv ${O}_t.npz ${O}_w.npz
done
python3 revsx.py $I ${O}_w.npz $O.npz | tail -1; rm -f ${O}_w.npz
