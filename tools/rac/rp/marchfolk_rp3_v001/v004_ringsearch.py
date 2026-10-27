# v004_ringsearch.py OUT.json STATION[,STATION...] : order a18371c §5 / §6 -- candidate single-ring insertions for the hip and toe-2 / toe-3 root bands
# on the frozen v003 topology. Every adjacent closed-loop pair (equal length, clean quad strip) passing through the station band is split by one
# ring (linear rows) and scored on ALL FOUR family configurations with the authoritative validator (D1 + D3 + D4). Left side only (the build mirrors).
import sys, os, json, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v004_lib import *
from val2lib import evaluate, REF_STATURE_CM
OUT = sys.argv[1]; targets = sys.argv[2].split(','); t0 = time.time()
KB, KM = (float(x) for x in sys.argv[sys.argv.index('--window') + 1].split(',')) if '--window' in sys.argv else (1.5, 2.5)   # band / mean-offset window (x W)
B = load_base(); Q = B['Q3']; M = B['M3']; UV = B['UV3']
D5 = '--d5' in sys.argv; BASE = sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else None
if BASE:                                                          # search on a successor core (e.g. the v005 TW base) instead of frozen v003
    bz = np.load(BASE); Q = np.asarray(bz['Q']); M = csr(bz); UV = bz['UV'].astype(float)
nV = M.shape[0]; loops = closed_loops(Q, nV)
L3 = {frozenset(l.tolist()): i for i, l in enumerate(closed_loops(B['Q3'], B['M3'].shape[0]))}   # frozen-v003 loop id of a loop made only of v003 vertices
VC = {cid: M @ B['C'][cid]['Vh'] for cid in CFG}
St = {cid: {s[0]: s for s in stations(B['C'][cid]['meta'])} for cid in CFG}
base = {cid: evaluate(VC[cid], Q, B['C'][cid]['meta'], REF_STATURE_CM, names=targets, loops=loops, d5=D5)['stations'] for cid in CFG}
res = {}; Q0 = quality(VC['MF-M-R'], Q)
for nm in targets:
    _, c, d, Wd, Rr, need, Rp = St['MF-M-R'][nm]; c = np.asarray(c, float); d = unit(np.asarray(d, float)); V = VC['MF-M-R']
    cands = []
    for li, L in enumerate(loops):
        P = V[L] - c; t = P @ d; rad = np.linalg.norm(P - np.outer(t, d), axis=1)
        if ((np.abs(t) <= KB * Wd) & (rad <= Rr)).sum() >= 2 and abs(t.mean()) <= KM * Wd and len(L) <= 400: cands.append(li)
    vl = {}
    for li in cands:
        for v in loops[li]: vl.setdefault(int(v), []).append(li)
    seen = set(); out = []
    print(nm, 'candidate loops', len(cands), flush=True)
    for li in cands:
        A_ = loops[li]; sa = set(A_.tolist()); nb = set()
        for q in Q[np.nonzero(np.isin(Q, A_).sum(1) == 2)[0]].tolist():
            for v in q:
                if v not in sa:
                    for lj in vl.get(v, []):
                        if lj != li: nb.add(lj)
        for lj in nb:
            key = (min(li, lj), max(li, lj))
            if key in seen or len(loops[lj]) != len(A_): continue
            seen.add(key); r = insert_ring(Q, UV, M, A_.tolist(), loops[lj].tolist())
            if r is None: continue
            Qx, UVx, Mx, ext = r; lx = closed_loops(Qx, Mx.shape[0]); sc = {}
            for cid in CFG:
                e = evaluate(Mx @ B['C'][cid]['Vh'], Qx, B['C'][cid]['meta'], REF_STATURE_CM, names=[nm], loops=lx, d5=D5)['stations'][nm]
                sc[cid] = dict(loops=e['loops_v2'], margin=e['margin'], firm=e['firm_D1_D3'], crease_own=e['crease_poles_own_digit'], sides=[x.get('loops') if x['defined'] else None for x in e['sides']])
            fs0 = strip_faces(Q, A_.tolist(), loops[lj].tolist()); _, as0, va0, vs0 = Q0
            Vx = Mx @ B['C']['MF-M-R']['Vh']; nf = np.nonzero(np.isin(Qx, np.arange(nV, Mx.shape[0])).any(1))[0]; _, as1, va1, vs1 = quality(Vx, Qx[nf])
            qual = dict(strip_T4_before=int((va0 | vs0)[fs0].sum()), new_faces_T4=int((va1 | vs1).sum()), new_faces=len(nf), max_aspect_new=round(float(as1.max()), 2), max_aspect_strip_before=round(float(as0[fs0].max()), 2))
            out.append(dict(loops_pair=list(key), v003_loops=[L3.get(frozenset(loops[li].tolist())), L3.get(frozenset(loops[lj].tolist()))], ring_len=len(A_), min_margin=min(s['margin'] for s in sc.values()), all_firm=all(s['firm'] for s in sc.values()),
                            axial_offset_cm=round(float(((M @ B['A'])[A_] - c).mean(0) @ d), 3), quality=qual, scores=sc))
            print('  ', key, len(A_), out[-1]['min_margin'], out[-1]['all_firm'], qual, {k: (v['loops'], v['firm']) for k, v in sc.items()}, '%.0fs' % (time.time() - t0), flush=True)
    out.sort(key=lambda x: (-x['all_firm'], -x['min_margin'], -x['scores']['MF-M-R']['margin'], x['ring_len']))
    res[nm] = dict(baseline={cid: dict(loops=base[cid][nm]['loops_v2'], margin=base[cid][nm]['margin'], firm=base[cid][nm]['firm_D1_D3']) for cid in CFG}, candidates=out)
json.dump(res, open(OUT, 'w'), indent=1)
