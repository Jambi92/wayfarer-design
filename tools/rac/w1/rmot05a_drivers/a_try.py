import sys, json; sys.argv += []
import a_preview as AP
S = AP.S; A = json.load(open(sys.argv[1])); tag = sys.argv[2]
print('GR', AP.make(S + '/w2c/b/GR218R/GR218R', A['GR'], 'GRA' + tag))
print('GO', AP.make(S + '/w2d/b/GO229/GO229', A['GO'], 'GOA' + tag))
AP.PK.reg('SK218x', S + '/w2c/sk/SKM218', 'Skarn 218'); AP.PK.reg('GR218x', S + '/w2c/b/GR218R/GR218R', 'Grask 218 W2')
AP.PK.reg('GO229x', S + '/w2d/b/GO229/GO229', 'Gorrund 229 W2')
AP.PK.BODIES['GRA' + tag] = (AP.OUT + '/GRA' + tag, 'Grask 218 ' + tag); AP.PK.BODIES['GOA' + tag] = (AP.OUT + '/GOA' + tag, 'Gorrund 229 ' + tag)
AP.PK.SH = AP.OUT
for v in ('F', 'P', 'Q', 'RQ'):
    AP.PK.row_sheet('prev_%s_%s.jpg' % (tag, v), 'RM-OT-05A preview %s %s body only' % (tag, v), '', ['SK218x', 'GR218x', 'GRA' + tag, 'GO229x', 'GOA' + tag], v, headless=True)
