import json, sys
a = json.load(open(sys.argv[1])); r0, r1 = int(sys.argv[2]), int(sys.argv[3]); skip = int(sys.argv[4]) if len(sys.argv) > 4 else 0
idx = [i for i, x in enumerate(a) if x.get('text') == 'e'] + [len(a)]
out = []
for r in range(r0, r1):
    seg = a[idx[r]:idx[r + 1]]
    if r == r0: seg = seg[skip:]
    out += seg + [{'action': 'zoom', 'region': [1040, 56, 1180, 135], 'scale': 0.4}]
print(json.dumps(out, separators=(',', ':')))
