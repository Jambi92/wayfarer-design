# ring_probe.py FAM.npz STATION [search] : closed rings around any validator ring station (core3lib.ring_stations, D4 stature-scaled), ordered along the
# station axis: t (cm), r_max, limit flags. Shows whether a FAIL_LOOPS is a missing ring or a ring outside the stature-scaled radius / window.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from core3lib import closed_loops, ring_stations, encircling, ring_name
z = np.load(sys.argv[1]); st = sys.argv[2]; srch = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
V = z['V'].astype(float); Q = np.asarray(z['Q']); meta = json.loads(str(z['meta'])); s = (V[:, 2].max() - V[:, 2].min()) / 173.143
JR = {j[0]: j for j in ring_stations(meta)}; nm, c, d, rmax, win = JR[ring_name(st)]; d = d / np.linalg.norm(d); rmax *= s; win *= s
if st.startswith('thumb_mcp'): rmax = 3.0 * s
L = closed_loops(Q, len(V)); ids = encircling(V, L, c, d, rmax * srch, win * srch * 2)
out = []
for li in ids:
    P = V[L[li]] - c; t = P @ d; r = np.linalg.norm(P - np.outer(t, d), axis=1); out.append((t.mean(), r.max(), len(L[li])))
print('%s  s %.3f  rmax %.3f  win %.3f' % (st, s, rmax, win))
for t, r, n in sorted(out): print('  t %+.3f  rmax %.3f %s  n %d  %s' % (t, r, 'R' if r <= rmax else '-', n, 'W' if abs(t) <= win else '-'))
