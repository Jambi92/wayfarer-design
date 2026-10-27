# validator_v2.py CAND.npz OUT.json [--scale-ref 173.143] [--d5] [--d6-native NATIVE.npz] : RAC §7 station validator v2 -- CLI over val2lib.evaluate() (D1 + D3 accepted 85b7c1c,
# D4 stature-normalised station geometry accepted a18371c, D5 interdigital endpoint validity accepted 33a2dfe).
# D6 foreign-segment endpoint ownership accepted d921903 (needs the race's native hm08 source for skin weights).
# AUTHORITATIVE MPFB-family verdict (d921903): --scale-ref 173.143 --d5 --d6-native src/<ID>_native.npz (D1 + D3 + D4 + D5 + D6). Every station reports the legacy verdict AND the v2 verdict with an explicit status,
# its loop count, contract minimum and margin (loops - minimum). --scale-ref 0 / absent = D4 off (D1 + D3 only).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from val2lib import evaluate
cz = np.load(sys.argv[1]); OUT = sys.argv[2]
REF = float(sys.argv[sys.argv.index('--scale-ref') + 1]) if '--scale-ref' in sys.argv else 0.0
D6 = None
if '--d6-native' in sys.argv:   # D6 (accepted d921903): skin weights of the native hm08 source carried through the family map
    import scipy.sparse as sp
    nz = np.load(sys.argv[sys.argv.index('--d6-native') + 1]); Mf = sp.csr_matrix((cz['M_data'], cz['M_indices'], cz['M_indptr']), shape=tuple(cz['M_shape']))
    assert np.array_equal(nz['src_index'], cz['src_index']); D6 = (np.asarray(Mf @ nz['W']), [str(b) for b in nz['bones']])
res = evaluate(cz['V'].astype(float), np.asarray(cz['Q']), json.loads(str(cz['meta'])), REF, d5='--d5' in sys.argv, d6=D6)
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps({k: res['summary'][k] for k in ('D1_D3_firm_fail', 'margin_zero', 'firm_pass_count', 'stations')}, indent=1))
