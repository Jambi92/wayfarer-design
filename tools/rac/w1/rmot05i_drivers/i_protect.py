# RAC RM-OT-05I hand / digit PROTECTION OVERLAY (order §3). Derives the sculpt-side protected hand / digit set from the SAME criterion
# the authoritative re-entry guard uses (rmot05f_drivers/f_guard.py, hand_foot_topology):
#     hf = clip(w_hand_l + w_hand_r + w_fingers_l + w_fingers_r + w_ball_l + w_ball_r [+ w_toes_* if present], 0, 1) > 0.5   (keep vertices)
# on the accepted Gorrund skeleton route (SKELETON_BODY, the body whose weights every GO5F<SID> build carries), restricted to the
# 13 380 exported body vertices. The guard is NOT changed; the release regions.json is NOT changed in place.
# Output: reviews/rac-rmot05i-protection/regions_05i.json = the frozen 05G regions + one added key
#     NO_TOUCH_hands_digits_guard05i = guard hand/digit vertices (hand + fingers part) not already in NO_TOUCH_hands_digits
# (the foot part of the guard mask is already fully inside NO_TOUCH_toes_forefoot). Every exporter / preflight check that iterates
# NO_TOUCH_* keys (exporter X9, preflight P4 / P5 anchors / P7) therefore covers the added vertices with the unchanged 0.5 cm limit.
# Usage: python3 i_protect.py [--package-out DIR]   (DIR: optional derivative package = copy of the 05G handoff with regions_05i.json)
import os, sys, json, hashlib, shutil, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rmot05f_drivers'))
from f_common import *
OUT = REPO + '/reviews/rac-rmot05i-protection'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def derive():
    V0, B, L, J, f, z0 = route_state(SKELETON_BODY); keep = B['keep'].astype(bool)
    ks = [k for k in ('hand_l', 'hand_r', 'fingers_l', 'fingers_r', 'ball_l', 'ball_r', 'toes_l', 'toes_r') if 'w_' + k in B.files]
    hf = ((np.clip(sum(B['w_' + k] for k in ks), 0, 1) > 0.5) & keep)[:NBODY]
    hand = (np.clip(sum(B['w_' + k] for k in ks if k.startswith(('hand', 'fingers'))), 0, 1) > 0.5)[:NBODY]
    foot = (np.clip(sum(B['w_' + k] for k in ks if k.startswith(('ball', 'toes'))), 0, 1) > 0.5)[:NBODY]
    R = json.load(open(HANDOFF + '/data/regions.json')); G = {k: np.array(v) for k, v in R['regions'].items()}
    old = np.zeros(NBODY, bool); old[G['NO_TOUCH_hands_digits']] = True
    toes = np.zeros(NBODY, bool); toes[G['NO_TOUCH_toes_forefoot']] = True
    fam = {k: set(v.tolist()) for k, v in G.items() if not k.startswith('NO_TOUCH')}
    add = np.where(hand & ~old)[0]
    R2 = json.loads(json.dumps(R)); R2['regions']['NO_TOUCH_hands_digits_guard05i'] = add.tolist()
    R2['overlay_05i'] = {'order': 'RM-OT-05I section 3', 'source_rule': 'f_guard.py hand_foot_topology mask: clip(sum w_%s, 0, 1) > 0.5 on keep, body vertices 0..13379, skeleton route %s' % ('+'.join(ks), SKELETON_BODY),
                         'base_regions_sha256': sha(HANDOFF + '/data/regions.json'), 'guard_mask_body_vertices': int(hf.sum()), 'guard_hand_part': int(hand.sum()), 'guard_foot_part': int(foot.sum()),
                         'old_NO_TOUCH_hands_digits': int(old.sum()), 'added': int(len(add)), 'new_protected_hand_digit_total': int((old | hand).sum()),
                         'foot_part_outside_NO_TOUCH_toes_forefoot': int((foot & ~toes).sum()), 'old_hands_outside_guard_mask': int((old & ~hand).sum()),
                         'added_vertices_also_in_family': {k: int(len(set(add.tolist()) & s)) for k, s in fam.items()},
                         'note': 'protection / tooling correction only: thresholds, guard and biology unchanged; family vertices listed above are now protected (hands are not to be edited)'}
    return R2
if __name__ == '__main__':
    R2 = derive(); os.makedirs(OUT, exist_ok=True); p = OUT + '/regions_05i.json'; json.dump(R2, open(p, 'w'))
    print(json.dumps(R2['overlay_05i'], indent=1)); print('regions_05i.json sha256', sha(p))
    if '--package-out' in sys.argv:
        d = sys.argv[sys.argv.index('--package-out') + 1]
        if os.path.exists(d): shutil.rmtree(d)
        shutil.copytree(HANDOFF, d); shutil.copy(p, d + '/data/regions.json'); print('derivative package', d)
