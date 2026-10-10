# RAC W3B RM-UF-03 guard evaluation over the spacing sweep / head corners (diagnostic thresholds; all values in results.json).
#   G1 platform containment: orbital-platform breadth grows <= 1 % over the same head corner at dx = 0 (beyond: the orbit complex becomes
#      the lateral head contour - lateral reptile placement / loss of the broad orbital-temporal platform)
#   G2 lateral (postorbital / temporal) support >= 75 % of the corner's own value (implausibly thin support)
#   G3 tissue strain in the interorbital-canthal, brow-supraorbital, postorbital-temporal and rostral-base regions within [0.67, 1.5]
#      (0.5th / 99.5th percentile edge-length ratio vs the corner at dx = 0; W2I precedent: x0.66 accepted, x1.5 flagged) - pinched /
#      crowded canthus and rostral base (inward), stretched brow / canthal web (outward)
#   G4 topology: 0 flipped, 0 degenerate faces
#   G5 eye / lid / aperture fit: aperture-fit ratio (eye-surface radius / orbital-margin radius) within 3 % of the corner at dx = 0; margin
#      ring circularity rms <= 0.30 cm (the orbit complex is carried rigidly: no independent eyeball scaling)
#   G6 symmetry: bilateral centre asymmetry <= max(0.30 cm, corner's own dx = 0 value + 0.20 cm) (ring-fit noise 0.1-0.46 cm)
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C
def guards(r, r0):
    g = {}
    g['G1_platform'] = r['platform_breadth'] / r0['platform_breadth'] - 1 <= 0.01
    g['G2_support'] = r['lateral_support_min'] >= 0.75 * r0['lateral_support_min']
    lo = min(v[0] for v in r['strain'].values()); hi = max(v[2] for v in r['strain'].values())
    g['G3_strain'] = (lo >= 0.67) and (hi <= 1.5)
    g['G4_topology'] = r['quality']['flipped'] == 0 and r['quality']['degenerate'] == 0
    g['G5_fit'] = abs(r['aperture_fit'] / r0['aperture_fit'] - 1) <= 0.03 and r['ring_rms'] <= 0.30
    g['G6_symmetry'] = r['asym_cm'] <= max(0.30, r0['asym_cm'] + 0.20)      # ring-fit noise: some corners carry 0.3-0.46 cm at dx = 0
    return g, lo, hi
def table(res):
    rows = []
    corners = sorted(set(r['corner'] for r in res.values()))
    for c in corners:
        rs = sorted([r for r in res.values() if r['corner'] == c], key=lambda r: r['dx_local']); r0 = next(r for r in rs if r['dx_local'] == 0)
        for r in rs:
            g, lo, hi = guards(r, r0); rows.append(dict(corner=c, dx_local=r['dx_local'], dx_world=r['dx_world'], IOD=r['IOD'], IOD_pct=100 * (r['IOD'] / r0['IOD'] - 1),
                IOD_over_cranial=r['IOD_over_cranial'], IOD_globe=r['IOD_globe'], strain_lo=lo, strain_hi=hi, platform_pct=100 * (r['platform_breadth'] / r0['platform_breadth'] - 1),
                support=r['lateral_support_min'], flips=r['quality']['flipped'], fit_pct=100 * (r['aperture_fit'] / r0['aperture_fit'] - 1), asym=r['asym_cm'],
                fails=[k for k, v in g.items() if not v], valid=all(g.values())))
    return rows
if __name__ == '__main__':
    res = json.load(open(C.W + '/orbit/results.json')); rows = table(res); json.dump(rows, open(C.W + '/orbit/guards.json', 'w'), indent=1)
    for c in sorted(set(r['corner'] for r in rows)):
        rr = [r for r in rows if r['corner'] == c]
        print(c, ' '.join('%+.2f%s' % (r['dx_local'], '' if r['valid'] else '!' + ','.join(f[:2] for f in r['fails'])) for r in rr))
