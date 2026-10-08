cd /home/claude/wayfarer-design/tools/rac/w1
S=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad
python3 w2d_drivers/go_body.py GOREF 0.8369140625 > $S/w2d/logs/GOREF.log 2>&1 &
python3 w2d_drivers/go_body.py GO218 0.7503 > $S/w2d/logs/GO218.log 2>&1
wait
python3 w2d_drivers/go_body.py GO239 0.8913 > $S/w2d/logs/GO239.log 2>&1 &
python3 w2d_drivers/go_body.py GO251 0.9718 > $S/w2d/logs/GO251.log 2>&1
wait; echo ST_DONE
