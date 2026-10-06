# RAC W1h driver AS RUN: GR final build
cd /home/claude/wayfarer-design/tools/rac/w1/w1g_drivers
python3 -c "
import gn3; r,C=gn3.build('GR','GR',{'pelvis':[0.985,1,1]},None,wd=gn3.G+'/final'); print('GR', r['r6']['stature'])"
cp /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/final/GR-LEAN_rest.npz /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/final/GR-LEAN_r6.npz /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/final_lean/
cd /home/claude/wayfarer-design/tools/rac/w1
python3 run_candidate.py /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/final GR /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1f/final/MF-M-R_rest.npz > /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/final/GR.rc.log 2>&1
REF=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/final LEAN=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/final_lean python3 w1g_drivers/cib_all.py GR
cp /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/final/GR_meas.json /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1g/cand/
echo GRDONE
