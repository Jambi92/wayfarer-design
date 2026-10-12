# RAC RM-OT-05G repository-side generator of the PERSISTENCE-PREVIEW data used by g_preview.py in Blender. It exports, for the low
# composition (muscle 0, weight 0.5) and the Narrow / Broad Frame states of the accepted Gorrund route, exactly the quantities that the
# 05F transport (race_base.sculpt_layer) uses:
#   GO_<state>_route_r6.obj        the unorganized route surface of that state (template vertex order, same frame conventions)
#   GO_<state>_true_floor_r6.obj   that state's 05D true skeletal floor
#   GO_<state>_transport.npz       T (n,3,3) = R_state R_ref^T   (skinned-frame rotation from the reference to the state)
#                                  s (n,)    = blended bone length ratio state / reference
# so that   preview_state = route_state + s * T @ (sculpt - template)          (the delivered displacement, transported)
# This is the transport BEFORE the true-floor clamp and the volume-restoring layer; f_reentry remains the authoritative build. No body is
# generated: the preview is only ever computed from a delivered (or tooling-fixture) sculpt. It does NOT scale the body or invent shape.
# Verification: with the 05F T1 tooling fixture, preview_state is compared with the built GO5FT1 states (report printed / saved).
# Usage: python3 g_make_transport.py [--verify]
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'rmot05f_drivers'))
from f_common import *
OUT = HANDOFF + '/blender/transport'
STATES = (('low', SKELETON_BODY + '-LOW'), ('narrow', SKELETON_BODY + 'N'), ('broad', SKELETON_BODY + 'B'))
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    V0, B, L, J, f, z0 = route_state(SKELETON_BODY); F = B['F']
    Rr, lr = RB.skin_frames(dict(L), J)
    rep = {}
    for st, body in STATES:
        Vs, Bs, Ls, Js, fs, z0s = route_state(body)
        Rs, ls = RB.skin_frames(dict(Ls), Js)
        T = np.einsum('nij,nkj->nik', Rs, Rr)[:NBODY].astype(np.float32); s = np.where(lr > 1e-6, ls / np.maximum(lr, 1e-6), 1.0)[:NBODY].astype(np.float32)
        hdr = 'RM-OT-05G persistence-preview data (NOT a sculpt target): %s state of the accepted Gorrund route. cm, Z up, +Y anterior, +X body left, R-6.' % st
        write_obj(OUT + '/GO_%s_route_r6.obj' % st, Vs, F, hdr)
        write_obj(OUT + '/GO_%s_true_floor_r6.obj' % st, floor_in_body_frame(Ls, fs, z0s), F, hdr + ' 05D true skeletal floor of this state.')
        np.savez_compressed(OUT + '/GO_%s_transport.npz' % st, T=T, s=s)
        rep[st] = {'rotation_max_deg': float(np.degrees(np.arccos(np.clip((np.trace(T, axis1=1, axis2=2) - 1) / 2, -1, 1))).max()), 's_range': [float(s.min()), float(s.max())]}
        if '--verify' in sys.argv:       # T1 tooling fixture (failed 05D E1 surface used only as a displacement signal), built by f_reentry in 05F
            sig = read_obj(WORK + '/selftest/T1.obj')[0] - V0[:NBODY]
            prev = Vs[:NBODY] + s[:, None] * np.einsum('nij,nj->ni', T, sig)
            sfx = {'low': '-LOW', 'narrow': 'N', 'broad': 'B'}[st]
            built = np.load(CG.path('GO5FT1' + sfx) + '_r6.npz', allow_pickle=True)['V'].astype(float)[:NBODY]
            e = np.linalg.norm(prev - built, axis=1); m = np.linalg.norm(sig, axis=1) > 0.5
            rep[st]['verify_T1_preview_vs_built_cm'] = {'p50': round(float(np.median(e)), 3), 'p90': round(float(np.percentile(e, 90)), 3), 'max': round(float(e.max()), 3),
                                                       'p90_on_signal_vertices': round(float(np.percentile(e[m], 90)), 3)}
    json.dump(rep, open(OUT + '/transport_report.json', 'w'), indent=1); print(json.dumps(rep, indent=1))
