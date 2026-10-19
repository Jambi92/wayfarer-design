"""Plan the UI build of the toe tubes in a fixed Front-ortho view (sx = 598.25 + 10.6*x, sy = 427.5 - 10.6*z, cm).
Round 1 = t1 + t3 of both feet (selected by clicks on the K ring), round 2 = t2 + t4 (Non Manifold select).
Writes toes_plan.json with: edges (cap split edges), r1_select, rounds[ {tubes, rings:[{moves:[(click, target_m)]}], tips} ]."""
import json, numpy as np
p = json.load(open('feet_plan.json'))
S = 10.6; A = 598.25; BF = 374.5 + S * 5
scr = lambda q: np.array([A + S * q[0], BF - S * q[2]])
foot = {}
for s in 'LR':
    D = json.load(open('fdesign_%s.json' % s)); K = np.array(p[s]['rings'][6])
    k = list(range(14))
    if D['flipped']:
        dI = {3: k[0], 2: k[1], 1: k[2], 0: k[3]}; pI = {j: k[4 + j] for j in range(7)}; dI.update({6: k[11], 5: k[12], 4: k[13]})
    else:
        dI = {3: k[0], 4: k[1], 5: k[2], 6: k[3]}; pI = {6 - j: k[4 + j] for j in range(7)}; dI.update({0: k[11], 1: k[12], 2: k[13]})
    tubes = {}
    for nm, cs in {'t1': [0, 1], 't2': [2], 't3': [3], 't4': [4, 5]}.items():
        c = cs[0]
        base = [dI[c], dI[c + 1], pI[c + 1], pI[c]] if len(cs) == 1 else [dI[c], dI[c + 1], dI[c + 2], pI[c + 2], pI[c + 1], pI[c]]
        B = K[base]; rings = np.array(p[s]['tubes'][nm]); nb = len(base); best = None
        for sh in range(nb):
            for rev in (False, True):
                o = [(sh + j) % nb for j in range(nb)]
                if rev: o = o[::-1]
                cst = np.linalg.norm(B - rings[0][o], axis=1).sum()
                if best is None or cst < best[0]: best = (cst, o)
        o = best[1]
        tubes[nm] = dict(base=B, rings=[r[o] for r in rings])
    foot[s] = dict(K=K, dI=dI, pI=pI, tubes=tubes)
out = {'edges': [], 'r1_select': [], 'rounds': []}
# cap split edges d2-p2, d3-p3, d4-p4 ; only K ring visible
Kall = np.vstack([foot[s]['K'] for s in 'LR'])
def clr(pt, pts):
    d = np.linalg.norm(scr_all(pts) - scr(pt), axis=1); d = d[d > 1e-6]; return float(d.min()) if len(d) else 1e9
def scr_all(P): return np.array([scr(q) for q in P])
for s in 'LR':
    F = foot[s]
    for j in (2, 3, 4):
        a, b = F['K'][F['dI'][j]], F['K'][F['pI'][j]]
        out['edges'].append(dict(side=s, j=j, a=scr(a).round(1).tolist(), b=scr(b).round(1).tolist(), ca=clr(a, Kall), cb=clr(b, Kall)))
for s in 'LR':
    for nm in ('t1', 't3'):
        for q in foot[s]['tubes'][nm]['base']:
            out['r1_select'].append(dict(side=s, t=nm, c=scr(q).round(1).tolist(), clr=clr(q, Kall)))
warn = 0
for rnd in (('t1', 't3'), ('t2', 't4')):
    T = [(s, nm) for s in 'LR' for nm in rnd]
    cur = {key: foot[key[0]]['tubes'][key[1]]['base'].copy() for key in T}
    nmax = max(len(foot[s]['tubes'][nm]['rings']) for s, nm in T); R = {'tubes': T, 'rings': []}
    for ri in range(nmax):
        act = [key for key in T if len(foot[key[0]]['tubes'][key[1]]['rings']) > ri]
        moves = []
        todo = [(key, j) for key in act for j in range(len(cur[key]))]
        while todo:
            vis = lambda: np.vstack([cur[key] for key in act])
            best = None
            for (key, j) in todo:
                c = clr(cur[key][j], vis())
                if best is None or c > best[0]: best = (c, key, j)
            c, key, j = best
            if c < 10: warn += 1; print('WARN', ri, key, j, round(c, 1))
            tg = foot[key[0]]['tubes'][key[1]]['rings'][ri][j]
            moves.append(dict(tube=list(key), j=j, click=scr(cur[key][j]).round(1).tolist(), clr=round(c, 1), tgt=(tg / 100).round(4).tolist()))
            cur[key][j] = tg.copy(); todo.remove((key, j))
        done = [key for key in act if len(foot[key[0]]['tubes'][key[1]]['rings']) == ri + 1]
        tips = []
        for key in done:
            P = cur[key]; vis = np.vstack([cur[k2] for k2 in act])
            quads = [[0, 1, 2, 3]] if len(P) == 4 else [[0, 1, 2, 3], [3, 4, 5, 0]]
            tips.append(dict(tube=list(key), quads=[[dict(c=scr(P[i]).round(1).tolist(), clr=round(clr(P[i], vis), 1)) for i in qd] for qd in quads]))
        cont = [key for key in act if key not in done]
        R['rings'].append(dict(ri=ri, active=[list(k) for k in act], moves=moves, tips=tips,
                               cont=[dict(tube=list(key), c=[scr(q).round(1).tolist() for q in cur[key]]) for key in cont]))
    out['rounds'].append(R)
json.dump(out, open('toes_plan.json', 'w'), indent=0)
print('edges', [(e['side'], e['j'], round(e['ca'], 1), round(e['cb'], 1)) for e in out['edges']])
print('r1 select min clr', min(e['clr'] for e in out['r1_select']))
for R in out['rounds']:
    for r in R['rings']:
        print('ring', r['ri'], 'moves', len(r['moves']), 'min clr', min(m['clr'] for m in r['moves']), 'tips', [t['tube'] for t in r['tips']],
              'tipclr', [min(q['clr'] for qd in t['quads'] for q in qd) for t in r['tips']])
print('warn', warn)
allc = [m['click'] for R in out['rounds'] for r in R['rings'] for m in r['moves']]
a = np.array(allc); print('screen range x', a[:, 0].min(), a[:, 0].max(), 'y', a[:, 1].min(), a[:, 1].max())
