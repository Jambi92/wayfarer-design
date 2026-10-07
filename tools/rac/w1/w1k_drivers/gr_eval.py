# RAC W1k Grask gate evaluation. For each body: skeletal (CIB) rows via gn3.checks where the body has its own skeleton
# (central / s01 / frames), directional and skin rows via the standard check scripts with this body's measurements in the GR slot
# and the ACCEPTED Gorrund (W1i/W1j retained point) in the GO slot. Writes reviews/rac-w1k-gr-evidence/eval.json.
# Usage: python3 gr_eval.py name=dir[:skel] ...   (skel = has its own skp_<name>; otherwise skeletal rows = the candidate's)
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1g_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn3, directional_checks as DC, w1e_checks as WC
R = '/home/claude/wayfarer-design'; EV = R + '/reviews/rac-w1k-gr-evidence'; os.makedirs(EV, exist_ok=True)
GO_ACC = R + '/reviews/rac-w1i-evidence/candidates/GO_meas.json'
def cls(op, va, vb):
    if va is None or vb is None: return "NOT RUN"
    rel = abs(va - vb) / max(abs(vb), 1e-9)
    holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}.get(op)
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    if op in (">=", "<="): return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
    return None
def evaluate(name, d, skel):
    tmp = gn3.S + '/w1k/cand_' + name
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(gn3.G + '/cand', tmp); shutil.copy(GO_ACC, tmp + '/GO_meas.json'); shutil.copy(d + '/%s_meas.json' % name, tmp + '/GR_meas.json')
    out = {"dir": d}
    dr = [r for r in DC.run(tmp) if 'GR' in (r.get('cand'), r.get('b'), r.get('a'))]
    for r in dr:
        o = r['op']; r['result_ADG10'] = cls(o, r['va'], r['vb']) if o in ('>', '<') else ("PASS" if r['pass'] else "FAIL")
    out["directional"] = dr
    out["skin"] = [r for r in WC.run(tmp) if 'GR' in (r.get('cand'), r.get('b'))]
    if skel:
        rows = gn3.checks('GR', name, wd=d)
        out["skeletal"] = [r for r in rows if r.get('cand') == 'GR' or r.get('b') == 'GR']
    m = json.load(open(d + '/%s_meas.json' % name))
    out["stature"] = m.get("stature_r6")
    return out
if __name__ == '__main__':
    p = EV + '/eval.json'; res = json.load(open(p)) if os.path.exists(p) else {}
    for a in sys.argv[1:]:
        nm, rest = a.split('=', 1); skel = rest.endswith(':skel'); d = rest[:-5] if skel else rest
        res[nm] = evaluate(nm, d, skel); json.dump(res, open(p, 'w'), indent=1, default=float)
        bad = [(x.get('check'), x.get('result', x.get('result_ADG10'))) for k in ('skeletal', 'skin', 'directional') for x in res[nm].get(k, [])
               if x.get('result', x.get('result_ADG10')) not in ('PASS', 'REPORT', None)]
        print(nm, res[nm]['stature'], 'non-PASS:', bad, flush=True)
