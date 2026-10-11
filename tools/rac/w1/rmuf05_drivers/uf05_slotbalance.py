# RAC RM-UF-05: slot-balance sensitivity - how much does collapsing ONE UFCA slot (to a single value + 1 % jitter) lower the batch median
# NN distance under D1 vs D2, for a 1-control slot vs the largest slot, on the inventory slot-count profiles (unit-span diagnostic sampling).
import os, sys, json, numpy as np
from scipy.stats import qmc
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import uf05_metrics as UM, uf05_eval as UE
out = {}
for pop, cnt in UE.PROF.items():
    sl = np.concatenate([[i] * c for i, c in enumerate(cnt)]); d = len(sl); present = [i for i, c in enumerate(cnt) if c]
    small = min(present, key=lambda i: cnt[i]); large = max(present, key=lambda i: cnt[i]); row = {}
    for tag, s in (('smallest_slot', small), ('largest_slot', large)):
        drops = []
        for sd in (101, 202, 303, 404):
            rng = np.random.default_rng(sd); U = qmc.Sobol(d, scramble=True, seed=sd).random(256); b1 = np.median(UM.nn(UM.d1(U))); b2 = np.median(UM.nn(UM.d2(U, sl)))
            m = sl == s; U[:, m] = np.clip(U[0, m] + rng.normal(0, 0.01, (256, m.sum())), 0, 1)
            drops.append([1 - np.median(UM.nn(UM.d1(U))) / b1, 1 - np.median(UM.nn(UM.d2(U, sl))) / b2])
        row[tag] = dict(slot_index=int(s), controls=int(cnt[s]), D1_drop=float(np.mean(drops, 0)[0]), D2_drop=float(np.mean(drops, 0)[1]))
    out[pop] = row; print(pop, row)
json.dump(out, open(UE.S + '/slotbalance.json', 'w'), indent=1)
