# RAC W2H (short-race family) body registry: the accepted W1 references (Durrim DU-NAT 137, Pipkin PK-NAT 107, Cogling CGJ7 91; unchanged), the
# W2H stature families / frames / composition / named bodies (w2h_drivers/sr_build.py; grids by w2a_drivers/mfm_grid.py), the DU-P4 composition
# bodies, the generator human-child proxies (diagnostic only), and the comparators: real matched-height Marchfolk / Sagekin at 152 cm only (W1t / W2E),
# Marchfolk 173 (MF-M-R) as the NORMALIZED comparator for Pipkin / Cogling / Durrim proportions, Fenn FNL4 and Grask GR218R (normalized).
# Usage: python3 w2h_reg.py OUT.json
import sys, json, os, glob
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2h'; N = S + '/s7n'
R = {}
def add(name, meas, grid, race=None, joint=None, skp_id="MF-M-R"):
    R[name] = {"meas": meas, "skp": grid, "skp_id": skp_id, "joint": joint or os.path.basename(meas), "race": race}
G = lambda n: W + '/g/%s/skp' % n
# references and families (all native short-adult route)
add("DU137", S + '/w1f/final/DU-NAT', G("DU-NAT"), "DU", "DU-NAT"); add("PK107", S + '/w1f/final/PK-NAT', G("PK-NAT"), "PK", "PK-NAT")
add("CG91", S + '/w1r/probe/CGJ7', G("CGJ7"), "CG", "CGJ7")
for n, race in (("DU122", "DU"), ("DU152", "DU"), ("PK91", "PK"), ("PK122", "PK"), ("CG76", "CG"), ("CG107", "CG")):
    add(n, W + '/st/%s-NAT' % n, G(n + "-NAT"), race, n + "-NAT")
for n in ("DU137R", "PK107R", "CG91R"): add(n, W + '/st/%s-NAT' % n, None, None, n + "-NAT")      # route reproduction checks
for p in sorted(glob.glob(W + '/fr/*_build.json')):
    n = os.path.basename(p)[:-11]; add(n, W + '/fr/' + n, G(n), n[:2], n)
# composition at the references (same skeleton -> reference grid)
for p in sorted(glob.glob(W + '/comp/*_build.json')):
    n = os.path.basename(p)[:-11]; ref = {"DU": "DU137", "PK": "PK107", "CG": "CG91"}[n[:2]]; add(n, W + '/comp/' + n, R[ref]["skp"], n[:2], n)
# named: composition on frame skeletons; COG-12 / -13 own skeletons
for n, sk, race in (("COG04", "CGN91", "CG"), ("COG05", "CGB91", "CG"), ("PKBHM", "PKB107", "PK"), ("DUNLOW", "DUN137", "DU")):
    add(n, W + '/nm/' + n, G(sk), race, n)
for n in ("COG12", "COG13"): add(n, W + '/nm/%s-NAT' % n, G(n + "-NAT"), "CG", n + "-NAT")
# DU-P4 composition bodies at 152 cm (skeleton of DU152 / MF152)
for c in ("LOW", "MIN", "HIBOTH"):
    add("DU152-" + c, W + '/p4/DU152-' + c, G("DU152-NAT"), "DU", "DU152-" + c)
    add("MF152-" + c, W + '/p4/MF152-' + c, G("MF152-NAT"), None, "MF152-" + c)
# DU-P4 diagnostic probes (NOT applied): W1t pelvis Z x1.04 / x1.06 at 152 cm (w2h_drivers/p4_probe.py)
for n in ("DU152P4", "DU152P6"): add(n, S + '/w1t/bnd/%s-NAT' % n, G(n + "-NAT"), None, n + "-NAT")
# comparators
E = S + '/w2e'
add("MF152", S + '/w1t/bnd/MF152-NAT', G("MF152-NAT"), None, "W1T-MF152-NAT")          # re-gridded on the W2 method (like-for-like with DU152)
add("MF152s7n", S + '/w1t/bnd/MF152-NAT', N + '/w1t_g152mf', None, "W1T-MF152-NAT")     # W1t S7-normalized grid (cross-check)
add("SG152", E + '/st/SG152-NAT', E + '/g/SG152-NAT/skp', None, "SG152-NAT")
add("MF173", S + '/w1f/final/MF-M-R', N + '/w1i_base', None, "MF-M-R")
for c in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH", "LOW", "MIN"):
    e = json.load(open('/home/claude/wayfarer-design/reviews/rac-w2f-elf-evidence/closure/registry_closure.json'))["MF-" + c]; e = dict(e); e.pop("race", None)
    e["joint"] = os.path.basename(e["meas"]); R["MF173-" + c] = e      # exact-plane sections: w2h j_joints_mfc.json
for k in ("MFB173", "MFN173"):     # accepted Marchfolk W2A1 frames (frame-matched normalized comparators)
    e = dict(json.load(open('/home/claude/wayfarer-design/reviews/rac-w2e-sg-evidence/registry.json'))[k]); e.pop("race", None); R[k] = e
add("FN181", S + '/w1p/cand/FNL4', N + '/w1p_fnl4', None, "FNL4", skp_id="FN")
add("GR218", S + '/w2c/b/GR218R/GR218R', S + '/w2c/b/GR218R/skp_GR218R', None, "GR218R", skp_id="GR218R")
# generator human-child proxies (diagnostic only; never a race baseline)
for n, d in (("CHILD1", W + '/child/CHILD1'), ("CHILD3", S + '/w1r/child/CHILD3'), ("CHILD6", S + '/w1q/child/CHILD6'), ("CHILD9", S + '/w1t/child/CHILD9')):
    add(n, d, None, None, n)
json.dump(R, open(sys.argv[1], 'w'), indent=1); print(len(R), "bodies")
