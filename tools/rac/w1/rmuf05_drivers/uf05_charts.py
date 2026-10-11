# RAC RM-UF-05 sheets 4 and 5: statistically sensitive population (Sagekin profile) and Halvren anti-50/50 / source-passing diagnostic.
# DIAGNOSTIC COVERAGE SAMPLING - NOT POPULATION FREQUENCY: unit-span coordinates on the inventory slot-count profiles; no Sagekin or Halvren
# numeric range or face anchor exists, so these sheets show validator behaviour only.
import os, sys, json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.stats import qmc
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import uf05_metrics as UM, uf05_eval as UE
S = UE.S; os.makedirs(S + '/sheets', exist_ok=True)
INK, INK2, C1, C2, C3 = '#0b0b0b', '#52514e', '#2a78d6', '#eb6834', '#1baf7a'
plt.rcParams.update({'font.size': 11, 'axes.edgecolor': '#b5b4ae', 'axes.labelcolor': INK2, 'xtick.color': INK2, 'ytick.color': INK2, 'axes.spines.top': False, 'axes.spines.right': False})
def prof_sl(cnt): return np.concatenate([[i] * c for i, c in enumerate(cnt)])
# ---- sheet 4: Sagekin profile
sl = prof_sl(UE.PROF['SG']); d = len(sl); rng = np.random.default_rng(101)
B = {'broad diagnostic coverage': qmc.Sobol(d, scramble=True, seed=101).random(256), 'central concentration (statistical identity)': np.clip(0.5 + rng.uniform(-0.1, 0.1, (256, d)), 0, 1)}
P = rng.random((3, d)); B['near-clone (3 templates)'] = np.clip(P[rng.integers(0, 3, 256)] + rng.normal(0, 0.01, (256, d)), 0, 1)
fig, ax = plt.subplots(figsize=(11, 5.2), dpi=110)
for (nm, U), c in zip(B.items(), (C1, C3, C2)):
    n = UM.nn(UM.d2(U, sl)); ax.hist(n, bins=np.linspace(0, 0.4, 81), color=c, alpha=0.85, label='%s  (median %.3f)' % (nm, np.median(n)), edgecolor='#fcfcfb', linewidth=0.5)
for x, lab, yf in ((0.015, 'A / B near-clone distance 0.015', 0.97), (0.09, 'C median floor 0.09', 0.80)):
    ax.axvline(x, color=INK2, lw=1.2, ls='--'); ax.text(x + 0.004, ax.get_ylim()[1] * yf, lab, color=INK2, fontsize=10)
ax.set_xlabel('nearest-neighbour distance D2 (slot-balanced, normalized)'); ax.set_ylabel('faces in batch (N = 256)')
ax.set_title('Statistically sensitive case: Sagekin slot profile (53 DIR, 8 slots)\nCentral concentration passes A and B and is wrongly rejected by C; near-clones fail all', loc='left', color=INK, fontsize=12)
ax.legend(frameon=False, loc='upper right', bbox_to_anchor=(1, 0.82)); fig.text(0.01, 0.01, 'DIAGNOSTIC COVERAGE SAMPLING - NOT POPULATION FREQUENCY. Sagekin facial ranges are QUALITATIVE; values are unit-span coordinates.', color=INK2, fontsize=9)
fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(S + '/sheets/uf05_4_sagekin_statistical.png'); plt.close(fig)
# ---- sheet 5: Halvren anti-50/50 / source passing
sl = prof_sl(UE.PROF['HV']); d = len(sl); S_ = sorted(set(sl)); rng = np.random.default_rng(202)
A = rng.uniform(0.15, 0.35, d); Bv = rng.uniform(0.65, 0.85, d)                      # two synthetic source centres (unit span)
def mk(T): return A + T * (Bv - A)                                                   # per-axis position t on the source axis
def slot_t(n): return np.repeat(rng.random((n, len(S_))), [np.sum(sl == s) for s in S_], axis=1) * 0 + rng.random((n, len(S_)))[:, np.searchsorted(S_, sl)]
batches = {'valid mixed (slots independent)': mk(np.clip(rng.random((256, len(S_)))[:, np.searchsorted(S_, sl)] + rng.normal(0, 0.05, (256, d)), 0, 1)),
           'exact 50/50 midpoint collapse': mk(np.clip(0.5 + rng.normal(0, 0.06, (256, d)), 0, 1)),
           'source passing (near-duplicate source)': mk(np.clip(rng.integers(0, 2, (256, 1)) + rng.normal(0, 0.03, (256, d)), 0, 1))}
rows = []
for nm, U in batches.items():
    T = (U - A) / (Bv - A); ts = np.stack([T[:, sl == s].mean(1) for s in S_], 1)
    mid = np.mean(np.all(np.abs(ts - 0.5) < 0.1, 1)); src = np.mean(np.all(ts < 0.1, 1) | np.all(ts > 0.9, 1)); n = np.median(UM.nn(UM.d2(U, sl)))
    rows.append((nm, n, mid, src))
fig, axs = plt.subplots(1, 3, figsize=(13, 4.6), dpi=110)
for j, (title, k, ref) in enumerate((('median NN distance D2', 1, 0.015), ('50/50 midpoint share (all slots |t - 0.5| < 0.1)', 2, None), ('source-passing share (all slots t < 0.1 or > 0.9)', 3, None))):
    ax = axs[j]; vals = [r[k] for r in rows]; ax.bar(range(3), vals, color=[C1, C2, C3], width=0.6)
    for i, v in enumerate(vals): ax.text(i, v, '%.3f' % v if k == 1 else '%.0f %%' % (100 * v), ha='center', va='bottom', color=INK, fontsize=10)
    if ref: ax.axhline(ref, color=INK2, ls='--', lw=1); ax.text(2.35, ref, 'A near-clone 0.015', color=INK2, fontsize=9, va='bottom', ha='right')
    ax.set_xticks(range(3)); ax.set_xticklabels(['valid\nmixed', '50/50\ncollapse', 'source\npassing'], color=INK2); ax.set_title(title, loc='left', fontsize=11, color=INK)
fig.suptitle('Halvren anti-50/50 and source-passing: pairwise distance alone passes the 50/50 collapse; the bundle diagnostics catch it', x=0.01, ha='left', color=INK, fontsize=12)
fig.text(0.01, 0.01, 'DIAGNOSTIC: synthetic source centres on the Halvren slot profile (50 DIR); no Halvren face anchor exists. t = position between the two source centres per slot.', color=INK2, fontsize=9)
fig.tight_layout(rect=(0, 0.05, 1, 0.93)); fig.savefig(S + '/sheets/uf05_5_halvren_50_50.png'); plt.close(fig)
json.dump({'halvren': rows}, open(S + '/halvren_demo.json', 'w'), indent=1); print(rows)
