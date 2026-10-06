# RAC W1g driver AS RUN (scratch paths = this session's working directories; kept for provenance).
"""AD-G14 evaluation WITH the W1g composition-infimum bony envelope (CIB) in the loop: build skeleton (lean_B, bone scales) ->
trunk sculpt -> reference envelope -> composition grid (same route) -> CIB -> skeletal proxy -> skeletal checks."""
import sys, os, json, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import skeleton_envelope as SE, skeletal_checks as SC, bony_envelope as BE, skeletal_proxy as SP, profile_bump as PB
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
F, G = S + '/w1f', S + '/w1g'; T = '/home/claude/wayfarer-design/tools/rac/w1'
SKP = os.environ.get('SKPBASE', G + '/skp')       # comparator skeletal readings (CIB) for every other body
RACE = {"GO": {"base": F + '/base_w1c/GO_build.json', "donor": F + '/go/GO0', "did": "GO0"},
        "GR": {"base": F + '/base/GR_build.json', "donor": F + '/gr/GR0', "did": "GR0"}}

def build(race, name, B, sculpt=None, wd=None, base=None, donor=None, did=None, extra_ov=None):
    R = RACE[race]; base = base or R["base"]; donor = donor or R["donor"]; did = did or R["did"]
    wd = wd or G + '/solve_' + race; os.makedirs(wd, exist_ok=True)
    ov = {"muscle": 0.0, "weight": 0.0, "bone_scales": B}; ov.update(extra_ov or {}); json.dump(ov, open(wd + '/%s_ov.json' % name, 'w'))
    subprocess.run(['python3', T + '/build_variant.py', base, wd + '/%s_ov.json' % name, wd, name + '-LEAN'], check=True, capture_output=True)
    r = SE.make(wd + '/' + name + '-LEAN', donor, donor + '-LEAN', wd + '/' + name, tag=name, sculpt=sculpt)   # sculpt written back into -LEAN
    gd = wd + '/grid_' + name
    if os.path.exists(gd): shutil.rmtree(gd)
    os.makedirs(gd)
    comps = BE.assemble_grid(wd + '/' + name + '-LEAN', G + '/donor', did, donor + '-LEAN', gd, name) + [wd + '/' + name + '_rest.npz']
    C = BE.cib(wd + '/' + name + '_rest.npz', comps); cj = wd + '/%s_cib.json' % name; json.dump(C, open(cj, 'w'), indent=1, default=float)
    SP.main(wd, wd, name, wd + '/skp_' + name, cj)
    return r, C

def checks(race, name, wd=None, skpbase=None):
    wd = wd or G + '/solve_' + race; tmp = wd + '/chk_' + name
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(skpbase or SKP, tmp, symlinks=True, ignore=shutil.ignore_patterns('*_skp.json', '*.jpg', 'skeletal_checks.json'))
    for t in ('0.0', '0.5', '1.0'):
        dst = tmp + '/t%s/%s_meas.json' % (t, race)
        if os.path.lexists(dst): os.remove(dst)
        shutil.copy(wd + '/skp_%s/t%s/%s_meas.json' % (name, t, name), dst)
    return SC.run(tmp)

def report(race, name, rows, wd=None):
    wd = wd or G + '/solve_' + race
    mine = [x for x in rows if (x['cand'] == race or x.get('b') == race) and x['result'] not in ('REPORT', 'NOT RUN')]
    bad = [x for x in mine if x['result'] != 'PASS']
    print(name, 'rows', len(mine), 'non-pass', len(bad), flush=True)
    for x in bad: print('   ', x['result'], x['cand'], x['check'][:70], {t: round(v['va'], 4) for t, v in x['by_t'].items()}, x['op'], round(x['vb'], 4), flush=True)
    return mine, bad

if __name__ == '__main__':
    race, name = sys.argv[1], sys.argv[2]; B = json.loads(sys.argv[3]); sc = json.loads(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != '-' else None
    r, C = build(race, name, B, sc); rows = checks(race, name); report(race, name, rows)
    print('stature', round(r['r6']['stature'], 2), 'S5 bony', round(C['bony']['S5'][0], 2), C['argmin']['S5'], 'S2', round(C['bony']['S2'][0], 2))
