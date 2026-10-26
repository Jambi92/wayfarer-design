# recipe.sh IN OUT : quad-quality recipe used for L2v (qopt hard/soft alternating with light crease re-capture)
set -e; cd /tmp/claude-0/rt; I=$1; O=$2
python3 qopt.py $I ${O}1.npz 15 | tail -1
python3 qopt.py ${O}1.npz ${O}2.npz 20 soft | tail -1
python3 crease.py ${O}2.npz ${O}3.npz 2 0.03 | tail -1
python3 qopt.py ${O}3.npz ${O}4.npz 6 | tail -1
python3 qopt.py ${O}4.npz ${O}5.npz 12 soft | tail -1
python3 crease.py ${O}5.npz ${O}6.npz 1 0.03 | tail -1
python3 qopt.py ${O}6.npz ${O}.npz 8 | tail -1
rm -f ${O}[1-6].npz
python3 hardlist.py ${O}.npz ${O}_hard.json | tail -1
python3 dev.py ${O}.npz ${O}_dev.json
echo RECIPEDONE
