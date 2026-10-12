import json, copy
B = json.load(open('/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/rmot05c/specs_final.json'))
grC = B['GR']['C']; goB = B['GO']['B']
GR, GO = {}, {}
GR['C5'] = copy.deepcopy(grC); GO['B5'] = copy.deepcopy(goB)              # 05C baselines, old guard (provenance)
g = copy.deepcopy(grC); g['floor'] = 'true'; GR['C0'] = g                  # baseline, true floor
o = copy.deepcopy(goB); o['floor'] = 'true'; GO['B0'] = o
# --- Grask D1: baseline + freed girdle / pelvis / tuck-up
g = copy.deepcopy(grC); g['floor'] = 'true'
g['yoke'].update({'max_in': 4.0, 'drop': 14, 'convex': 0.5})
g['fold']['iters'] = 40
g['loft']['ops'] = [o_ for o_ in g['loft']['ops'] if not (o_['op'] == 'scale' and o_['ang'] == [157.5, 180])]
g['loft']['ops'] += [{"op": "scale", "ang": [135, 180], "r": [-0.35, 0.1], "k": 0.84},
                     {"op": "bump", "ang": [112.5, 157.5], "at": 0.13, "w": 0.07, "cm": 1.5},
                     {"op": "scale", "ang": [0, 45], "r": [0.15, 0.48], "k": 0.88},
                     {"op": "bump", "ang": [135, 180], "at": 0.42, "w": 0.14, "cm": 1.5}]
GR['D1'] = g
# --- Gorrund D1: baseline + freed posterior column + structural transitions
o = copy.deepcopy(goB); o['floor'] = 'true'; o['fold']['iters'] = 70
o['loft']['ops'] += [{"op": "line", "ang": [157.5, 180], "r": [-0.35, 0.55], "convex": 1.0, "strength": 0.8},
                     {"op": "smooth", "ang": [112.5, 180], "r": [-0.4, 0.6], "sigma": 0.15}]
for L_ in o['limbs']:
    if L_['seg'] in ('thigh', 'shank'): L_['muscles'][0]['ramp'] = 0.05; L_['tr0'] = 0.04; L_['tr1'] = 0.04
GO['D1'] = o
json.dump({'GR': GR, 'GO': GO}, open('d1.json', 'w'), indent=1)
