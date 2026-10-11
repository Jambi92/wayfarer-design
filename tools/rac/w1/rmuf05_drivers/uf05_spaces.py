# RAC RM-UF-05: normalized structural facial DIR spaces used by the batch-diversity diagnostic.
# Only author-accepted numeric DIR ranges (Saurin, SAURIN_V1 s258/s259/s267) or named accepted anchors (Skarn / Marchfolk, W3C / W3D)
# define a span. Everything else is UNSCALED / EXCLUDED (coverage loss reported, see coverage.json). Nothing here is a frequency or a
# creator interval: anchor spans are DIAGNOSTIC ANCHOR SCALES only.
import numpy as np
SAURIN = {  # axis: (slot, lo, hi, ref, class)  multipliers on the W2 reference; first-pass creator hard bounds
    'head_scale': (1, 0.92, 1.08, 1.0, 'NUM SA s258'), 'cran_len': (2, 0.92, 1.08, 1.0, 'NUM SA s259'), 'cran_w': (2, 0.92, 1.08, 1.0, 'NUM SA s259'),
    'cran_d': (2, 0.93, 1.07, 1.0, 'NUM SA s259'), 'ridge_m': (2, 0.90, 1.30, 1.0, 'NUM SA s267.3 (canonical relief: m >= 0.90)'),
    'orbit': (3, 0.92, 1.08, 1.0, 'NUM SA s259'), 'iod': (3, 0.92, 1.03, 1.0, 'NUM SA s267.2 (binding conflict: UFCA s4 Bound-locked)'),
    'ros_len': (5, 0.85, 1.20, 1.0, 'NUM SA s259'), 'ros_bw': (5, 0.88, 1.12, 1.0, 'NUM SA s259'), 'ros_aw': (5, 0.85, 1.15, 1.0, 'NUM SA s259'),
    'ros_d': (5, 0.88, 1.12, 1.0, 'NUM SA s259'), 'jaw_d': (8, 0.88, 1.15, 1.0, 'NUM SA s259')}
HUMAN = {  # MPFB target units; span = the accepted W3C / W3D anchors (overlap cases, C1R, C2) - DIAGNOSTIC ANCHOR SCALE
    'head_w': (2, 0.0, 0.24, None, 'ANCH (C1R 0.12, C2 0.24)'), 'head_d': (2, 0.0, 0.16, None, 'ANCH (C1R 0.08, C2 0.16)'),
    'brow': (3, -0.30, 0.60, None, 'ANCH (light-brow SK -0.30 .. strong-brow MF +0.60)'),
    'cheek': (5, -0.30, 0.60, None, 'ANCH (lighter-midface SK -0.30 .. substantial-midface MF +0.60)'),
    'nose_v': (6, 0.0, 0.30, None, 'ANCH (MF midface +0.30)'), 'nose_h': (6, -0.15, 0.30, None, 'ANCH (SK -0.15 .. MF +0.30)'), 'nose_d': (6, -0.15, 0.30, None, 'ANCH (SK -0.15 .. MF +0.30)'),
    'jaw_w': (8, -0.30, 0.60, None, 'ANCH (lighter-jaw SK -0.30 .. robust-jaw MF +0.60)'), 'jaw_drop': (8, 0.0, 0.30, None, 'ANCH (C1R 0.15 .. C2 / MF 0.30)')}
SK_REF = {'head_w': 0.12, 'head_d': 0.08, 'brow': 0.30, 'cheek': 0.30, 'nose_v': 0.15, 'nose_h': 0.15, 'nose_d': 0.15, 'jaw_w': 0.30, 'jaw_drop': 0.15}   # C1R
MF_REF = {k: 0.0 for k in HUMAN}
def axes(space, drop=()):
    return [k for k in space if k not in drop]
def norm(space, names, X):
    lo = np.array([space[k][1] for k in names]); hi = np.array([space[k][2] for k in names]); return (X - lo) / (hi - lo)
def denorm(space, names, U):
    lo = np.array([space[k][1] for k in names]); hi = np.array([space[k][2] for k in names]); return lo + U * (hi - lo)
def slots(space, names): return np.array([space[k][0] for k in names])
def saurin_valid(names, X):
    """SAURIN coupled validators (s259 / s267) evaluated on raw multipliers; returns a boolean mask"""
    d = dict(zip(names, X.T)); ok = np.ones(len(X), bool)
    cl = d.get('cran_len', np.ones(len(X))); rl = d['ros_len']
    ok &= rl >= 0.85 + np.clip(cl - 1.0, 0, None) * (0.8847473 - 0.85) / 0.08          # rostrum minimum rises with cranial length (index floor; W1 coupled corner)
    big = rl > 1.10; ok &= ~big | ((d['ros_d'] >= 1.0) & (d['jaw_d'] >= 1.0))         # rostrum > +10 % -> rostral and posterior jaw depth >= reference
    r = (0.685 * d['ros_aw']) / d['ros_bw']; ok &= (r >= 0.60) & (r <= 0.73)            # anterior / base ratio 0.60-0.73 (reference 0.685); anterior <= base
    return ok
