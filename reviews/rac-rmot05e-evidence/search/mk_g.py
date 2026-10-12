import json, copy
E = json.load(open('../../rmot05d/specs_final.json'))['GO']
def pl(t0, t1, a=1.0, ramp=0.05, phi=0, hw=180): return {"kind": "plateau", "phi": phi, "hw": hw, "t0": t0, "t1": t1, "ramp": ramp, "a": a}
def limbs(k):
    return [
     {"seg": "shank", "j0": 0.08, "j1": 0.92, "fb": 0.88, "tr0": 0.04, "tr1": 0.03, "mfade": 0.3,
      "muscles": [pl(0.1, 0.5, 0.45, 0.06), pl(0.42, 0.9, 1.0, 0.12)],
      "pads": [{"t": 0.02, "cm": 1.6 * k, "w": 0.05}, {"t": 0.95, "cm": 1.8 * k, "w": 0.05}]},
     {"seg": "thigh", "j0": 0.22, "j1": 0.9, "fb": 0.88, "tr0": 0.04, "tr1": 0.04, "muscles": [pl(0.2, 0.88, 1.0, 0.05)],
      "pads": [{"t": 0.97, "cm": 1.8 * k, "w": 0.05}]},
     {"seg": "upperarm", "j0": 0.2, "j1": 0.9, "fb": 0.88, "tr0": 0.06, "tr1": 0.06, "muscles": [pl(0.2, 0.88, 1.0, 0.1)],
      "pads": [{"t": 0.97, "cm": 1.2 * k, "w": 0.05, "phi": 180, "hw": 110}]},
     {"seg": "forearm", "j0": 0.06, "j1": 0.92, "fb": 0.88, "tr0": 0.05, "tr1": 0.03, "mfade": 0.3,
      "muscles": [pl(0.06, 0.5, 0.5, 0.06), pl(0.42, 0.9, 1.0, 0.12)],
      "pads": [{"t": 0.03, "cm": 1.2 * k, "w": 0.05, "phi": 180, "hw": 110}, {"t": 0.95, "cm": 1.3 * k, "w": 0.045}]}]
def trunk(base, aframe):
    L = copy.deepcopy(base['loft'])
    for o in L['ops']:
        if o['op'] == 'line' and o['ang'] == [112.5, 180]: o['convex'] = 0.5
    L['ops'] += [{"op": "line", "ang": [67.5, 112.5], "r": [-0.15, 0.8], "convex": 0.0, "strength": 1.0},
                 {"op": "line", "ang": [135, 180], "r": [-0.3, 0.92], "convex": 0.5, "strength": 0.9}]
    if aframe: L['ops'] += [{"op": "scale", "ang": [67.5, 157.5], "r": [0.5, 0.85], "k": 1 - aframe, "edge": 0.12},
                            {"op": "scale", "ang": [67.5, 157.5], "r": [-0.15, 0.35], "k": 1 + aframe, "edge": 0.12}]
    return L
out = {}
g1 = copy.deepcopy(E['E1']); g1['limbs'] = limbs(1.0); g1['loft'] = trunk(E['E1'], 0); out['G1'] = g1
g2 = copy.deepcopy(E['E1']); g2['limbs'] = limbs(1.4); g2['loft'] = trunk(E['E1'], 0.05); out['G2'] = g2
out['E1'] = E['E1']
json.dump({'GO': out}, open('g.json', 'w'), indent=1)
