# RAC RM-OT-05F handoff export: everything a sculptor needs to sculpt the Gorrund hard-form base mesh on the accepted skeleton route,
# written to reviews/rac-rmot05f-handoff/template/ (meshes) and .../data/ (joints, stations, protected relations, region masks).
#   GO_ref_route_r6.obj      START MESH: unorganized accepted-route Gorrund reference body (230.9 cm, reference composition, R-6)
#   GO_low_route_r6.obj      the same route at low composition (muscle 0, weight 0.5): persistence preview only, never sculpted
#   GO_true_floor_r6.obj     the 05D TRUE SKELETAL FLOOR (hard limit: no sculpted vertex may go inside it)
#   GO_old_lean_r6.obj       the superseded MPFB minimum-body -LEAN (context only: the sculpt MAY go inside it, down to the true floor)
#   data/joints_r6.json      R-6 joint heads / tails in the template frame (the accepted skeleton; read-only)
#   data/stations.json       skeleton-anchored ALPC station heights + protected Gorrund relations (05D semantics)
#   data/regions.json        vertex-index lists of the six hard-form families A-F and the no-touch zones
# Usage: python3 f_export.py
import os, sys, json, numpy as np
from f_common import *
import skeletal_stations as SS
if __name__ == '__main__':
    T = HANDOFF + '/template'; Dd = HANDOFF + '/data'; os.makedirs(T, exist_ok=True); os.makedirs(Dd, exist_ok=True)
    V, B, L, J, f, z0 = route_state(SKELETON_BODY); F = B['F']
    Vl, Bl, Ll, Jl, fl, z0l = route_state(SKELETON_BODY + '-LOW')
    Fl = floor_in_body_frame(L, f, z0); Lb = f(L['V'].astype(float)) - [0, 0, z0]
    hdr = ('RM-OT-05F Gorrund hand-sculpt handoff. Units cm, Z up, ground z = 0, +Y anterior, +X = body LEFT. R-6 neutral stance.\n'
           '13380 vertices in template order; DO NOT add, delete, weld, reorder vertices or change faces.')
    write_obj(T + '/GO_ref_route_r6.obj', V, F, hdr + '\nSTART MESH: unorganized accepted-route reference body, 230.9 cm, reference composition.')
    write_obj(T + '/GO_low_route_r6.obj', Vl, F, hdr + '\nLow composition (muscle 0, weight 0.5) of the same route. Preview only; do not sculpt.')
    write_obj(T + '/GO_true_floor_r6.obj', Fl, F, hdr + '\n05D TRUE SKELETAL FLOOR. Hard limit: every sculpted vertex must stay outside this surface.')
    write_obj(T + '/GO_old_lean_r6.obj', Lb, F, hdr + '\nSuperseded MPFB minimum-body -LEAN (context only). The sculpt may go inside it, down to the true floor.')
    json.dump({'convention': hdr, 'joints': J}, open(Dd + '/joints_r6.json', 'w'), indent=1)
    keep = B['keep'].astype(bool)
    st = SS.read_body(CG.path(SKELETON_BODY), [S + '/w2c/donor', S + '/w2d/h', S + '/w1g/donor', S + '/w2d/donor'])
    lev = SS.levels(CG.path(SKELETON_BODY) + '-LEAN_rest.npz')
    json.dump({'stature_reference_cm': float(V[keep, 2].max()), 'stature_low_cm': float(Vl[keep, 2].max()),
               'note': 'Station levels are taken from the accepted skeleton (-LEAN, rest pose) by skeletal_stations.levels; protected relations '
                       'are read on the unorganized route (composition-infimum) at those levels and are fixed by the skeleton: the sculpt cannot '
                       'and must not change them. Organized-surface readings are diagnostics only (05E author ruling 2).',
               'skeleton_station_level_indices_rest (bony_envelope.fast_stations level grid of the -LEAN)': lev, 'protected_relations': st['protected_unorganized_route'],
               'true_floor_section_relations': st.get('true_floor'), 'canon_relations': {
                   'GO-P2b': 'bitrochanteric / iliac-crest breadth ~ MF (no lateral outrigging) - on the skeleton',
                   'GO-P4': 'pelvic AP depth / iliac-crest breadth > MF and > SK - on the skeleton',
                   'GO-P6': 'thorax -> lower trunk -> pelvis with no abrupt step in breadth or depth; waist definition allowed',
                   'GO-G1': 'shoulder-joint breadth / thoracic breadth not greater than MF (no girdle overhang)'}},
              open(Dd + '/stations.json', 'w'), indent=1, default=float)
    R = regions(B, V, J)
    json.dump({'convention': 'indices into the 13380-vertex template (0-based); families A-F of the 05F brief; NO_TOUCH zones must stay within 0.5 cm of the template',
               'regions': {k: np.where(m[:NBODY])[0].tolist() for k, m in R.items()}}, open(Dd + '/regions.json', 'w'))
    print({k: int(m.sum()) for k, m in R.items()}, 'stature', float(V[keep, 2].max()), float(Vl[keep, 2].max()))
