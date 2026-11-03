#!/bin/sh
# runfit.sh CFG : resumable corrective fit. Resumes from the last saved CF_<c>.json (partial or final) if present.
c=$1; R=/tmp/claude-0/rp6; cd /home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001
if [ -f $R/CF_$c.json ] && [ -f $R/CF_$c.npz ]; then cp $R/CF_$c.json $R/CF_${c}_init.json; cp $R/CF_$c.npz $R/CF_${c}_init.npz; export INIT=$R/CF_${c}_init.json; fi
echo "START $(date +%T) INIT=${INIT:-none}" >> $R/fit_$c.log
python3 sa6_fit.py $c $R/CF_$c.json $R/W_$c.npz >> $R/fit_$c.log 2>&1
echo EXIT $? >> $R/fit_$c.log
