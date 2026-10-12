import json, copy
d2 = json.load(open('d2.json')); GR, GO = {}, {}
g = copy.deepcopy(d2['GR']['D2'])
for L_ in g['limbs']:
    if L_['seg'] == 'thigh':
        L_['muscles'][0].update({'tp': 0.42, 't1': 0.72, 'hw': 110}); L_['muscles'][1].update({'tp': 0.38})
GR['D3'] = g
o = copy.deepcopy(d2['GO']['D2'])
for op in o['loft']['ops']:
    if op['op'] == 'line' and op['ang'] == [135, 180]: op['ang'] = [112.5, 180]
    if op['op'] == 'bump' and op['at'] == 0.6: op['ang'] = [112.5, 180]
o['loft']['smooth'] = 12
GO['D3'] = o
json.dump({'GR': GR, 'GO': GO}, open('d3.json', 'w'), indent=1)
