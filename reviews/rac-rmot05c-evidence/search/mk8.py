import json, copy
def grlimbs(k):   # k = tendon strength scale
    return [
  {"seg": "shank", "j0": 0.1, "j1": 0.92, "fb": 0.95, "tr0": 0.08, "tr1": 0.1, "muscles": [
     {"phi": 180, "hw": 100, "t0": 0.1, "tp": 0.22, "t1": 0.44, "a": 1.0}, {"phi": 30, "hw": 70, "t0": 0.1, "tp": 0.2, "t1": 0.46, "a": 0.5}],
   "tendon": [{"t0": 0.48, "t1": 0.92, "k": 0.38 * k}]},
  {"seg": "thigh", "j0": 0.22, "j1": 0.9, "fb": 0.95, "tr0": 0.12, "tr1": 0.1, "muscles": [
     {"phi": 0, "hw": 100, "t0": 0.22, "tp": 0.36, "t1": 0.66, "a": 1.0}, {"phi": 180, "hw": 90, "t0": 0.22, "tp": 0.34, "t1": 0.6, "a": 0.9}],
   "tendon": [{"t0": 0.7, "t1": 0.9, "k": 0.2 * k}]},
  {"seg": "upperarm", "j0": 0.2, "j1": 0.88, "fb": 0.95, "tr0": 0.08, "tr1": 0.1, "muscles": [
     {"phi": 0, "hw": 90, "t0": 0.2, "tp": 0.32, "t1": 0.6, "a": 1.0}, {"phi": 180, "hw": 90, "t0": 0.2, "tp": 0.3, "t1": 0.58, "a": 1.0}],
   "tendon": [{"t0": 0.66, "t1": 0.88, "k": 0.15 * k}]},
  {"seg": "forearm", "j0": 0.08, "j1": 0.92, "fb": 0.95, "tr0": 0.06, "tr1": 0.1, "muscles": [
     {"phi": 0, "hw": 180, "t0": 0.06, "tp": 0.18, "t1": 0.42, "a": 1.0}],
   "tendon": [{"t0": 0.48, "t1": 0.92, "k": 0.35 * k}]}]
chest = {"op": "smooth", "ang": [0, 67.5], "r": [0.55, 1.02], "sigma": 0.08}
glute = [{"op": "bump", "ang": [157.5, 180], "at": 0.26, "w": 0.08, "cm": 1.2}, {"op": "scale", "ang": [135, 180], "r": [-0.08, 0.12], "k": 0.9}]
def wing(cm): return [{"op": "bump", "ang": [112.5, 157.5], "at": 0.7, "w": 0.12, "cm": cm}, {"op": "bump", "ang": [90, 112.5], "at": 0.66, "w": 0.1, "cm": cm / 2}]
GR = {
 "A": {"smooth": 6, "limbs": grlimbs(0.5), "loft": {"taubin": 30, "detail": 0.2, "ops": [chest] + glute}},
 "B": {"smooth": 6, "limbs": grlimbs(0.8), "loft": {"taubin": 40, "detail": 0.1, "ops": [chest] + glute + wing(2.5)}, "yoke": {"drop": 14, "xn": 9, "convex": 1.0, "max_in": 2.0}},
 "C": {"smooth": 6, "limbs": grlimbs(1.0), "loft": {"taubin": 40, "detail": 0.1, "ops": [chest] + glute + wing(4.0)}, "yoke": {"drop": 14, "xn": 9, "convex": 1.0, "max_in": 2.5},
       "trunk": [{"kind": "add", "r": [0.55, 0.95], "sector": [0, 14], "cm": 1.0}]}}
def golimbs(j1, tr1, ridge):
    L = []
    for seg, j0, t0 in (("shank", 0.08, 0.1), ("thigh", 0.22, 0.2), ("upperarm", 0.2, 0.2), ("forearm", 0.06, 0.05)):
        m = [{"kind": "plateau", "phi": 0, "hw": 180, "t0": t0, "t1": j1 - 0.02, "ramp": 0.1, "a": 1.0}]
        if ridge and seg in ("shank", "thigh"): m.append({"kind": "plateau", "phi": 90, "hw": 30, "t0": t0, "t1": j1 - 0.04, "ramp": 0.1, "a": 0.35})
        L.append({"seg": seg, "j0": j0, "j1": j1, "fb": 0.88, "tr0": 0.06, "tr1": tr1, "muscles": m})
    return L
goloft = {"taubin": 40, "detail": 0.1, "ops": [
  {"op": "line", "ang": [0, 22.5], "r": [0.05, 0.6], "convex": 0.6},
  {"op": "hull", "ang": [45, 180], "r": [-0.05, 0.85]},
  {"op": "smooth", "ang": [0, 67.5], "r": [0.55, 1.02], "sigma": 0.1},
  {"op": "smooth", "ang": [135, 180], "r": [-0.08, 0.6], "sigma": 0.1}]}
goloftC = copy.deepcopy(goloft); goloftC["ops"].append({"op": "bump", "ang": [112.5, 180], "at": 0.95, "w": 0.08, "cm": 2.0})
GO = {
 "A": {"smooth": 6, "loft": goloft, "fold": {"r": [-0.45, 0.12], "strength": 0.7}},
 "B": {"smooth": 6, "limbs": golimbs(0.9, 0.06, False), "loft": goloft, "fold": {"r": [-0.45, 0.12]}},
 "C": {"smooth": 6, "limbs": golimbs(0.96, 0.03, True), "loft": goloftC, "fold": {"r": [-0.45, 0.12]}}}
json.dump({"GR": GR, "GO": GO}, open("s8.json", "w"), indent=1)
