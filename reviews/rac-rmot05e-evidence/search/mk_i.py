import json, copy
H = json.load(open('h.json'))['GO']
out = {}
for nm, base, tv, sv, uv, fv in (('I1', 'H1', 0.85, 1.25, 0.9, 1.2), ('I2', 'H2', 0.75, 1.45, 0.8, 1.35)):
    s = copy.deepcopy(H[base])
    for l in s['limbs']:
        l['vol'] = {'thigh': tv, 'shank': sv, 'upperarm': uv, 'forearm': fv}[l['seg']]
    out[nm] = s
json.dump({'GO': out}, open('i.json', 'w'), indent=1)
