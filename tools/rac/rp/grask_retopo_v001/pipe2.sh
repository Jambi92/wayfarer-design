set -e; cd /tmp/claude-0/rt; C=$1; O=$2; BP=/home/claude/stc/bin/python3
python3 subproj.py $C ${O}a.npz 3
python3 polish.py ${O}a.npz ${O}b.npz 2
python3 crease.py ${O}b.npz ${O}c.npz 6 0.03
python3 fixfold.py ${O}c.npz ${O}d.npz 0.06 3
python3 crease.py ${O}d.npz ${O}e.npz 4 0.03
$BP sxfix.py -- ${O}e.npz ${O}f.npz 10
python3 crease.py ${O}f.npz ${O}g.npz 3 0.03
$BP sxfix.py -- ${O}g.npz ${O}h.npz 10
python3 crease.py ${O}h.npz ${O}i.npz 2 0.03
$BP sxfix.py -- ${O}i.npz ${O}.npz 10
python3 dev.py ${O}.npz ${O}_dev.json; python3 flipchk.py ${O}.npz 2>/dev/null | head -2; python3 wherep.py ${O}.npz 1.0
python3 gate.py ${O}.npz ${O}_gate.json | tail -5 | cut -c1-300
echo PIPEDONE
