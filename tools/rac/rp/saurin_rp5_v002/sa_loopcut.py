# sa_loopcut.py IN.npz OUT.npz : AUTHORED edge-loop insertion for the T-4 production pass (order 236dddc §6, §7, §9 "ring redistribution / web depth").
#   For every quad with aspect > 4 outside the explicit tip exceptions, the quad strip that crosses its two LONG opposite edges is walked; if it closes on
#   itself locally (a ring around a digit, a web band, a limb segment; <= MAXLEN quads, never into the tail module / caps) one new edge loop is cut
#   through it (midpoints of the crossed edges, projected onto the working source) -> every quad of the strip is split in two across its long edges.
#   Strips that do not close locally are left to sa_qopt. Topology stays 100 % quads, closed, consistently oriented; c1 / c2 share the new face list.
import sys, os, numpy as np, collections, igl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa_geo as G
IN, OUT = sys.argv[1:3]; MAXLEN = int(os.environ.get('MAXLEN', 90)); ATH = float(os.environ.get('ATH', 4.0))
z = dict(np.load(IN)); Q = [list(q) for q in z['Q']]; V = list((z['bc'][:, :, None] * G.V[G.F[z['tri']]]).sum(1)); nb = int(z['n_body']); nold = len(V)
ql = list(z['qlab'].astype(str)); qc = list(z['qcoarse']); NOCUT = {'tail', 'finger_cap', 'thumb_cap', 'toe_cap'}
def ekey(a, b): return (a, b) if a < b else (b, a)
cuts = 0; log = collections.Counter()
for rnd in range(4):
    Va = np.array(V); Qa = np.array(Q); sd = np.linalg.norm(np.roll(Va[Qa], -1, 1) - Va[Qa], axis=2); asp = sd.max(1) / sd.min(1)
    bad = [i for i in np.argsort(-asp) if asp[i] > ATH and ql[i] not in NOCUT]
    if not bad: break
    EQ = collections.defaultdict(list)
    for i, q in enumerate(Q):
        for k in range(4): EQ[ekey(q[k], q[(k + 1) % 4])].append(i)
    used = set(); newq = []
    for b in bad:
        if b in used: continue
        q = Q[b]; k = 0 if sd[b][0] + sd[b][2] >= sd[b][1] + sd[b][3] else 1          # long opposite pair (k, k+2)
        strip = [(b, k)]; cur, ck = b, k; ok = False
        while len(strip) <= MAXLEN:
            qq = Q[cur]; e = ekey(qq[(ck + 2) % 4], qq[(ck + 3) % 4]); nxt = [j for j in EQ[e] if j != cur]
            if not nxt: break
            j = nxt[0]
            if j == b: ok = True; break
            if ql[j] in NOCUT or j in used or any(v >= nb for v in Q[j]): break
            qj = Q[j]; kj = [t for t in range(4) if ekey(qj[t], qj[(t + 1) % 4]) == e][0]; strip.append((j, kj)); cur, ck = j, kj
        if not ok or any(i in used for i, _ in strip): continue
        # admissible only if no quad of the strip becomes thin: after the cut each half has the crossed edges halved
        def half_asp(i, kk):
            qq = Va[Q[i]]; e = [np.linalg.norm(qq[(t + 1) % 4] - qq[t]) for t in range(4)]
            L1, S1, L2, S2 = e[kk] / 2, e[(kk + 1) % 4], e[(kk + 2) % 4] / 2, e[(kk + 3) % 4]
            return max(max(L1, S1, L2) / max(min(L1, S1, L2), 1e-9), max(L1, S2, L2) / max(min(L1, S2, L2), 1e-9))
        if max(half_asp(i, kk) for i, kk in strip) > float(os.environ.get("HALF", 3.6)): continue
        mid = {}
        def m(a, c):
            key = ekey(a, c)
            if key not in mid: mid[key] = len(V); V.append(0.5 * (V[a] + V[c]))
            return mid[key]
        for i, kk in strip:
            qq = Q[i]; a, b1, c, d = qq[kk], qq[(kk + 1) % 4], qq[(kk + 2) % 4], qq[(kk + 3) % 4]
            m1 = m(a, b1); m2 = m(c, d)
            Q[i] = [a, m1, m2, d]; newq.append(([m1, b1, c, m2], ql[i], qc[i])); used.add(i)
        cuts += 1; log[ql[b]] += 1
    for q, l, c in newq: Q.append(q); ql.append(l); qc.append(c)
    print('round', rnd, 'loops cut so far', cuts, dict(log), flush=True)
# new body vertices before the module block; project the new vertices onto the source
V = np.array(V); Q = np.array(Q); nnew = len(V) - nold
if nnew:
    _, _, cp = igl.point_mesh_squared_distance(V[nold:], G.V, G.F); V[nold:] = cp
perm = np.r_[np.arange(nb), np.arange(nold, len(V)), np.arange(nb, nold)]; inv = np.empty_like(perm); inv[perm] = np.arange(len(perm))
V = V[perm]; Q = inv[Q]
ec = collections.Counter(ekey(q[k], q[(k + 1) % 4]) for q in Q for k in range(4)); assert min(ec.values()) == 2 and max(ec.values()) == 2
dirE = collections.Counter((q[k], q[(k + 1) % 4]) for q in Q for k in range(4)); assert max(dirE.values()) == 1
fi, bc, dist = G.embed(V); out = dict(z); out.update(V=V, Q=Q, tri=fi, bc=bc, qlab=np.array(ql), qcoarse=np.array(qc), n_body=nb + nnew, tail_ring=inv[z['tail_ring']], pinned=inv[z['pinned']])
np.savez_compressed(OUT, **out); print('loops', cuts, dict(log), '->', len(V), 'V', len(Q), 'Q')
