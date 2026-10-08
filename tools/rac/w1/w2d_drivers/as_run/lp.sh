cd /home/claude/wayfarer-design/tools/rac/w1
S=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad
while ! grep -q FR_DONE $S/w2d/logs/fr.log; do sleep 10; done
python3 w2d_drivers/go_body.py GOLP218 0.7503 - '{"measure-upperarm-length-decr":null,"measure-lowerarm-length-decr":null,"measure-napetowaist-dist-incr":null}' > $S/w2d/logs/GOLP218.log 2>&1
echo LP_DONE >> $S/w2d/logs/GOLP218.log
