# cg_toe_diag.py OUT.json FAM.npz [FAM...] (copy of pipkin_rp4_v001/toe_station_diag.py with an output path) : DIAGNOSTIC ONLY (the authoritative validator is not changed). Re-evaluates the toe joint stations with the toe-length
# term of the probe radius NOT double-scaled: core3lib builds rr = 0.5 |JC(j+1) - JC(j)| + 0.6 cm from the body's own (already stature-sized) joint spacing, and
# D4 then multiplies rr by s = stature / 173.143 again. Here the joint-spacing term is taken in reference units (divided by s before D4 scales it), i.e. the
# probe has the same size relative to the body as on Marchfolk 173. Everything else (W, D1 / D3 / D5) is exactly val2lib.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
import core3lib, val2lib
_orig = core3lib.stations
def make(scale):
    def st(meta):
        S = _orig(meta); out = []
        for nm, c, d, Wd, Rr, need, Rp in S:
            if nm.startswith('toe') and Rp is not None:
                rr = Rp / 1.15; L = (rr - 0.6) * 2; rr2 = 0.5 * L / scale + 0.6; out.append((nm, c, d, Wd, rr2 * 1.3, need, 1.15 * rr2))
            else: out.append((nm, c, d, Wd, Rr, need, Rp))
        return out
    return st
res = {}
OUT = sys.argv[1]
for p in sys.argv[2:]:
    z = np.load(p); V = z['V'].astype(float); Q = np.asarray(z['Q']); meta = json.loads(str(z['meta'])); s = (V[:, 2].max() - V[:, 2].min()) / 173.143
    names = [n[0] for n in _orig(meta) if n[0].startswith('toe')]
    a = val2lib.evaluate(V, Q, meta, ref_stature=173.143, names=names, d5=True)
    val2lib.stations = make(s); b = val2lib.evaluate(V, Q, meta, ref_stature=173.143, names=names, d5=True); val2lib.stations = _orig
    fa = sorted(k for k, v in a['stations'].items() if not v['firm_D1_D3']); fb = sorted(k for k, v in b['stations'].items() if not v['firm_D1_D3'])
    res[p.split('/')[-1]] = dict(s=round(s, 4), toe_stations=len(names), authoritative_fail=fa, diagnostic_unscaled_toe_term_fail=fb)
    print(p.split('/')[-1], json.dumps(res[p.split('/')[-1]]))
json.dump(res, open(OUT, 'w'), indent=1)
