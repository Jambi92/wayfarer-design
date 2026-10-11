# RAC W3D: C1R validation sheet + neck-correction close-up (same renderer / cameras as W3C).
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3c_face as WF, w3c_sheets as WS
S = WS.S
B = {'MFM190': S + '/w2b/st/MFM190', 'SKM190-C1': S + '/w3c/b/SKM190-C1', 'SKM190-C1R': S + '/w3d/b/SKM190-C1R', 'SKM190-N50': S + '/w3d/b/SKM190-N50',
     'SK208': S + '/w1f/final/SK', 'SK208-C1R': S + '/w3d/b/SK208-C1R', 'SKF190': S + '/w2b/st/SKF190', 'SKF190-C1R': S + '/w3d/b/SKF190-C1R', 'MFF190': S + '/w2b/st/MFF190K3',
     'SKM183-C1R': S + '/w3d/b/SKM183-C1R', 'SKM203-C1R': S + '/w3d/b/SKM203-C1R', 'SKM190-NLOW-C1R': S + '/w3d/b/SKM190-NLOW-C1R', 'SKM190-B-C1R': S + '/w3d/b/SKM190-B-C1R'}
for k, p in B.items():
    if k not in WS.M: m = WF.metrics(p + '_r6.npz'); m['path'] = p; WS.M[k] = m
WS.SH = S + '/w3d/sheets'; os.makedirs(WS.SH, exist_ok=True)
L = WS.lab
WS.grid('w3d_1_c1r_validation.jpg', 'W3D - C1R central Skarn face: validation set', ['Old accepted face vs C1R on the same body (body unchanged: 0.0000 cm outside head / neck).', 'Neutral expression, one grey material, matched ortho scale 36 cm.'],
        [('SK208', L('SK208', 'old SK reference (generic face)')), ('SK208-C1R', L('SK208-C1R', 'C1R central reference')), ('SKM190-C1R', L('SKM190-C1R', '190 config 1')),
         ('SKF190', L('SKF190', 'old config 2')), ('SKF190-C1R', L('SKF190-C1R', '190 config 2')), ('SKM183-C1R', L('SKM183-C1R', '183 lower adult')), ('SKM203-C1R', L('SKM203-C1R', '203')),
         ('SKM190-NLOW-C1R', L('SKM190-NLOW-C1R', 'Narrow + low muscle')), ('SKM190-B-C1R', L('SKM190-B-C1R', 'Broad, ref. comp.'))], 'head', ['F', 'Q', 'P'], ['front', 'three-quarter', 'profile'], cell=280)
WS.grid('w3d_2_neck_correction.jpg', 'W3D - neck-to-jaw correction (190 cm config 1)', ['C1 (W3C) -> C1R (neck width 0.30) -> rejected heavier option (0.50). Marchfolk for reference.'],
        [('MFM190', L('MFM190', 'Marchfolk')), ('SKM190-C1', L('SKM190-C1', 'C1 (W3C)')), ('SKM190-C1R', L('SKM190-C1R', 'C1R selected')), ('SKM190-N50', L('SKM190-N50', 'neck 0.50 (not used)'))],
        'head', ['F', 'Q', 'P'], ['front', 'three-quarter', 'profile'], cell=300)
