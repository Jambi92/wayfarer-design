# pipeL.sh CAGE OUT LEVEL : production pipeline at subdivision LEVEL
set -e; cd /tmp/claude-0/rt; C=$1; O=$2; LV=$3; BP=/home/claude/stc/bin/python3
python3 subproj.py $C ${O}a.npz $LV
python3 polish.py ${O}a.npz ${O}b.npz 2
python3 crease.py ${O}b.npz ${O}c.npz 6 0.03
python3 fixfold.py ${O}c.npz ${O}d.npz 0.06 3
python3 crease.py ${O}d.npz ${O}e.npz 4 0.03
$BP sxfix.py -- ${O}e.npz ${O}f.npz 10
python3 crease.py ${O}f.npz ${O}g.npz 3 0.03
$BP sxfix.py -- ${O}g.npz ${O}h.npz 10
python3 crease.py ${O}h.npz ${O}i.npz 2 0.03
$BP sxfix.py -- ${O}i.npz ${O}j.npz 10
$BP sxfinal.py -- ${O}j.npz ${O}k.npz | tail -1
python3 foldfix.py ${O}k.npz ${O}.npz | tail -1
rm -f ${O}[b-k].npz
$BP /tmp/claude-0/rp2/sxq.py ${O}.npz ${O}_sx.npy | grep PAIRS
python3 dev.py ${O}.npz ${O}_dev.json
python3 gate.py ${O}.npz ${O}_gate.json > /dev/null
python3 worst.py ${O}.npz 2>/dev/null | head -2 | cut -c1-300
echo PIPEDONE
