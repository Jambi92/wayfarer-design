# RAC RM-OT-05B visual package (order §8): matched ortho camera / ground / stature / reference composition / R-6 stance / grey material.
# Lineups W2 -> 05A -> 05B at 208 / 218 / 229 (body only + silhouette), stature transport (Grask 198-239, Gorrund 208-251 incl. 230.9),
# frames + composition states, close anatomical sheets at matched 229 (and Grask 218).
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'rmot05a_drivers'))
import a_package as AP
PK = AP.PK; S = AP.S; RV = AP.RV
OUT = S + '/rmot05b/sheets'; os.makedirs(OUT, exist_ok=True); PK.SH = OUT; PK.R = S + '/rmot05b/rend_pkg'; os.makedirs(PK.R, exist_ok=True)
g = lambda n: S + '/w2c/b/%s/%s' % (n, n); o = lambda n: S + '/w2d/b/%s/%s' % (n, n)
B = dict(AP.B)
for h in (198, 208, 218, 229, 239): B['GR5B%d' % h] = (g('GR5B%d' % h), 'GR %d 05B' % h)
for h in (208, 218, 229, 239, 251): B['GO5B%d' % h] = (o('GO5B%d' % h), 'GO %d 05B' % h)
B.update({'GO5BREF': (o('GO5BREF'), 'GO 230.9 05B'), 'GR5BN': (g('GR5BN'), 'GR 218 N 05B'), 'GR5BB': (g('GR5BB'), 'GR 218 B 05B'),
          'GRLOWa': (g('B_GR-BODY-06'), 'GR 218 low-mus 05B'), 'GRLOWb': (g('B_GR-LOW'), 'GR 218 low m+f 05B'),
          'GO5BN': (o('GO5BN'), 'GO 230.9 N 05B'), 'GO5BB': (o('GO5BB'), 'GO 230.9 B 05B'),
          'GOLOWa': (o('B_GOR-BODY-06'), 'GO 230.9 low-mus 05B'), 'GOLOWb': (o('B_GOR-BODY-16'), 'GO 230.9 low m+f 05B'),
          'SKN': (S + '/w2b/fr/SKMNarrow', 'SK N (208)'), 'SKBR': (S + '/w2b/fr/SKMBroad', 'SK B (208)'), 'SKLOW': (S + '/w2b/comp/SKM-LOWMUS', 'SK low-mus (208)')})
PK.BODIES.clear(); PK.BODIES.update(B); AP.B.clear(); AP.B.update(B)
SETS = {208: ['MF203', 'SK208', 'GRW208', 'GRA208', 'GR5B208', 'GOW208', 'GOA208', 'GO5B208'], 218: ['SK218', 'GRW218', 'GRA218', 'GR5B218', 'GOW218', 'GOA218', 'GO5B218'],
        229: ['SK229', 'GRW229', 'GRA229', 'GR5B229', 'GOW229', 'GOA229', 'GO5B229', 'GO5BREF']}
if __name__ == '__main__':
    what = sys.argv[1:] or ['main', 'extra', 'close']
    if 'main' in what:
        for h, ids in SETS.items():
            for vn, vl in AP.VN:
                PK.row_sheet('b_%d_%s_body.jpg' % (h, vn), 'RM-OT-05B %d cm - %s - body only (head / neck removed)' % (h, vl), 'W2 -> 05A -> 05B. SK Skarn, GR Grask, GO Gorrund, MF Marchfolk. Matched ortho camera / ground / stature / reference composition.', ids, vn, headless=True)
                if vn in ('F', 'P'):
                    PK.row_sheet('b_%d_%s_sil.jpg' % (h, vn), 'RM-OT-05B %d cm - %s - pure silhouette, body only' % (h, vl), 'Black silhouette, head / neck removed.', ids, vn, sil=True, headless=True)
                if vn == 'Q':
                    PK.row_sheet('b_%d_%s_grey.jpg' % (h, vn), 'RM-OT-05B %d cm - %s - neutral grey with head' % (h, vl), 'Technical continuity view.', ids, vn)
    if 'extra' in what:
        for vn, vl in (('F', 'front'), ('P', 'profile'), ('RQ', 'rear 3/4')):
            PK.row_sheet('b_stature_GR_%s.jpg' % vn, 'RM-OT-05B Grask stature transport 198-239 - %s - body only' % vl, 'Same 05B recipe at every stature; no uniform scaling.', ['GR5B198', 'GR5B208', 'GR5B218', 'GR5B229', 'GR5B239'], vn, headless=True)
            PK.row_sheet('b_stature_GO_%s.jpg' % vn, 'RM-OT-05B Gorrund stature transport 208-251 - %s - body only' % vl, '229 nominal / 230.9 ARM kept distinct; 251 = current world-validation upper end, not permanent.', ['GO5B208', 'GO5B218', 'GO5B229', 'GO5BREF', 'GO5B239', 'GO5B251'], vn, headless=True)
            PK.row_sheet('b_frames_comp_%s.jpg' % vn, 'RM-OT-05B frames + composition - %s - body only' % vl, 'Skarn controls; Grask 218 N / ref / B / low-muscle (0, 0.5) / low muscle + fat (0.25, 0.25); Gorrund 230.9 same.',
                         ['SKN', 'SKBR', 'SKLOW', 'GR5BN', 'GR5B218', 'GR5BB', 'GRLOWa', 'GRLOWb', 'GO5BN', 'GO5BREF', 'GO5BB', 'GOLOWa', 'GOLOWb'], vn, headless=True)
            PK.row_sheet('b_frames_comp_%s_sil.jpg' % vn, 'RM-OT-05B frames + composition - %s - silhouette' % vl, 'As above, pure silhouette.',
                         ['SKN', 'SKBR', 'SKLOW', 'GR5BN', 'GR5B218', 'GR5BB', 'GRLOWa', 'GRLOWb', 'GO5BN', 'GO5BREF', 'GO5BB', 'GOLOWa', 'GOLOWb'], vn, sil=True, headless=True)
    if 'close' in what:
        AP.OUT = OUT; AP.PFX = 'RM-OT-05B'
        _orig = AP.Image.Image.save
        AP.close_sheets(['SK229', 'GRW229', 'GRA229', 'GR5B229', 'GOW229', 'GOA229', 'GO5B229'], 229)
        AP.close_sheets(['SK218', 'GRW218', 'GRA218', 'GR5B218'], 218)
