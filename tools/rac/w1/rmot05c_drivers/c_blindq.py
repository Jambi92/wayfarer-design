# RAC RM-OT-05C uninformed probe (as rmot05a_drivers/a_blindq.py): body-only grey, front + profile, height-normalized, shuffled codes.
# Usage: python3 c_blindq.py OUT_TAG SEED PREVIEW_ID...   (human-family controls Skarn 218 and Marchfolk reference always included)
import sys, os
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05a_drivers')
import a_blindq as Q, c_preview as P
Q.PK.R = P.S + '/rmot05c/rend_prev'; S = P.S
Q.PK.reg('SK218x', S + '/w2c/sk/SKM218', 'x'); Q.PK.reg('MFx', S + '/w1f/final/MF-M-R', 'x')
ids = sys.argv[3:]
for b in ids: Q.PK.BODIES[b] = (P.PREV + '/' + b, 'x')
Q.sheet(['SK218x', 'MFx'] + ids, P.S + '/rmot05c/prevsheets/blindq_%s.jpg' % sys.argv[1], int(sys.argv[2]))
