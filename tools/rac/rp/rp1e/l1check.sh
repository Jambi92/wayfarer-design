#!/bin/bash
# l1check.sh TAG CAGE COL : sim levels 1-2 only and print self-x
cd /home/claude/stc/rp1e
FNSMR=0 bash bsim6.sh $1 $2 $3 tg_r2m5 2 PN 1,3,4,5,6,7,8,9,10,11,12,13,14,15,16 0 2 2>&1 | grep -E "L1_sx|L2_sx"
