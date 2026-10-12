# RAC RM-OT-05F RE-ENTRY ORCHESTRATOR for a delivered Gorrund hand-sculpt (order §5.3). One command:
#   1. f_ingest (I1-I6) on the OBJ; a FAIL stops here (nothing is built);
#   2. writes the race_base spec {"floor": "true", "keep_volume": true, "sculpt": {"delta": ...}} (no procedural organization at all);
#   3. builds GO5F<SID> (reference), GO5F<SID>-LOW (muscle 0 / weight 0.5), GO5F<SID>N / GO5F<SID>B (Narrow / Broad frames) on the accepted
#      skeleton route with the unchanged 05D builder (rmot05d_drivers/d_build.py, 05B cfg_final);
#   4. runs f_guard (the 05D / 05E guards, thresholds unchanged) on all four states, incl. composition and frame ordering;
#   5. transport report: how much of the delivered displacement survives in each state (per hard-form family), and how exactly the
#      reference state reproduces the delivered surface.
# Usage: python3 f_reentry.py SCULPT.obj SID [--no-build]     (SID = two characters, e.g. S1)   ->  WORK/reentry_SID.json
import os, sys, json, subprocess, numpy as np
from f_common import *
import f_ingest as FI
CFG = REPO + '/reviews/rac-rmot05b-evidence/cfg_final.json'
def run(args):
    r = subprocess.run(['python3'] + args, capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    return r.stdout[-2000:] + r.stderr[-2000:]
def transport(sid, raw):
    V0, B, L, J, f, z0 = route_state(SKELETON_BODY); F = B['F']; keep = B['keep'].astype(bool); R = regions(B, V0, J)
    n0 = TE.outward_normals(V0, F, keep); raw_n = np.einsum('ij,ij->i', raw, n0)
    out = {}
    for suf, lab in (('', 'reference'), ('-LOW', 'low'), ('N', 'narrow'), ('B', 'broad')):
        nm = 'GO5F%s%s' % (sid, suf); Vb = np.load(CG.path(nm) + '_r6.npz', allow_pickle=True)['V'].astype(float)
        Vr = route_state(nm)[0]; A = Vb - Vr; An = np.einsum('ij,ij->i', A, TE.outward_normals(Vr, F, keep))
        fam = {}
        for k, m in R.items():
            if k.startswith('NO_TOUCH'): continue
            sig = m & (np.abs(raw_n) > 0.5)
            fam[k] = {'n_signal_vertices': int(sig.sum()), 'retention_median': (round(float(np.median(An[sig] / raw_n[sig])), 3) if sig.any() else None),
                      'retention_p10': (round(float(np.percentile(An[sig] / raw_n[sig], 10)), 3) if sig.any() else None)}
        rec = {'families': fam}
        if lab == 'reference':
            e = np.linalg.norm(A - raw, axis=1)[keep]
            rec['reproduction_error_vs_delivered_cm'] = {'p50': round(float(np.percentile(e, 50)), 3), 'p90': round(float(np.percentile(e, 90)), 3), 'max': round(float(e.max()), 3)}
        out[lab] = rec
    return out
if __name__ == '__main__':
    obj, sid = sys.argv[1], sys.argv[2]; assert len(sid) == 2, 'SID must be two characters'
    rep, delta = FI.ingest(obj, sid); json.dump(rep, open(WORK + '/ingest_%s.json' % sid, 'w'), indent=1, default=float)
    summary = {'sid': sid, 'sculpt_obj': os.path.basename(obj), 'ingest': {k: v['pass'] for k, v in rep['checks'].items()}, 'ingest_pass': rep['pass']}
    if not rep['pass']:
        summary['reentry_pass'] = False; json.dump(summary, open(WORK + '/reentry_%s.json' % sid, 'w'), indent=1); print('INGEST FAIL - nothing built', summary); sys.exit(1)
    spec = {'GO': {sid: {'floor': 'true', 'keep_volume': True, 'sculpt': {'delta': delta}}}}
    sp = WORK + '/spec_%s.json' % sid; json.dump(spec, open(sp, 'w'), indent=1)
    names = ['GO5F%s' % sid, 'GO5F%s-LOW' % sid, 'GO5F%sN' % sid, 'GO5F%sB' % sid]
    if '--no-build' not in sys.argv:
        print(run([W1 + '/rmot05d_drivers/d_build.py', CFG, sp] + names), flush=True)
    gj = WORK + '/guard_%s.json' % sid; print(run(['f_guard.py', gj] + names)[-1500:], flush=True)
    G = json.load(open(gj))
    passes = {n: {k: v['pass'] for k, v in G[n].items() if isinstance(v, dict) and 'pass' in v} for n in names}
    V0 = route_state(SKELETON_BODY)[0]; Vs = read_obj(obj)[0]; raw = np.zeros_like(V0); raw[:NBODY] = Vs - V0[:NBODY]
    summary.update({'guards': passes, 'volume_ratio_vs_route': {n: G[n]['volume_ratio_vs_route'] for n in names},
                    'protected_relations': {n: G[n]['skeletal_stations']['protected_unorganized_route'].get('ratios') for n in names if 'skeletal_stations' in G[n]},
                    'transport': transport(sid, raw)})
    summary['reentry_pass'] = bool(rep['pass'] and all(all(p.values()) for p in passes.values()))
    json.dump(summary, open(WORK + '/reentry_%s.json' % sid, 'w'), indent=1, default=float)
    print('RE-ENTRY', 'PASS' if summary['reentry_pass'] else 'FAIL', json.dumps(summary['transport'])[:1500])
    sys.exit(0 if summary['reentry_pass'] else 1)
