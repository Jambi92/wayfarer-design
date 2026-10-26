# topo_audit.py OUTDIR [POSED_NPZ ...] : NON-DESTRUCTIVE topology-density audit of the left elbow (order 6c38d75 §13). Reads the frozen v003
# read-back only. Ring sequence: starting from the tagged LOOP_elbow_l_22 ring, walk edge rings distally (forearm) and proximally (upper arm)
# through the mesh (ring k+1 = edge neighbours of ring k not in rings k / k-1). Per ring: centroid axial position s along the elbow bisector axis,
# vertex count, spacing to the next ring (mean / inner-crease side / outer side), along-ring and across-ring edge lengths, quad aspect, valence;
# density = rings per cm in the flexion zone vs adjacent upper-arm / forearm. Optional posed meshes: per ring pair the inner-side spacing ratio.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diag_lib import bl_to_src
O = sys.argv[1]; POSED = sys.argv[2:]; os.makedirs(O, exist_ok=True)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V = Z['V'].astype(float); Q = np.asarray(Z['Q'])
LOOPS = json.load(open('/tmp/claude-0/rt/r4/loops.json'))
rig = json.load(open('/tmp/claude-0/rt/rd/rig/rig_v001.json')); B = {b['name']: b for b in rig['bones']}
hd = lambda k: bl_to_src(np.array(B[k]['head'])[None])[0]; tl = lambda k: bl_to_src(np.array(B[k]['tail'])[None])[0]
e = hd('forearm_l'); ua = e - hd('upperarm_l'); ua /= np.linalg.norm(ua); fa = tl('forearm_l') - e; fa /= np.linalg.norm(fa); ax = ua + fa; ax /= np.linalg.norm(ax)
ant = np.array([0, 1.0, 0]); ant -= (ant @ ax) * ax; ant /= np.linalg.norm(ant)
E = np.unique(np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1), axis=0)
nb = [[] for _ in range(len(V))]
for a, b in E: nb[a].append(b); nb[b].append(a)
val = np.array([len(x) for x in nb])
# rings by quad-strip walking: from a closed edge loop R, the parallel loop on one side = the opposite edges of the quads that share an edge with R
# on that side (the side is chosen by axial position s). Stops when the walk stops producing a closed 2-regular ring of similar size (pole / branch).
from collections import defaultdict
EF_ = defaultdict(list)
for fi, q in enumerate(Q):
    for k in range(4): EF_[tuple(sorted((q[k], q[(k + 1) % 4])))].append(fi)
sv = (V - e) @ ax
def ring_edges(R):
    Rs = set(R); return [ed for v in R for w in nb[v] if w in Rs and v < w for ed in [(v, w)]]
def step(R, prevR):
    Rs = set(R); Ps = set(prevR); nxt = set()
    for ed in ring_edges(R):
        for fi in EF_[ed]:
            q = list(Q[fi]); other = [x for x in q if x not in ed]
            if any(x in Ps or x in Rs for x in other): continue
            nxt.update(other)
    return sorted(nxt)
def closed(R):
    Rs = set(R); return len(R) > 0 and all(sum(1 for w in nb[v] if w in Rs) == 2 for v in R)
def walk_dir(start, prev, n):
    out = []; cur, pv = start, prev
    for _ in range(n):
        nx = step(cur, pv)
        if not closed(nx) or abs(len(nx) - len(cur)) > 8: break
        out.append(np.array(nx)); pv, cur = cur, nx
    return out
r22 = LOOPS['LOOP_elbow_l_22']; r21 = LOOPS['LOOP_elbow_l_21']
# the neighbouring ring of 22 toward 21 (proximal) is found by stepping away from nothing and keeping the side with smaller s
def side_step(R, sign):
    Rs = set(R); cand = defaultdict(set)
    for ed in ring_edges(R):
        for fi in EF_[ed]:
            other = [x for x in Q[fi] if x not in ed]
            if any(x in Rs for x in other): continue
            sd = 1 if sv[other].mean() > sv[list(ed)].mean() else -1; cand[sd].update(other)
    return sorted(cand[sign])
p1 = side_step(r22, -1); d1 = side_step(r22, +1)
prox = [np.array(p1)] + walk_dir(p1, r22, 60); dist = [np.array(d1)] + walk_dir(d1, r22, 60)
rings = list(reversed(prox)) + [np.array(r22)] + dist
names = ['P%d' % (len(prox) - i) for i in range(len(prox))] + ['elbow_l_22'] + ['D%d' % (i + 1) for i in range(len(dist))]
TAG = {tuple(sorted(LOOPS['LOOP_elbow_l_%d' % t])): 'elbow_l_%d' % t for t in (18, 19, 20, 21, 22)}
names = [TAG.get(tuple(sorted(np.asarray(r).tolist())), n) for r, n in zip(rings, names)]
def ringstats(Vx, r):
    c = Vx[r].mean(0); return c
rows = []
for i, (nm, r) in enumerate(zip(names, rings)):
    r = np.array(r); c = V[r].mean(0); s = (c - e) @ ax
    q = V[r] - c; rad = q - np.outer(q @ ax, ax); cth = (rad @ ant) / np.maximum(np.linalg.norm(rad, axis=1), 1e-9)
    row = dict(ring=nm, verts=int(len(r)), s_cm=round(float(s), 3), valence_counts={int(k): int((val[r] == k).sum()) for k in np.unique(val[r])})
    rs = set(r.tolist()); ea = [(a, b) for a, b in E if a in rs and b in rs]; la = np.linalg.norm(V[[a for a, b in ea]] - V[[b for a, b in ea]], axis=1)
    row['along_ring_edge_cm'] = dict(mean=round(float(la.mean()), 3), min=round(float(la.min()), 3), max=round(float(la.max()), 3))
    if i + 1 < len(rings):
        r2 = np.array(rings[i + 1]); dd = np.linalg.norm(V[r][:, None] - V[r2][None], axis=2); sp = dd.min(1); j2 = r2[dd.argmin(1)]
        row['spacing_to_next_cm'] = dict(mean=round(float(sp.mean()), 3), inner=round(float(sp[cth > 0.7].mean()), 3), outer=round(float(sp[cth < -0.7].mean()), 3), min=round(float(sp.min()), 3), max=round(float(sp.max()), 3))
        row['quad_aspect_mean'] = round(float(la.mean() / sp.mean()), 3); row['_pairs'] = (r.tolist(), j2.tolist(), (cth > 0.7).tolist())
    rows.append(row)
# density: rings per cm by zone of s
S = np.array([r['s_cm'] for r in rows]); sp = np.array([r['spacing_to_next_cm']['mean'] if 'spacing_to_next_cm' in r else np.nan for r in rows])
dens = {}
for lab, lo, hi in (('upper arm 8-15 cm proximal (s -15..-8)', -15, -8), ('flexion zone (s -6..+6)', -6, 6), ('forearm 8-15 cm distal (s +8..+15)', 8, 15)):   # s > 0 = distal
    k = (S >= lo) & (S <= hi)
    dens[lab] = dict(rings=int(k.sum()), mean_spacing_cm=round(float(np.nanmean(sp[k])), 3) if k.any() else None)
# posed: inner-side spacing ratio per ring pair
posed = {}
for pf in POSED:
    Vp = np.load(pf)['V'].astype(float); tag = os.path.basename(pf)[:-4]; pr = []
    for row in rows:
        if '_pairs' not in row: continue
        a, b, inn = row['_pairs']; a, b, inn = np.array(a), np.array(b), np.array(inn)
        r0 = np.linalg.norm(V[a] - V[b], axis=1); r1 = np.linalg.norm(Vp[a] - Vp[b], axis=1); rr = r1 / r0
        pr.append(dict(pair=row['ring'], s_cm=row['s_cm'], min_ratio=round(float(rr.min()), 3), inner_mean_ratio=round(float(rr[inn].mean()), 3), outer_mean_ratio=round(float(rr[~inn].mean()), 3)))
    posed[tag] = pr
for r in rows: r.pop('_pairs', None)
out = dict(note='analysis only; frozen v003 read-back; nothing edited', axis=ax.tolist(), pivot_src_cm=e.tolist(), rings=rows, density=dens, posed_inner_spacing=posed,
           ring_ids={nm: [int(x) for x in r] for nm, r in zip(names, rings)})
json.dump(out, open(O + '/topology_density_audit.json', 'w'), indent=1)
print('rings', len(rows), [(r['ring'], r['s_cm'], r.get('spacing_to_next_cm', {}).get('mean')) for r in rows]); print(dens)
for t, pr in posed.items(): print(t, [(p['pair'], p['s_cm'], p['min_ratio'], p['inner_mean_ratio']) for p in pr])
