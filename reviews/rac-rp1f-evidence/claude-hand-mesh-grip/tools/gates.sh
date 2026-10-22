cd /tmp/claude-0/hand; T=$1; P=/home/claude/stc/bin/python3
$P tools/gate_topo.py $T/prod_final.npz $T/topo_final.json > $T/topo_final.log 2>&1
$P tools/sx.py $T/prod_final.npz $T/sx_final.npy > $T/sx_final.log 2>&1
$P tools/gate_dev.py $T/prod_final.npz $T/dev_final.json > $T/dev_final.log 2>&1
echo DONE > $T/gates.done
