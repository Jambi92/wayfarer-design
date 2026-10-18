#!/bin/bash
f=/mnt/user-data/uploads/RaceBodies/source/Gorrund-Neutral-C/05AW4/$1.blend
sleep 2; cp $f real/ && /home/claude/bpyenv/bin/python ../readvf.py real/$1.blend real/$1_VF.npz 2>&1 | grep NV
