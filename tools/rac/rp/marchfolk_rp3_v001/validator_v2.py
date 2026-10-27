# validator_v2.py CAND.npz OUT.json [--scale-ref 173.143] : RAC §7 station validator v2 -- CLI over val2lib.evaluate() (D1 + D3 accepted 85b7c1c,
# D4 stature-normalised station geometry accepted a18371c). Every station reports the legacy verdict AND the v2 verdict with an explicit status,
# its loop count, contract minimum and margin (loops - minimum). --scale-ref 0 / absent = D4 off (D1 + D3 only).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from val2lib import evaluate
cz = np.load(sys.argv[1]); OUT = sys.argv[2]
REF = float(sys.argv[sys.argv.index('--scale-ref') + 1]) if '--scale-ref' in sys.argv else 0.0
res = evaluate(cz['V'].astype(float), np.asarray(cz['Q']), json.loads(str(cz['meta'])), REF)
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps({k: res['summary'][k] for k in ('D1_D3_firm_fail', 'margin_zero', 'firm_pass_count', 'stations')}, indent=1))
