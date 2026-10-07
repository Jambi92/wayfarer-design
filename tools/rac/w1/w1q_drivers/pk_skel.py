# RAC W1q: skeletal (CIB) rows for Pipkin bodies on the W1i skeletal base, with the accepted Grask (W1l), Aelari (AEL1), Vael (VAL4) and
# Fenn (FNL4) readings in their slots; Pipkin candidate readings copied into both the PK and PK-NAT slots. Optional DU slot override
# (diagnostic Narrow Durrim). Usage: python3 pk_skel.py TAG=pk_skp_dir[,du_skp_dir] ...  -> reviews/rac-w1q-pk-evidence/skeletal_<TAG>.json
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import skeletal_checks as SC
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
SLOTS = {"GR": (S + '/w1l/probe/skp_GRL925_1200', 'GRL925_1200'), "AE": (S + '/w1m/ael1/skp', 'AE'), "VA": (S + '/w1n/val4/skp', 'VA'), "FN": (S + '/w1p/fnl4/skp', 'FN')}
for a in sys.argv[1:]:
    tag, dirs = a.split('=', 1); skp, du = (dirs.split(',') + [None])[:2]; tmp = S + '/w1q/chk_' + tag
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(R + '/reviews/rac-w1i-evidence/skeletal', tmp, ignore=shutil.ignore_patterns('*.jpg', 'skeletal_checks.json', '*.log'))
    for t in ('0.0', '0.5', '1.0'):
        for slot in ('PK', 'PK-NAT'): shutil.copy(skp + '/t%s/PK-NAT_meas.json' % t, tmp + '/t%s/%s_meas.json' % (t, slot))
        if du:
            for slot in ('DU', 'DU-NAT'): shutil.copy(du + '/t%s/DU-NAT_meas.json' % t, tmp + '/t%s/%s_meas.json' % (t, slot))
        for slot, (d, nm) in SLOTS.items(): shutil.copy(d + '/t%s/%s_meas.json' % (t, nm), tmp + '/t%s/%s_meas.json' % (t, slot))
    rows = [r for r in SC.run(tmp) if 'PK' in (r.get('cand'), r.get('b'))]
    json.dump(rows, open(R + '/reviews/rac-w1q-pk-evidence/skeletal_%s.json' % tag, 'w'), indent=1, default=float)
    print(tag, len(rows), 'non-PASS:', [(r['cand'], r['check'], r['result']) for r in rows if r['result'] not in ('PASS', 'REPORT')])
