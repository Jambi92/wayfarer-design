RA=/home/claude/wayfarer-design/reviews/reference-assets; D=/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v001; W1=/home/claude/wayfarer-design/tools/rac/w1
cd /tmp/claude-0/rt/du
for id in DU122C-NAT DU152C-NAT; do /home/claude/stc/bin/python3 $D/du_regen.py $RA/builds/${id}_build.json $RA/r6/${id}_r6.npz src > logs/regen_$id.log 2>&1 & done
for n in DUF137C MF152 MFF152; do (cd $W1 && python3 native_short.py /tmp/claude-0/rt/du/nat/$n.cfg.json /tmp/claude-0/rt/du/nat > /tmp/claude-0/rt/du/logs/nat_$n.log 2>&1) & done
wait; echo PARTA_BUILDS_DONE
