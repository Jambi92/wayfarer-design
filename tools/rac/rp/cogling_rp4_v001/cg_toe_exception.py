# cg_toe_exception.py OUT.json BODY=RAW_VALIDATOR.json:MESH.npz ... : RP4 COGLING approved toe-station validator-geometry exception (order
# reviews/chatgpt-rac-rp4-cogling-author-rulings-final-production-order.md §2; copy of pipkin_rp4_v001/pk_toe_exception.py with the Cogling scope / label;
# separate record from the Pipkin exception, no universal compact-race exception). Machine-recordable; the raw authoritative result is kept unchanged.
# A station is re-classified PASS_PIPKIN_TOE_PROBE_GEOMETRY_EXCEPTION only if ALL hold:
#   1. body in {CG76H-NAT, CGJ7, CG107-NAT} and station in {toe3_j1_l, toe3_j1_r, toe4_j1_l, toe4_j1_r};
#   2. raw D1+D3 status == FAIL_LOOPS with loop_mode closed_ring_fallback and NO crease poles (the documented D4 probe-scaling case);
#   3. the size-consistent toe-probe diagnostic (toe_station_diag.make: toe-spacing term of the probe radius not double-scaled; all else val2lib) PASSES it;
#   4. no foot topology was added: every non-v005 vertex of the realization belongs to the thumb patch (branch_part thumb_new / thumb_moved only).
# Any other failure stays a failure. Adjusted count = raw firm passes + exception passes. Global D4 / other races are untouched.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/pipkin_rp4_v001')
import core3lib, val2lib
EXC_BODIES = {'CG76H-NAT', 'CGJ7', 'CG107-NAT'}; EXC_ST = {'toe3_j1_l', 'toe3_j1_r', 'toe4_j1_l', 'toe4_j1_r'}
STATUS = 'PASS_COGLING_TOE_PROBE_GEOMETRY_EXCEPTION'
_orig = core3lib.stations
def diag_stations(scale):
    def st(meta):
        out = []
        for nm, c, d, Wd, Rr, need, Rp in _orig(meta):
            if nm.startswith('toe') and Rp is not None:
                rr = Rp / 1.15; L = (rr - 0.6) * 2; rr2 = 0.5 * L / scale + 0.6; out.append((nm, c, d, Wd, rr2 * 1.3, need, 1.15 * rr2))
            else: out.append((nm, c, d, Wd, Rr, need, Rp))
        return out
    return st
OUT = sys.argv[1]; res = dict(exception='Cogling toe-station validator-geometry exception (author-approved, order f58dbd9 §2); separate from the Pipkin record', status_label=STATUS,
                              scope=dict(bodies=sorted(EXC_BODIES), stations=sorted(EXC_ST)), global_D4_changed=False, universal_compact_race_exception=False, bodies={})
for arg in sys.argv[2:]:
    body, rest = arg.split('=', 1); vp, mp = rest.split(':')
    raw = json.load(open(vp)); st = raw['stations']; z = np.load(mp); V = z['V'].astype(float); Q = np.asarray(z['Q']); meta = json.loads(str(z['meta']))
    s = (V[:, 2].max() - V[:, 2].min()) / 173.143; raw_fail = sorted(k for k, v in st.items() if not v['firm_D1_D3'])
    part = np.asarray(z['branch_part']).astype(str); no_foot_topology = bool(all(p.startswith('thumb') for p in part[part != 'v005']))
    cand = [k for k in raw_fail if body in EXC_BODIES and k in EXC_ST]
    diag = {}
    if cand:
        val2lib.stations = diag_stations(s)
        try: dz = val2lib.evaluate(V, Q, meta, ref_stature=173.143, names=cand, d5=True)['stations']
        finally: val2lib.stations = _orig
        diag = {k: dz[k]['firm_D1_D3'] for k in cand}
    rows = {}
    for k in raw_fail:
        v = st[k]; documented = (k in cand and v['status_D1_D3'] == 'FAIL_LOOPS' and v['loop_mode'] == 'closed_ring_fallback' and not v['crease_poles'] and no_foot_topology)
        ok = documented and diag.get(k, False)
        rows[k] = dict(raw_status=v['status_D1_D3'], raw_loops=v['loops_v2'], raw_loop_mode=v['loop_mode'], raw_crease_poles=v['crease_poles'], documented_case=bool(documented),
                       size_consistent_probe_pass=diag.get(k), adjusted_status=STATUS if ok else v['status_D1_D3'], exception_applied=bool(ok))
    exc = [k for k, r in rows.items() if r['exception_applied']]; rem = [k for k, r in rows.items() if not r['exception_applied']]
    res['bodies'][body] = dict(raw_validator=vp.split('/')[-1], stations=raw['summary']['stations'], raw_firm=raw['summary']['firm_pass_count'], raw_fail=raw_fail,
                               foot_topology_unchanged=no_foot_topology, exception_applied=exc, adjusted_firm=raw['summary']['firm_pass_count'] + len(exc), adjusted_fail=rem, rows=rows)
    print(body, 'raw %d / %d' % (raw['summary']['firm_pass_count'], raw['summary']['stations']), '-> adjusted %d / %d' % (raw['summary']['firm_pass_count'] + len(exc), raw['summary']['stations']), 'exc', exc, 'remaining', rem)
res['all_adjusted_69'] = all(b['adjusted_firm'] == b['stations'] == 69 for b in res['bodies'].values())
json.dump(res, open(OUT, 'w'), indent=1); print('ALL ADJUSTED 69/69:', res['all_adjusted_69'])
