import json, copy
E = json.load(open('../../rmot05d/specs_final.json'))['GO']
def sq(t0, t1, a=1.0, ramp=0.05):   # squared section: four diagonal lobes -> flat faces anterior / lateral / posterior / medial
    return [{"kind": "plateau", "phi": p, "hw": 45, "t0": t0, "t1": t1, "ramp": ramp, "a": a} for p in (45, 135, -45, -135)]
def rnd(t0, t1, a=1.0, ramp=0.05): return [{"kind": "plateau", "phi": 0, "hw": 180, "t0": t0, "t1": t1, "ramp": ramp, "a": a}]
def limbs(k, square):
    m = sq if square else rnd
    return [
     {"seg": "shank", "j0": 0.08, "j1": 0.9, "fb": 0.88, "tr0": 0.04, "tr1": 0.04, "mfade": 0.5,
      "muscles": m(0.1, 0.52, 1.0, 0.03) + m(0.56, 0.88, 0.3, 0.03),
      "pads": [{"t": 0.02, "cm": 1.2 * k, "w": 0.05}, {"t": 0.97, "cm": 0.9 * k, "w": 0.04, "phi": 90, "hw": 70}, {"t": 0.97, "cm": 0.9 * k, "w": 0.04, "phi": -90, "hw": 70}]},
     {"seg": "thigh", "j0": 0.22, "j1": 0.9, "fb": 0.88, "tr0": 0.04, "tr1": 0.04, "muscles": m(0.2, 0.88, 1.0, 0.05),
      "pads": [{"t": 0.97, "cm": 1.2 * k, "w": 0.05}]},
     {"seg": "upperarm", "j0": 0.2, "j1": 0.9, "fb": 0.88, "tr0": 0.06, "tr1": 0.06, "muscles": rnd(0.2, 0.88, 1.0, 0.1),
      "pads": [{"t": 0.97, "cm": 0.9 * k, "w": 0.05, "phi": 180, "hw": 100}]},
     {"seg": "forearm", "j0": 0.06, "j1": 0.9, "fb": 0.88, "tr0": 0.05, "tr1": 0.05, "mfade": 0.5,
      "muscles": sq(0.08, 0.5, 1.0, 0.04) + sq(0.54, 0.88, 0.45, 0.04),
      "pads": [{"t": 0.03, "cm": 0.9 * k, "w": 0.05, "phi": 180, "hw": 100}, {"t": 0.96, "cm": 0.7 * k, "w": 0.04}]}]
def trunk(base, sq_k, post_convex, waist=True):
    L = copy.deepcopy(base['loft'])
    for o in L['ops']:
        if o['op'] == 'line' and o['ang'] == [112.5, 180]: o['convex'] = post_convex
    L['ops'] += [{"op": "scale", "ang": [45, 45], "r": [-0.3, 0.95], "k": 1 + sq_k, "edge": 0.08},
                 {"op": "scale", "ang": [135, 135], "r": [-0.3, 0.95], "k": 1 + sq_k, "edge": 0.08},
                 {"op": "scale", "ang": [90, 90], "r": [-0.3, 0.9], "k": 1 - sq_k * 0.7, "edge": 0.08}]
    if waist: L['ops'] += [{"op": "line", "ang": [67.5, 112.5], "r": [-0.25, 0.85], "convex": 0.0, "strength": 0.9}]
    return L
out = {}
f1 = copy.deepcopy(E['E1']); f1['limbs'] = limbs(1.0, False); f1['loft'] = trunk(E['E1'], 0.05, 1.5); out['F1'] = f1
f2 = copy.deepcopy(E['E1']); f2['limbs'] = limbs(1.4, True); f2['loft'] = trunk(E['E1'], 0.08, 1.0); out['F2'] = f2
json.dump({'GO': out}, open('f.json', 'w'), indent=1)
json.dump({'GO': {'E1': E['E1']}}, open('e1.json', 'w'), indent=1)
