# runhand.sh TAG CAGE.npz BASEFSM : sim with r3 targets
T=$1; C=$2; B=${3:-fsm_tgR1.txt}
bash mkfsm.sh $C ${C%.npz}_remap.npy $B fsm_$T.txt; cp $C cage_$T.npz; cp ${C%.npz}_col.npy cage_${T}_col.npy
TPRE=tg_r3m5 FINALSM=3 FSMF=0.5 FSMV=$PWD/fsm_$T.txt ./runv.sh $T cage_$T.npz cage_${T}_col.npy PN 1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24 > /dev/null 2>&1
grep -E "L[1-4]_sx" $T.log | cut -c1-110; tail -8 $T.log | grep hand
