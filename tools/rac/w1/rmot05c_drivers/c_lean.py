# RAC RM-OT-05C search: render the base surfaces (-LEAN) of preview bodies next to the 05B lean.  Usage: python3 c_lean.py TAG
import os, sys
import c_preview as P
sys.path.insert(0, P.W1 + '/rmot05_drivers'); import ot05r_package as PK
S = P.S; tag = sys.argv[1]
PK.R = S + '/rmot05c/rend_prev'; PK.SH = S + '/rmot05c/prevsheets'
for race, b in (('GR', S + '/w2c/b/GR5B218/GR5B218-LEAN'), ('GO', S + '/w2d/b/GO5BREF/GO5BREF-LEAN')):
    ids = [race + 'L5B']; PK.BODIES[race + 'L5B'] = (b, race + ' 05B lean')
    for f in sorted(os.listdir(P.PREV)):
        if f.startswith(race + '_') and f.endswith('-LEAN_r6.npz') and ('_%s' % tag) in f:
            bid = f[:-7]; PK.BODIES[bid] = (P.PREV + '/' + bid, bid); ids.append(bid)
            for v in PK.VIEWS:
                q = '%s/%s_nh_%s.png' % (PK.R, bid, v[0])
                if os.path.exists(q): os.remove(q)
    for v in ('F', 'P', 'RQ'): PK.row_sheet('p_%s_%sL_%s.jpg' % (race, tag, v), 'lean %s %s' % (race, tag), '', ids, v, headless=True)
