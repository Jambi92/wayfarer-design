# 6-body uninformed probe (as rmot05a_drivers/a_blindq.py) for RM-OT-05B previews
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05a_drivers')
import a_blindq as Q, b_preview as P
Q.PK.R = P.S + '/rmot05b/rend'
tag = sys.argv[1]; S = P.S
Q.PK.reg('SK218x', S + '/w2c/sk/SKM218', 'x'); Q.PK.reg('MFx', S + '/w1f/final/MF-M-R', 'x'); Q.PK.reg('GRAx', S + '/w2c/b/GRA218/GRA218', 'x'); Q.PK.reg('GOAx', S + '/w2d/b/GOA229/GOA229', 'x')
Q.PK.BODIES['GRB' + tag] = (P.PREV + '/GRB' + tag, 'x'); Q.PK.BODIES['GOB' + tag] = (P.PREV + '/GOB' + tag, 'x')
Q.AP.OUT = P.PREV
Q.sheet(['SK218x', 'MFx', 'GRAx', 'GOAx', 'GRB' + tag, 'GOB' + tag], P.PREV + '/blindq_%s.jpg' % tag, int(sys.argv[2]))
