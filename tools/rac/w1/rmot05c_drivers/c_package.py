# RAC RM-OT-05C visual-first candidate package (order §7.1): one ground plane, matched orthographic camera and reference distance, neutral
# grey material, R-6 stance, head / neck removed (skin weight > 0.3). Per race:
#   1. candidates A / B / C at reference composition: front, front 3/4, profile, rear 3/4 (grey) and front / profile pure silhouette, with
#      the matched-height Skarn, the Marchfolk reference control and the current provisional 05B body;
#   2. low-composition diagnostic (muscle 0, weight 0.5) of every candidate with the matching Skarn / 05B low states;
#   3. frame diagnostic (Narrow / reference / Broad) where built;
#   4. Grask matched-height comparison at 229 cm against Skarn 229;
#   5. close architecture strips (each tile centred on that body's own joint, same cm-per-pixel within a sheet).
# Usage: python3 c_package.py [main] [low] [frames] [m229] [close]
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'rmot05a_drivers'))
import a_package as AP
PK = AP.PK; S = AP.S
OUT = S + '/rmot05c/sheets'; os.makedirs(OUT, exist_ok=True); PK.SH = OUT; PK.R = S + '/rmot05c/rend_pkg'; os.makedirs(PK.R, exist_ok=True)
g = lambda n: S + '/w2c/b/%s/%s' % (n, n); o = lambda n: S + '/w2d/b/%s/%s' % (n, n)
CAND = {'A': 'A restrained', 'B': 'B balanced', 'C': 'C assertive'}
B = dict(AP.B)
B.update({'MFR': (S + '/w1f/final/MF-M-R', 'MF ref (control)'), 'SKLOW': (S + '/w2b/comp/SKM-LOWMUS', 'SK low-mus (208)'),
          'GR5B': (g('GR5B218'), 'GR 218 05B'), 'GR5BLOW': (g('B_GR-BODY-06'), 'GR 218 05B low'), 'GR5B229': (g('GR5B229'), 'GR 229 05B'),
          'GO5B': (o('GO5BREF'), 'GO 230.9 05B'), 'GO5BLOW': (o('B_GOR-BODY-06'), 'GO 230.9 05B low')})
for c, cl in CAND.items():
    B['GR5C' + c] = (g('GR5C' + c), 'GR 218 05C-' + c); B['GR5C%s-LOW' % c] = (g('GR5C%s-LOW' % c), 'GR 218 05C-%s low' % c)
    B['GR5C%s229' % c] = (g('GR5C%s229' % c), 'GR 229 05C-' + c); B['GR5C%sN' % c] = (g('GR5C%sN' % c), 'GR 218 N 05C-' + c); B['GR5C%sB' % c] = (g('GR5C%sB' % c), 'GR 218 B 05C-' + c)
    B['GO5C' + c] = (o('GO5C' + c), 'GO 230.9 05C-' + c); B['GO5C%s-LOW' % c] = (o('GO5C%s-LOW' % c), 'GO 230.9 05C-%s low' % c)
    B['GO5C%sN' % c] = (o('GO5C%sN' % c), 'GO 230.9 N 05C-' + c); B['GO5C%sB' % c] = (o('GO5C%sB' % c), 'GO 230.9 B 05C-' + c)
PK.BODIES.clear(); PK.BODIES.update(B); AP.B.clear(); AP.B.update(B)
have = lambda ids: [i for i in ids if os.path.exists(B[i][0] + '_r6.npz')]
NOTE = 'Matched ortho camera / ground plane / reference distance, neutral grey, R-6 stance, head and neck removed. SK Skarn, MF Marchfolk, GR Grask, GO Gorrund.'
if __name__ == '__main__':
    what = sys.argv[1:] or ['main', 'low', 'frames', 'm229', 'close']
    for race, sk, ref, h in (('GR', 'SK218', 'GR5B', '218'), ('GO', 'SK229', 'GO5B', '230.9')):
        ids = have([sk, 'MFR', ref] + [race + '5C' + c for c in 'ABC'])
        if 'main' in what:
            for vn, vl in AP.VN:
                PK.row_sheet('c_%s_%s_grey.jpg' % (race, vn), 'RM-OT-05C %s %s cm candidates - %s - body only, neutral grey' % (race, h, vl), NOTE, ids, vn, headless=True)
            for vn, vl in (('F', 'front'), ('P', 'profile')):
                PK.row_sheet('c_%s_%s_sil.jpg' % (race, vn), 'RM-OT-05C %s %s cm candidates - %s - pure black silhouette, body only' % (race, h, vl), NOTE, ids, vn, sil=True, headless=True)
        if 'low' in what:
            lids = have(['SKLOW', race + '5BLOW'] + [race + '5C%s-LOW' % c for c in 'ABC'])
            for vn, vl in (('F', 'front'), ('P', 'profile'), ('RQ', 'rear 3/4')):
                PK.row_sheet('c_%s_low_%s.jpg' % (race, vn), 'RM-OT-05C %s low composition (muscle 0, weight 0.5) - %s - body only' % (race, vl), 'Does the race organization survive low composition? ' + NOTE, lids, vn, headless=True)
            for vn, vl in (('F', 'front'), ('P', 'profile')):
                PK.row_sheet('c_%s_low_%s_sil.jpg' % (race, vn), 'RM-OT-05C %s low composition - %s - silhouette' % (race, vl), NOTE, lids, vn, sil=True, headless=True)
        if 'frames' in what:
            fids = []
            for c in 'ABC': fids += have([race + '5C%sN' % c, race + '5C' + c, race + '5C%sB' % c]) if os.path.exists(B[race + '5C%sN' % c][0] + '_r6.npz') else []
            if fids:
                for vn, vl in (('F', 'front'), ('P', 'profile'), ('RQ', 'rear 3/4')):
                    PK.row_sheet('c_%s_frames_%s.jpg' % (race, vn), 'RM-OT-05C %s frame diagnostic (Narrow / reference / Broad) - %s - body only' % (race, vl), NOTE, fids, vn, headless=True)
        if 'm229' in what and race == 'GR':
            mids = have(['SK229', 'GR5B229'] + ['GR5C%s229' % c for c in 'ABC'])
            for vn, vl in (('F', 'front'), ('P', 'profile'), ('RQ', 'rear 3/4')):
                PK.row_sheet('c_GR_229_%s.jpg' % vn, 'RM-OT-05C Grask matched-height comparison 229 cm - %s - body only' % vl, NOTE, mids, vn, headless=True)
        if 'close' in what:
            AP.OUT = OUT; AP.PFX = 'RM-OT-05C ' + race
            AP.close_sheets(have([sk, ref] + [race + '5C' + c for c in 'ABC']), 218 if race == 'GR' else 229)
