# RAC W1m (Aelari W1 acceptance gate): central AE re-check against the CURRENT comparator set.
# Directional and skin rows: standard check scripts with the accepted Gorrund (W1i/W1j) and accepted Grask (W1l) in the GO / GR
# slots; every other body as measured (AE, FN, VA unchanged since W1g). Skeletal (CIB) rows: W1i run (AE geometry unchanged,
# sha256 880b4f0b...). Elongation-distribution table: segment shares and absolute lengths, AE vs MF-M-R / FN / VA / SG / SK.
# Usage: python3 ae_eval.py [AE_meas.json] [tag]   (default: the W1g AE) -> reviews/rac-w1m-ae-evidence/central_<tag>.json
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import directional_checks as DC, w1e_checks as WC
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
EV = R + '/reviews/rac-w1m-ae-evidence'; G = S + '/w1g'
AEM = sys.argv[1] if len(sys.argv) > 1 else G + '/cand/AE_meas.json'; TAG = sys.argv[2] if len(sys.argv) > 2 else 'W1g'
def cls(op, va, vb):
    rel = abs(va - vb) / max(abs(vb), 1e-9)
    holds = {">": va > vb, "<": va < vb}[op]
    return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
tmp = S + '/w1m/cand_' + TAG
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(G + '/cand', tmp)
shutil.copy(R + '/reviews/rac-w1i-evidence/candidates/GO_meas.json', tmp + '/GO_meas.json')
shutil.copy(S + '/w1l/probe/GRL925_1200_meas.json', tmp + '/GR_meas.json')
shutil.copy(AEM, tmp + '/AE_meas.json')
inv = lambda r: 'AE' in (r.get('cand'), r.get('b'), r.get('a'))
out = {"ae_meas": AEM, "directional": [], "skin": [r for r in WC.run(tmp) if inv(r)]}
for r in DC.run(tmp):
    if not inv(r): continue
    if r['op'] in ('>', '<'): r['result_ADG10'] = cls(r['op'], r['va'], r['vb'])
    else: r['result_ADG10'] = 'PASS' if r['pass'] else 'FAIL'
    out["directional"].append(r)
sk = json.load(open(R + '/reviews/rac-w1i-evidence/skeletal/skeletal_checks.json'))
sk = sk if isinstance(sk, list) else sk.get('rows', [])
out["skeletal_W1i"] = [r for r in sk if isinstance(r, dict) and inv(r)]
L = lambda i: json.load(open(tmp + '/%s_meas.json' % i))["combined"]
M = {i: L(i) for i in ("AE", "MF-M-R", "FN", "VA", "SG", "SK")}
keys = ["HH_share", "neck_share", "torso_share", "leg_share", "thigh_share", "shin_share", "arm_share", "hand_share", "foot_share",
        "upperarm_over_arm", "forearm_over_arm", "waist_interval_over_torso", "thorax_depth_share", "thorax_breadth_share"]
out["distribution"] = {i: {k: M[i]["ratio"].get(k) for k in keys} for i in M}
for i in M: out["distribution"][i]["stature"] = M[i]["stature"]; out["distribution"][i]["HH_cm"] = M[i]["cranio"]["HH"]; out["distribution"][i]["FVB"] = M[i]["cranio"]["FVB"]
# W1m added row (canon AE L58 / L167 "even elongation through thigh and lower leg", "not one extremely long segment"):
# lower leg / thigh ~ MF-M-R within the same +/-0.010 method tolerance the existing arm row uses (forearm / upper arm ~ MF).
# Diagnostic convention, not a canon magnitude.
sh = lambda i: M[i]["ratio"]["shin_share"] / M[i]["ratio"]["thigh_share"]
out["leg_evenness"] = {"check": "even leg elongation: lower leg / thigh ~ MF (+/-0.010; W1m row, AE L58, L167)", "AE": sh("AE"), "MF-M-R": sh("MF-M-R"),
                       "FN": sh("FN"), "VA": sh("VA"), "SG": sh("SG"), "SK": sh("SK"), "result": "PASS" if abs(sh("AE") - sh("MF-M-R")) <= 0.010 else "FAIL"}
print("leg evenness", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out["leg_evenness"].items() if k != "check"})
json.dump(out, open(EV + '/central_%s.json' % TAG, 'w'), indent=1, default=float)
bad = [(r['cand'], r['check'], r.get('result', r.get('result_ADG10'))) for k in ('skeletal_W1i', 'skin', 'directional') for r in out[k] if r.get('result', r.get('result_ADG10')) not in ('PASS', 'REPORT')]
print(TAG, {k: len(out[k]) for k in ('skeletal_W1i', 'skin', 'directional')}, 'non-PASS:', bad)
print('%-26s' % 'share' + ''.join('%10s' % i[:6] for i in M))
for k in keys + ["stature", "HH_cm", "FVB"]: print('%-26s' % k + ''.join('%10.4f' % out["distribution"][i][k] for i in M))
