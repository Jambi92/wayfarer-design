# RAC W3A body registry: the accepted W2G Halvren registry (reviews/rac-w2g-hv-evidence/registry.json: W2G Halvren family, frames, expressions,
# composition, stress, accepted W2 source families) + Marchfolk 147 (W2A configuration 1, native) + every W3A body (tail_build.py), with its
# skeletal-proxy grid where one was run. Tail endpoint bodies listed in G carry race 'HV' (accepted W1 Halvren rows; fixed W1 references = report-level).
# Usage: python3 w3a_reg.py OUT.json
import sys, os, glob, json
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w3a'
R = json.load(open('/home/claude/wayfarer-design/reviews/rac-w2g-hv-evidence/registry.json'))
for e in R.values(): e.pop("race", None)        # the W2G G rows are accepted W2G results; W3A runs the G rows only for its own tail endpoints
R["MF147"] = {"meas": S + '/w2a/st/MFM147-NAT', "skp": S + '/w2a/g/MFM147/skp', "skp_id": "MF-M-R", "joint": "MFM147-NAT"}
G = {"HL147p2C", "HL147p2M", "HU228p8S", "HU220p8A", "HU228p8SA", "HU228p8C"}
for d in ('lo', 'up', 'src', 'ctl', 'fr', 'comp', 'val', 'probe', 'rs'):
    for p in sorted(glob.glob('%s/%s/*_build.json' % (W, d))):
        nid = os.path.basename(p)[:-11]; n = nid.replace('-NAT', '')
        g = W + '/g/%s/skp' % nid
        R[n] = {"meas": '%s/%s/%s' % (W, d, nid), "skp": g if os.path.exists(g + '/t1.0/MF-M-R_meas.json') else None, "skp_id": "MF-M-R", "joint": nid,
                "race": "HV" if n in G else None}
json.dump(R, open(sys.argv[1], 'w'), indent=1); print(len(R), "bodies")
