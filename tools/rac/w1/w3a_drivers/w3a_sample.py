# RAC W3A: deterministic diagnostic sample generator for RM-OT-03 (source-passing statistics) and the emulator validation builds.
# A sample = (stature h, hidden expression coordinates e over the six sources, frame coordinate phi, composition muscle / weight).
# e are TEST COORDINATES of the diagnostic generator (tail_build.t_gen: convex combination of HVC1 and the source targets on each named system),
# never genealogy percentages, lore, player controls or canon. The sampling design is a COVERAGE design (uniform over the boundary region and over
# the expression simplex, with the stratum's supporting source drawn uniformly over its full 0..1 range so the duplication corner is reached);
# it is NOT a population / prevalence model, and rates computed under it are design-conditional (order §13: population frequency not identifiable).
# Strata (H-1 / H-5; source-first: a single supporting source never carries a tail beyond its own valid adult range):
#   L-MF   lower tail, Marchfolk support            h ~ U(147, 152)  open interval   supporting source MF
#   U-SK   upper tail, Skarn support                h ~ U(213, 229)                  supporting source SK
#   U-AE   upper tail, Aelari support               h ~ U(213, 221]                  supporting source AE
#   U-SA   upper tail, combined Skarn + Aelari      h ~ U(213, 229)                  SK and AE both drawn
#   C-L-FN / VA / SG, C-U-FN / VA / SG / MF  controls: the tail stature attributed to a source that does not reach it (H-1) - classified, not built
import numpy as np
SRC = ("MF", "FN", "AE", "VA", "SK", "SG")
STRATA = {"L-MF": ((147.0, 152.0), ("MF",)), "U-SK": ((213.0, 229.0), ("SK",)), "U-AE": ((213.0, 221.0), ("AE",)), "U-SA": ((213.0, 229.0), ("SK", "AE"))}
SEED = {"L-MF": 30491, "U-SK": 30502, "U-AE": 30513, "U-SA": 30524, "VAL": 30535}
def draw(stratum, n, seed=None, frames=True):
    (lo, hi), sup = STRATA[stratum]; rng = np.random.RandomState(SEED[stratum] if seed is None else seed)
    h = lo + (hi - lo) * rng.uniform(0, 1, n)
    h = np.clip(h, lo + 0.05, hi - (0.05 if stratum != "U-AE" else 0.0))       # strictly inside the H-5 bound (AE: up to its valid maximum)
    E = np.zeros((n, len(SRC)))
    if len(sup) == 1:
        es = rng.uniform(0, 1, n); rest = rng.dirichlet(np.ones(6), n)            # rest over (HV-central, the five other sources)
        oth = [s for s in SRC if s != sup[0]]
        E[:, SRC.index(sup[0])] = es
        for i, s in enumerate(oth): E[:, SRC.index(s)] = (1 - es) * rest[:, 1 + i]
    else:
        tot = rng.uniform(0, 1, n); split = rng.uniform(0, 1, n); rest = rng.dirichlet(np.ones(5), n)
        E[:, SRC.index("SK")] = tot * split; E[:, SRC.index("AE")] = tot * (1 - split)
        oth = [s for s in SRC if s not in sup]
        for i, s in enumerate(oth): E[:, SRC.index(s)] = (1 - tot) * rest[:, 1 + i]
    phi = rng.uniform(-1, 1, n) if frames else np.zeros(n)
    m = rng.uniform(0, 1, n) if frames else np.full(n, 0.5); w = rng.uniform(0, 1, n) if frames else np.full(n, 0.5)
    return {"h": h, "E": E, "phi": phi, "muscle": m, "weight": w}
def val_set():
    """emulator validation builds (real generator): 8 L-MF, 5 U-SK, 4 U-AE, 3 U-SA at reference frame / composition; seeds SEED['VAL'] + k"""
    out = []
    for k, (st, n) in enumerate((("L-MF", 8), ("U-SK", 5), ("U-AE", 4), ("U-SA", 3))):
        d = draw(st, n, SEED["VAL"] + k, frames=False)
        for i in range(n): out.append(("V%s%d" % (st.replace("-", ""), i), st, float(round(d["h"][i], 2)), {s: float(round(d["E"][i, j], 4)) for j, s in enumerate(SRC) if d["E"][i, j] > 1e-4}))
    return out
