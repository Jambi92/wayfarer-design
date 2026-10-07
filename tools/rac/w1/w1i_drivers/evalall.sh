# RAC W1i driver AS RUN (same as w1h_drivers/evalall.sh, output to w1i/ev) (scratch paths = this session's working directories): skeletal, ALPC, directional, skin, ALPC-8 evaluation
cd /home/claude/wayfarer-design/tools/rac/w1
EV=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1i/ev
mkdir -p $EV
for t in 0.0 0.5 1.0; do cp /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/skp/t$t/SKB229_meas.json /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/skp/t$t/SKB_meas.json; done
python3 skeletal_checks.py /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/skp $EV/skeletal_checks.json > $EV/skeletal_checks.log 2>&1
SKIN_DIR=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/cand python3 w1g_drivers/alpc_w1g.py /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/skp /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/stress /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/go16/GOR-BODY-16_meas.json /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1f/low/MF-M-R-LOW_meas.json /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1f/low/SK-LOW_meas.json $EV/alpc_w1i.json > $EV/alpc.log 2>&1
python3 directional_checks.py /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/cand $EV/directional_checks.json > $EV/dir.log 2>&1
python3 w1e_checks.py /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/cand $EV/w1e_checks.json > $EV/w1e.log 2>&1
python3 silhouette_test.py /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1f/final_lean/DU-NAT-LEAN_r6.npz /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/final_lean/GO-LEAN_r6.npz $EV/alpc8 > $EV/sil.log 2>&1
echo EVAL1 DONE
