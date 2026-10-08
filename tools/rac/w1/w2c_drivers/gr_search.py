# RAC W2C named-extreme search: proportion probes (gr_body.quick, stature re-solved to 218 cm) scored on the canonical Grask directional
# and skin rows (gr_eval.evaluate without skeleton). Prints each probe's non-PASS rows and thinnest margin; writes OUT.json.
# Usage: python3 gr_search.py OUT.json NAME[@STATURE]='{targets}' ...
import sys, os, json
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
os.environ.setdefault('SKPBASE', S + '/s7n/w1i_base'); os.environ.setdefault('EVDIR', S + '/w2c/ev')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1k_drivers')
import gr_body as GB, gr_eval as GE
out = json.load(open(sys.argv[1])) if os.path.exists(sys.argv[1]) else {}
for a in sys.argv[2:]:
    nm, tg = a.split('=', 1); tg = json.loads(tg); H = '218'
    if '@' in nm: nm, H = nm.split('@')
    c = GB.quick(nm, H, None, tg)
    res = GE.evaluate(nm, GB.W + '/q/' + nm, False)
    rows = []
    for r in res["directional"] + res["skin"]:
        rs = r.get("result_ADG10") or r.get("result")
        if r.get("op") in (">", "<") and r.get("va") is not None: m = 100 * (abs(r["va"] - r["vb"]) / abs(r["vb"])) * (1 if rs == "PASS" else -1)
        else: m = None
        rows.append({"check": r["check"], "cand": r.get("cand"), "result": rs, "margin": m, "va": r.get("va"), "vb": r.get("vb")})
    gr = [x for x in rows if x["margin"] is not None and x["cand"] == "GR"]
    thin = min(gr, key=lambda x: x["margin"])
    out[nm] = {"targets": tg, "stature": c["stature"], "ratio": {k: c["ratio"].get(k) for k in ("torso_share", "leg_share", "arm_share", "span_der", "upperarm_over_arm", "forearm_over_arm", "shin_over_leg", "hand_share", "finger_over_palm", "neck_share", "HH_share")},
               "rows": rows, "non_pass": [(x["check"], x["result"]) for x in rows if x["result"] not in ("PASS", "REPORT", None)], "thinnest": (thin["check"], thin["margin"])}
    json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
    r = out[nm]["ratio"]; print(nm, round(c["stature"], 2), "torso %.4f leg %.4f arm %.4f span %.4f fa/arm %.4f shin/leg %.4f hand %.4f" % (r["torso_share"], r["leg_share"], r["arm_share"], r["span_der"], r["forearm_over_arm"], r["shin_over_leg"], r["hand_share"]),
          "| thinnest %s %+.2f%%" % (thin["check"][:40], thin["margin"]), "| non-pass", out[nm]["non_pass"], flush=True)
