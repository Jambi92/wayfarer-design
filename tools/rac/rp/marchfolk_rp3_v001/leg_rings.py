# leg_rings.py CAND_S1.npz LOOPS.npz OUT_RINGS.json : RP3 v002 step-2 selection -- consecutive closed rings around each thigh and calf (between the first
# ring below the hip junction and the last ring above the ankle junction) whose connecting strip is a clean closed quad strip; one new ring is inserted
# in every such strip (subdiv.py step 2), halving the lengthwise edge length of the legs (contract §8 limb ceiling 0.6 % of stature).
import sys, json, numpy as np
z = np.load(sys.argv[1]); V = z['V']; Q = z['Q']; meta = json.loads(str(z['meta'])); H = {k: np.array(v) for k, v in meta['heads'].items()}; Tl = {k: np.array(v) for k, v in meta['tails'].items()}
loops = np.load(sys.argv[2], allow_pickle=True)['loops']; out = []
for s in ('l', 'r'):
    for seg in ('thigh', 'calf'):
        c = H['%s_%s' % (seg, s)]; d = Tl['%s_%s' % (seg, s)] - c; Ld = np.linalg.norm(d); d /= Ld; rings = []
        for L in loops:
            P = V[L] - c; t = P @ d; rad = P - np.outer(t, d); rr = np.linalg.norm(rad, axis=1)
            if rr.max() > 16 or t.mean() < 0 or t.mean() > Ld: continue
            u = np.cross(d, [1.0, 0, 0]); u /= np.linalg.norm(u); vv = np.cross(d, u); th = np.arctan2(rad @ vv, rad @ u); dth = np.diff(np.r_[th, th[0]]); dth = (dth + np.pi) % (2 * np.pi) - np.pi
            if abs(abs(dth.sum()) - 2 * np.pi) < 0.5: rings.append((float(t.mean()), [int(x) for x in L]))
        rings.sort()
        for (ta, A), (tb, B) in zip(rings[:-1], rings[1:]):
            if len(A) != len(B): continue
            sa, sb = set(A), set(B); strip = [q for q in Q if sum(v in sa for v in q) == 2 and sum(v in sb for v in q) == 2]
            if len(strip) == len(A): out.append(dict(name='%s_%s_%.1f_%.1f' % (seg, s, ta, tb), A=A, B=B))
json.dump(dict(rings=out), open(sys.argv[3], 'w')); print('rings', len(out), sorted(set(r['name'].rsplit('_', 2)[0] for r in out)))
