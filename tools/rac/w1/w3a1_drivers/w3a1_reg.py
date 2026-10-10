# RAC W3A1 body registry: the W3A registry (reviews/rac-w3a-hv-evidence/registry.json: W2G + W3A bodies) + every W3A1 body (w3a1_build.py) with
# its skeletal-proxy grid where one was run; the W3A lower-tail samples re-gridded in W3A1 (AD-W3A-4 re-evaluation) get their new grid.
# Coupled endpoint bodies listed in G carry race 'HV' (accepted W1 Halvren rows; fixed W1 references = report-level).   Usage: python3 w3a1_reg.py OUT.json
import sys, os, glob, json
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w3a1'
R = json.load(open('/home/claude/wayfarer-design/reviews/rac-w3a-hv-evidence/registry.json'))
for e in R.values(): e.pop("race", None)
G = {"HU228p8Sc", "HU221Ac", "HU228p8SAc"}
def grid(n): g = W + '/g/%s/skp' % n; return g if os.path.exists(g + '/t1.0/MF-M-R_meas.json') else None
for d in ('up', 'ks', 'src', 'fr', 'comp', 'rsup', 'cen'):
    for p in sorted(glob.glob('%s/%s/*_build.json' % (W, d))):
        nid = os.path.basename(p)[:-11]; n = nid.replace('-NAT', '')
        R[n] = {"meas": '%s/%s/%s' % (W, d, nid), "skp": grid(n), "skp_id": "MF-M-R", "joint": nid, "race": "HV" if n in G else None}
for n, e in R.items():
    if n.startswith(("RLMF", "VLMF")) and grid(n): e["skp"] = grid(n)
json.dump(R, open(sys.argv[1], 'w'), indent=1); print(len(R), "bodies")
