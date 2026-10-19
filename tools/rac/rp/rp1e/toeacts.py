import json, sys
sys.path.insert(0, '.')
from uigen import keys
o = json.load(open('toes_plan.json'))
rnd, ri, a0, a1 = map(int, sys.argv[1:5])
ms = o['rounds'][rnd]['rings'][ri]['moves'][a0:a1]
acts = []
for m in ms:
    acts += [{'action': 'left_click', 'coordinate': [int(round(m['click'][0])), int(round(m['click'][1]))]},
             {'action': 'double_click', 'coordinate': [1110, 92]}, {'action': 'wait', 'duration': 0.3}]
    for k in range(3):
        acts += [{'action': 'key', 'text': 'ctrl+a'}] + [dict(a) for a in keys(m['tgt'][k])] + [{'action': 'key', 'text': 'Tab' if k < 2 else 'Return'}]
for a in acts: a.pop('action_summary', None)
acts += [{'action': 'wait', 'duration': 0.4}, {'action': 'zoom', 'region': [1040, 86, 1180, 120], 'scale': 0.6}]
print(json.dumps(acts, separators=(',', ':')))
print('#', [(m['tube'], m['j'], m['clr'], m['click'], m['tgt']) for m in ms], file=sys.stderr)
