# RAC W1m: skeletal (CIB) rows for Aelari candidates on the W1i skeletal base (reviews/rac-w1i-evidence/skeletal, all accepted
# comparators) with the accepted Grask W1l readings in the GR slot. Usage: python3 ae_skel.py TAG=skp_dir ...  -> skeletal_<TAG>.json
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import skeletal_checks as SC
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
GRS = S + '/w1l/probe/skp_GRL925_1200'
for a in sys.argv[1:]:
    tag, skp = a.split('=', 1); tmp = S + '/w1m/chk_' + tag
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(R + '/reviews/rac-w1i-evidence/skeletal', tmp, ignore=shutil.ignore_patterns('*.jpg', 'skeletal_checks.json', '*.log'))
    for t in ('0.0', '0.5', '1.0'):
        shutil.copy(skp + '/t%s/AE_meas.json' % t, tmp + '/t%s/AE_meas.json' % t)
        shutil.copy(GRS + '/t%s/GRL925_1200_meas.json' % t, tmp + '/t%s/GR_meas.json' % t)
    rows = [r for r in SC.run(tmp) if 'AE' in (r.get('cand'), r.get('b'))]
    json.dump(rows, open(R + '/reviews/rac-w1m-ae-evidence/skeletal_%s.json' % tag, 'w'), indent=1, default=float)
    print(tag, len(rows), 'non-PASS:', [(r['cand'], r['check'], r['result']) for r in rows if r['result'] not in ('PASS', 'REPORT')])
