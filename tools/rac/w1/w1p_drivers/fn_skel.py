# RAC W1p: skeletal (CIB) rows for Fenn candidates (copy of w1n_drivers/va_skel.py; accepted Vael VAL4 also in its slot) on the W1i skeletal base with the ACCEPTED Aelari (AEL1) and Grask (W1l) readings
# in their slots. Usage: python3 va_skel.py TAG=skp_dir ...  -> reviews/rac-w1p-fn-evidence/skeletal_<TAG>.json
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import skeletal_checks as SC
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
SLOTS = {"GR": (S + '/w1l/probe/skp_GRL925_1200', 'GRL925_1200'), "AE": (S + '/w1m/ael1/skp', 'AE'), "VA": (S + '/w1n/val4/skp', 'VA')}
for a in sys.argv[1:]:
    tag, skp = a.split('=', 1); tmp = S + '/w1p/chk_' + tag
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(R + '/reviews/rac-w1i-evidence/skeletal', tmp, ignore=shutil.ignore_patterns('*.jpg', 'skeletal_checks.json', '*.log'))
    for t in ('0.0', '0.5', '1.0'):
        shutil.copy(skp + '/t%s/FN_meas.json' % t, tmp + '/t%s/FN_meas.json' % t)
        for slot, (d, nm) in SLOTS.items(): shutil.copy(d + '/t%s/%s_meas.json' % (t, nm), tmp + '/t%s/%s_meas.json' % (t, slot))
    rows = [r for r in SC.run(tmp) if 'FN' in (r.get('cand'), r.get('b'))]
    json.dump(rows, open(os.environ.get('EVDIR', R + '/reviews/rac-w1p-fn-evidence') + '/skeletal_%s.json' % tag, 'w'), indent=1, default=float)
    print(tag, len(rows), 'non-PASS:', [(r['cand'], r['check'], r['result']) for r in rows if r['result'] not in ('PASS', 'REPORT')])
