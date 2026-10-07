# RAC W1i: Gorrund at the canonical minimum stature. GOR-BODY-02 uses the W1f 208 cm donor (height macro 0.7019), but the W1i skeleton
# adds height (210.8 cm). This builds a donor at a lower height macro so the W1i GO skeleton lands at ~208 cm (order §4: test 208 cm;
# do not narrow the range), then reads it like the other stature bodies: ALPC-0...4 (ordinary rule), ALPC-7 vs Broad Skarn 208 / 215 /
# 222 / 229 cm, arm tests, flank flare, continuity. Usage: python3 true208.py params.json height_macro out.json
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gn6, gn3, sens6, alpc_invariance as AI, profile_bump as PB, arm_clearance as AC
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1h_drivers'); import rebuild as RB
G, F, T = gn3.G, gn3.F, gn3.T

def main(pfile, macro, out):
    x = json.load(open(pfile))["x"]; macro = float(macro); n = "GO0M208"
    gi = json.load(open(F + '/base_w1c/GO_build.json')); d = dict(gi); d["height_macro"] = macro; d["id"] = n
    json.dump(d, open(G + '/h/%s_src.json' % n, 'w'))
    RB.par([(G + '/h/%s_src.json' % n, {}, G + '/h', n)]); RB.par([(G + '/h/%s_build.json' % n, RB.LEANOV, G + '/h', n + '-LEAN')])
    RB.par([(G + '/h/%s_build.json' % n, {"muscle": m, "weight": w}, G + '/donor', '%s-%s' % (n, RB.tag(m, w))) for m, w in RB.GRID])
    for st in ("rest", "r6"):
        p = G + '/donor/%s-C050050_%s.npz' % (n, st)
        if not os.path.lexists(p): os.symlink(G + '/h/%s_%s.npz' % (n, st), p)
    B, sc = gn6.unpack(x); wd = G + '/true208'; nm = 'GO-H208'
    r, C = gn3.build("GO", nm, B, sc, wd=wd, base=G + '/h/%s_build.json' % n, donor=G + '/h/' + n, did=n)
    res = {"height_macro": macro, "stature": r['r6']['stature'],
           "not_pass_ALPC_0_4": sens6.bad(gn3.checks("GO", nm, wd=wd), keep=lambda y: AI.keep_row(y['check'])),
           "flank_flare": PB.flank_flare(wd + '/%s_r6.npz' % nm)['flank_flare'], "arm_clearance_cm": AC.signed_clearance(wd + '/%s_r6.npz' % nm),
           "arm_tube": AC.arm_tube_test(wd + '/%s_r6.npz' % nm), "continuity_skin": gn6.cont(wd + '/%s_rest.npz' % nm), "continuity_skeleton": gn6.cont(wd + '/%s-LEAN_rest.npz' % nm)}
    for hs in (208, 215, 222, 229):
        rows = gn6.pair_rows(wd, nm, hs); res["ALPC-7 vs SKB%d" % hs] = {"not_pass": sens6.bad(rows), "n": len(rows),
              "rows": [{k: y[k] for k in ("check", "result", "op", "by_t")} for y in rows]}
    json.dump(res, open(out, 'w'), indent=1, default=float); print(json.dumps({k: v for k, v in res.items() if k not in ("arm_tube",)}, default=float)[:1500])

if __name__ == "__main__":
    main(*sys.argv[1:4])
