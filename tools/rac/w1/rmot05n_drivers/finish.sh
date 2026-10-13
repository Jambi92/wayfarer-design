#!/bin/bash
# finish.sh RAW.obj OUTPREFIX ratio : largest component -> l_finish (relax + decimate) -> body-only npz (neck-root cut 191)
D=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad
T=/home/claude/wayfarer-design/tools/rac/w1/rmot05l_drivers
python3 -c "
import sys
import trimesh,sys
m=trimesh.load('$1',process=False); c=m.split(only_watertight=False); c=sorted(c,key=lambda x:-len(x.faces)); print('components',len(c)); c[0].export('$2_lc.obj')"
python3 /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/rd/rd_finish.py $2_lc.obj $2 ${3:-0.15} 2>/dev/null | tail -1
python3 $T/l_npz.py $2.obj $2 191
