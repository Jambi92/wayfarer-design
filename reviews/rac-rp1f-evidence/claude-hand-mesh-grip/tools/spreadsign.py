# spreadsign.py (bpy python) -- RIGDIR : per finger, the abduction sign (local Z) that moves its tip away from the middle finger
import sys, json, numpy as np, os; sys.path.insert(0, '/tmp/claude-0/hand/tools'); import bpy; from fastpose import Hand
import pickle
rd = sys.argv[sys.argv.index('--') + 1]; out = {}
for side in 'LR':
    H = Hand(rd, side); J = pickle.load(open(os.path.join(rd, 'rig_data.pkl'), 'rb'))[side]['joints']
    digs = {'L': ['A_L17', 'A_L18', 'A_L19', 'A_L20'], 'R': ['A_R21', 'A_R22', 'A_R23', 'A_R24']}[side]
    tip = lambda S, k: (S[H.idx[k + '_2']] @ np.r_[np.array(J[k]['tip']) / 100, 1])[:3]
    S0 = H.skin_mats({}); mid = 'A_L19' if side == 'L' else 'A_R22'   # reference: the middle finger
    ref = tip(S0, mid)
    for k in digs:
        if k == mid: continue
        dp = np.linalg.norm(tip(H.skin_mats({k + '_0': [0, 5, 0]}), k) - ref); dm = np.linalg.norm(tip(H.skin_mats({k + '_0': [0, -5, 0]}), k) - ref)
        out[k] = 1 if dp > dm else -1
    # middle finger: spread toward the side with more room (away from the ring finger)
    ring = 'A_L18' if side == 'L' else 'A_R23'; rr = tip(S0, ring)
    dp = np.linalg.norm(tip(H.skin_mats({mid + '_0': [0, 5, 0]}), mid) - rr); dm = np.linalg.norm(tip(H.skin_mats({mid + '_0': [0, -5, 0]}), mid) - rr)
    out[mid] = 1 if dp > dm else -1
print(json.dumps(out)); json.dump(out, open(os.path.join(rd, 'spread_sign.json'), 'w'))
