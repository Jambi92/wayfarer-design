# RAC W3C: measure every W3C body (accepted anatomy + diagnostic candidates) -> scratch w3c/metrics.json
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3c_face as WF
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
BODIES = {  # id: (path, class)
 'SKM183': (S + '/w2b/st/SKM183', 'accepted'), 'MFM183': (S + '/w3c/b/MFM183', 'matched build (accepted MF route, H183)'),
 'SKM190': (S + '/w2b/st/SKM190', 'accepted'), 'MFM190': (S + '/w2b/st/MFM190', 'accepted'),
 'SKM203': (S + '/w2b/st/SKM203', 'accepted'), 'MFM203': (S + '/w2a/st/MFM203', 'accepted'),
 'SK208': (S + '/w1f/final/SK', 'accepted (Skarn reference)'),
 'SKF190': (S + '/w2b/st/SKF190', 'accepted'), 'MFF190': (S + '/w2b/st/MFF190K3', 'accepted'),
 'SKF203': (S + '/w2b/st/SKF203', 'accepted'), 'MFF203': (S + '/w2a/st/MFF203', 'accepted'),
 'SKM190-NLOW': (S + '/w3c/b/SKM190-NLOW', 'matched build (accepted Narrow frame + low muscle)'), 'MFM190-NLOW': (S + '/w3c/b/MFM190-NLOW', 'matched build (accepted Narrow frame + low muscle)'),
 'SKM190-B': (S + '/w3c/b/SKM190-B', 'matched build (accepted Broad frame, reference composition)'), 'MFM190-B': (S + '/w3c/b/MFM190-B', 'matched build (accepted Broad frame, reference composition)'),
 'SK208-HIFAT': (S + '/w2b/comp/SKM-HIFAT', 'accepted composition'), 'SK208-HIMUS': (S + '/w2b/comp/SKM-HIMUS', 'accepted composition'),
 'SKM190-C1': (S + '/w3c/b/SKM190-C1', 'candidate'), 'SKM190-C2': (S + '/w3c/b/SKM190-C2', 'candidate'), 'SKM190-C3': (S + '/w3c/b/SKM190-C3', 'candidate'),
 'SKF190-C1': (S + '/w3c/b/SKF190-C1', 'candidate'),
 'SKM190-SKOV_BROW': (S + '/w3c/b/SKM190-SKOV_BROW', 'overlap candidate'), 'SKM190-SKOV_JAW': (S + '/w3c/b/SKM190-SKOV_JAW', 'overlap candidate'),
 'SKM190-SKOV_MID': (S + '/w3c/b/SKM190-SKOV_MID', 'overlap candidate'),
 'MFM190-MFOV_BROW': (S + '/w3c/b/MFM190-MFOV_BROW', 'overlap candidate'), 'MFM190-MFOV_JAW': (S + '/w3c/b/MFM190-MFOV_JAW', 'overlap candidate'),
 'MFM190-MFOV_MID': (S + '/w3c/b/MFM190-MFOV_MID', 'overlap candidate')}
if __name__ == '__main__':
    out = {}
    for k, (p, cl) in BODIES.items():
        m = WF.metrics(p + '_r6.npz'); m['class'] = cl; m['path'] = p; out[k] = m
        print(k.ljust(18), ' '.join('%s %.4f' % (q, m[q]) for q in WF.KEYS), 'H %.1f HH %.2f' % (m['H'], m['HH']), flush=True)
    os.makedirs(S + '/w3c', exist_ok=True); json.dump(out, open(S + '/w3c/metrics.json', 'w'), indent=1)
