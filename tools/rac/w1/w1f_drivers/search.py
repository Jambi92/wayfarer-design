# RAC W1f driver script AS RUN (scratch paths are the session's working directories; kept for provenance of the AD-G14 construction)
import sys, os, json, subprocess, shutil, glob
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import skeleton_envelope as SE, skeletal_checks as SC
F = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1f'
T = '/home/claude/wayfarer-design/tools/rac/w1'
def ev(B, name, race="GO", base=None, donor=None, extra_ov=None, quiet=False):
    base = base or F + '/base_w1c/%s_build.json' % race; donor = donor or F + '/go/%s0' % race
    d = F + '/go'
    ov = {"muscle": 0.0, "weight": 0.0, "bone_scales": B}; ov.update(extra_ov or {})
    json.dump(ov, open(d + '/%s_ov.json' % name, 'w'))
    subprocess.run(['python3', T + '/build_variant.py', base, d + '/%s_ov.json' % name, d, name + '-LEAN'], check=True, capture_output=True)
    r = SE.make(d + '/' + name + '-LEAN', donor, donor + '-LEAN', d + '/' + name, tag=name)
    subprocess.run(['python3', T + '/skeletal_proxy.py', d, d, name, d + '/skp_' + name], check=True, capture_output=True)
    tmp = d + '/chk_' + name
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(F + '/skp', tmp, symlinks=True, ignore=shutil.ignore_patterns('*.json') if False else None)
    for t in ('0.0', '0.5', '1.0'):
        dst = tmp + '/t%s/%s_meas.json' % (t, race)
        if os.path.islink(dst) or os.path.exists(dst): os.remove(dst)
        shutil.copy(d + '/skp_%s/t%s/%s_meas.json' % (name, t, name), dst)
    rows = SC.run(tmp)
    mine = [x for x in rows if x['cand'] == race or x.get('b') == race]
    bad = [x for x in mine if x['result'] not in ('PASS', 'REPORT', 'NOT RUN')]
    if not quiet:
        print(name, 'stature r6 %.2f' % r['r6']['stature'], 'non-pass', len(bad))
        for x in bad: print('   ', x['result'], x['cand'], x['check'], {t: round(v['va'], 4) for t, v in x['by_t'].items()}, x['op'], round(x['vb'], 4))
    return bad, r, rows
if __name__ == '__main__':
    B = json.loads(sys.argv[2]); ev(B, sys.argv[1])
