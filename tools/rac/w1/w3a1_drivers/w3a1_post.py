# RAC W3A1: exact-plane joint sections for every W3A1 body, and CIB skeletal-proxy grids (w2a_drivers/mfm_grid.py) for the bodies whose full
# 24-reading source-passing protocol the closure scores: the W3A lower-tail near-duplicate and ambiguous samples (AD-W3A-4 re-evaluation), the
# central native-range confirmation bodies + Marchfolk 157, and the coupled upper-tail endpoints with their frames.
# Usage: python3 w3a1_post.py joints | grids
import sys, os, glob, json, subprocess
from concurrent.futures import ThreadPoolExecutor
T = '/home/claude/wayfarer-design/tools/rac/w1'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w3a1'
SUB = ('up', 'ks', 'src', 'fr', 'comp', 'rsup', 'cen')
def bodies():
    return [(d, os.path.basename(p)[:-11]) for d in SUB for p in sorted(glob.glob('%s/%s/*_build.json' % (W, d)))]
if sys.argv[1] == 'joints':
    pre = ['%s/%s/%s' % (W, d, n) for d, n in bodies() if os.path.exists('%s/%s/%s_rest.npz' % (W, d, n))]
    old = json.load(open(W + '/joint_sections.json')) if os.path.exists(W + '/joint_sections.json') else {}
    new = [p for p in pre if os.path.basename(p) not in old]
    if new:
        subprocess.run(['python3', T + '/w2c1_drivers/joint_section.py', S + '/w1r/jbw2', W + '/js_new.json'] + new, cwd=T, check=True)
        old.update(json.load(open(W + '/js_new.json')))
    json.dump(old, open(W + '/joint_sections.json', 'w'), indent=1); print('JOINTS', len(old), 'new', len(new))
if sys.argv[1] == 'grids':
    rs = json.load(open(S + '/w3a/rs.json'))["samples"]
    low = [x["id"] for x in rs if x["stratum"] == "L-MF" and (x["dup_matched"] or x["ambiguous"])]
    B = [('%s/w3a/%s/%s-NAT_build.json' % (S, 'val' if n.startswith('V') else 'rs', n), n) for n in low]
    B += [('%s/%s/%s_build.json' % (W, d, n), n.replace('-NAT', '')) for d, n in bodies() if d == 'cen' or n == 'MF157-NAT' or
          (d == 'up' and n in ('HU228p8Sc', 'HU228p8Cc', 'HU221Ac', 'HU220p8Ac', 'HU228p8SAc', 'HU221Sc', 'HU225Sc')) or d == 'fr']
    def g(bn):
        b, n = bn
        if os.path.exists(W + '/g/%s/skp/t1.0/MF-M-R_meas.json' % n): return
        with open(W + '/logs/grid_%s.log' % n, 'w') as f:
            rc = subprocess.run(['python3', 'w2a_drivers/mfm_grid.py', b, W + '/g/' + n], cwd=T, stdout=f, stderr=subprocess.STDOUT).returncode
        print('GRID', n, rc, flush=True)
    print('GRIDS TO RUN', len(B), flush=True)
    with ThreadPoolExecutor(2) as ex: list(ex.map(g, B))
    print('GRIDS_DONE', flush=True)
