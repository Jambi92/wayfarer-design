# splice.py VARIANT OUT.npz : render-only mockup mesh = v014 with each nail's claw target patch spliced in (radius RS around the claw)
import sys, json, numpy as np
vn, out = sys.argv[1], sys.argv[2]; RS = float(sys.argv[3]) if len(sys.argv) > 3 else 1.8
fl = np.array([1, -1, 1])
z = np.load('/tmp/claude-0/rp1f/t3.npz'); V = z['V'] * fl; F = z['F']
d = json.load(open('/tmp/claude-0/rp1f/mock2_sdf.json'))
keep = np.ones(len(F), bool); parts_V = []; parts_F = []; off = 0
for k, p in d.items():
    if not k.startswith(vn + '__'): continue
    T = np.array(p['T']); C = np.array(p['C']); e = (T - C) / np.linalg.norm(T - C); cc = T + 0.3 * e
    keep &= np.linalg.norm(V[F].mean(1) - cc, axis=1) > RS
    t = np.load('/tmp/claude-0/rp1f/m2_%s.npz' % k); tv = t['V'] * fl; tf = t['F'][:, ::-1]
    m = np.linalg.norm(tv[tf].mean(1) - cc, axis=1) < RS + 0.05; tf = tf[m]; u = np.unique(tf); r = -np.ones(len(tv), int); r[u] = np.arange(len(u))
    parts_V.append(tv[u]); parts_F.append(r[tf])
VV = [V]; FF = [F[keep]]; o = len(V)
for pv, pf in zip(parts_V, parts_F): VV.append(pv); FF.append(pf + o); o += len(pv)
VV = np.vstack(VV) * fl; FF = np.vstack(FF)
np.savez_compressed(out, V=VV, F=FF, Q=FF[:, ::-1])
print(vn, 'faces', len(FF))
