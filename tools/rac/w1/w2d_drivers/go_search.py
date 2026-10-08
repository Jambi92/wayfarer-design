# RAC W2D limb-present Gorrund search (AD-3): proportion probes (go_body.quick at the 218 cm height macro) scored on the canonical
# Gorrund directional and skin rows (directional_checks / w1e_checks with the probe in the GO slot; accepted comparators), and their
# relative limb contribution compared with the shortest-limbed valid Grask GR-BODY-10 (218 cm, accepted W2C). Writes OUT.json.
# Usage: python3 go_search.py OUT.json NAME[@MACRO]='{targets}' ...
import sys, os, json, shutil
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import go_body as GB, directional_checks as DC, w1e_checks as WC
G10 = json.load(open(S + '/w2c/b/GR-BODY-10/GR-BODY-10_meas.json'))["combined"]["ratio"]
def ev(name, d):
    tmp = S + '/w2d/cand_' + name
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(GB.G + '/cand', tmp); shutil.copy(d + '/%s_meas.json' % name, tmp + '/GO_meas.json')
    rows = []
    for r in DC.run(tmp) + WC.run(tmp):
        if 'GO' not in (r.get('cand'), r.get('a'), r.get('b')): continue
        op = r.get('op'); va, vb = r.get('va'), r.get('vb')
        if op in ('>', '<') and va is not None and vb:
            rel = abs(va - vb) / abs(vb); holds = va > vb if op == '>' else va < vb; res = ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
        else: res = r.get('result') or ("PASS" if r.get('pass') else "FAIL")
        rows.append({"check": r["check"], "cand": r.get("cand"), "op": op, "va": va, "vb": vb, "result": res})
    return rows
if __name__ == '__main__':
    out = json.load(open(sys.argv[1])) if os.path.exists(sys.argv[1]) else {}
    for a in sys.argv[2:]:
        nm, tg = a.split('=', 1); tg = json.loads(tg); m = 0.7503
        if '@' in nm: nm, m = nm.split('@'); m = float(m)
        c = GB.quick(nm, m, None, tg); rows = ev(nm, GB.W + '/q/' + nm); r = c["ratio"]
        lim = {k: 100 * (r[k] / G10[k] - 1) for k in ("leg_share", "arm_share", "span_der", "torso_share")}
        out[nm] = {"targets": tg, "stature": c["stature"], "ratio": {k: r.get(k) for k in ("torso_share", "leg_share", "arm_share", "span_der", "forearm_over_arm", "shin_over_leg", "thorax_depth_share", "thorax_breadth_share", "shoulder_joint_share")},
                   "vs_GR_BODY_10_pct": lim, "rows": rows, "non_pass": [(x["check"], x["result"]) for x in rows if x["result"] not in ("PASS", "REPORT", None)]}
        json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
        print(nm, round(c["stature"], 2), "torso %.4f leg %.4f arm %.4f span %.4f" % (r["torso_share"], r["leg_share"], r["arm_share"], r["span_der"]),
              "| vs GR-10 leg %+.1f%% arm %+.1f%% span %+.1f%%" % (lim["leg_share"], lim["arm_share"], lim["span_der"]), "| non-pass", out[nm]["non_pass"], flush=True)
