# RAC RM-UF-05: deterministic diagnostic batches (N 256, seeds 101 / 202 / 303 / 404). DIAGNOSTIC COVERAGE SAMPLING - NOT POPULATION FREQUENCY.
# Conditions: central (reference +-10 % of span, Subtle-like), broad (scrambled Sobol over the demonstrated valid space, reject / resample
# through validators), converge (3 prototypes + 1 % jitter: near-clone failure), mixed (50 % broad + 50 % converge), cliche (canon-prohibited
# bundle forced, other axes broad), slotcollapse (one slot collapsed to a single value). Writes scratch rmuf05/batches/*.npz + manifest.json.
import os, sys, json, numpy as np
from scipy.stats import qmc
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import uf05_spaces as SP
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/rmuf05'; os.makedirs(S + '/batches', exist_ok=True)
N = 256; SEEDS = [101, 202, 303, 404]
POP = {'SA': (SP.SAURIN, SP.axes(SP.SAURIN, drop=('iod',)), {k: (v[3] - v[1]) / (v[2] - v[1]) for k, v in SP.SAURIN.items()}),
       'SK': (SP.HUMAN, SP.axes(SP.HUMAN), {k: (SP.SK_REF[k] - v[1]) / (v[2] - v[1]) for k, v in SP.HUMAN.items()}),
       'MF': (SP.HUMAN, SP.axes(SP.HUMAN), {k: (SP.MF_REF[k] - v[1]) / (v[2] - v[1]) for k, v in SP.HUMAN.items()})}
CLICHE = {'SK': {'brow': (0.85, 1.0), 'jaw_w': (0.85, 1.0), 'jaw_drop': (0.85, 1.0), 'head_w': (0.85, 1.0)},          # mandatory heavy-brow / square-jaw "Viking face" (SKARN L48 / L154; W3C order)
          'SA': {'ros_len': (0.85, 1.0), 'ros_aw': (0.0, 0.2), 'ridge_m': (0.8, 1.0)}}                                 # dragon-like wedge head (SAURIN L752, s29)
def valid(pop, names, U):
    if pop != 'SA': return np.ones(len(U), bool)
    return SP.saurin_valid(names, SP.denorm(SP.SAURIN, names, U))
def draw(pop, cond, seed):
    space, names, ref = POP[pop]; d = len(names); rng = np.random.default_rng(seed); r0 = np.array([ref[k] for k in names]); out = []
    sob = qmc.Sobol(d, scramble=True, seed=seed)
    def broad(n):
        acc = []
        while sum(len(a) for a in acc) < n:
            u = sob.random(512); acc.append(u[valid(pop, names, u)])
        return np.concatenate(acc)[:n]
    if cond == 'broad': U = broad(N)
    elif cond == 'central':
        acc = []
        while sum(len(a) for a in acc) < N:
            u = np.clip(r0 + rng.uniform(-0.10, 0.10, (512, d)), 0, 1); acc.append(u[valid(pop, names, u)])
        U = np.concatenate(acc)[:N]
    elif cond in ('converge', 'mixed'):
        P = broad(3); acc = []
        while sum(len(a) for a in acc) < N:
            u = np.clip(P[rng.integers(0, 3, 512)] + rng.normal(0, 0.01, (512, d)), 0, 1); acc.append(u[valid(pop, names, u)])
        U = np.concatenate(acc)[:N]
        if cond == 'mixed': U = np.concatenate([U[:N // 2], broad(N)[N // 2:]])
    elif cond == 'slotcollapse':   # broad, except one UFCA slot collapsed to a single value + 1 % jitter (single-region convergence)
        U = broad(N); sl = SP.slots(space, names); tgt = 5 if pop == 'SA' else 3; m = sl == tgt
        U[:, m] = np.clip(U[0, m] + rng.normal(0, 0.01, (N, m.sum())), 0, 1)
    elif cond == 'cliche':
        acc = []
        while sum(len(a) for a in acc) < N:
            u = sob.random(512)
            for k, (a, b) in CLICHE[pop].items(): j = names.index(k); u[:, j] = a + (b - a) * rng.random(512)
            acc.append(u[valid(pop, names, u)])
        U = np.concatenate(acc)[:N]
    return U, names
if __name__ == '__main__':
    man = {}
    for pop in POP:
        for cond in ['central', 'broad', 'converge', 'mixed', 'slotcollapse'] + (['cliche'] if pop in CLICHE else []):
            for sd in SEEDS:
                U, names = draw(pop, cond, sd); f = '%s/batches/%s_%s_%d.npz' % (S, pop, cond, sd)
                np.savez(f, U=U, names=np.array(names)); man['%s_%s_%d' % (pop, cond, sd)] = dict(file=f, N=len(U), seed=sd, axes=names, label='DIAGNOSTIC COVERAGE SAMPLING - NOT POPULATION FREQUENCY')
    json.dump(man, open(S + '/manifest.json', 'w'), indent=1); print(len(man), 'batches')
