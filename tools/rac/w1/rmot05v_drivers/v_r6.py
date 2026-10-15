# RM-OT-05V measurement-pose derivative (order §6): the smallest RIGID whole-body repositioning that gives full plantigrade
# contact (heel and forefoot on the ground). The candidate stands on its forefeet with both heels ~1.5 cm off the ground and the
# trunk leaning slightly forward; one rigid pitch about the forefoot contact line brings the heels down. Every length, joint
# relation and the anatomy are preserved exactly (rigid transform); only the orientation in the measurement frame changes.
# Usage: python3 v_r6.py STATE.npz OUT.npz OUT.json
import sys, json, numpy as np
d = dict(np.load(sys.argv[1])); V = d['V'].astype(np.float64); X0 = -0.5
feet = (V[:, 2] < 12) & (np.abs(V[:, 0] - X0) > 5)
P = V[feet]; ground = V[:, 2].min()
fore = P[(P[:, 2] < ground + 0.35)]; y_piv = float(np.median(fore[:, 1]))
heel = P[P[:, 1] < P[:, 1].min() + 10]; hz = float(heel[:, 2].min() - ground); hy = float(heel[np.argmin(heel[:, 2]), 1])
alpha = -float(np.arctan2(hz, y_piv - hy))          # pitch so the heel comes down onto the ground (pivot = forefoot contact)
c, s = np.cos(alpha), np.sin(alpha); y = V[:, 1] - y_piv; z = V[:, 2] - ground
V2 = V.copy(); V2[:, 1] = y_piv + c * y + s * z
V2[:, 2] = ground + (-s * y + c * z)
V2[:, 2] -= V2[:, 2].min() - ground                 # re-ground (sole at the original ground level)
d['V'] = V2.astype(np.float32); np.savez_compressed(sys.argv[2], **{k: v for k, v in d.items() if k != 'meta'})
P2 = V2[feet]; h2 = P2[P2[:, 1] < P2[:, 1].min() + 10]
rep = dict(rigid_pitch_deg=round(float(np.degrees(alpha)), 3), pivot_y_cm=round(y_piv, 2), heel_gap_before_cm=round(hz, 3),
           heel_gap_after_cm=round(float(h2[:, 2].min() - V2[:, 2].min()), 3), skull_vertex_shift_cm=None,
           note='rigid transform: all inter-vertex distances unchanged (checked)')
i, j = np.random.default_rng(0).integers(0, len(V), (2, 2000)); rep['max_pair_distance_change_cm'] = float(np.abs(np.linalg.norm(V[i] - V[j], axis=1) - np.linalg.norm(V2[i] - V2[j], axis=1)).max())
json.dump(rep, open(sys.argv[3], 'w'), indent=1); print(json.dumps(rep))
