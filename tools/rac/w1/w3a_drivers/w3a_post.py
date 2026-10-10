# RAC W3A: exact-plane joint sections (w2c1_drivers/joint_section.py, MODDIR w1r/jbw2) for every W3A body, and CIB skeletal-proxy grids
# (w2a_drivers/mfm_grid.py) for the bodies whose skeletal readings the gate scores (tail search points, endpoints, matched sources, frames).
# Usage: python3 w3a_post.py joints | grids
import sys, os, glob, json, subprocess
from concurrent.futures import ThreadPoolExecutor
T = '/home/claude/wayfarer-design/tools/rac/w1'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w3a'
SUB = ('lo', 'up', 'src', 'ctl', 'fr', 'comp', 'val', 'probe', 'rs')
def bodies():
    out = []
    for d in SUB:
        for p in sorted(glob.glob('%s/%s/*_build.json' % (W, d))): out.append((d, os.path.basename(p)[:-11]))
    return out
if sys.argv[1] == 'joints':
    pre = ['%s/%s/%s' % (W, d, n) for d, n in bodies() if os.path.exists('%s/%s/%s_rest.npz' % (W, d, n))]
    old = json.load(open(W + '/joint_sections.json')) if os.path.exists(W + '/joint_sections.json') else {}
    new = [p for p in pre if os.path.basename(p) not in old]
    if new:
        subprocess.run(['python3', T + '/w2c1_drivers/joint_section.py', S + '/w1r/jbw2', W + '/js_new.json'] + new, cwd=T, check=True)
        old.update(json.load(open(W + '/js_new.json')))
    json.dump(old, open(W + '/joint_sections.json', 'w'), indent=1); print('JOINTS', len(old), 'new', len(new))
if sys.argv[1] == 'grids':
    want = [x for x in sys.argv[2:]] if len(sys.argv) > 2 else None
    B = [(d, n) for d, n in bodies() if d in ('lo', 'up', 'src', 'fr') and (want is None or n in want)]
    def g(dn):
        d, n = dn
        if os.path.exists(W + '/g/%s/skp/t1.0/MF-M-R_meas.json' % n): return
        with open(W + '/logs/grid_%s.log' % n, 'w') as f:
            rc = subprocess.run(['python3', 'w2a_drivers/mfm_grid.py', '%s/%s/%s_build.json' % (W, d, n), W + '/g/' + n], cwd=T, stdout=f, stderr=subprocess.STDOUT).returncode
        print('GRID', n, rc, flush=True)
    with ThreadPoolExecutor(2) as ex: list(ex.map(g, B))
    print('GRIDS_DONE', flush=True)
