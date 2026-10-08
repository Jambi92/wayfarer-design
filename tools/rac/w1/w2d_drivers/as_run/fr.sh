cd /home/claude/wayfarer-design/tools/rac/w1
S=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad
python3 w2d_drivers/go_body.py GO208 0.685 > $S/w2d/logs/GO208.log 2>&1 &
python3 w2d_drivers/go_body.py GON 0.8369140625 '{"bone_scales":{"LR:clavicle":[1,0.95,1],"spine_02":[0.95,1,1],"spine_03":[0.95,1,1],"pelvis":[0.95,1,1]},"kb_nodes":[0.95,0.95,0.95,0.95,0.95,0.95]}' > $S/w2d/logs/GON.log 2>&1
wait
python3 w2d_drivers/go_body.py GONF 0.8369140625 '{"bone_scales":{"LR:clavicle":[1,0.95,1],"spine_02":[0.95,1,1],"spine_03":[0.95,1,1],"pelvis":[0.95,1,1],"LR:thigh":[0.95,1,0.95]},"kb_nodes":[0.95,0.95,0.95,0.95,0.95,0.95]}' > $S/w2d/logs/GONF.log 2>&1 &
python3 w2d_drivers/go_body.py GOB 0.8369140625 '{"bone_scales":{"LR:clavicle":[1,1.05,1],"spine_02":[1.05,1,1],"spine_03":[1.05,1,1],"pelvis":[1.05,1,1]},"kb_nodes":[1.05,1.05,1.05,1.05,1.05,1.05]}' > $S/w2d/logs/GOB.log 2>&1
wait
python3 w2d_drivers/go_body.py GOBF 0.8369140625 '{"bone_scales":{"LR:clavicle":[1,1.05,1],"spine_02":[1.05,1,1],"spine_03":[1.05,1,1],"pelvis":[1.05,1,1],"LR:thigh":[1.05,1,1.05]},"kb_nodes":[1.05,1.05,1.05,1.05,1.05,1.05]}' > $S/w2d/logs/GOBF.log 2>&1 &
for c in "GOR-BODY-06 0.0 0.5" "GOR-BODY-07 1.0 0.5" "GOR-BODY-08 0.5 0.0" "GOR-BODY-09 0.5 1.0" "GOR-BODY-10 1.0 1.0" "GOR-BODY-11 0.0 1.0" "GOR-BODY-16 0.25 0.25"; do set -- $c; python3 w2d_drivers/go_comp.py $1 GOREF $2 $3 >> $S/w2d/logs/comp.log 2>&1; done
wait; echo FR_DONE
