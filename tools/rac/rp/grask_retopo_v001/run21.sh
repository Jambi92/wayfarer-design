cd /tmp/claude-0/rt; BP=/home/claude/stc/bin/python3
bash pipe2.sh cage21.npz q21
$BP sxfinal.py -- q21.npz q21t.npz | tail -1
python3 foldfix.py q21t.npz q21u.npz | tail -1
$BP sxfinal.py -- q21u.npz q21v.npz | tail -1
python3 foldfix.py q21v.npz final.npz | tail -1
$BP /tmp/claude-0/rp2/sxq.py final.npz final_sx.npy | grep PAIRS
python3 dev.py final.npz final_dev.json > final_dev.txt; cat final_dev.txt
python3 gate.py final.npz final_gate.json > final_gate.txt
python3 tagloops.py cage21.npz q21a.npz final_loops.json
python3 loopaudit.py final.npz final_loops_audit.json | tail -3
python3 lm.py final.npz final_lm.json && python3 lmdrift.py lm_src.json final_lm.json final_lmdrift.json
python3 identity.py final.npz final_identity.json
python3 seams.py final.npz final_loops.json final_seams.json
python3 folds.py final.npz | tee final_folds.txt
echo ALLDONE
