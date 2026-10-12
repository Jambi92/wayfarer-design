# RAC RM-OT-05F blind-gate TALLY (order §5.4 pass condition), mechanical over the scorers' JSON (f_scorer_prompt.md).
# Per run (3 scorers), for the Gorrund sculpt reference (GO-S-ref) and low composition (GO-S-low) codes:
#   G1 C from >= 2 / 3 scorers at reference          G2 C from >= 2 / 3 scorers at low composition
#   G3 stable grouping: >= 2 scorers put ref and low in one group marked stable that contains no human control and no Grask code
#   G4 distinguishable from Grask: >= 2 scorers place the Grask E3 codes in a different group from the sculpt codes
#   G5 basis = organization for the sculpt at ref AND at low from >= 2 scorers (not bulk / fatness / muscularity / thinness / stature / single feature)
#   G6 >= 2 scorers name >= 1 axial cue AND >= 1 limb cue for the sculpt
#   G7 no human-control collapse: no control receives C from >= 2 scorers and no control sits in the sculpt's group for >= 2 scorers
# Reported (author attention, not a gate line): posture_read counts for the sculpt (hunched / crouched / digitigrade reading).
# The gate passes only if EVERY run passes all of G1-G7 and at least two replicated runs exist.
# Usage: python3 f_tally.py KEY.json SCORER1.json SCORER2.json SCORER3.json [-- KEY2.json S1 S2 S3 ...]   -> prints JSON verdict
import sys, json
HUMAN = lambda k: k.startswith('MF-') or k.startswith('SK-')
def tally_run(key, scorers):
    codes = key['codes']; inv = {v: k for k, v in codes.items()}
    sref, slow = codes['GO-S-ref'], codes['GO-S-low']; gr = [codes['GR-E3-ref'], codes['GR-E3-low']]; ctrl = [v for k, v in codes.items() if HUMAN(k)]
    def grp(sc, c):
        for g in sc.get('groups', []):
            if c in g.get('codes', []): return g
        return None
    nC = lambda c: sum(sc['bodies'].get(c, {}).get('class', '').strip().upper().startswith('C') for sc in scorers)
    G = {}
    G['G1_ref_C'] = {'n_C': nC(sref), 'pass': nC(sref) >= 2}
    G['G2_low_C'] = {'n_C': nC(slow), 'pass': nC(slow) >= 2}
    st = 0
    for sc in scorers:
        g = grp(sc, sref)
        if g and slow in g['codes'] and g.get('stable') and not any(c in g['codes'] for c in ctrl + gr): st += 1
    G['G3_stable_group'] = {'n_scorers': st, 'pass': st >= 2}
    dg = sum(1 for sc in scorers if grp(sc, sref) is not None and all(grp(sc, c) is not grp(sc, sref) for c in gr))
    G['G4_distinct_from_Grask'] = {'n_scorers': dg, 'pass': dg >= 2}
    org = sum(1 for sc in scorers if all(sc['bodies'].get(c, {}).get('basis', '') == 'organization' for c in (sref, slow)))
    G['G5_organization_basis'] = {'n_scorers': org, 'pass': org >= 2}
    cues = sum(1 for sc in scorers if any(sc['bodies'].get(c, {}).get('axial_cues') for c in (sref, slow)) and any(sc['bodies'].get(c, {}).get('limb_cues') for c in (sref, slow)))
    G['G6_axial_and_limb_cues'] = {'n_scorers': cues, 'pass': cues >= 2}
    bad = [inv[c] for c in ctrl if nC(c) >= 2 or sum(1 for sc in scorers if grp(sc, sref) is not None and c in grp(sc, sref)['codes']) >= 2]
    G['G7_no_control_collapse'] = {'controls_collapsed': bad, 'pass': not bad}
    post = {lab: sum(1 for sc in scorers if sc['bodies'].get(c, {}).get('posture_read')) for lab, c in (('ref', sref), ('low', slow))}
    return {'gate_lines': G, 'posture_read_counts_author_attention': post, 'run_pass': all(v['pass'] for v in G.values()),
            'grask_E3_C': {'ref': nC(gr[0]), 'low': nC(gr[1])}}
if __name__ == '__main__':
    args = sys.argv[1:]; runs = []; cur = []
    for a in args + ['--']:
        if a == '--':
            if cur: runs.append(cur); cur = []
        else: cur.append(a)
    res = []
    for r in runs:
        key = json.load(open(r[0])); scorers = [json.load(open(p)) for p in r[1:]]
        assert len(scorers) == 3, 'exactly 3 scorers per run'
        res.append({'key': r[0], **tally_run(key, scorers)})
    out = {'runs': res, 'n_runs': len(res), 'gate_pass': len(res) >= 2 and all(x['run_pass'] for x in res)}
    print(json.dumps(out, indent=1))
