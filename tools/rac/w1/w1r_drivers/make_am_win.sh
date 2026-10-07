# W1r: am_win.py = arm_measure.py with the joint-breadth slab half-width (1.0 cm) made a module variable JBWIN[0]; used by jbw.py.
# Usage: sh make_am_win.sh MODDIR
mkdir -p $1; sed 's/m = np.abs(t) < 1.0/m = np.abs(t) < JBWIN[0]/; s/^import json, sys, numpy as np/import json, sys, numpy as np\nJBWIN = [1.0]/' /home/claude/wayfarer-design/tools/rac/w1/arm_measure.py > $1/am_win.py
