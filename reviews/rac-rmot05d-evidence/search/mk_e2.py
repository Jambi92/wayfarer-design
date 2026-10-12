import json, copy
e1 = json.load(open('e1.json'))
g = copy.deepcopy(e1['GR']['E1'])
for o in g['loft']['ops']:
    if o['op'] == 'bump' and o['ang'] == [112.5, 157.5] and o['at'] == 0.66: o.update({'cm': 6.0})
    if o['op'] == 'scale' and o['ang'] == [0, 45]: o['k'] = 0.78
g['loft']['ops'] += [{"op": "bump", "ang": [146, 170], "at": 0.45, "w": 0.3, "cm": 2.0}]   # paraspinal columns (157.5 deg only: midline groove)
for L_ in g['limbs']:
    for t in L_.get('tendon', []): t['k'] = min(0.55, t['k'] * 1.25)
g['trunk'] = [{"kind": "add", "r": [0.5, 0.95], "sector": [0, 14], "cm": 2.5}]
o = copy.deepcopy(e1['GO']['E1'])
for op in o['loft']['ops']:
    if op['op'] == 'line' and op['ang'] == [112.5, 180]: op['convex'] = 5.0
o['loft']['ops'] += [{"op": "bump", "ang": [112.5, 180], "at": 0.78, "w": 0.18, "cm": 2.5}]
json.dump({'GR': {'E2': g}, 'GO': {'E2': o}}, open('e2.json', 'w'), indent=1)
