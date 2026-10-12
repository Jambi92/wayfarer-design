import json, copy
d1 = json.load(open('d1.json')); GR, GO = {}, {}
g = copy.deepcopy(d1['GR']['D1'])
for o in g['loft']['ops']:
    if o['op'] == 'bump' and o['ang'] == [112.5, 157.5] and o['at'] == 0.66: o.update({'cm': 5.0, 'w': 0.2})
    if o['op'] == 'scale' and o['ang'] == [0, 45]: o['k'] = 0.82
for L_ in g['limbs']:
    for t in L_.get('tendon', []): t['k'] = min(0.5, t['k'] * 1.2)
g['trunk'] = [{"kind": "add", "r": [0.55, 0.95], "sector": [0, 14], "cm": 1.5}]
GR['D2'] = g
o = copy.deepcopy(d1['GO']['D1'])
o['loft']['ops'] += [{"op": "line", "ang": [135, 180], "r": [-0.35, 1.0], "convex": 3.0, "strength": 0.9},
                     {"op": "bump", "ang": [112.5, 157.5], "at": 0.6, "w": 0.3, "cm": 1.5},
                     {"op": "bump", "ang": [90, 157.5], "at": 1.02, "w": 0.06, "cm": 1.5}]
GO['D2'] = o
json.dump({'GR': GR, 'GO': GO}, open('d2.json', 'w'), indent=1)
