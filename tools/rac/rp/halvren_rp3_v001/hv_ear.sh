# hv_ear.sh WORK CANON CAND HEAD : Halvren mixed-ear order (chatgpt-rac-rp3-halvren-central-accept-ear-architecture-order) -- one Halvren ear realization on
# a propagated Halvren family head (EAR_CF, default the HB2+HF2+HP-B family workspace /tmp/claude-0/rt/hv/hpe): engineering ear topology v002 sheet with the
# cuff canon CANON (FN = FENN_EAR_BRANCH_CUFF_CANON_v002, five rings; RI3 = VAEL_EAR_CUFF_CANON_v001, six rings; both read-only), the deformation-aware
# guard (fenn run_ear_v002_head.sh), integrity / T-4 / density / root audit, measurement. EAR_UNT_MODE=contacts (as Vael RI3).
W=$1; K=$2; C=$3; H=$4; B=/home/claude/stc/bin/python3; T=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001; R=/home/claude/wayfarer-design/reviews/rac-rp3-evidence
export EAR_CF=${EAR_CF:-/tmp/claude-0/rt/hv/hpe} EAR_TOPO=v002 EAR_UNT_MODE=${EAR_UNT_MODE:-contacts}
mkdir -p $W/{build,audit,meas,deform,probe}; cd $W
case $K in RI3) cp -n $R/vael_rp3_ear_root_integration/topology/VAEL_EAR_CUFF_CANON_v001.json canon_branch_topology.json;; FN) cp -n $R/fenn_ear_v002/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json canon_branch_topology.json;; esac
if [ "${HV_REPAIR:-0}" = 1 ]; then EAR_CAND=$C bash /home/claude/wayfarer-design/tools/rac/rp/halvren_rp3_v001/hv_run_head.sh $H $W > build/${H}_${C}_guard.log 2>&1   # Halvren realization path (HR1 + cuff repair)
else EAR_CAND=$C bash $T/run_ear_v002_head.sh $H $W > build/${H}_${C}_guard.log 2>&1; fi
$B $T/ear_audit.py -- build/${H}_${C}_branch.npz $EAR_CF/fam/${H}_fam.npz audit/${H}_${C}_audit.json > audit/${H}_$C.log 2>&1
python3 $T/ear_measure.py build/${H}_${C}_branch.npz meas/${H}_${C}_measure.json > meas/${H}_$C.log 2>&1
echo "HVEAR $K $C $H $(tail -1 build/${H}_${C}_guard.log)"
