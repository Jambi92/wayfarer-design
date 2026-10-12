import json, copy
exec(open('mk_g.py').read().split('out = {}')[0])
def box(L, k):
    L['detail'] = 0.1
    L['ops'] += [{"op": "line", "ang": [0, 22.5], "r": [-0.05, 0.95], "convex": 0.0, "strength": 1.0},
                 {"op": "scale", "ang": [45, 45], "r": [-0.2, 0.95], "k": 1 + k, "edge": 0.08},
                 {"op": "scale", "ang": [135, 135], "r": [-0.2, 0.95], "k": 1 + k, "edge": 0.08}]
    return L
out = {}
h1 = copy.deepcopy(E['E1']); h1['limbs'] = limbs(1.0); h1['loft'] = box(trunk(E['E1'], 0), 0.05); out['H1'] = h1
h2 = copy.deepcopy(E['E1']); h2['limbs'] = limbs(2.2)
for l in h2['limbs']: l['mfade'] = 0.0
h2['loft'] = box(trunk(E['E1'], 0.04), 0.08); out['H2'] = h2
json.dump({'GO': out}, open('h.json', 'w'), indent=1)
