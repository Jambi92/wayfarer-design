# RAC RM-OT-05D candidate sheets (order §7). The views are the 10 required: front, front 3/4, profile and rear 3/4 grey; front and
# profile black silhouette; and close strips of shoulder / thorax, pelvis / sacrum / proximal thigh, knee / shank, and forearm / wrist / hand.
# Same camera, ground, stature, R-6 stance and neutral grey on every sheet. Body only.
# Controls: Skarn at matched height, the Marchfolk reference, and the 05C developmental baseline (Grask C / Gorrund B) for provenance.
# States: reference composition, low composition (muscle 0 / weight 0.5), and Narrow / Broad frames.
# Usage: python3 d_package.py [main] [low] [frames] [close]
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'rmot05a_drivers'))
import a_package as AP
PK = AP.PK; S = AP.S
OUT = S + '/rmot05d/sheets'; os.makedirs(OUT, exist_ok=True); PK.SH = OUT; PK.R = S + '/rmot05d/rend_pkg'; os.makedirs(PK.R, exist_ok=True)
g = lambda n: S + '/w2c/b/%s/%s' % (n, n); o = lambda n: S + '/w2d/b/%s/%s' % (n, n)
B = dict(AP.B)
B.update({'MFR': (S + '/w1f/final/MF-M-R', 'MF ref (control)'), 'SKLOW': (S + '/w2b/comp/SKM-LOWMUS', 'SK low-mus (208)'), 'SKN': (S + '/w2b/fr/SKMNarrow', 'SK N (208)'), 'SKBR': (S + '/w2b/fr/SKMBroad', 'SK B (208)'),
          'GR5C': (g('GR5CC'), 'GR 05C-C baseline'), 'GR5CLOW': (g('GR5CC-LOW'), 'GR 05C-C low'), 'GR5CN': (g('GR5CCN'), 'GR N 05C-C'), 'GR5CB': (g('GR5CCB'), 'GR B 05C-C'),
          'GO5C': (o('GO5CB'), 'GO 05C-B baseline'), 'GO5CLOW': (o('GO5CB-LOW'), 'GO 05C-B low'), 'GO5CN': (o('GO5CBN'), 'GO N 05C-B'), 'GO5CB': (o('GO5CBB'), 'GO B 05C-B')})
for c in ('E1', 'E2', 'E3'):
    for race, f, h in (('GR', g, '218'), ('GO', o, '230.9')):
        n = race + '5D' + c
        B[n] = (f(n), '%s %s 05D-%s' % (race, h, c)); B[n + '-LOW'] = (f(n + '-LOW'), '%s 05D-%s low' % (race, c))
        B[n + 'N'] = (f(n + 'N'), '%s N 05D-%s' % (race, c)); B[n + 'B'] = (f(n + 'B'), '%s B 05D-%s' % (race, c))
PK.BODIES.clear(); PK.BODIES.update(B); AP.B.clear(); AP.B.update(B)
AP.CLOSE = AP.CLOSE + [('pelvis_RQ', 'thigh_l', 150, 4, 70, 'mid'), ('wrist_P', 'hand_l', 90, 0, 40, 'joint'), ('shank_P', 'calf_l', 90, 0, 60, 'joint')]
have = lambda ids: [i for i in ids if os.path.exists(B[i][0] + '_r6.npz')]
NOTE = 'Matched ortho camera / ground plane / stature, neutral grey, R-6 stance, head and neck removed. SK Skarn, MF Marchfolk, GR Grask, GO Gorrund.'
if __name__ == '__main__':
    what = sys.argv[1:] or ['main', 'low', 'frames', 'close']
    for race, sk, h in (('GR', 'SK218', '218'), ('GO', 'SK229', '230.9')):
        ids = have([sk, 'MFR', race + '5C', race + '5DE1', race + '5DE2', race + '5DE3'])
        if 'main' in what:
            for vn, vl in AP.VN:
                PK.row_sheet('d_%s_%s_grey.jpg' % (race, vn), 'RM-OT-05D %s %s cm candidates - %s - body only, neutral grey' % (race, h, vl), NOTE, ids, vn, headless=True)
            for vn, vl in (('F', 'front'), ('P', 'profile')):
                PK.row_sheet('d_%s_%s_sil.jpg' % (race, vn), 'RM-OT-05D %s %s cm candidates - %s - black silhouette, body only' % (race, h, vl), NOTE, ids, vn, sil=True, headless=True)
        if 'low' in what:
            lids = have(['SKLOW', race + '5CLOW', race + '5DE1-LOW', race + '5DE2-LOW', race + '5DE3-LOW'])
            for vn, vl in AP.VN:
                PK.row_sheet('d_%s_low_%s.jpg' % (race, vn), 'RM-OT-05D %s low composition (muscle 0, weight 0.5) - %s - body only' % (race, vl), NOTE, lids, vn, headless=True)
            for vn, vl in (('F', 'front'), ('P', 'profile')):
                PK.row_sheet('d_%s_low_%s_sil.jpg' % (race, vn), 'RM-OT-05D %s low composition - %s - silhouette' % (race, vl), NOTE, lids, vn, sil=True, headless=True)
        if 'frames' in what:
            fids = have(['SKN', 'SKBR', race + '5CN', race + '5CB'] + [race + '5D%s%s' % (c, v) for c in ('E1', 'E2', 'E3') for v in ('N', '', 'B')])
            for vn, vl in (('F', 'front'), ('P', 'profile'), ('RQ', 'rear 3/4')):
                PK.row_sheet('d_%s_frames_%s.jpg' % (race, vn), 'RM-OT-05D %s frame diagnostic (Narrow / reference / Broad) - %s - body only' % (race, vl), NOTE, fids, vn, headless=True)
        if 'close' in what:
            AP.OUT = OUT; AP.PFX = 'RM-OT-05D ' + race
            AP.close_sheets(have([sk, race + '5C', race + '5DE1', race + '5DE2', race + '5DE3']), 218 if race == 'GR' else 229)
