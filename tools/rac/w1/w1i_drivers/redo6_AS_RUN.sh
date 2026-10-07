# RAC W1i AS RUN: final build -> evaluation -> post -> sensitivity, with stage markers (container restarts)
set -e
cd /home/claude/wayfarer-design/tools/rac/w1
[ -f /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1i/STAGE_final ] || { bash w1i_drivers/final6.sh /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1i/GO_W1i_x.json; touch /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1i/STAGE_final; }
[ -f /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1i/STAGE_eval ] || { bash w1i_drivers/evalall.sh; touch /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1i/STAGE_eval; }
[ -f /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1i/STAGE_post ] || { bash w1i_drivers/post3.sh; touch /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1i/STAGE_post; }
[ -f /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1i/STAGE_sens ] || { cd w1i_drivers && python3 sens6.py /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/final/GO_params.json /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1i/ev/sensitivity_w1i.json && touch /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1i/STAGE_sens; }
echo REDO6 DONE
