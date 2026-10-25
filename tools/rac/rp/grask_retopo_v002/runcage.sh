# runcage.sh NAME TAG : build cage NAME.npz (env params), x2 fit, quality recipe, gate, loop audit, iterated repair
set -e; cd /tmp/claude-0/rt; C=$1; T=$2
python3 build_cage.py $C.npz > $C.log 2>&1
bash pipeL.sh $C.npz $T 2
bash recipe.sh $T.npz ${T}v
python3 gate.py ${T}v.npz ${T}v_gate.json >/dev/null
timeout 3000 python3 loopaudit.py ${T}v.npz ${T}v_loops_audit.json | cut -c1-250 | tail -8
bash repairall.sh ${T}v.npz ${T}Rw 3
/home/claude/stc/bin/python3 sxfix.py -- ${T}Rw.npz ${T}Rx.npz 10 | tail -1
/home/claude/stc/bin/python3 sxfinal.py -- ${T}Rx.npz ${T}Ry.npz | tail -1
python3 foldfix.py ${T}Ry.npz ${T}R.npz | tail -1
rm -f ${T}Rx.npz ${T}Ry.npz
python3 hardlist.py ${T}R.npz ${T}R_hard.json | tail -1
python3 dev.py ${T}R.npz ${T}R_dev.json
/home/claude/stc/bin/python3 /tmp/claude-0/rp2/sxq.py ${T}R.npz ${T}R_sx.npy | grep PAIRS
echo RUNDONE
