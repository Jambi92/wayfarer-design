# RAC RM-OT-05E focused visual evidence (order §6). Matched camera / ground / stature, body only, neutral grey, R-6 stance.
# Views: front, front 3/4, profile, rear 3/4 grey; black silhouette front + profile; close strips knee / shank / ankle, elbow / forearm / wrist,
# posterior thoracolumbar / sacral load path, pelvis / proximal thigh. Controls: Marchfolk, Skarn (matched height), accepted Grask E3,
# Gorrund 05D E1 baseline and E2 provenance control. States: reference, low composition (muscle 0 / weight 0.5), Narrow / Broad.
# Usage: python3 e_package.py [main] [low] [frames] [close]
import os, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'rmot05d_drivers'))
import d_package as DP
AP, PK, S, B = DP.AP, DP.PK, DP.S, DP.B
OUT = S + '/rmot05e/sheets'; os.makedirs(OUT, exist_ok=True); PK.SH = OUT; PK.R = S + '/rmot05e/rend_pkg'; os.makedirs(PK.R, exist_ok=True)
o = lambda n: S + '/w2d/b/%s/%s' % (n, n)
for c in ('P1', 'P2', 'P3'):
    n = 'GO5E' + c
    B[n] = (o(n), 'GO 230.9 05E-%s' % c); B[n + '-LOW'] = (o(n + '-LOW'), 'GO 05E-%s low' % c)
    B[n + 'N'] = (o(n + 'N'), 'GO N 05E-%s' % c); B[n + 'B'] = (o(n + 'B'), 'GO B 05E-%s' % c)
B['GR5DE3'] = (B['GR5DE3'][0], 'GR 218 E3 (accepted dir.)'); B['GO5DE1'] = (B['GO5DE1'][0], 'GO 05D-E1 baseline'); B['GO5DE2'] = (B['GO5DE2'][0], 'GO 05D-E2 (provenance)')
PK.BODIES.clear(); PK.BODIES.update(B); AP.B.clear(); AP.B.update(B)
AP.CLOSE = [c for c in AP.CLOSE if c[0] in ('knee_F', 'knee_P', 'elbow_F', 'elbow_P', 'pelvis_Q', 'pelvis_P', 'pelvis_RQ', 'thorax_P', 'thorax_RQ', 'shank_P', 'wrist_P')] + [
    ('ankle_F', 'foot_l', 0, 0, 40, 'joint'), ('ankle_P', 'foot_l', 90, 0, 40, 'joint'), ('forearm_F', 'hand_l', 0, 0, 60, 'joint'),
    ('back_R', 'spine_01', 180, 4, 95, 'mid'), ('sacrum_RQ', 'pelvis', 150, 4, 70, 'mid')]
have = DP.have
NOTE = DP.NOTE + ' GO 05E = RM-OT-05E Gorrund structural candidates.'
if __name__ == '__main__':
    what = sys.argv[1:] or ['main', 'low', 'frames', 'close']
    ids = have(['MFR', 'SK229', 'GR5DE3', 'GO5DE1', 'GO5DE2', 'GO5EP1', 'GO5EP2', 'GO5EP3'])
    if 'main' in what:
        for vn, vl in AP.VN:
            PK.row_sheet('e_GO_%s_grey.jpg' % vn, 'RM-OT-05E Gorrund 230.9 cm structural candidates - %s - body only, neutral grey' % vl, NOTE, ids, vn, headless=True)
        for vn, vl in (('F', 'front'), ('P', 'profile')):
            PK.row_sheet('e_GO_%s_sil.jpg' % vn, 'RM-OT-05E Gorrund candidates - %s - black silhouette, body only' % vl, NOTE, ids, vn, sil=True, headless=True)
    if 'low' in what:
        lids = have(['SKLOW', 'GR5DE3-LOW', 'GO5DE1-LOW', 'GO5DE2-LOW', 'GO5EP1-LOW', 'GO5EP2-LOW', 'GO5EP3-LOW'])
        for vn, vl in AP.VN:
            PK.row_sheet('e_GO_low_%s.jpg' % vn, 'RM-OT-05E Gorrund low composition (muscle 0, weight 0.5) - %s - body only' % vl, NOTE, lids, vn, headless=True)
        for vn, vl in (('F', 'front'), ('P', 'profile')):
            PK.row_sheet('e_GO_low_%s_sil.jpg' % vn, 'RM-OT-05E Gorrund low composition - %s - silhouette' % vl, NOTE, lids, vn, sil=True, headless=True)
    if 'frames' in what:
        fids = have(['SKN', 'SKBR', 'GO5DE1N', 'GO5DE1B'] + ['GO5E%s%s' % (c, v) for c in ('P1', 'P2', 'P3') for v in ('N', '', 'B')])
        for vn, vl in (('F', 'front'), ('P', 'profile'), ('RQ', 'rear 3/4')):
            PK.row_sheet('e_GO_frames_%s.jpg' % vn, 'RM-OT-05E Gorrund frame diagnostic (Narrow / reference / Broad) - %s - body only' % vl, NOTE, fids, vn, headless=True)
    if 'close' in what:
        AP.OUT = OUT; AP.PFX = 'RM-OT-05E GO'
        AP.close_sheets(have(['SK229', 'GR5DE3', 'GO5DE1', 'GO5DE2', 'GO5EP1', 'GO5EP2', 'GO5EP3']), 229)
